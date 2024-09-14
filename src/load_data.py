from services.neo4j_service import Neo4JService
from services.postgres_service import PostgresService, Table
from prompts.nl2cypher_prompt import NL2CypherPrompt
from services.ai_model_service import AIModelService

if __name__ == "__main__":
    psql_service = PostgresService()
    neo4j_service = Neo4JService()
    continents = Table(psql_service, "continents")
    countries = Table(psql_service, "countries")
    cities = Table(psql_service, "cities")
    rels = [
        ("cities", "countries", "country_id", "country_id", "IS_LOCATED_IN"),
        ("countries", "continents", "continent_id", "continent_id", "IS_LOCATED_IN"),
    ]
    neo4j_service.import_pg_schema([cities, countries, continents], rels=rels)
