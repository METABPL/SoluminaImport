import uuid
import re
import sys
import os

from .ingester import (load_plan, load_plan_from_string)
from .class_model import *

classmodel = sys.modules[FCO.__module__]

embedded_re = re.compile(".*TextObject[(].*OBJECT_ID=([^,]*),.*")
condition_forms = [
    re.compile("(.*),? +go to .*"),
    re.compile("(.*): +proceed to .*"),
    re.compile("(.*) +proceed to .*"),
    re.compile("(.*) +skip ahead to .*"),
]

op_forms = [
    re.compile(".*[Oo][Pp] *([0-9]+).*"),
    re.compile(".*[Oo][Pp][Ee][Rr][Aa][Tt][Ii][Oo][Nn] *([0-9]+).*"),
]

start = "SFPL_PLAN_DESC"

translate_table = {
    "SFPL_PLAN_DESC": {"type": "Process",
                       "attributes": {
                           "bplProcessName": "PLAN_NO",
                           "bplProcessId": "PLAN_ID",
                           "bplElementUUID": "PLAN_ID",
                           "description": "${PLAN_NO}_${PLAN_TITLE}",
                           "name": "${PLAN_NO}_${PLAN_TITLE}",
                       },
                       "children": [
                           {"table": "SFPL_MFG_BOM_TOOL",
                            "parent_field": "resourceRequirements", "keys": ["BOM_ID"]},
                           {"table": "SFPL_MFG_BOM_COMP",
                            "parent_field": "resourceRequirements", "keys": ["BOM_ID"]},
                           {"table": "SFPL_PLAN_NODE", "keys": ["PLAN_ID"],
                            "parent_field": "bplElements"}],
                       "links":
                           {"table": "SFPL_PLAN_LINK", "keys": ["PLAN_ID"], "only": ["SFPL_PLAN_NODE"]},
    },
    "SFPL_PLAN_NODE": [{
        "type": "Exclusive",
        "selector": [("NODE_TYPE", "Decision")],
        "attributes": {
            "bplElementName": "${NODE_TYPE}${NODE_NO}",
            "bplElementId": "NODE_ID",
            "bplElementUUID": "NODE_ID",
            "description": "NODE_TITLE",
            "name": "NODE_TITLE",
            "decision": "NODE_DESC",
            "decisionType": "DECISION_TYPE"
        },
        "children": [],
        "positioning": { "x": {"key": "NODE_COLUMN", "mult": 150},
                         "y": {"key": "NODE_ROW", "mult": 100 }},
    },
    {
        "type": "UserTask",
        "selector": [("NODE_TYPE", "Return")],
        "attributes": {
            "bplElementName": "${NODE_TYPE}${NODE_NO}",
            "bplElementId": "NODE_ID",
            "bplElementUUID": "NODE_ID",
            "description": "Return to ${RETURN_TO_OPER_NO}",
            "name": "Return to ${RETURN_TO_OPER_NO}",
        },
        "link_to": [{"keys": [("RETURN_TO_OPER_KEY","OPER_KEY")]}],
        "positioning": {"x": {"key": "NODE_COLUMN", "mult": 150},
                        "y": {"key": "NODE_ROW", "mult": 100}},
    },
    {
        "type": "SubProcess",
        "attributes": {
            "bplElementName": "${NODE_TYPE}${NODE_NO}",
            "bplElementId": "NODE_ID",
            "bplElementUUID": "NODE_ID",
            "description": "$first(NODE_TITLE,${NODE_TYPE}${NODE_NO})",
            "name": "$first(NODE_TITLE,${NODE_TYPE}${NODE_NO})",
        },
        "children": [
                     {"table": "SFPL_STEP_REV_Header", "keys": ["PLAN_ID", "OPER_KEY"], "orderBy": "STEP_NO",
                      "connect": True,
                      "parent_field": "bplElements"},
                     {"table": "SFPL_STEP_REV", "keys": ["PLAN_ID", "OPER_KEY"], "orderBy": "STEP_NO", "connect": True,
                     "parent_field": "bplElements"},
                     {"table": "SFPL_STEP_REV_Footer", "keys": ["PLAN_ID", "OPER_KEY"], "orderBy": "STEP_NO",
                      "connect": True,
                      "parent_field": "bplElements"},

                     {"table": "SFPL_OPER_SKILL",
                      "keys": ["PLAN_ID", "OPER_KEY"],
                      "parent_field": "resourceRequirements"}
                     ],
        "positioning": {"x": {"key": "NODE_COLUMN", "mult": 150},
                        "y": {"key": "NODE_ROW", "mult": 100}},
    },
    ],
    "SFPL_PLAN_LINK": {
        "type": "Link",
        "src": "PRED_NODE_ID",
        "dst": "SUCC_NODE_ID"
    },
    "SFPL_STEP_REV": [{
        "type": "UserTask",
        "selector": [("!STEP_NO", "...")],
        "join": [{"table": "SFPL_STEP_DESC", "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"]},
                 {"table": "SFPL_STEP_TEXT", "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"]}],
        "attributes": {
            "bplElementName": "Operation${OPER_NO}Step${STEP_NO}",
            "bplElementId": "${PLAN_ID}_${OPER_KEY}_${STEP_KEY}",
            "bplElementUUID": "${PLAN_ID}_${OPER_KEY}_${STEP_KEY}",
            "name": "Operation${OPER_NO}Step${STEP_NO}",
            "description": "STEP_TITLE",
            "documentation": "$text(TEXT)",
        },
        "children": [{"table": "SFPL_STEP_TOOL",
                      "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
                      "parent_field": "resourceRequirements"},
                     {"table": "SFPL_STEP_ITEMS",
                      "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
                      "parent_field": "resourceRequirements"}],
        "siblings": [{"table": "SFPL_STEP_DAT_COL", "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
                      "parent_field": "bplElements"},
                     {"table": "SFPL_STEP_BUYOFF", "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
                     "parent_field": "bplElements"}],
    }],
    "SFPL_STEP_REV_Header": {
        "type": "SubProcess",
        "table": "SFPL_STEP_REV",
        "selector": [("STEP_NO", "...")],
        "join": [{"table": "SFPL_OPERATION_TEXT", "keys": ["PLAN_ID", "OPER_KEY","TEXT_TYPE=HEADER_PLANNING"]}],
        "attributes": {
            "bplElementName": "HEADER_${OPER_NO}",
            "bplElementId": "${PLAN_ID}_${OPER_KEY}_Header",
            "bplElementUUID": "${PLAN_ID}_${OPER_KEY}_Header",
            "description": "HEADER_${OPER_NO}",
            "name": "HEADER_${OPER_NO}",
            "textAnnotation": "$text(TEXT)",
        },
        "children": [{"table": "SFPL_STEP_TOOL",
                      "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
                      "parent_field": "resourceRequirements"},
                     {"table": "SFPL_STEP_ITEMS",
                      "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
                      "where": [("PART_ACTION", "USE")],
                      "parent_field": "resourceRequirements"},
                     {"table": "SFPL_STEP_DAT_COL", "connect": True,
                      "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
                      "parent_field": "bplElements"},
                     ],
    },
    "SFPL_STEP_REV_Footer": {
        "table": "SFPL_STEP_REV",
        "type": "Footer",
        "selector": [("STEP_NO", "...")],
        "join": [{"table": "SFPL_STEP_TEXT", "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"]}],
        "attributes": {
            "bplElementName": "FOOTER_${OPER_NO}",
            "bplElementId": "${PLAN_ID}_${OPER_KEY}_Footer",
            "bplElementUUID": "${PLAN_ID}_${OPER_KEY}_Footer",
            "description": "FOOTER_${OPER_NO}",
            "name": "FOOTER_${OPER_NO}",
            "documentation": "$text(TEXT)",
        },
        "children": [
            {"table": "SFPL_STEP_ITEMS",
             "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
             "where": [("PART_ACTION", "REMOVE")],
             "parent_field": "bplElements"},
            {"table": "SFPL_STEP_BUYOFF", "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"], "connect": True,
            "parent_field": "bplElements"},
        ],
    },
    "SFPL_STEP_DAT_COL": {
        "type": "DataCollectionTask",
        "join": [{"table": "SFPL_STEP_DAT_COL_LIMIT", "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY",
                                                               "DAT_COL_ID"]}],
        "attributes": {
            "bplElementName": "DAT_COL_ID",
            "bplElementId": "DAT_COL_ID",
            "bplElementUUID": "DAT_COL_ID",
            "name": "DataCollection${OPER_KEY}Step${STEP_KEY}Dat${DAT_COL_ID}",
            "description": "DAT_COL_TITLE",
            "upperLimit": "UPPER_LIMIT",
            "lowerLimit": "LOWER_LIMIT",
            "targetValue": "TARGET_VALUE",
            "unitOfMeasure": "DAT_COL_UOM",
        },
        "custom_content": None,
    },
    "SFPL_STEP_TOOL": {
        "type": "ToolResource",
        "attributes": {
            "bplElementName": "TOOL_NO",
            "bplElementId": "TOOL_ID",
            "bplElementUUID": "TOOL_ID",
            "description": "TOOL_TITLE",
            "name": "TOOL_TITLE",
            "quantity": "QTY",
        },
        "children": [],
    },
    "SFPL_MFG_BOM_TOOL": {
        "type": "ToolResource",
        "join": [{"table": "SFPL_ITEM_DESC_MASTER_ALL", "keys": ["ITEM_ID"]}],
        "attributes": {
            "bplElementName": "TOOL_NO",
            "bplElementId": "BOM_COMP_TOOL_ID",
            "bplElementUUID": "BOM_COMP_TOOL_ID",
            "description": "PART_TITLE",
            "name": "PART_TITLE",
            "quantity": "QTY",
        },
        "children": [],
    },
    "SFPL_OPER_SKILL": {
        "type": "HumanResource",
        "attributes": {
            "bplElementName": "${PLAN_ID}_${OPER_KEY}_${clean(SKILL_CATEGORY)}",
            "bplElementId": "${PLAN_ID}_${OPER_KEY}_${clean(SKILL_CATEGORY)}",
            "bplElementUUID": "${PLAN_ID}_${OPER_KEY}_${clean(SKILL_CATEGORY)}",
            "description": "SKILL_CATEGORY",
            "name": "SKILL_CATEGORY",
        },
        "children": [],
    },
    "SFPL_STEP_ITEMS": {
        "type": "ConsumableResource",
        "attributes": {
            "bplElementName": "PART_NO",
            "bplElementId": "${PLAN_ID}_${OPER_KEY}_${STEP_KEY}_${PART_DAT_COL_ID}",
            "bplElementUUID": "${PLAN_ID}_${OPER_KEY}_${STEP_KEY}_${PART_DAT_COL_ID}",
            "description": "PART_TITLE",
            "name": "PART_TITLE",
            "quantity": "ITEM_QTY",
        },
        "children": [],
    },
    "SFPL_MFG_BOM_COMP": {
        "type": "ConsumableResource",
        "join": [{"table": "SFPL_ITEM_DESC_MASTER_ALL", "keys": ["ITEM_ID"]}],
        "attributes": {
            "bplElementName": "PART_NO",
            "bplElementId": "BOM_COMP_ID",
            "bplElementUUID": "BOM_COMP_ID",
            "description": "PART_TITLE",
            "name": "PART_TITLE",
            "quantity": "QTY",
        },
        "children": [],
    },
    "SFPL_STEP_BUYOFF": {
        "type": "BuyoffTask",
        "attributes": {
            "bplElementName": "BUYOFF_ID",
            "bplElementId": "BUYOFF_ID",
            "bplElementUUID": "BUYOFF_ID",
            "description": "${BUYOFF_TYPE} Buyoff",
            "name": "BUYOFF_TITLE",
            "cert": "BUYOFF_CERT",
            "buyoffType": "BUYOFF_TYPE",
            "buyoffStatus": "BUYOFF_STATUS",
        },
        "children": [],
        "custom_content": None,
    },
}

