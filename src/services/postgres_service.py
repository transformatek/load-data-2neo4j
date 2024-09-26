import os
from dotenv import load_dotenv, find_dotenv
import psycopg2

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

PSQL_PASSWORD = os.getenv("PSQL_PASSWORD", "postgres")
PSQL_USER = os.getenv("PSQL_USER", "postgres")
PSQL_HOST = os.getenv("PSQL_HOST", "localhost")
PSQL_PORT = os.getenv("PSQL_PORT", "5432")


class PostgresService:

    def __init__(self, database="testdb"):
        conn = psycopg2.connect(
            database=database,
            user=PSQL_USER,
            password=PSQL_PASSWORD,
            host=PSQL_HOST,
            port=PSQL_PORT,
        )
        conn.autocommit = True
        self.conn = conn

    def __call__(self):
        cursor = self.conn.cursor()
        return cursor

    @property
    def tables(self):
        """
        Retrieves the names of all tables in a PostgreSQL database.
        Returns:
            list: A list of table names as strings.
        """

        cursor = self()
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        )
        return [table[0] for table in cursor.fetchall()]

    def table_exists(self, table_name: str):
        """
        Checks if a table exists in a PostgreSQL database.
        Args:
            table_name (str): The name of the table to check for.
        Returns:
            bool: True if the table exists, False otherwise.
        """
        query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')"
        return self.run_query(query)[0]

    def run_query(self, query: str):
        """
        Executes a SQL query on a PostgreSQL database.
        Args:
            query (str): The SQL query to execute.
        Returns:
            list: The returned records as a list of tuples.
        """
        cursor = self()
        cursor.execute(query)

        return cursor.fetchall()

    def run_queries(self, queries: list[str]):
        """
        Executes a SQL query on a PostgreSQL database.
        Args:
            queries (list): The SQL queries to execute.
        Returns:
            list: The returned records as a list of tuples.
        """
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
            columns = ", ".join([f"{name} {type}" for (name, type) in cols])
            service.run_query(f"CREATE TABLE IF NOT EXISTS {name} ({columns})")
        else:
            raise ValueError("Please provide names for your columns.")

    def __repr__(self):
        return self.name

    def retrieve(self, columns: list[str] = "*", limit: int = 25):
        """
        Retrieves records from a table in a PostgreSQL database.
        If columns are specified, only those columns will be returned, otherwise all columns will be returned.
        Args:
            columns (list): The columns to retrieve.
            limit (int): The maximum number of records to retrieve.
        Returns:
            list: A list of dictionaries representing the records, containing their type, column name, and value.
        """
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
        """
        Retrieves records from a table in a PostgreSQL database.
        If columns are specified, only those columns will be returned, otherwise all columns will be returned.
        Args:
            columns (list): The columns to retrieve.
            limit (int): The maximum number of records to retrieve.
        Returns:
            list: A list of tuples representing the records, containing column name and value.
        """
        """
        Retrieves records 
        """
        records = self.retrieve(columns, limit)
        return [
            {key: record[key]["value"] for key in record.keys()} for record in records
        ]

    def columns(self, cols: list[str] = "*"):
        """
        Returns the list of columns of a table
        If columns are specified, only those columns, along with their types will be returned, otherwise all columns will be returned.
        Args:
            cols (list): The columns to retrieve.
        Returns:
            list: A list of tuples representing the columns, containing column name and type
        """
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
