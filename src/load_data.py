import os
from dotenv import load_dotenv, find_dotenv
import psycopg2
from neo4j import GraphDatabase
from services.neo4j_service import Neo4JService
from services.postgres_service import PostgresService

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


if __name__ == "__main__":
    psql_service = PostgresService("testdb", "postgres")
    tripdata = psql_service.Table(psql_service, "tripdata")
    print(tripdata.columns())
    print(tripdata.retrieve(["congestion_surcharge"]))
    neo4j_service = Neo4JService()
    neo4j_service.import_pg(tripdata)
    neo4j_service.clean()
    neo4j_service.close()
