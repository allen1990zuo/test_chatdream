import os

import openai

openai.api_key = os.environ['OPENAPI_API_KEY']

prompt="hello professor, when is the reading week?"

# Completion does not have conversation context, have to load all given knowledge
response = openai.Completion.create(
        model="text-curie-001", prompt=prompt, temperature=0.0)
