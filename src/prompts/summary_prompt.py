from services.ai_model_service import AIModelService
from services.neo4j_service import Neo4JService


class SummaryPrompt:

    def __init__(self):
        self.ai_model_service = AIModelService()

        try:
            self.neo4j_service = Neo4JService()

        except Exception as e:
            raise e

        self.database_schema = self.neo4j_service.get_schema()

    def gen_summary_prompt(self) -> str:
        """
        Generates a prompt for summarizing the data in the Neo4j database.
        Returns:
            str: A prompt for summarizing the data in the Neo4j database.
        """
        context = f"""
        This is the data present in the Neo4j database:
        
        {self.neo4j_service.nodes(limit=100)}
        """

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
        """
        Prompts an AI model for an answer
        Args:
            prompt (str): The prompt to provide to the AI model.
        Returns:
            str: The response from the LLM
        """
        return self.ai_model_service(prompt)
