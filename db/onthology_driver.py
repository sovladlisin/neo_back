from .driver import NeoApp
from .onthology_namespace import *
class Onthology:

    def __init__(self, uri, user, password):
        self.driver = NeoApp(uri,user, password)


    def getClasses(self):
        return self.driver.get_nodes_by_label(CLASS)

    def getSubClassesById(self, id):
        return self.driver.get_node_children(id, SUB_CLASS, CLASS)

    def getParentClasses(self, uri):
        res = self.driver.get_node_without_children(CLASS, SUB_CLASS, CLASS)
        return res
        return list(filter(lambda x: x.get('uri') == uri, res))

    def getClassObjects(self, id):
        node = self.driver.get_node_by_ID(id)
        return self.driver.get_nodes_by_label(node.get('uri'))

    def nodeToDict(self, node):
        result = {}
        result['id'] = node.id
        result['labels'] = list(node.labels)
        result['params'] = list(node.keys())
        for param in node.keys():
            result[param] = node.get(param)
        return result


    def close(self):
        self.driver.close()
        return True