def create_class(class_name):
    class_ = getattr(classmodel, class_name)
    return class_()

def compute_object_index(plan):
    object_id_table = {}
    for objs in plan.values():
        for obj in objs:
            if "OBJECT_ID" in obj.schema:
                object_id_table[obj.OBJECT_ID] = obj

def sort_items(items, keys):
    def dot_at_end(str):
        if str == "...":
            return "~~~"
        else:
            return str

    def get_key(item):
        if isinstance(keys, list):
            return [dot_at_end(getattr(item, key)) for key in keys]
        else:
            return dot_at_end(getattr(item, keys))
    items.sort(key=get_key)

def clean(s):
    return s.replace(" ", "_")

def get_embedded(desc):
    names = []
    start_pos = 0
    while True:
        idx = desc.find("${", start_pos)
        if idx < 0:
            return names
        end_idx = desc.find("}", idx+1)
        if end_idx < 0:
            return names
        names.append(desc[idx+2:end_idx])
        start_pos = end_idx+1

def embedded_replace(desc, obj, joins):
    names = get_embedded(desc)
    attr_value = desc
    for name in names:
        clean_value = False
        if name.startswith("clean("):
            clean_value = True
            name = name[6:len(name)-1]
        col_value = None
        if hasattr(obj, name):
            col_value = getattr(obj, name)
        if col_value is None:
            for join in joins:
                if hasattr(join, name):
                    col_value = getattr(obj, name)
                if col_value is not None:
                    break
            if col_value is None:
                col_value = ""
        if clean_value:
            col_value = clean(col_value)
            attr_value = attr_value.replace("${clean(" + name + ")}", str(col_value))
        else:
            attr_value = attr_value.replace("${" + name + "}", str(col_value))
    return attr_value


