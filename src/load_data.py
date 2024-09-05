import os
from dotenv import find_dotenv, load_dotenv
import psycopg2
from neo4j import GraphDatabase

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


class PostgresService:

    def __init__(self, database, user, host="127.0.0.1", port="5432"):
        PSQL_PASSWORD = os.getenv("PSQL_PASSWORD")
        conn = psycopg2.connect(
            database=database,
            user=user,
            password=PSQL_PASSWORD,
            host=host,
            port=port,
        )
        conn.autocommit = True
        self.conn = conn

    def __call__(self):
        cursor = self.conn.cursor()
        return cursor

    def columns(self, table: str):
        cursor = self()
        cursor.execute(
            """
            SELECT column_name FROM information_schema.columns WHERE table_schema = 'testdb'
            """
        )
        print(cursor.fetchall())
        cursor.execute(f"SELECT * FROM {table} LIMIT 0")
        columns = [desc[0] for desc in cursor.description]
        return columns

    def run_query(self, query: str):
        cursor = self()
        cursor.execute(query)
        return cursor

    def run_queries(self, queries: list[str]):
        cursor = self()
        result = []
        for query in queries:
            cursor.execute(query)
            result.append(cursor)

        return result

    def close(self):
        self.conn.close()


class Neo4JService:
    def __init__(self, uri):
        NEO4J_AUTH = os.getenv("NEO4J_AUTH")
        self.driver = GraphDatabase.driver(uri, auth=NEO4J_AUTH)

    def __call__(self, database):
        session = self.driver.session(database=database)
        transaction = session.begin_transaction()
        return transaction

    def nodes(self, table, limit=25):
        query = f"MATCH (n:{table}) RETURN n LIMIT {limit}"
        result = self()
        result.run(query)
        return [record for record in result]

    def create(self, table, data):
        props = [
            (
                "{"
                + ", ".join([f'{key}: "{value}"' for key,
                            value in item.items()])
                + "}"
            )
            for item in data
        ]
        queries = "\n".join([f"CREATE (:{table} {prop})" for prop in props])

        result = self()
        result.run(queries)

    def delete_table(self, table):
        query = f"MATCH (t: {table}) DELETE t"
        result = self()
        result.run(query)

    def delete_all(self):
        query = f"MATCH (n) DETACH DELETE n"
        result = self()
        result.run(query)

    def close(self):
        self.driver.close()


if __name__ == '__main__':
    ...
