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

        context = self.database_schema

        task = f"""You are required to generate Cypher queries that answer the following question(s) 
        based on the Graph schema:
        
        '{user_input}'
        """

        constraints = """
        Do not include any explanations, apologies, or anything other than the Cypher query in your answer.
        Make sure that the Cypher query does run successfully on the given schema."""
        return f"""Context:
            {context} 
            
            Task:
            {task}
            
            Constraints:
            {constraints}
            
            Answer:
            """

    def prompt_llm(self, prompt):
        return self.ai_model_service(prompt)