class ImportSolumina:
    def is_process(self, node):
        return isinstance(node, Process) or isinstance(node, SubProcess)

    def connector_endpoint_type(self, node):
        if isinstance(node, Activity):
            return "Activity"
        elif isinstance(node, Gateway):
            return "Gateway"
        elif isinstance(node, Event):
            return "Event"
        else:
            return None

    def make_connector(self, parent, src, dst, output=None, condition_expression=None, target_op=None):
        src_type = self.connector_endpoint_type(src)
        dst_type = self.connector_endpoint_type(dst)

        if src_type is not None and dst_type is not None:
            connector_node = create_class(src_type + "2" + dst_type)
            setattr(connector_node, "bplElementUUID", src.bplElementUUID+"_"+dst.bplElementUUID)
            setattr(connector_node, "bplElementId", src.bplElementUUID+"_"+dst.bplElementUUID)
            setattr(connector_node, "bplElementName", src.bplElementUUID+"_"+dst.bplElementUUID)
            setattr(connector_node, "name", src_type + "2" + dst_type)
            setattr(connector_node, "src", src.bplElementId)
            setattr(connector_node, "dst", dst.bplElementId)
            setattr(connector_node, "fromNode", src)
            setattr(connector_node, "toNode", dst)
            if parent is not None:
                connector_node.parent = parent
            src.nexts.append(connector_node)

            if target_op is not None:
                setattr(connector_node, "conditionTarget", target_op)
            else:
                setattr(connector_node, "conditionTarget", "")

            if condition_expression is not None:
                setattr(connector_node, "conditionExpression", condition_expression)

            if output is not None:
                setattr(connector_node, "output", output)
        if hasattr(dst, "prevs") and src not in dst.prevs:
            dst.prevs.append(src)

    def query(self, table_name, columns, plan_table):
        matches = []
        if table_name not in plan_table:
            return matches
        for obj in plan_table[table_name]:
            found = True
            for column in columns:
                if not hasattr(obj, column[0]):
                    found = False
                    break
                if str(column[1]) != str(getattr(obj, column[0])):
                    found = False
                    break
            if found:
                matches.append(obj)
        return matches

    def get_text(self, plan_table, text):
        if text is None:
            return ""
        match = embedded_re.match(text)
        if match is None:
            if text.startswith("<IMG"):
                return ""
            return text

        texts = self.query("SFFND_TEXT_OBJECT", [("OBJECT_ID", match.group(1))], plan_table)
        if len(texts) > 0:
            return getattr(texts[0], "PLAIN_TEXT")
        else:
            return text

    def compute_condition_expression(self, expr, true_path):
        if expr is None or expr == "":
            return ("", "")
        if expr.lower().startswith("else"):
            (ex2, _) = self.compute_condition_expression(true_path, true_path)
            op = None
            expr = expr[4:]
            if expr.startswith(","):
                expr = expr[1:].strip()
            for op_form in op_forms:
                matches = op_form.match(expr)
                if matches is not None:
                    op = matches.group(1)
                    while len(op) < 3:
                        op = "0" + op
                    break
            if ex2 is not None:
                return ("Not("+ex2+")", "Operation"+op)
            else:
                return ("", "")
        if expr.startswith("If "):
            expr = expr[3:]
        condition = None
        for cond_form in condition_forms:
            matches = cond_form.match(expr)
            if matches is not None:
                cond = matches.group(1)
                parts = cond.split(" ")
                if parts[len(parts)-1].lower() == "passed":
                    condition = "_".join(parts[:len(parts)-1])+"==\"passed\""
                    break
                elif parts[len(parts)-1].lower() == "failed":
                    condition = "_".join(parts[:len(parts)-1])+"==\"failed\""
                    break
                else:
                    condition = "_".join(parts)
                    break
        if condition is None:
            return (None, None)

        op = None
        for op_form in op_forms:
            matches = op_form.match(expr)
            if matches is not None:
                op = matches.group(1)
                while len(op) < 3:
                    op = "0"+op
                break
        condition = condition.strip()
        if condition.endswith(","):
            condition = condition[:-1]
        if condition.endswith("."):
            condition = condition[:-1]
        return (condition, "Operation"+op)

    def compute_condition(self, condition_type, condition, dest, other_dest_name):
        if condition_type == "MANUAL":
            dest_name = getattr(dest, "bplElementName")
            parts = condition.split("\r")
            true_path = None
            false_path = None
            if len(parts) == 1:
                parts = re.split("[Ee][Ll][Ss][Ee]", parts)

            parts = [p.strip() for p in parts if len(p.strip()) > 0]
            if len(parts) == 3 and parts[1].lower().startswith("if"):
                parts = parts[1:]
            for p in parts:
                if len(p) > 0:
                    if true_path is None:
                        true_path = p
                    elif false_path is None:
                        false_path = p
            (condition, op) = self.compute_condition_expression(true_path, true_path)
            (false_condition, false_op) = self.compute_condition_expression(false_path, true_path)

            if condition is not None and op is not None:
                if op == dest_name:
                    return (condition, op)

            if false_condition is not None and op is not None:
                if false_op == dest_name:
                    return (false_condition, false_op)

            if condition is not None and op is not None:
                if op == other_dest_name:
                    return (false_condition, false_op)

            if false_condition is not None and op is not None:
                if false_op == other_dest_name:
                    return (condition, op)

            return (condition, op)
        else:
            return (None, None)

    def reachable_from(self, src_id, dst_id, link_map):
        if src_id not in link_map:
            return None

        if dst_id in link_map[src_id]:
            return 1

        closest = None
        for next in link_map[src_id]:
            reachable_count = self.reachable_from(next, dst_id, link_map)
            if reachable_count is None:
                continue
            if closest is None:
                closest = reachable_count
            elif closest > reachable_count:
                closest = reachable_count
        return closest

    def shift_children_x(self, node, from_x):
        if hasattr(node, "bplElements"):
            for child in node.bplElements:
                if hasattr(child, "x") and hasattr(child, "y"):
                    if child.x == from_x:
                        child.x = child.x + 150

    def create_object(self, parent, parent_field, obj, table_name, plan_table, object_id_table, added_links):
        object_info = translate_table[table_name]

        found = True
        if not isinstance(object_info, list):
            object_info = [object_info]

        for select_oi in object_info:
            if "selector" not in select_oi:
                object_info = select_oi
                found = True
                break
            selectors = select_oi["selector"]
            found = True
            for selector in selectors:
                if selector[0].startswith("!"):
                    if str(getattr(obj, selector[0][1:])) != str(selector[1]):
                        found = True
                        object_info = select_oi
                        break
                    else:
                        found = False
                        break
                else:
                    if str(getattr(obj, selector[0])) != str(selector[1]):
                        found = False
                        break
                    else:
                        pass
            if found:
                object_info = select_oi
                break

        if not found:
            return (None, None)

        node = create_class(object_info["type"])
        if parent is not None and parent_field is not None:
            getattr(parent, parent_field).append(node)
        if parent is not None:
            node.parent = parent

        if "positioning" in object_info:
            positioning = object_info["positioning"]
            x = None
            y = None
            if "x" in positioning:
                if hasattr(obj, positioning["x"]["key"]):
                    xstr = getattr(obj, positioning["x"]["key"])
                    x = int(xstr)
                    if "mult" in positioning["x"]:
                        x = x * positioning["x"]["mult"]

            if "y" in positioning:
                if hasattr(obj, positioning["y"]["key"]):
                    ystr = getattr(obj, positioning["y"]["key"])
                    y = int(ystr)
                    if "mult" in positioning["y"]:
                        y = y * positioning["y"]["mult"]

            if x is not None and y is not None:
                setattr(node, "x", x)
                setattr(node, "y", y)

        joins = []
        if "join" in object_info:
            for join in object_info["join"]:
                columns = []
                for key in join["keys"]:
                    if "=" in key:
                        parts=key.split("=")
                        columns.append((parts[0], parts[1]))
                    else:
                        columns.append((key, getattr(obj, key)))
                joined_objs = self.query(join["table"], columns, plan_table)
                if len(joined_objs) > 1:
                    pass
                elif len(joined_objs) == 1:
                    joins.append(joined_objs[0])

        use_uuid = None
        for attr_name, attr_column in object_info["attributes"].items():
            if attr_column.startswith("$first("):
                attr_columns = [col.strip() for col in attr_column[7:-1].split(",")]
            else:
                attr_columns = [attr_column]

            for attr_column in attr_columns:
                if attr_column == "$uuid":
                    if use_uuid is None:
                        use_uuid = str(uuid.uuid4())
                    attr_value = use_uuid
                elif attr_column.startswith("$text("):
                    attr_value = ""
                    text_cols = attr_column[6:len(attr_column)-1].split(",")
                    for text_col in text_cols:
                        if hasattr(obj, text_col):
                            next_attr_value = self.get_text(plan_table, getattr(obj, text_col))
                            if attr_value is None or attr_value == "" and next_attr_value is not None and next_attr_value != "":
                                attr_value = next_attr_value
                        else:
                            for join in joins:
                                if hasattr(join, text_col):
                                    next_attr_value = self.get_text(plan_table, getattr(join, text_col))
                                    if attr_value is None or attr_value == "" and next_attr_value is not None and next_attr_value != "":
                                        attr_value = next_attr_value
                                    if attr_value is not None:
                                        break
    #                        print("{} has no column named {}".format(table_name, text_col))
                elif "${" in attr_column:
                    attr_value = embedded_replace(attr_column, obj, joins)
                else:
                    attr_value = None
                    if hasattr(obj, attr_column):
                        attr_value = getattr(obj, attr_column)
                    if attr_value is None:
                        for join in joins:
                            if hasattr(join, attr_column):
                                attr_value = getattr(join, attr_column)
                            if attr_value is not None:
                                break

                if attr_value is not None:
                    setattr(node, attr_name, attr_value)
                    break

        if "custom_content" in object_info:
            custom_func = object_info["custom_content"]
            if custom_func is not None:
                custom_func(node, obj, object_info, plan_table, object_id_table)

        containers = {}

        added_children = {}

        if "link_to" in object_info:
            for link in object_info["link_to"]:
                added_links.append((node, obj, link["keys"]))

        created_start = False
        prev_child = None
        start_parent_field = None
        if "children" in object_info:
            for child in object_info["children"]:

                if self.is_process(node) and "connect" in child and child["connect"] and not created_start:
                    prev_child = create_class("StartEvent")
                    getattr(node, child["parent_field"]).append(prev_child)
                    setattr(prev_child, "name", "StartEvent")
                    new_uuid = node.bplElementUUID + "_Start"
                    setattr(prev_child, "bplElementName", new_uuid)
                    setattr(prev_child, "bplElementId", new_uuid)
                    setattr(prev_child, "bplElementUUID", new_uuid)
                    if parent is not None:
                        prev_child.parent = parent
                    created_start = True
                    start_parent_field = child["parent_field"]

                child_table = child["table"]
                if "table" in translate_table[child_table]:
                    child_table = translate_table[child_table]["table"]
                if child_table not in plan_table:
                    continue
                children = plan_table[child_table][:]
                if "orderBy" in child:
                    sort_items(children, child["orderBy"])

                for child_obj in children:
                    matches = True
                    key_matches = []
                    for key in child["keys"]:
                        if type(key) is tuple:
                            parent_val = getattr(obj, key[0])
                            child_val = getattr(child_obj,key[1])
                            if str(parent_val) != str(child_val):
                                matches = False
                                break
                            else:
                                key_matches.append("{}.{} ({}) = {}.{} ({})".format(
                                    table_name, key[0], parent_val, child_table, key[1], child_val))
                        else:
                            parent_val = getattr(obj, key)
                            child_val = getattr(child_obj,key)
                            if str(parent_val) != str(child_val):
                                matches = False
                                break
                            else:
                                key_matches.append("{}.{} ({}) = {}.{} ({})".format(
                                table_name, key, parent_val, child_table, key, child_val))
                    if "where" in child:
                        for (col,val) in child["where"]:
                            if not hasattr(child_obj, col):
                                matches = False
                                break
                            if str(getattr(child_obj, col)) != val:
                                matches = False
                                break
                    if matches:
                        new_child = None
                        if "container" in child:
                            container_info = child["container"]
                            if container_info["title"] not in containers:
                                container_node = create_class(container_info["type"])
                                setattr(container_node, "name", container_info["title"])
                                getattr(node, container_info["parent_field"]).append(container_node)
                                new_uuid = node.bplElementUUID + "_{}".format(container_info[parent_field])
                                setattr(container_node, "bplElementName", container_info["title"])
                                setattr(container_node, "bplElementId", new_uuid)
                                setattr(container_node, "bplElementUUID", new_uuid)
                                setattr(container_node, "description", container_info["title"])
                                if parent is not None:
                                    container_node.parent = parent

                                containers[container_info["title"]] = container_node
                            (contained_child, _) = self.create_object(container_node, child_obj, child["table"], plan_table, object_id_table, added_links)
                            if contained_child is not None:
                                added_children[self.core.get_attribute(contained_child, "bplElementId")] = (container_node,child_obj,child)
                        else:
                            (new_child, siblings) = self.create_object(node, child["parent_field"], child_obj,
                                                                       child["table"], plan_table, object_id_table, added_links)
                            if new_child is not None:
                                if hasattr(new_child, "bplElementId"):
                                    added_children[getattr(new_child, "bplElementId")] = (new_child, child_obj,child)
                                elif hasattr(new_child, "bplElementUUID"):
                                    added_children[getattr(new_child, "bplElementUUID")] = (new_child, child_obj,child)
                                else:
