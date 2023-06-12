import os
import json
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
import Chroma_server

def lambda_handler(event, context):
    
    body = event.get('body')
    body = json.loads(body)

    query = body['query']
    print("get query string:")
    print(query)

    load_dotenv()
    # main function moved to Chroma_server.py
    ans = Chroma_server.process_text(query)
    
    data = {
        "query": query,
        "answer": ans
    }
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            'Access-Control-Allow-Headers': "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            # You can add more headers as needed
        },
        "body": json.dumps(data),
    }

