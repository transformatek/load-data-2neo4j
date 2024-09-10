import os
from dotenv import load_dotenv, find_dotenv
from huggingface_hub import InferenceClient

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


API_KEY = os.getenv("HF_TOKEN")


class AIModelService:

    def __init__(self, api_key=API_KEY):
        self.api_key = api_key

    def __call__(self, prompt):
        client = InferenceClient(api_key=self.api_key)
        return client.text_generation(prompt)
