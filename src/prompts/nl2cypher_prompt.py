from services.ai_model_service import AIModelService
from services.neo4j_service import Neo4JService


class NL2CypherPrompt:

    def __init__(self):
        self.ai_model_service = AIModelService()

        try:
            self.neo4j_service = Neo4JService()

        except Exception as e:
            raise e

        self.database_schema = self.neo4j_service.get_schema()

    def gen_prompt(self, user_input) -> str:

        # TODO use self.database_schema
        context = f"""...."""

        instructions = f"""..."""

        task = f"""... and the following question: 
            {user_input}"""

        return f"""Context:
            {context} 

            Instructions:
            {instructions} 
            
            Task:
            {task}

            Answer :
            """
