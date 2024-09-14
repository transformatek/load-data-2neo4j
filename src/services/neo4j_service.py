import os
from dotenv import load_dotenv, find_dotenv
from neo4j import GraphDatabase
from services.postgres_service import Table

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
                + ", ".join([f'{key}: "{value}"' for key,
                            value in item.items()])
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

    def import_pg(self, tables: list[Table], rels: list):
        for table in tables:
            records = table.records()
            self.create(table.name, records)

        for source_table, target_table, source_col, target_col, rel_name in rels:
            query = f"""
            MATCH (a:{source_table}), (b:{target_table})
            WHERE a.{source_col} = b.{target_col}
            CREATE (a)-[:{rel_name}]->(b)
            """

            self.run_query(query)

    def clean(self):
        query = f"MATCH (n) DETACH DELETE n"
        with self.driver.session() as session:
            session.run(query)

    def close(self):
        self.driver.close()

    @property
    def node_props(self):
        query = """CALL db.schema.nodeTypeProperties()"""
        return self.run_query(query)

    @property
    def rel_type_props(self):
        query = """
        CALL db.schema.relTypeProperties()
        """
        rel_props = self.run_query(query)
        return rel_props

    @property
    def visualization(self):
        query = """
        CALL db.schema.visualization()
        """
        return self.run_query(query)

    def get_schema(self):
        schema = f"""
        This is the schema representation of the Neo4J database:
        \n\n\n
        Node type properties are as follows:
        
        {self.node_props}
         
        Relationship type properties are as follows:
        
        {self.rel_type_props}
        
        The database is visualized as follows:
        
        {self.visualization}
        """

        return schema
