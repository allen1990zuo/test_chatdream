import os
import numpy as np
import openai
import json
import tiktoken
import pickle

from dotenv import load_dotenv
# Load the .env file
load_dotenv()

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

# get tokens with tiktoken
def get_token_count(string):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(string))
    return num_tokens

openai.api_key = os.environ['OPENAI_API_KEY']
EMBEDDING_MODEL = "text-embedding-ada-002"
CONTEXT_TOKEN_LIMIT = 1024

def get_embedding_SB(sentence: str):
    # sentence = 'This is the first sentence.'
    embedding = model.encode(sentence)
    return embedding

def get_embedding_openai(text: str, model: str = EMBEDDING_MODEL) -> list[float]:
    result = openai.Embedding.create(
        model=model,
        input=text
    )
    return result["data"][0]["embedding"]

embeddings = []
key_word = []
with open('content.json', 'r',encoding="utf-8") as f:
    content = json.load(f)
# write to piclke
# with open('content_update.pickle', 'wb') as f:
#     pickle.dump(content, f, protocol=pickle.HIGHEST_PROTOCOL)

token_count_list = []
counter=0
for key_word in content.keys():
    # with open('content_update.json', 'r',encoding="utf-8") as f:
    #     content = json.load(f)
    #read from pickle
    
    with open('content_update.pickle', 'rb') as f:
        content = pickle.load(f)

    print(key_word)

    meaning_list = content[key_word]["meaning"]
    if "embedding" in content[key_word]:
        continue

    embedding_list = []
    for meaning in meaning_list:
        # embedding = get_embedding_openai(meaning)
        # embedding = get_token_count(meaning)
        embedding = get_embedding_SB(meaning)
        embedding_list.append(embedding)
        # token_count_list.append(get_token_count(meaning))

    content[key_word]["embedding"] = embedding_list
    # save json file
    # with open('content_update.json', 'w', encoding="utf-8") as f:
    #     json.dump(content, f)
    # write to piclke
    with open('content_update.pickle', 'wb') as f:
        pickle.dump(content, f, protocol=pickle.HIGHEST_PROTOCOL)
    counter+=1
    print(counter)
    # if counter>10:
    #     break

print(sum(token_count_list))
