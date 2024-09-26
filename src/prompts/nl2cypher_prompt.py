from services.ai_model_service import AIModelService
from services.neo4j_service import Neo4JService
from services.dynamic_example import DynamicExample


class NL2CypherPrompt:

    def __init__(self):
        self.ai_model_service = AIModelService()
        self.dynamic_example = DynamicExample()
        try:
            self.neo4j_service = Neo4JService()

        except Exception as e:
            raise e

        self.database_schema = self.neo4j_service.get_schema()

    def gen_prompt(self, user_input) -> str:
        """
        Generates a prompt for the user to generate Cypher queries based on the given user input.
        Args:
            user_input (str): The user input to generate the prompt for.
        Returns:
            str: A prompt for generating Cypher queries based on the user input."""

        examples = self.dynamic_example.get_examples(user_input)
        context = self.database_schema

        task = f"""You are required to generate Cypher queries that answer the following question(s) 
        based on the Graph schema:
        
        '{user_input}'
        """

        constraints = f"""
        Make sure that the Cypher query does run successfully on the given schema.
        Make sure that your answer is logical.
        Follow the structure of the database schema strictly.
        Do not include any explanations, apologies, or anything other than the Cypher query in your answer.
        """

        if len(examples) > 0:
            questions = [example["input"] for example in examples]
            queries = [example["query"] for example in examples]

            examples_ = f"""
            
            Examples:
            Here are a few examples on some similar user inputs and the appropriate Cypher queries that answer them:
            
            {'\n\n'.join([f"Input: {question}\nQuery: {query}" for question, query in zip(questions, queries)])}
            """
            constraints += examples_

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
