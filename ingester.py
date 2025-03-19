from xml.dom import minidom, Node
from class_defs import *

def get_element_text(parent, element_name):
    children = parent.getElementsByTagName(element_name)
    if len(children) == 0:
        return ""
    return children[0].firstChild.nodeValue

def load_plan(filename):
    doc = minidom.parse(filename)
    return load_plan_from_doc(doc)

def load_plan_from_string(plan_string):
    doc = minidom.parseString(plan_string)
    return load_plan_from_doc(doc)

def load_plan_from_doc(doc):
    xml_tables = doc.getElementsByTagName("tableData")

    tables = {}
    classes = {}
    table_schemas = {}
    for xml_table in xml_tables:
        table_name = get_element_text(xml_table, "tableName")
        column_names = xml_table.getElementsByTagName("columnNames")[0]
        schema = []
        for child in column_names.childNodes:
            if child.nodeType == Node.ELEMENT_NODE and child.tagName == "string":
                schema.append(child.firstChild.nodeValue)
        table_schemas[table_name] = schema

        table_data = []
        new_classes = []
        rows = xml_table.getElementsByTagName("rows")[0]
        for row in rows.getElementsByTagName("row"):
            offset = 0
            table_row = {}
            for child in row.getElementsByTagName("columnValues")[0].childNodes:
                if child.nodeType != Node.ELEMENT_NODE:
                    continue
                if child.tagName == "null":
                    table_row[schema[offset]] = None
                    offset += 1
                elif child.tagName == "string":
                    if child.firstChild is None:
                        table_row[schema[offset]] = None
                    else:
                        table_row[schema[offset]] = child.firstChild.nodeValue
                    offset += 1
            table_data.append(table_row)
            newclass = globals()[table_name](table_row)
            new_classes.append(newclass)

        tables[table_name] = table_data
        classes[table_name] = new_classes

    for table_name, instances in classes.items():
        for inst in instances:
            for fk in inst.foreign_keys:
                if fk.remote_table not in classes:
                    continue
                for other_inst in classes[fk.remote_table]:
                    if not hasattr(other_inst, fk.name):
                        continue
                    match = True
                    for i in range(0, len(fk.columns)):
                        inst_val = getattr(inst, fk.columns[i])
                        other_inst_val = getattr(other_inst, fk.remote_columns[i])
                        if inst_val != other_inst_val:
                            match = False
                            break

                    if match:
                        getattr(other_inst, fk.name).append(inst)
    return classes