#                                    print("child doesn't have a bplElementId or a bplElementUUID")
                                    pass

                        if new_child is not None and prev_child is not None and self.is_process(node) and "connect" in child and child["connect"]:
                            self.make_connector(node, prev_child, new_child)
                            prev_child = new_child

                            for sibling in siblings:
                                self.make_connector(node, prev_child, sibling)
                                prev_child = sibling

        created_end = False

        if "links" in object_info and object_info["links"]["table"] in plan_table:
            links = object_info["links"]
            cols = []
            for key in links["keys"]:
                cols.append((key, getattr(obj, key)))
            matching_links = self.query(links["table"], cols, plan_table)
            link_info = translate_table[links["table"]]

            start_nodes = set()
            end_nodes = set()

            for child_id in added_children:
                if "only" in links:
                    (_nc, _obj, child_info) = added_children[child_id]
                    if child_info["table"] in links["only"]:
                        start_nodes.add(child_id)
                        end_nodes.add(child_id)

            link_map = {}
            for link in matching_links:
                src_id = getattr(link, link_info["src"])
                dst_id = getattr(link, link_info["dst"])
                if src_id not in link_map:
                    link_map[src_id] = set()
                link_map[src_id].add(dst_id)

            incoming_count = {}
            outgoing_count = {}
            for link in matching_links:
                src_id = getattr(link, link_info["src"])
                dst_id = getattr(link, link_info["dst"])

                if not src_id in outgoing_count:
                    outgoing_count[src_id] = 1
                else:
                    outgoing_count[src_id] += 1

                if not dst_id in incoming_count:
                    incoming_count[dst_id] = 1
                else:
                    incoming_count[dst_id] += 1

            alternate_src = {}
            alternate_dst = {}

            multiple_incoming = set()
            for (dst_id, count) in incoming_count.items():
                if count > 1:
                    multiple_incoming.add(dst_id)

            for (src_id, count) in outgoing_count.items():
                if count <= 1:
                    continue

                old_src = added_children[src_id][0]
                if isinstance(old_src, Exclusive):
                    continue

                if hasattr(old_src, "x"):
                    self.shift_children_x(node, old_src.x+150)

                parallel = create_class("Parallel")

                setattr(parallel, "name", "GW Split")
                new_uuid = node.bplElementUUID + "_GW_Split"
                setattr(parallel, "bplElementName", new_uuid)
                setattr(parallel, "bplElementId", new_uuid)
                setattr(parallel, "bplElementUUID", new_uuid)
                if parent is not None:
                    parallel.parent = parent
                    parent.bplElements.add(parallel)

                if hasattr(old_src, "x"):
                    parallel.x = old_src.x
                    parallel.y = old_src.y
                    old_src.x += 150
                self.make_connector(node, old_src, parallel)
                alternate_src[src_id] = parallel

            for gateway in alternate_src:
                best_dst = None
                best_count = None

                for (dst_id, count) in incoming_count.items():
                    if count != outgoing_count[gateway]:
                        continue

                    reachable_count = 0
                    reachable = True
                    for src in link_map[gateway]:
                        reach = self.reachable_from(src, dst_id, link_map)
                        if reach is None:
                            reachable = False
                            break
                        reachable_count += reach
                    if not reachable:
                        continue
                    if best_count is None or reachable_count < best_count:
                        best_dst = dst_id
                        best_count = reachable_count

                if best_dst is not None:
                    old_dst = added_children[best_dst][0]

                    if hasattr(old_dst, "x"):
                        self.shift_children_x(node, old_dst.x + 150)

                    joiner = create_class("Parallel")

                    setattr(joiner, "name", "GW Join")
                    new_uuid = node.bplElementUUID + "_GW_Join"
                    setattr(joiner, "bplElementName", new_uuid)
                    setattr(joiner, "bplElementId", new_uuid)
                    setattr(joiner, "bplElementUUID", new_uuid)
                    if parent is not None:
                        joiner.parent = parent
                        parent.bplElements.add(joiner)

                    if hasattr(old_dst, "x"):
                        joiner.x = old_dst.x
                        joiner.y = old_dst.y
                        old_dst.x += 150
                    self.make_connector(node, joiner, old_dst)
                    alternate_dst[best_dst] = joiner

            min_op = None
            min_src = None
            for link in matching_links:
                src_id = getattr(link, link_info["src"])
                dst_id = getattr(link, link_info["dst"])

                if src_id not in added_children:
                    continue

                if dst_id not in added_children:
                    continue

                src_node = added_children[src_id][0]
                dst_node = added_children[dst_id][0]

                if src_node.bplElementName.startswith("Operation"):
                    if min_op is None:
                        min_op = src_node.bplElementName
                        min_src = src_node
                    elif src_node.bplElementName < min_op:
                        min_op = src_node.bplElementName
                        min_src = src_node

                if dst_id in start_nodes:
                    start_nodes.remove(dst_id)
                if src_id in end_nodes:
                    end_nodes.remove(src_id)

                if hasattr(src_node, "decision"):
                    decision = getattr(src_node, "decision")
                else:
                    decision = None
                condition = None
                op = None
                if decision is not None:
                    other_target = None
                    for other_link in matching_links:
                        other_src_id = getattr(other_link, link_info["src"])
                        other_dst_id = getattr(other_link, link_info["dst"])
                        if other_src_id == src_id and other_dst_id != dst_id:
                            for other_conn in src_node.nexts:
                                if isinstance(other_conn, Gateway2Activity):
                                    if other_conn.src == src_node.bplElementId:
                                        other_target = getattr(other_conn, "conditionTarget")
                                        break

                    decision_type = getattr(src_node, "decisionType")
                    (condition, op) = self.compute_condition(decision_type, decision, dst_node, other_target)

                if src_id in alternate_src:
                    src_node = alternate_src[src_id]
                if dst_id in alternate_dst:
                    dst_node = alternate_dst[dst_id]
                self.make_connector(node, src_node, dst_node, condition_expression=condition, target_op=op)

            for added_link in added_links:
                (from_node, node_info, keys) = added_link
                for added_child in added_children.values():
                    found = True
                    for key in keys:
                        if not hasattr(added_child[1], key[1]):
                            found = False
                            break
                        if str(getattr(node_info, key[0])) != str(getattr(added_child[1], key[1])):
                            found = False
                            break
                    if found:
                        self.make_connector(node, from_node, added_child[0])
                        src_id = getattr(from_node, "bplElementId")
                        dst_id = getattr(added_child[0], "bplElementId")

                        if dst_id in start_nodes:
                            start_nodes.remove(dst_id)
                        if src_id in end_nodes:
                            end_nodes.remove(src_id)

            if len(start_nodes) != 1 and len(added_links) > 0 and min_src is not None:
                start_evt = create_class("StartEvent")
                setattr(start_evt, "name", "StartEvent")
                getattr(node, "bplElements").append(start_evt)
                new_uuid = node.bplElementUUID + "_Start"
                setattr(start_evt, "bplElementName", new_uuid)
                setattr(start_evt, "bplElementId", new_uuid)
                setattr(start_evt, "bplElementUUID", new_uuid)
                if parent is not None:
                    start_evt.parent = parent
                created_start = True

                self.make_connector(node, start_evt, min_src)
            elif len(start_nodes) == 1 and not created_start:
                start_evt = create_class("StartEvent")
                setattr(start_evt, "name", "StartEvent")
                getattr(node, "bplElements").append(start_evt)
                new_uuid = node.bplElementUUID + "_Start"
                setattr(start_evt, "bplElementName", new_uuid)
                setattr(start_evt, "bplElementId", new_uuid)
                setattr(start_evt, "bplElementUUID", new_uuid)
                if parent is not None:
                    start_evt.parent = parent
                created_start = True

                self.make_connector(node, start_evt, added_children[start_nodes.pop()][0])

            end_evt = create_class("EndEvent")
            setattr(end_evt, "name", "EndEvent")
            getattr(node, "bplElements").append(end_evt)
            new_uuid = node.bplElementUUID + "_End"
            setattr(end_evt, "bplElementName", new_uuid)
            setattr(end_evt, "bplElementId", new_uuid)
            setattr(end_evt, "bplElementUUID", new_uuid)
            if parent is not None:
                end_evt.parent = parent

            for end_src in end_nodes:
                self.make_connector(node, added_children[end_src][0], end_evt)
            created_end = True

        if isinstance(node, Process) and "SFPL_PLAN_LINK" not in plan_table and len(node.bplElements) == 1:
            start_evt = create_class("StartEvent")
            setattr(start_evt, "name", "StartEvent")
            new_uuid = node.bplElementUUID + "_Start"
            setattr(start_evt, "bplElementName", new_uuid)
            setattr(start_evt, "bplElementId", new_uuid)
            setattr(start_evt, "bplElementUUID", new_uuid)
            if parent is not None:
                start_evt.parent = parent
            created_start = True

            self.make_connector(node, start_evt, node.bplElements[0])

            end_evt = create_class("EndEvent")
            setattr(end_evt, "name", "EndEvent")
            new_uuid = node.bplElementUUID + "_End"
            setattr(end_evt, "bplElementName", new_uuid)
            setattr(end_evt, "bplElementId", new_uuid)
            setattr(end_evt, "bplElementUUID", new_uuid)
            if parent is not None:
                end_evt.parent = parent
            created_end = True

            self.make_connector(node, node.bplElements[0], end_evt)

            node.bplElements.append(start_evt)
            node.bplElements.append(end_evt)
        elif isinstance(node, Process) and "SFPL_PLAN_LINK" not in plan_table and len(node.bplElements) > 1:
            start_evt = create_class("StartEvent")
            setattr(start_evt, "name", "StartEvent")
            new_uuid = node.bplElementUUID + "_Start"
            setattr(start_evt, "bplElementName", new_uuid)
            setattr(start_evt, "bplElementId", new_uuid)
            setattr(start_evt, "bplElementUUID", new_uuid)
            if parent is not None:
                start_evt.parent = parent
            created_start = True

            end_evt = create_class("EndEvent")
            setattr(end_evt, "name", "EndEvent")
            new_uuid = node.bplElementUUID + "_End"
            setattr(end_evt, "bplElementName", new_uuid)
            setattr(end_evt, "bplElementId", new_uuid)
            setattr(end_evt, "bplElementUUID", new_uuid)
            if parent is not None:
                end_evt.parent = parent
            created_end = True

            parallel = create_class("Parallel")

            setattr(parallel, "name", "GW Split")
            new_uuid = node.bplElementUUID + "_GW_Split"
            setattr(parallel, "bplElementName", new_uuid)
            setattr(parallel, "bplElementId", new_uuid)
            setattr(parallel, "bplElementUUID", new_uuid)
            if parent is not None:
                parallel.parent = parent
                parent.bplElements.add(parallel)

            parallel.x = node.bplElements[0].x
            parallel.y = node.bplElements[0].y

            self.make_connector(node, start_evt, parallel)

            for child in node.bplElements:
                child.x += 150
                self.make_connector(node, parallel, child)

            joiner = create_class("Parallel")

            setattr(joiner, "name", "GW Join")
            new_uuid = node.bplElementUUID + "_GW_Join"
            setattr(joiner, "bplElementName", new_uuid)
            setattr(joiner, "bplElementId", new_uuid)
            setattr(joiner, "bplElementUUID", new_uuid)
            if parent is not None:
                joiner.parent = parent

            joiner.x = node.bplElements[0].x + 150
            joiner.y = node.bplElements[0].y

            for child in node.bplElements:
                self.make_connector(node, child, joiner)

            self.make_connector(node, joiner, end_evt)

            node.bplElements.append(start_evt)
            node.bplElements.append(parallel)
            node.bplElements.append(joiner)
            node.bplElements.append(end_evt)

        if created_start and not created_end:
            end_evt = create_class("EndEvent")
            setattr(end_evt, "name", "EndEvent")
            getattr(node, "bplElements").append(end_evt)
            new_uuid = node.bplElementUUID + "_End"
            setattr(end_evt, "bplElementName", new_uuid)
            setattr(end_evt, "bplElementId", new_uuid)
            setattr(end_evt, "bplElementUUID", new_uuid)
            if parent is not None:
                end_evt.parent = parent
            self.make_connector(node, prev_child, end_evt)

        return (node, self.create_siblings(parent, parent_field, obj, object_info, plan_table, object_id_table))

    def create_siblings(self, parent, parent_field, parent_obj, parent_info, plan_table, object_id_table):
        if "siblings" not in parent_info:
            return []
        created_siblings = []
        for sibling in parent_info["siblings"]:
            if sibling["table"] not in plan_table:
                continue
            siblings = plan_table[sibling["table"]][:]
            if "orderBy" in sibling:
                sort_items(siblings, sibling["orderBy"])
            for sibling_obj in siblings:
                matches = True
                for key in sibling["keys"]:
                    if type(key) is tuple:
                        parent_val = getattr(parent_obj, key[0])
                        sibling_val = getattr(sibling_obj, key[1])
                        if parent_val != sibling_val:
                            matches = False
                            break
                    else:
                        parent_val = getattr(parent_obj, key)
                        sibling_val = getattr(sibling_obj, key)
                        if parent_val != sibling_val:
                            matches = False
                            break
                if matches:
                    (new_sibling, sib_sibs) = self.create_object(parent, parent_field, sibling_obj, sibling["table"], plan_table, object_id_table, [])
                    if new_sibling is not None:
                        created_siblings.append(new_sibling)
                        for sib in sib_sibs:
                            created_siblings.append(sib)
        return created_siblings

    def import_plan(self, plan_table, plan_name):
        object_id_table = compute_object_index(plan_table)

        plan_desc = plan_table["SFPL_PLAN_DESC"][0]

        (process, _) = self.create_object(None, None, plan_desc, "SFPL_PLAN_DESC", plan_table, object_id_table, [])
        filename = os.path.basename(plan_name)
        process_pattern = re.compile("plan[-_]([0-9]*).*")
        matches = process_pattern.match(filename.lower())
        if matches is not None:
            process.bplProcessName = matches.group(1)
        return process

def load_process(filename):
    importer = ImportSolumina()

    plan_table = load_plan(filename)
    process = importer.import_plan(plan_table, filename)
    process.source = os.path.basename(filename)
    return process

def load_process_from_string(filename, contents):
    importer = ImportSolumina()

    plan_table = load_plan_from_string(contents)
    process = importer.import_plan(plan_table, filename)
    process.source = os.path.basename(filename)
    return process
