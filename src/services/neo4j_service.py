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
        """
        Retrieves the names of all labels in a Neo4J database.
        Returns:
            list: A list of label names as strings.
        """
        query = "CALL db.labels()"
        return [label["label"] for label in self(query)]

    def run_query(self, query):
        """
        Runs a Cypher query on a Neo4j database
        Args:
            query (str): The Cypher query to execute.
        Returns:
            list: A list of dictionaries containing the results of the query.
        """
        session = self()
        return session.run(query).data()

    def format_data(self, data):
        """
        Formats data from a Neo4j query into a human-readable string.
        Args:
            data (list): The data to format.
        Returns:
            str: A formatted string representation of the data.
        """
        formatted_data = ""
        for node in data:
            for key, value in node.items():
                formatted_data += f"{key.split('.').pop()}: {value}\n"
        return formatted_data

    def run_queries(self, queries):
        """
        Runs Cypher queries on a Neo4j database
        Args:
            queries (list): The Cypher queries to execute.
        Returns:
            list: A list of dictionaries containing the results of the query.
        """

        return [self.run_query(query) for query in queries]

    def label_exists(self, label_name):
        """
        Checks if a label exists in a Neo4j database
        Args:
            label_name (str): The name of the label to check for.
        Returns:
            bool: True if the label exists, False otherwise.
        """
        return label_name in self.labels

    def nodes(self, label="", limit=25):
        """
        Retrieves nodes from a Neo4j database.
        Args:
            label (str): The label of the nodes to retrieve.
            limit (int): The maximum number of nodes to retrieve.
        Returns:
            list: A list of nodes as dictionaries.
        """
        if label:
            query = f"MATCH (n:{label}) RETURN n LIMIT {limit}"
        else:
            query = f"MATCH (n) RETURN n LIMIT {limit}"
        with self.driver.session() as session:
            result = session.run(query)
            return [record["n"] for record in result]

    def create(self, label: str, data: list[dict]):
        """
        Creates nodes in a Neo4j database.
        Args:
            label (str): The label of the nodes to create.
            data (list): A list of dictionaries containing the properties of the nodes to create.
        Returns:
            None"""
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
        """
        Deletes all nodes of a specified label from a Neo4j database.
        Args:
            label (str): The label of the nodes to delete.
        Returns:
            None
        """
        query = f"MATCH (t: {label}) DELETE t"
        with self.driver.session() as session:
            session.run(query)

    def import_pg(self, tables: list[Table], rels: list):
        """
        Imports data from a PostgreSQL database into a Neo4j database.
        Args:
            tables (list): A list of Table objects representing the tables to import.
            rels (list): A list of tuples representing relationships between tables (the foreign key constraints).
        Returns:
            None
        """
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
        """
        Deletes all nodes and relationships from a Neo4j database.
        Returns:
            None
        """
        query = f"MATCH (n) DETACH DELETE n"
        with self.driver.session() as session:
            session.run(query)

    def close(self):
        self.driver.close()

    @property
    def node_props(self):
        """
        Retrieves the properties of node types in the Neo4j database schema.
        Returns:
            list: A list of dictionaries, where each dictionary contains the properties 
                  of a node type in the Neo4j database schema.
        """

        query = """CALL db.schema.nodeTypeProperties()"""
        return self.run_query(query)

    @property
    def rel_type_props(self):
        """
        Retrieves the properties of relationship types in the Neo4j database schema.
        Returns:
            list: A list of dictionaries, where each dictionary contains the properties 
                  of a relationship type in the Neo4j database schema.
        """
        query = """
        CALL db.schema.relTypeProperties()
        """
        rel_props = self.run_query(query)
        return rel_props

    @property
    def visualization(self):
        """
        Visualizes a Neo4j database schema.
        Returns:
            str: A string representation of the database schema visualization.
        """
        query = """
        CALL db.schema.visualization()
        """
        return self.run_query(query)

    def get_schema(self):
        """
        Retrieves the schema of a Neo4j database to be used for an LLM.
        Returns:
            str: A string representation of the database schema.
        """
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
