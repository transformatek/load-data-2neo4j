import os
from dotenv import load_dotenv, find_dotenv
from neo4j import GraphDatabase
from services.postgres_service import PostgresService

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

NEO4J_USER = os.getenv("NEO4J_USER", "")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")


class Neo4JService:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            uri=NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
        )

    def __call__(self):
        return self.driver.session()

    @property
    def labels(self):
        query = "CALL db.labels()"
        return [label["label"] for label in self(query)]

    def run_query(self, query):
        session = self()
        return session.run(query).data()

    def format_data(self, data):
        formatted_data = ""
        for node in data:
            for key, value in node.items():
                formatted_data += f"{key.split('.').pop()}: {value}\n"
        return formatted_data

    def run_queries(self, queries):
        return [self.run_query(query) for query in queries]

    def label_exists(self, label_name):
        return label_name in self.labels

    def nodes(self, label="", limit=25):
        if label:
            query = f"MATCH (n:{label}) RETURN n LIMIT {limit}"
        else:
            query = f"MATCH (n) RETURN n LIMIT {limit}"
        with self.driver.session() as session:
            result = session.run(query)
            return [record["n"] for record in result]

    def create(self, label: str, data: list[dict]):
        props = [
            (
                "{"
                + ", ".join([f'{key}: "{value}"' for key, value in item.items()])
                + "}"
            )
            for item in data
        ]
        queries = "\n".join([f"CREATE (:{label} {prop})" for prop in props])
        with self.driver.session() as session:
            session.run(queries)

    def delete_table(self, label):
        query = f"MATCH (t: {label}) DELETE t"
        with self.driver.session() as session:
            session.run(query)

    def import_pg(
        self, table: PostgresService.Table, columns: list[str] = "*", limit: int = 25
    ):
        records = table.records(columns=columns, limit=limit)
        self.create(table.name, data=records)

    def clean(self):
        query = f"MATCH (n) DETACH DELETE n"
        with self.driver.session() as session:
            session.run(query)

    def close(self):
        self.driver.close()

    @property
    def node_props(self):
        query = """MATCH (node) RETURN (node)"""
        return self.run_query(query)

    @property
    def rel_props(self):
        query = """
        MATCH (node_1)-[relationship]->(node_2) 
        RETURN node_1, relationship, node_2
        """
        rel_props = self.run_query(query)
        return rel_props

    def get_schema(self):
        schema = f"""
        This is the schema representation of the Neo4J database:
        \n\n\n
        Node properties are as follows:
        
        {self.node_props}
         
        Relationship properties are as follows:
        
        {self.rel_props}
        """

        return schema
