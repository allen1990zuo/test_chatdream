
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
load_dotenv()
# os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key:')
with open("context\dream_dict_context.txt", encoding="utf-8") as f:
    dream_meaning = f.read()

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
pages = text_splitter.split_text(dream_meaning)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=100)
docs = text_splitter.create_documents(pages)

persist_directory = 'data_en'
embedding = OpenAIEmbeddings()
vectordb = Chroma.from_documents(
    documents=docs, embedding=embedding, persist_directory=persist_directory)
