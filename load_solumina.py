import uuid
import re
import sys
import os

from .ingester import (load_plan, load_plan_from_string)
from .class_model import *

classmodel = sys.modules[FCO.__module__]

embedded_re = re.compile(".*TextObject[(].*OBJECT_ID=([^,]*),.*")

start = "SFPL_PLAN_DESC"

translate_table = {
    "SFPL_PLAN_DESC": {"type": "Process",
                       "attributes": {
                           "bplProcessName": "PLAN_ID",
                           "bplProcessId": "PLAN_ID",
                           "bplElementUUID": "$uuid",
                           "description": "${PLAN_NO}_${PLAN_TITLE}",
                           "name": "${PLAN_NO}_${PLAN_TITLE}",
                       },
                       "children": [
#                            {"table": "SFPL_MFG_BOM_TOOL", "container": {"type": "ResourceRequirement",
#                                                                         "parent_field": "resourceRequirements",
#                                                                                  "title": "ToolResReqmt"},
#                                         "parent_field": "resourceBases", "keys": ["BOM_ID"]},
#                            {"table": "SFPL_MFG_BOM_COMP",
#                                         "container": {"type": "ResourceRequirement",
#                                                       "parent_field": "resourceRequirements",
#                                                       "title": "ConsumablePartsResReqmt"},
#                                    "parent_field": "resourceBases", "keys": ["BOM_ID"]},
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
            "bplElementUUID": "$uuid",
            "description": "NODE_TITLE",
            "name": "NODE_TITLE",
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
            "bplElementUUID": "$uuid",
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
            "bplElementUUID": "$uuid",
            "description": "NODE_TITLE",
            "name": "NODE_TITLE",
        },
        "children": [{"table": "SFPL_STEP_REV", "keys": ["PLAN_ID", "OPER_KEY"], "orderBy": "STEP_NO",
                      "parent_field": "bplElements", "connect": True},


#                     {"table": "SFPL_OPER_SKILL", "container": {
#                         "type": "ResourceRequirement", "title": "SkillResReqmt",
#                        "parent_field": "resourceRequirements",},
#                      "keys": ["PLAN_ID", "OPER_KEY"],
#                      "parent_field": "resourceBases"}
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
        "type": "Footer",
        "selector": [("STEP_NO", "...")],
        "join": [{"table": "SFPL_STEP_TEXT", "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"]}],
        "attributes": {
            "bplElementName": "FOOTER_${OPER_NO}",
            "bplElementId": "$uuid",
            "bplElementUUID": "$uuid",
            "description": "FOOTER_${OPER_NO}",
            "name": "FOOTER_${OPER_NO}",
            "documentation": "$text(TEXT)",
        },
        "children": [
#            {"table": "SFPL_STEP_TOOL", "container": {"type": "ResourceRequirement",
#                                                               "title": "ToolResReqmt",
#                                                               "parent_field": "resourceRequirements"},
#                      "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
#                      "parent_field": "resourceBases"},
#                     {"table": "SFPL_STEP_ITEMS", "container": {"type": "ResourceRequirement",
#                                                                "title": "ConsumablePartsResReqmt",
#                                                                "parent_field": "resourceRequirements"},
#                      "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
#                      "parent_field": "resourceBases"},
            {"table": "SFPL_STEP_TOOL",
             "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
             "parent_field": "resourceRequirements"},
            {"table": "SFPL_STEP_ITEMS",
             "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
             "parent_field": "resourceRequirements"},
        ],
        "custom_content": None,
    },
        {
            "type": "UserTask",
            "join": [{"table": "SFPL_STEP_DESC", "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"]},
                {"table": "SFPL_STEP_TEXT", "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"]}],
            "attributes": {
                "bplElementName": "Operation${OPER_NO}Step${STEP_NO}",
                "bplElementId": "$uuid",
                "bplElementUUID": "$uuid",
                "name": "Operation${OPER_NO}Step${STEP_NO}",
                "description": "STEP_TITLE",
                "documentation": "$text(TEXT)",
            },
            "children": [
#                {"table": "SFPL_STEP_TOOL", "container": {"type": "ResourceRequirement",
#                                                                   "title": "ToolResReqmt",
#                                                                   "parent_field": "resourceRequirements"},
#                          "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
#                          "parent_field": "resourceBases"},
#                         {"table": "SFPL_STEP_ITEMS", "container": {"type": "ResourceRequirement",
#                                                                    "title": "ConsumablePartsResReqmt",
#                                                                    "parent_field": "resourceRequirements"},
#                          "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
#                          "parent_field": "resourceBases"}
                {"table": "SFPL_STEP_TOOL",
                 "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
                 "parent_field": "resourceRequirements"},
                {"table": "SFPL_STEP_ITEMS",
                 "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
                 "parent_field": "resourceRequirements"}
            ],
            "siblings": [{"table": "SFPL_STEP_DAT_COL", "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
                          "parent_field": "bplElements"}],
        }],
    "SFPL_STEP_DAT_COL": {
        "type": "DataCollection",
        "attributes": {
            "bplElementName": "DataCollection${OPER_KEY}Step${STEP_KEY}Dat${DAT_COL_ID}",
            "bplElementId": "$uuid",
            "bplElementUUID": "$uuid",
            "name": "DataCollection${OPER_KEY}Step${STEP_KEY}Dat${DAT_COL_ID}",
            "description": "DataCollection${OPER_KEY}Step${STEP_KEY}Dat${DAT_COL_ID}",
            "upperLimit": "UPPER_LIMIT",
            "lowerLimit": "LOWER_LIMIT",
            "targetValue": "TARGET_VALUE",
        },
        "siblings": [{"table": "SFPL_STEP_BUYOFF", "keys": ["PLAN_ID", "OPER_KEY", "STEP_KEY"],
                      "parent_field": "bplElements"},],
        "custom_content": None,
    },
    "SFPL_STEP_TOOL": {
        "type": "ToolResource",
        "attributes": {
            "bplElementName": "TOOL_NO",
            "bplElementId": "$uuid",
            "bplElementUUID": "$uuid",
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
            "bplElementName": "${BOM_ID}_${BOM_COMP_TOOL_ID}",
            "bplElementId": "$uuid",
            "bplElementUUID": "$uuid",
            "description": "PART_TITLE",
            "name": "PART_TITLE",
            "quantity": "QTY",
        },
        "children": [],
    },
    "SFPL_OPER_SKILL": {
        "type": "HumanResource",
        "attributes": {
            "bplElementName": "$uuid",
            "bplElementId": "$uuid",
            "bplElementUUID": "$uuid",
            "description": "SKILL_CATEGORY",
            "name": "SKILL_CATEGORY",
        },
        "children": [],
    },
    "SFPL_STEP_ITEMS": {
        "type": "ConsumableResource",
        "attributes": {
            "bplElementName": "PART_NO",
            "bplElementId": "$uuid",
            "bplElementUUID": "$uuid",
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
            "bplElementName": "${BOM_ID}_${BOM_COMP_TOOL_ID}",
            "bplElementId": "$uuid",
            "bplElementUUID": "$uuid",
            "description": "PART_TITLE",
            "name": "PART_TITLE",
            "quantity": "QTY",
        },
        "children": [],
    },
    "SFPL_STEP_BUYOFF": {
        "type": "SubProcess",
        "attributes": {
            "bplElementName": "$uuid",
            "bplElementId": "$uuid",
            "bplElementUUID": "$uuid",
            "description": "${BUYOFF_TYPE} Buyoff",
            "name": "BUYOFF_TITLE",
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
        attr_value = attr_value.replace("${" + name + "}", str(col_value))
    return attr_value


class ImportSolumina:
    def find_named_from(self, name, node):
        node_name = getattr(node, "name")
        if node_name == name:
            return node
        for child in self.core.load_children(node):
            found = self.find_named_from(name, child)
            if found is not None:
                return found
        return None

    def find_named(self, name):
        return self.find_named_from(name, self.root_node)

    def is_process(self, node):
        return isinstance(node, Process) or isinstance(node, SubProcess)

    def is_type(self, node, type_name):
        return type(node).__name__ == type_name

    def connector_endpoint_type(self, node):
        if self.is_type(node, "Activity"):
            return "Activity"
        elif self.is_type(node, "Gateway"):
            return "Gateway"
        elif self.is_type(node, "Event"):
            return "Event"
        else:
            return None

    def make_connector(self, parent, src, dst, output=None, condition_expression=None):
        if dst not in src.nexts:
            if condition_expression is not None:
                src.nexts[condition_expression] = dst
            else:
                src.nexts["default"] = dst
        if src not in dst.prevs:
            dst.prevs.append(src)

    def query(self, table_name, columns, plan_table):
        matches = []
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

    def create_object(self, parent, parent_field, obj, table_name, plan_table, object_id_table, added_links):
        object_info = translate_table[table_name]

        if isinstance(object_info, list):
            for select_oi in object_info:
                if "selector" not in select_oi:
                    object_info = select_oi
                    break
                selectors = select_oi["selector"]
                found = True
                for selector in selectors:
                    if str(getattr(obj, selector[0])) != str(selector[1]):
                        found = False
                        break
                if found:
                    object_info = select_oi
                    break

        node = create_class(object_info["type"])
        if parent is not None and parent_field is not None:
            getattr(parent, parent_field).append(node)

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
                    columns.append((key, getattr(obj, key)))
                joined_objs = self.query(join["table"], columns, plan_table)
                if len(joined_objs) > 1:
                    pass
                elif len(joined_objs) == 1:
                    joins.append(joined_objs[0])

        use_uuid = None
        for attr_name, attr_column in object_info["attributes"].items():
            if attr_column == "$uuid":
                if use_uuid is None:
                    use_uuid = str(uuid.uuid4())
                attr_value = use_uuid
            elif attr_column.startswith("$text("):
                text_col = attr_column[6:len(attr_column)-1]
                if hasattr(obj, text_col):
                    attr_value = self.get_text(plan_table, getattr(obj, text_col))
                else:
                    for join in joins:
                        if hasattr(join, text_col):
                            attr_value = self.get_text(plan_table, getattr(join, text_col))
                            if attr_value is not None:
                                break
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

        if "custom_content" in object_info:
            custom_func = object_info["custom_content"]
            if custom_func is not None:
                custom_func(node, obj, object_info, plan_table, object_id_table)

        containers = {}

        added_children = {}

        if "link_to" in object_info:
            for link in object_info["link_to"]:
                added_links.append((node, obj, link["keys"]))

        if "children" in object_info:
            for child in object_info["children"]:
                prev_child = None

                if self.is_process(node) and "connect" in child and child["connect"]:
                    prev_child = create_class("StartEvent")
                    getattr(node, child["parent_field"]).append(prev_child)
                    setattr(prev_child, "name", "StartEvent")
                    new_uuid = str(uuid.uuid4())
                    setattr(prev_child, "bplElementName", new_uuid)
                    setattr(prev_child, "bplElementId", new_uuid)
                    setattr(prev_child, "bplElementUUID", new_uuid)

                child_table = child["table"]
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
                    if matches:
                        if "container" in child:
                            container_info = child["container"]
                            if container_info["title"] not in containers:
                                container_node = create_class(container_info["type"])
                                setattr(container_node, "name", container_info["title"])
                                getattr(node, container_info["parent_field"]).append(container_node)
                                new_uuid = str(uuid.uuid4())
                                setattr(container_node, "bplElementName", container_info["title"])
                                setattr(container_node, "bplElementId", new_uuid)
                                setattr(container_node, "bplElementUUID", new_uuid)
                                setattr(container_node, "description", container_info["title"])

                                containers[container_info["title"]] = container_node
                            (contained_child, _) = self.create_object(container_node, container_info["parent_field"],
                                                                      child_obj, child_table, plan_table, object_id_table, added_links)
                            added_children[getattr(contained_child, "bplElementId")] = (container_node,child_obj,child)
                        else:
                            (new_child, siblings) = self.create_object(node, child["parent_field"], child_obj,
                                                                       child_table, plan_table, object_id_table, added_links)
                            added_children[getattr(new_child, "bplElementId")] = (new_child, child_obj,child)

                        if prev_child is not None and self.is_process(node):
                            self.make_connector(node, prev_child, new_child)
                            prev_child = new_child

                            for sibling in siblings:
                                self.make_connector(node, prev_child, sibling)
                                prev_child = sibling


                if self.is_process(node) and "connect" in child and child["connect"]:
                    new_child = create_class("EndEvent")
                    setattr(new_child, "name", "EndEvent")
                    getattr(node, child["parent_field"]).append(new_child)
                    new_uuid = str(uuid.uuid4())
                    setattr(new_child, "bplElementName", new_uuid)
                    setattr(new_child, "bplElementId", new_uuid)
                    setattr(new_child, "bplElementUUID", new_uuid)

                    self.make_connector(node, prev_child, new_child)

        if "links" in object_info:
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

            for link in matching_links:
                src_id = getattr(link, link_info["src"])
                dst_id = getattr(link, link_info["dst"])

                if src_id not in added_children:
                    continue

                if dst_id not in added_children:
                    continue

                src_node = added_children[src_id][0]
                dst_node = added_children[dst_id][0]

                if dst_id in start_nodes:
                    start_nodes.remove(dst_id)
                if src_id in end_nodes:
                    end_nodes.remove(src_id)

                self.make_connector(node, src_node, dst_node)

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

            if len(start_nodes) != 1 and len(added_links) > 0:
#                print("Error - there should be only one start node")
                pass
            elif len(start_nodes) == 1:
                start_evt = create_class("StartEvent")
                setattr(start_evt, "name", "StartEvent")
                getattr(node, "bplElements").append(start_evt)
                new_uuid = str(uuid.uuid4())
                setattr(start_evt, "bplElementName", new_uuid)
                setattr(start_evt, "bplElementId", new_uuid)
                setattr(start_evt, "bplElementUUID", new_uuid)

                self.make_connector(node, start_evt, added_children[start_nodes.pop()][0])

            end_evt = create_class("EndEvent")
            setattr(end_evt, "name", "EndEvent")
            getattr(node, "bplElements").append(end_evt)
            new_uuid = str(uuid.uuid4())
            setattr(end_evt, "bplElementName", new_uuid)
            setattr(end_evt, "bplElementId", new_uuid)
            setattr(end_evt, "bplElementUUID", new_uuid)

            for end_src in end_nodes:
                self.make_connector(node, added_children[end_src][0], end_evt)



        return (node, self.create_siblings(parent, obj, object_info, plan_table, object_id_table))

    def create_siblings(self, parent, parent_obj, parent_info, plan_table, object_id_table):
        if "siblings" not in parent_info:
            return []
        created_siblings = []
        for sibling in parent_info["siblings"]:
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
                    (new_sibling, sib_sibs) = self.create_object(parent, sibling["parent_field"], sibling_obj,
                                                                 sibling["table"], plan_table, object_id_table, [])
                    created_siblings.append(new_sibling)
                    for sib in sib_sibs:
                        created_siblings.append(sib)
        return created_siblings

    def create_data_collection(self, parent, parent_obj, parent_info, plan_table, object_id_table):
        data_coll_ok_out = create_class("OutputParameter")
        getattr(parent, "parameters").append(data_coll_ok_out)
        new_uuid = str(uuid.uuid4())
        setattr(data_coll_ok_out, "bplElementName", new_uuid)
        setattr(data_coll_ok_out, "bplElementId", new_uuid)
        setattr(data_coll_ok_out, "bplElementUUID", new_uuid)
        setattr(data_coll_ok_out, "name", "dataCollectionOkay")
        setattr(data_coll_ok_out, "paramName", "dataCollectionOkay")
        setattr(data_coll_ok_out, "paramType", "boolean")
        setattr(data_coll_ok_out, "scriptFormat", "javascript")

        prev_child = create_class("StartEvent")
        setattr(prev_child, "name", "StartEvent")
        getattr(parent, "bplElements").append(prev_child)
        new_uuid = str(uuid.uuid4())
        setattr(prev_child, "bplElementName", new_uuid)
        setattr(prev_child, "bplElementId", new_uuid)
        setattr(prev_child, "bplElementUUID", new_uuid)

        new_child = create_class("DataCollectionTask")
        getattr(parent, "bplElements").append(new_child)
        new_uuid = str(uuid.uuid4())
        setattr(new_child, "bplElementName", new_uuid)
        setattr(new_child, "bplElementId", new_uuid)
        setattr(new_child, "bplElementUUID", new_uuid)
        setattr(new_child, "description", "Enter "+getattr(parent_obj, "DAT_COL_TITLE")+" Value")

        limit_cols = ["PLAN_ID", "OPER_KEY", "STEP_KEY", "STEP_UPDT_NO", "DAT_COL_ID"]
        columns = []
        for col in limit_cols:
            columns.append((col, getattr(parent_obj, col)))
        joins = self.query("SFPL_STEP_DAT_COL_LIMIT", columns, plan_table)
        if len(joins) == 1:
            attr_value = getattr(joins[0], "LOWER_LIMIT")
            if attr_value is not None:
                setattr(new_child, "lowerLimit", attr_value)
            attr_value = getattr(joins[0], "UPPER_LIMIT")
            if attr_value is not None:
                setattr(new_child, "upperLimit", attr_value)
            attr_value = getattr(joins[0], "TARGET_VALUE")
            if attr_value is not None:
                setattr(new_child, "targetValue", attr_value)

        self.make_connector(parent, prev_child, new_child)
        prev_child = new_child

        new_child = create_class("Exclusive")
        getattr(parent, "bplElements").append(new_child)
        new_uuid = str(uuid.uuid4())
        setattr(new_child, "bplElementName", new_uuid)
        setattr(new_child, "bplElementId", new_uuid)
        setattr(new_child, "bplElementUUID", new_uuid)
        setattr(new_child, "description", "Is "+getattr(parent_obj, "DAT_COL_TITLE")+" within spec")

        data_coll_ok_in = create_class("InputParameter")
        getattr(parent, "parameters").append(data_coll_ok_in)
        new_uuid = str(uuid.uuid4())
        setattr(data_coll_ok_in, "bplElementName", new_uuid)
        setattr(data_coll_ok_in, "bplElementId", new_uuid)
        setattr(data_coll_ok_in, "bplElementUUID", new_uuid)
        setattr(data_coll_ok_in, "name", "dataCollectionOkay")
        setattr(data_coll_ok_in, "paramName", "dataCollectionOkay")
        setattr(data_coll_ok_in, "paramType", "boolean")
        setattr(data_coll_ok_in, "scriptFormat", "javascript")

        self.make_connector(parent, prev_child, new_child)
        prev_child = new_child

        end_event = create_class("EndEvent")
        setattr(end_event, "name", "EndEvent")
        getattr(parent, "bplElements").append(end_event)
        new_uuid = str(uuid.uuid4())
        setattr(end_event, "bplElementName", new_uuid)
        setattr(end_event, "bplElementId", new_uuid)
        setattr(end_event, "bplElementUUID", new_uuid)

        self.make_connector(parent, prev_child, end_event, output="Yes -> dataCollectionOkay=True",
                            condition_expression="dataCollectionOkay")

        error_event = create_class("ErrorEvent")
        getattr(parent, "bplElements").append(new_child)
        setattr(error_event, "name", "ErrorEvent")
        new_uuid = str(uuid.uuid4())
        setattr(error_event, "bplElementName", new_uuid)
        setattr(error_event, "bplElementId", new_uuid)
        setattr(error_event, "bplElementUUID", new_uuid)

        self.make_connector(parent, prev_child, error_event, output="No -> dataCollectionOkay=False",
                            condition_expression="!dataCollectionOkay")


    def create_buyoff(self, parent, parent_obj, parent_info, plan_table, object_id_table):
        prev_child = create_class("StartEvent")
        setattr(prev_child, "name", "StartEvent")
        getattr(parent, "bplElements").append(prev_child)
        new_uuid = str(uuid.uuid4())
        setattr(prev_child, "bplElementName", new_uuid)
        setattr(prev_child, "bplElementId", new_uuid)
        setattr(prev_child, "bplElementUUID", new_uuid)

        buyoff_task = create_class("UserTask")
        setattr(buyoff_task, "name", "BuyoffTask")
        getattr(parent, "bplElements").append(buyoff_task)
        new_uuid = str(uuid.uuid4())
        setattr(buyoff_task, "bplElementName", new_uuid)
        setattr(buyoff_task, "bplElementId", new_uuid)
        setattr(buyoff_task, "bplElementUUID", new_uuid)

        self.make_connector(parent, prev_child, buyoff_task)

        end_event = create_class("EndEvent")
        setattr(end_event, "name", "EndEvent")
        getattr(parent, "bplElements").append(end_event)
        new_uuid = str(uuid.uuid4())
        setattr(end_event, "bplElementName", new_uuid)
        setattr(end_event, "bplElementId", new_uuid)
        setattr(end_event, "bplElementUUID", new_uuid)

        self.make_connector(parent, buyoff_task, end_event)

    def create_footer(self, parent, parent_obj, parent_info, plan_table, object_id_table):
        data_coll_ok_in = create_class("InputParameter")
        getattr(parent, "parameters").append(data_coll_ok_in)
        new_uuid = str(uuid.uuid4())
        setattr(data_coll_ok_in, "bplElementName", new_uuid)
        setattr(data_coll_ok_in, "bplElementId", new_uuid)
        setattr(data_coll_ok_in, "bplElementUUID", new_uuid)
        setattr(data_coll_ok_in, "name", "dataCollectionOkay")
        setattr(data_coll_ok_in, "paramName", "dataCollectionOkay")
        setattr(data_coll_ok_in, "paramType", "boolean")
        setattr(data_coll_ok_in, "scriptFormat", "javascript")

        buyoff_ok_out = create_class("OutputParameter")
        getattr(parent, "parameters").append(buyoff_ok_out)
        new_uuid = str(uuid.uuid4())
        setattr(buyoff_ok_out, "bplElementName", new_uuid)
        setattr(buyoff_ok_out, "bplElementId", new_uuid)
        setattr(buyoff_ok_out, "bplElementUUID", new_uuid)
        setattr(buyoff_ok_out, "name", "buyoffOkay")
        setattr(buyoff_ok_out, "paramName", "buyoffOkay")
        setattr(buyoff_ok_out, "paramType", "boolean")
        setattr(buyoff_ok_out, "scriptFormat", "javascript")

        prev_child = create_class("StartEvent")
        setattr(prev_child, "name", "StartEvent")
        getattr(parent, "bplElements").append(prev_child)
        new_uuid = str(uuid.uuid4())
        setattr(prev_child, "bplElementName", new_uuid)
        setattr(prev_child, "bplElementId", new_uuid)
        setattr(prev_child, "bplElementUUID", new_uuid)

        end_event = create_class("EndEvent")

        setattr(end_event, "name", "EndEvent")
        getattr(parent, "bplElements").append(end_event)
        new_uuid = str(uuid.uuid4())
        setattr(end_event, "bplElementName", new_uuid)
        setattr(end_event, "bplElementId", new_uuid)
        setattr(end_event, "bplElementUUID", new_uuid)

        gateway = create_class("Exclusive")
        getattr(parent, "bplElements").append(gateway)
        new_uuid = str(uuid.uuid4())
        setattr(gateway, "name", "Exclusive")
        setattr(gateway, "bplElementName", new_uuid)
        setattr(gateway, "bplElementId", new_uuid)
        setattr(gateway, "bplElementUUID", new_uuid)
        setattr(gateway, "description", "dataCollectionOkay==True?")

        self.make_connector(parent, prev_child, gateway)

        self.make_connector(parent, gateway, end_event, output="No -> buyoffSuccessful=False",
                            condition_expression="!dataCollectionOkay")

        getattr(parent, "bplElements").append(end_event)
        buyoffs = self.query("SFPL_STEP_BUYOFF", [
            ("PLAN_ID", getattr(parent_obj, "PLAN_ID")),
            ("OPER_KEY", getattr(parent_obj, "OPER_KEY")),
            ("STEP_KEY", getattr(parent_obj, "STEP_KEY")),
            ("STEP_UPDT_NO", getattr(parent_obj, "STEP_UPDT_NO"))], plan_table)

        if len(buyoffs) == 0:
            self.make_connector(parent, gateway, end_event, output="No -> buyoffSuccessful=False",
                                condition_expression="dataCollectionOkay")
        elif len(buyoffs) == 1:
            (new_child, siblings) = self.create_object(parent, None, buyoffs[0], "SFPL_STEP_BUYOFF",
                                                       plan_table, object_id_table, [])
            getattr(parent, "bplElements").append(new_child)
            self.make_connector(parent, gateway, new_child, output="buyoffSuccessful")
            self.make_connector(parent, new_child, end_event, output="buyoffSuccessful")

            buyoff_ok = create_class("OutputParameter")
            getattr(parent, "parameters").append(buyoff_ok)
            new_uuid = str(uuid.uuid4())
            setattr(buyoff_ok, "bplElementName", new_uuid)
            setattr(buyoff_ok, "bplElementId", new_uuid)
            setattr(buyoff_ok, "bplElementUUID", new_uuid)
            setattr(buyoff_ok, "name", getattr(buyoffs[0], "BUYOFF_TYPE") + "BuyoffOkay")
            setattr(buyoff_ok, "paramName", getattr(buyoffs[0], "BUYOFF_TYPE") + "BuyoffOkay")
            setattr(buyoff_ok, "paramType", "boolean")
            setattr(buyoff_ok, "scriptFormat", "javascript")
        else:
            fork = create_class("Parallel")
            getattr(parent, "bplElements").append(fork)
            new_uuid = str(uuid.uuid4())
            setattr(fork, "name", "BuyoffStart")
            setattr(fork, "bplElementName", new_uuid)
            setattr(fork, "bplElementId", new_uuid)
            setattr(fork, "bplElementUUID", new_uuid)
            setattr(fork, "description", "Start Buyoffs")

            self.make_connector(parent, gateway, fork)

            join = create_class("Inclusive")
            getattr(parent, "bplElements").append(fork)
            new_uuid = str(uuid.uuid4())
            setattr(join, "name", "BuyoffFinish")
            setattr(join, "bplElementName", new_uuid)
            setattr(join, "bplElementId", new_uuid)
            setattr(join, "bplElementUUID", new_uuid)
            setattr(join, "description", "Finish Buyoffs")

            for buyoff in buyoffs:
                (new_child, siblings) = self.create_object(parent, None, buyoff, "SFPL_STEP_BUYOFF",
                                                           plan_table, object_id_table, {})
                getattr(parent, "bplElements").append(new_child)
                self.make_connector(parent, fork, new_child)
                self.make_connector(parent, new_child, join)

                buyoff_ok = create_class("OutputParameter")
                getattr(parent, "parameters").append(buyoff_ok)

                new_uuid = str(uuid.uuid4())
                setattr(buyoff_ok, "bplElementName", new_uuid)
                setattr(buyoff_ok, "bplElementId", new_uuid)
                setattr(buyoff_ok, "bplElementUUID", new_uuid)
                setattr(buyoff_ok, "name", getattr(buyoff, "BUYOFF_TYPE")+"BuyoffOkay")
                setattr(buyoff_ok, "paramName", getattr(buyoff, "BUYOFF_TYPE")+"BuyoffOkay")
                setattr(buyoff_ok, "paramType", "boolean")
                setattr(buyoff_ok, "scriptFormat", "javascript")


            self.make_connector(parent, join, end_event, "buyoffSuccessful")

    def import_plan(self, plan_table, plan_name):
        object_id_table = compute_object_index(plan_table)

        plan_desc = plan_table["SFPL_PLAN_DESC"][0]

        (process, _) = self.create_object(None, None, plan_desc, "SFPL_PLAN_DESC", plan_table, object_id_table, [])
        return process

def load_process(filename):
    importer = ImportSolumina()
    translate_table["SFPL_STEP_DAT_COL"]["custom_content"] = importer.create_data_collection
    translate_table["SFPL_STEP_REV"][0]["custom_content"] = importer.create_footer
    translate_table["SFPL_STEP_BUYOFF"]["custom_content"] = importer.create_buyoff

    plan_table = load_plan(filename)
    process = importer.import_plan(plan_table, filename)
    process.source = os.path.basename(filename)
    return process
