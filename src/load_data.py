from services.neo4j_service import Neo4JService
from services.postgres_service import PostgresService


if __name__ == "__main__":
    neo4j_service = Neo4JService()
    print(neo4j_service.get_schema())
    neo4j_service.close()
