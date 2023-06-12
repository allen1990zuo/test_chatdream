import gradio as gr
from googletrans import Translator
from langdetect import detect
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import ConversationalRetrievalChain, LLMChain
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT, QA_PROMPT
import os
import random
import datetime
load_dotenv()


def load_db(persist_directory='data_en', embedding=OpenAIEmbeddings()):
    # os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key:')
    db = Chroma(persist_directory=persist_directory,
                embedding_function=embedding)
    return db


def load_retriever(db, k=2, distance_metric='cos'):

    retriever = db.as_retriever()
    retriever.search_kwargs['distance_metric'] = distance_metric
    retriever.search_kwargs['k'] = k
    return retriever


def load_prompt_template():

    prompt_template = """You are an experienced dream interpreter. 
    You are professional at interpreting others' dream. 
    Please Use the following pieces of context to intepret the dream.
    You need to include the following points in your interpretation:
    1. What is the dream about?
    2. What items and keywords are in the dream?
    3. What is th implication of the dream regarding the person's personality, recent life, health, family, and wealth, if any?
    Please write at least 100 words.


    {context}

    Dream: {question}
    Interpretation:"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    return PROMPT


def openAPI_query(query, retriever, PROMPT, chat_history):

    # docs = retriever.get_relevant_documents(query)
    # streaming_llm = OpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)

    # chain = load_qa_chain(llm=llm,chain_type="stuff", prompt=PROMPT)
    # ans = chain({"input_documents": docs, "question": query})
    llm = OpenAI(temperature=0)
    streaming_llm = OpenAI(streaming=True, callbacks=[
                           StreamingStdOutCallbackHandler()], temperature=0.0)

    question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
    doc_chain = load_qa_chain(
        streaming_llm, chain_type="stuff", prompt=PROMPT)

    qa = ConversationalRetrievalChain(
        retriever=retriever, combine_docs_chain=doc_chain, question_generator=question_generator)
    ans = qa({"question": query,
              "chat_history": chat_history})

    return ans


def translate_to_dest(text, dest='en'):
    translator = Translator(service_urls=['translate.google.com'])
    translation = translator.translate(text, dest=dest)
    return translation.text


def get_lang_code(text):
    try:
        lang = detect(text)
        return lang
    except:
        return False


def process_text(query, chat_history):
    # query_en = "I had a dream last night, I was peeling an orange in a zoo for a monkey, and the monkey took the peeled orange, and then it friendly touched my head."
    # query_chinese = "昨晚做了一个梦，在动物园里给猴子剥橘子，猴子拿着剥好的橘子友好地摸了摸我的头。"
    # query_arabic = "حلمت الليلة الماضية ، كنت أقشر برتقالة في حديقة حيوانات من أجل قرد ، وأخذ القرد البرتقال المقشر ، ثم لمس رأسي بطريقة ودية."
    # chat_history[0][0]=""

    language_code = get_lang_code(query)
    print("language_code ", language_code)
    query_trans = query
    if language_code == False:
        ans = "Sorry, failed to detect language, please try again or use English."
    else:
        if language_code != 'en':
            print("translate to en")
            query_trans = translate_to_dest(query)
    print("query ", query_trans)

    db = load_db(persist_directory='data_en', embedding=OpenAIEmbeddings())
    retriever = load_retriever(db, k=4, distance_metric='cos')
    PROMPT = load_prompt_template()
    for idx, i in enumerate(chat_history):
        chat_history[idx] = tuple(i)
    # =====================
    # core API all in here
    ans = openAPI_query(query_trans, retriever, PROMPT, chat_history)
    # =====================

    response = ans["answer"]
    # log query and response to txt file
    with open("user_chat_log.txt", "a", encoding="utf-8") as f:
        f.write("\n")
        f.write(str({"time": str(datetime.datetime.now()),
                "user": user_name, "query": query, "response": response}))
    if language_code != 'en':
        response = translate_to_dest(response, dest=language_code)

    chat_history.append((query, response))

    return "", chat_history


if __name__ == "__main__":
    # generate random user name id
    user_name = "user_"+str(random.randint(0, 100))
    with gr.Blocks() as demo:
        gr.Markdown("Hello, I am your dream interpreter, please tell me what happend in your dream. You may use your own languge.")
        chatbot = gr.Chatbot()
        msg = gr.Textbox()

        with gr.Row():
            generate = gr.Button("submit")
            clear = gr.Button("Clear")

        msg.submit(process_text, [msg, chatbot], [msg, chatbot])
        generate.click(process_text, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)

    demo.launch(share=True)
