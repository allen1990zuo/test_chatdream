import os
import numpy as np
import openai
import json
import pickle


from dotenv import load_dotenv
# Load the .env file
load_dotenv()

from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')


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

def vector_similarity(x: list[float], y: list[float]) -> float:
    return np.dot(np.array(x), np.array(y))


def vector_similarity_SB(x: list[float], y: list[float]) -> float:
    return util.dot_score(x,y)

def order_document_sections_by_query_similarity(query: str, embeddings) -> list[(float, (str, str))]:
    query_embedding = get_embedding_SB(query)
    # query_embedding = get_embedding_openai(query)
    document_similarities = sorted([
        (vector_similarity_SB(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in enumerate(embeddings)
    ], reverse=True, key=lambda x: x[0])
    return document_similarities

def ask(question: str):

    embeddings, sources, keyword = load_embeddings()

    ordered_candidates = order_document_sections_by_query_similarity(
        question, embeddings)
    ctx = ""
    for candi in ordered_candidates:
        next = ctx + " " + sources[candi[1]]
        if len(next) > CONTEXT_TOKEN_LIMIT:
            break
        ctx = next
    if len(ctx) == 0:
        return ""

    prompt = "".join([
        u"你是一个专业的解梦专家，请根据\{\}内提供的上下文，和\[\]提供的梦境，对梦境进行解释，请简单复述梦境，并且根据梦里里提到的事物来进行解释和未来的预测:\n\n"
        u"\{上下文:" + ctx + u"\n\n"
        u"\}"
        u"\["+question+u"\n\n"
        u"\]"
        u"梦的解释:"])

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    return [prompt, completion.choices[0].message.content]


def load_embeddings():
    embeddings = []
    sources = []
    keywords = []
    # with open('content_update.json', 'r') as f:
    #     content = json.load(f)
    with open('content_update.pickle', 'rb') as f:
        content = pickle.load(f)
    
    for key_word in content.keys():
        meaning_list = content[key_word]["meaning"]
        embedding_list = []

        if "embedding" in content[key_word]:
            embedding_list = content[key_word]["embedding"]
            embeddings+=embedding_list
            sources+=meaning_list
            keywords+=[key_word]*len(meaning_list)
    return embeddings, sources, keywords 

# question="我做了一个梦，梦见了自己身处电梯，电梯坠落了，然后我就醒了"

# print(ask(question))