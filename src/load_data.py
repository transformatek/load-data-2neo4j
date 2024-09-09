import os
from dotenv import load_dotenv, find_dotenv
import psycopg2
from neo4j import GraphDatabase

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


class PostgresService:

    def __init__(self, database, user, password, host="127.0.0.1", port="5432"):
        conn = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port,
        )
        conn.autocommit = True
        self.conn = conn

    def __call__(self):
        cursor = self.conn.cursor()
        return cursor

    @property
    def tables(self):
        cursor = self()
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        )
        return [table[0] for table in cursor.fetchall()]

    def table_exists(self, table_name: str):
        query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')"
        return self.run_query(query)[0]

    def run_query(self, query: str):
        cursor = self()
        cursor.execute(query)

        return cursor.fetchall()

    def run_queries(self, queries: list[str]):
        cursor = self()
        result = []
        for query in queries:
            cursor.execute(query)
            result.append(cursor.fetchall())

        return result

    def close(self):
        self.conn.close()

    class Table:
        def __init__(self, service, name: str, cols: list = None):
            self.service = service
            self.name = name
            if service.table_exists(name):
                if not cols:
                    cols = "*"
                columns = ", ".join([f"{col}" for col in cols])
                service.run_query(f"SELECT {columns} FROM {name}")
            elif cols:
                columns = ", ".join(
                    [f"{name} {type}" for (name, type) in cols])
                service.run_query(
                    f"CREATE TABLE IF NOT EXISTS {name} ({columns})")
            else:
                raise ValueError("Please provide names for your columns.")

        def __repr__(self):
            return self.name

        def retrieve(self, columns: list[str] = "*", limit: int = 25):
            service = self.service
            query = f"SELECT {', '.join(columns)} FROM {self.name} LIMIT {limit}"
            records = service.run_query(query)
            result = []
            for record in records:
                record_dict = {}
                for (col_name, col_type), value in zip(self.columns(columns), record):
                    record_dict[col_name] = {"type": col_type, "value": value}
                result.append(record_dict)
            return result

        def records(self, columns: list[str] = "*", limit: int = 25):
            records = self.retrieve(columns, limit)
            return [
                {key: record[key]["value"] for key in record.keys()}
                for record in records
            ]

        def columns(self, cols: list[str] = "*"):
            cursor = self.service()
            if cols == "*":
                cursor.execute(f"SELECT * FROM {self.name} LIMIT 0")
            else:
                cursor.execute(
                    f"SELECT {', '.join([col for col in cols])} FROM {self.name} LIMIT 0"
                )
            columns = [(desc[0], desc[1]) for desc in cursor.description]
            updated_columns = []
            for column in columns:
                cursor.execute(
                    f"SELECT typname FROM pg_type WHERE oid={column[1]}")
                updated_columns.append((column[0], cursor.fetchall()[0][0]))
            return updated_columns


class Neo4JService:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def __call__(self):
        with self.driver.session() as session:
            return session

    @property
    def labels(self):
        query = "CALL db.labels()"
        return [label["label"] for label in self(query)]

    def run_query(self, query):
        session = self()
        return session.run(query).data()

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


if __name__ == "__main__":
    PSQL_PASSWORD = os.getenv("PSQL_PASSWORD")
    psql_service = PostgresService("testdb", "postgres", PSQL_PASSWORD)
    tripdata = psql_service.Table(psql_service, "tripdata")
    print(tripdata.columns())
    print(tripdata.retrieve(["congestion_surcharge"]))
    NEO4J_USER = os.getenv("NEO4J_USER")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
    neo4j_service = Neo4JService(
        "bolt://localhost:7687", NEO4J_USER, NEO4J_PASSWORD)
    neo4j_service.import_pg(tripdata)
    neo4j_service.clean()
    neo4j_service.close()
