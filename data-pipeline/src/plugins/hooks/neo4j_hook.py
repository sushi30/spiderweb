from airflow.hooks.dbapi_hook import DbApiHook
from neo4j import GraphDatabase


class Neo4jHook(DbApiHook):
    conn_name_attr = "neo4j_conn_id"
    default_conn_name = "ne4j_default"

    def get_conn(self):
        conn = self.get_connection(self.neo4j_conn_id)
        return GraphDatabase.driver(
            "{c.conn_type}://{c.host}:{c.port}".format(c=conn),
            auth=(conn.login, conn.password),
        )
