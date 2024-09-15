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
        Make sure that the Cypher query does run successfully on the given schema.
        Make sure that your answer is logical.
        Follow the structure of the database schema strictly.
        Do not include any explanations, apologies, or anything other than the Cypher query in your answer.
        """
        return f"""Context:
            {context} 
            
            Task:
            {task}
            
            Constraints:
            {constraints}
            
            Answer:
            """

    def gen_summary_prompt(self) -> str:

        context = self.neo4j_service.nodes(limit=100)

        task = f"""
        You are required to generate a textual summary of the data provided in the Neo4j database:
        """

        constraints = """
        Do not include any explanations, apologies, recommendations, or anything other than the summary of the data in your response.
        """
        return f"""
            Context:
            {context} 
            
            Task:
            {task}
            
            Constraints:
            {constraints}
            
            Answer:
            """

    def prompt_llm(self, prompt):
        return self.ai_model_service(prompt)
