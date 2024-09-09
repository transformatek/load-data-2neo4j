import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

API_KEY = os.getenv("OPENAI_API_KEY")
# import OpenIA / Hugging faces

client = OpenAI(api_key=API_KEY)

completion = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': "system", 'content': "You are a helpful assistant."},
        {
            'role': 'user',
            'content': 'What is the capital of the United States?'
        }
    ]
)


print(completion.choices[0].message)


class AIModelService:

    def __init__(self, api_key):
        self.apiy_ky = api_key

    def __call__(self, prompt):
        # TODO call to the API
        pass
