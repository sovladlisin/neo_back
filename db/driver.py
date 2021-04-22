from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import json

class NeoApp:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def get_nodes_by_label(self, label):

        def _service_func(tx,label):
            query = 'MATCH (n:`{label}`) RETURN n AS node'.format(label=label)
            request = tx.run(query)
            return [record['node'] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func, label)
        
        return list(result)

    def get_nodes_by_params(self, label, params):

        def _service_func(tx,label, params):
            search_query = "WHERE"
            iter = 0
            for param in params:
                value = params[param]
                key = param
                link = " " if iter == 0 else " AND"  
                search_query += "{link} n.{key} = {value} ".format(link=link ,key=key, value=value)
                iter += 1

            query = "MATCH (n:`{label}`) {search} RETURN n AS node".format(label=label, search=search_query)
            request = tx.run(query)
            return [record["node"] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func, label, params)
        
        return list(result)
    
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

    def get_node_children(self, id, relation, child_label):
        def _service_func(tx,id):
            query = "MATCH (node:`{child_label}`) -[r:`{relation}`]-> (n) WHERE ID(n) = {id} RETURN node".format(id=id, relation=relation, child_label=child_label)
            request = tx.run(query)
            return [record["node"] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func, id)
        
        return result

    def get_node_without_children(self, parent_label ,relation, child_label):
        def _service_func(tx,id):
            query = "MATCH (node:`{parent_label}`) WHERE NOT (node) - [:`{relation}`] -> (:`{child_label}`) RETURN node".format(relation=relation, child_label=child_label, parent_label=parent_label)
            request = tx.run(query)
            return [record["node"] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func, id)
        
        return result

    def create_node(self, label, props):
        def _service_func(tx, label, props):
            data = '{'
            for p in props:
                temp = p
                temp +=':'
                temp += props[p]
                data+= temp + ','
            data = data[:-1]
            data += '}'
                
            query = ("CREATE (n:{label} {data}) RETURN n AS node").format(label=label, data=data)
            request = tx.run(query, label=label, props=props)
            return [record["node"] for record in request]

        with self.driver.session() as session:
            result = session.write_transaction(_service_func,  label, props)
        
        return result[0]

    

        