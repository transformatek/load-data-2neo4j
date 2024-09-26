import os
from dotenv import load_dotenv, find_dotenv
from huggingface_hub import InferenceClient

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


API_KEY = os.getenv("HF_TOKEN")


class AIModelService:

    def __init__(self, api_key=API_KEY):
        self.api_key = api_key
        self.client = InferenceClient(api_key=self.api_key)

    def __call__(self, prompt):
        return self.client.text_generation(prompt, max_new_tokens=10000)

    def humanize_answer(self, question, data):
        """
        Given a question and a set of data that answers that question, generates a human-readable answer.
        Args:
            question (str): The question to answer.
            data (str): The data that answers the question.
        Returns:
            str: A human-readable answer to the question.
        """
        prompt = f"""
        Consider the following question: "{question}"
        And the following set of data which is an answer to that question: {data}
        
        Can you make it so that the answer is more human-readable?
        
        Constraints:
            Don't include any apologies, explanations, or anything other than the answer to the prompt.
            
        Answer:
        
        """
        return self(prompt)
