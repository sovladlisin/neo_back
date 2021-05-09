from .driver import NeoApp
from .onthology_namespace import *
import json
class Onthology:

    def __init__(self, uri, user, password):
        self.driver = NeoApp(uri,user, password)


    def getClasses(self):
        return self.driver.get_nodes_by_label(CLASS)

    def getSubClassesById(self, id):
        return self.driver.get_node_children(id, [SUB_CLASS], [CLASS])

    def getParentClasses(self, uri):
        res = self.driver.get_node_without_children(CLASS, SUB_CLASS, CLASS)
        return res
        return list(filter(lambda x: x.get('uri') == uri, res))

    def getClassById(self, id):
        class_node = self.driver.get_node_by_ID(id)
        attributes = self.driver.get_node_children(id, [PROPERTY_DOMAIN],[PROPERTY_LABEL])
        attributes_obj = self.driver.get_node_children(id, [PROPERTY_DOMAIN],[PROPERTY_LABEL_OBJECT])
        attributes_types = {}
        attributes_types_obj = {}
        for attr in attributes:
            types = self.driver.get_node_parents(attr.id, [PROPERTY_RANGE],['Resource'])
            attributes_types[attr.id] = None if len(types) == 0 else types[0]
        for attr in attributes_obj:
            types = self.driver.get_node_parents(attr.id, [PROPERTY_RANGE],[CLASS])
            attributes_types_obj[attr.id] = None if len(types) == 0 else types[0]

        objects = self.driver.get_nodes_by_labels([class_node.get('uri')])
        return class_node, attributes, objects, attributes_types, attributes_obj, attributes_types_obj

    def getClassObjects(self, id):
        node = self.driver.get_node_by_ID(id)
        return self.driver.get_nodes_by_labels([node.get('uri')])

    def getClassObject(self, id):
        node = self.driver.get_node_by_ID(id)
        node_labels = list(node.labels)
        label = ''
        for l in node_labels:
            if 'http://erlangen-crm.org/current/' in l:
                label = l
        class_node = self.driver.get_nodes_by_params(['Resource'],{'uri': label })[0]
        signature = class_node.get('signature')
        attributes = self.driver.get_node_children(class_node.id, [PROPERTY_DOMAIN],[PROPERTY_LABEL])
        attributes_obj = self.driver.get_connections_with_labels(id, [OBJECT])

        return node, signature, attributes, attributes_obj

    def nodeToDict(self, node):
        result = {}
        if node is None:
            return None
        result['id'] = node.id
        result['labels'] = list(node.labels)
        result['params'] = list(node.keys())
        for param in node.keys():
            result[param] = node.get(param)
        return result

    def relToDict(self, node):
        result = {}
        if node is None:
            return None
        result['id'] = node.id
        result['labels'] = [node.type]
        result['params'] = list(node.keys())
        result['start_node'] = self.nodeToDict(node.start_node)
        result['end_node'] = self.nodeToDict(node.end_node)
        for param in node.keys():
            result[param] = node.get(param)
        return result

    def updateEntity(self, new_node):
        params = new_node['params']
        id = new_node['id']
        props = {}
        for p in params:
            props[p] = new_node[p]
        return self.driver.set_node(id, props)

    def createEntity(self, labels, new_node):
        props = {}
        obj_props = {}
        for param in new_node:
            if isinstance(new_node[param], dict):
                obj_props[param] = new_node[param]
            else: 
                props[param] = new_node[param]
        
        created_node = self.driver.create_node(labels, props)
        print('IDIDIDIDIDI:', created_node.id)

        for key in obj_props:
            rel = obj_props[key]
            if (rel['direction'] == 1):
                self.driver.create_relation_forward(created_node.id, rel['object']['id'], [key], {})
            if (rel['direction'] == 0):
                self.driver.create_relation_forward( rel['object']['id'],created_node.id, [key], {})

        return created_node


    def addClassAttribute(self, class_id, type_uri, label, uri):
        type_node = self.driver.get_node_by_params({'uri': type_uri})
        type_id = type_node.id
        created_attr = self.driver.create_node(['Resource',PROPERTY_LABEL], {'uri':uri, LABEL: label})
        attr_id = created_attr.id
        print(attr_id)
        new_rel1 = self.driver.create_relation_forward(attr_id, class_id, [PROPERTY_DOMAIN], {})
        new_rel2 = self.driver.create_relation_forward(attr_id, type_id, [PROPERTY_RANGE], {})

        print(new_rel1, new_rel2)
        # new_rel = self.driver.create_relation(id_1, id_2, type, props)
        return created_type

    def getCorpuses(self):
        res = self.driver.get_node_without_children_reverse(CORPUS,CORPUS_RELATION, CORPUS)
        return res

    def getSubCorpuses(self,id):
        res = self.driver.get_node_parents(id,[CORPUS_RELATION], ['Resource'])
        return res

    def getClassesWithSignatures(self):
        query = "match (node:`{class_}`) where not node.signature is null return node".format(class_=CLASS)
        res = self.driver.custom_query(query, 'node')
        return res

    def getObjectsByClassUri(self, uri):
        return self.driver.get_nodes_by_labels([uri])

    def deleteEntity(self, id):
        return self.driver.delete_node_by_ID(id)

    def close(self):
        self.driver.close()
        return True


