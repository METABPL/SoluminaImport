from . import class_model

class WebgmeImport:
    def __init__(self, core, namespace, meta):
        self.core = core
        self.namespace = namespace
        self.namespace_prefix = namespace + "."
        self.meta = meta

    def get_type(self, node):
        return self.core.get_attribute(self.core.get_meta_type(node), "name")

    def is_type(self, node, type_name):
#        if not type_name.startswith(self.namespace_prefix):
#            type_name = self.namespace_prefix + type_name
        return self.core.is_type_of(node, self.meta[type_name])

    def copy_attrs(self, webgme_node, dest_node):
        vars_map = {}
        node_attrs = vars(dest_node)
        for var_name in node_attrs.keys():
            vars_map[var_name.lower()] = var_name

        for webgme_attr_name in self.core.get_attribute_names(webgme_node):
            if webgme_attr_name.lower() in vars_map:
                attr_val = self.core.get_attribute(webgme_node, webgme_attr_name)
                if attr_val is not None:
                    setattr(dest_node, vars_map[webgme_attr_name.lower()], attr_val)

    def add_to_node_list(self, node, node_list):
        for curr_node in node_list:
            if node.bplElementUUID == curr_node.bplElementUUID:
                return
        node_list.append(node)

    def import_node(self, node, node_map):
        node_type = self.get_type(node)

        if not hasattr(class_model, node_type):
            return None

        node_uuid = self.core.get_attribute(node, "BPLElementUUID")
        if node_uuid is not None and node_uuid in node_map:
            return node_map[node_uuid]

        new_node =  getattr(class_model, node_type)()
        self.copy_attrs(node, new_node)

        for child in self.core.load_children(node):
            if self.is_type(child, "ConnectionBase"):
                child_uuid = self.core.get_attribute(child, "BPLElementUUID")
                if child_uuid in node_map:
                    continue

                src_node = self.core.load_pointer(child, "src")
                new_src = self.import_node(src_node, node_map)
                if new_src is None:
                    continue
                dst_node = self.core.load_pointer(child, "dst")
                new_dst = self.import_node(dst_node, node_map)
                if new_dst is None:
                    continue

                child_type = self.get_type(child)
                new_child = getattr(class_model, child_type)()
                node_map[child_uuid] = new_child
                self.copy_attrs(child, new_child)
                new_child.fromNode = new_src
                new_child.toNode = new_dst

                new_child.parent = node
                self.add_to_node_list(new_child, new_src.nexts)
                self.add_to_node_list(new_child, new_dst.prevs)
                self.add_to_node_list(new_child, new_node.bplElements)

            elif self.is_type(child, "BPLElement"):
                child_uuid = self.core.get_attribute(child, "BPLElementUUID")
                if child_uuid not in node_map:
                    child_type = self.get_type(child)
                    new_child = getattr(class_model, child_type)()
                    self.copy_attrs(child, new_child)
                    node_map[child_uuid] = new_child
                    new_child.parent = node
                else:
                    new_child = node_map[child_uuid]

                self.add_to_node_list(new_child, new_node.bplElements)

            elif self.is_type(child, "ResourceRequirement"):
                for res_req in self.core.load_children(child):
                    new_res_req = self.import_node(res_req, node_map)
                    new_res_req.parent = node
                    if new_res_req is not None:
                        self.add_to_node_list(new_res_req, new_node.resourceRequirements)

        return new_node
