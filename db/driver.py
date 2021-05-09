from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import json

class NeoApp:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def get_nodes_by_labels(self, labels):

        def _service_func(tx,labels):
            t_labels = self.transform_labels(labels)
            query = 'MATCH (n:{labels}) RETURN n AS node'.format(labels=t_labels)
            request = tx.run(query)
            return [record['node'] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func, labels)
        
        return list(result)

    def get_nodes_by_params(self, labels, params):

        def _service_func(tx,labels, params):
            search_query = "WHERE"
            iter = 0
            for param in params:
                value = params[param]
                key = param
                link = " " if iter == 0 else " AND"  
                search_query += "{link} n.`{key}` = {value} ".format(link=link ,key=key, value=json.dumps(value))
                iter += 1
            t_labels = self.transform_labels(labels)

            query = "MATCH (n:{labels}) {search} RETURN n AS node".format(labels=t_labels, search=search_query)
            request = tx.run(query)
            return [record["node"] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func, labels, params)
        
        return list(result)

    def get_node_by_params(self, params):

        def _service_func(tx, params):
            search_query = "WHERE"
            iter = 0
            for param in params:
                value = params[param]
                key = param
                link = " " if iter == 0 else " AND"  
                search_query += "{link} n.`{key}` = {value} ".format(link=link ,key=key, value=json.dumps(value))
                iter += 1

            query = "MATCH (n) {search} RETURN n AS node".format(search=search_query)
            request = tx.run(query)
            return [record["node"] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func, params)
        
        return result[0]
    
    def get_all_labels(self):

        def _service_func(tx):
            request = tx.run("MATCH (n) RETURN distinct labels(n), count(*)")
            return [{"label": record["labels(n)"][0], "count": record["count(*)"]} for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func)
        
        return result

    def get_node_by_ID(self, id):
        def _service_func(tx,id):
            query = "MATCH (n) WHERE ID(n) = {id} RETURN n as node".format(id=id)
            request = tx.run(query)
            return [record["node"] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func, id)
        
        return result[0]

    def get_node_children(self, id, relation_labels, child_labels):
        def _service_func(tx,id,relation_labels,child_labels):
            t_child_labels = self.transform_labels(child_labels)
            t_relation_labels = self.transform_labels(relation_labels)
            query = "MATCH (node:{child_labels}) -[r:{relation_labels}]-> (n) WHERE ID(n) = {id} RETURN node".format(id=id, relation_labels=t_relation_labels, child_labels=t_child_labels)
            
            request = tx.run(query)
            return [record["node"] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func, id,relation_labels,child_labels)
        
        return result

    def get_node_parents(self, id, relation_labels, child_labels):
        def _service_func(tx,id,relation_labels,child_labels):
            t_child_labels = self.transform_labels(child_labels)
            t_relation_labels = self.transform_labels(relation_labels)
            query = "MATCH (node:{child_labels}) <-[r:{relation_labels}]- (n) WHERE ID(n) = {id} RETURN node".format(id=id, relation_labels=t_relation_labels, child_labels=t_child_labels)
            
            request = tx.run(query)
            return [record["node"] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func, id,relation_labels,child_labels)
            print(result)
        return result

    def get_node_without_children(self, parent_label ,relation, child_label):
        def _service_func(tx,id):
            query = "MATCH (node:`{parent_label}`) WHERE NOT (node) - [:`{relation}`] -> (:`{child_label}`) RETURN node".format(relation=relation, child_label=child_label, parent_label=parent_label)
            request = tx.run(query)
            return [record["node"] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func, id)
        
        return result

    def get_node_without_children_reverse(self, parent_label ,relation, child_label):
        def _service_func(tx,id):
            query = "MATCH (node:`{child_label}`) WHERE NOT (node) <- [:`{relation}`] - (:`{parent_label}`) RETURN node".format(relation=relation, child_label=child_label, parent_label=parent_label)
            request = tx.run(query)
            return [record["node"] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func, id)
        
        return result

    def get_connections_with_labels(self, id, labels):
        def _service_func(tx,id, labels):
            t_labels = self.transform_labels(labels)

            query = "MATCH (node) - [r] - (n:{labels}) WHERE ID(node) = {id} RETURN n,r".format(id=id, labels=t_labels)
            request = tx.run(query)
            return [record["r"] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func, id, labels)
        
        return result

    def custom_query(self, query, params):
        def _service_func(tx,query,params):
            request = tx.run(query)
            return [record[params] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func,query,params)
        
        return result

    def create_node(self, labels, props):
        def _service_func(tx, labels, props):
            data = self.transform_props(props)
            t_labels = self.transform_labels(labels)
            query = ("CREATE (n:{labels} {data}) RETURN n AS node").format(labels=t_labels, data=data)
            request = tx.run(query)
            return [record["node"] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func,  labels, props)
        
        return result[0]

    def create_relation_forward(self, id_1, id_2, r_labels, props):
        def _service_func(tx, id_1, id_2, r_labels, props):
            data = self.transform_props(props)
            t_labels = self.transform_labels(r_labels)
            query = """
                    MATCH
                    (a),
                    (b)
                    WHERE ID(a) = {id_1} AND ID(b) = {id_2}
                    CREATE (a)-[r:{r_labels} {data}]->(b)
                    RETURN r
            """.format(id_1=id_1, id_2=id_2, r_labels = t_labels, data=data)

            request = tx.run(query, r_labels=r_labels, props=props)
            return [record["r"] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func,  id_1, id_2, r_labels, props)
        
        return result[0]

    def set_node(self, id, props):
        def _service_func(tx, id, props):
            data = self.transform_props(props)
            query = "MATCH (n) WHERE ID(n) = {id} SET n += {data} RETURN n AS node".format(id=id, data=data)
            request = tx.run(query)
            return [record["node"] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func,  id, props)
        
        return result[0]
    
    def delete_node_by_ID(self, id):
        def _service_func(tx, id):
            data = self.transform_props(props)
            query = "MATCH (n) WHERE ID(n) = {id} DETACH DELETE n".format(id=id)
            request = tx.run(query)
            return True

        with self.driver.session() as session:
            result = session.write_transaction(_service_func,  id)
        
        return result

    def transform_labels(self, labels):
        if len(labels) == 0:
            return '``'
        res = ''
        for l in labels:
            res +='`{l}`:'.format(l=l)
        return res[:-1]

    def transform_props(self, props):
        if len(props) == 0:
            return ''
        data = "{"
        # print(props)
        for p in props:
            temp = "`{p}`".format(p=p)
            temp +=':'
            temp += "{val}".format(val = json.dumps(props[p]))
            data += temp + ','
        data = data[:-1]
        data += "}"
        return data



        