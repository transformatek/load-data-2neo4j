from services.neo4j_service import Neo4JService
from services.postgres_service import PostgresService
from prompts.nl2cypher_prompt import NL2CypherPrompt
from services.ai_model_service import AIModelService

if __name__ == "__main__":
    ai_model_service = AIModelService()
