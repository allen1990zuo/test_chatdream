import gradio as gr
from googletrans import Translator
from langdetect import detect
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
load_dotenv()

def load_db(persist_directory = 'data_en',embedding = OpenAIEmbeddings()):
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


    {context}

    Dream: {question}
    Interpretation:"""
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    return PROMPT


def openAPI_query(query, retriever, PROMPT):

    docs = retriever.get_relevant_documents(query)
    doc_res = []
    for x in docs:
        doc_res.append(str(x))
    chain = load_qa_chain(OpenAI(temperature=0),
                          chain_type="stuff", prompt=PROMPT)
    ans = chain({"input_documents": docs, "question": query},
                return_only_outputs=True)
    ans = ans['output_text']+"\n\n"
    ans += "--------\n\n"
    ans += "Context:\n\n"
    for x in doc_res:
        ans += x+"\n\n"
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


def process_text(query):
    # query_en = "I had a dream last night, I was peeling an orange in a zoo for a monkey, and the monkey took the peeled orange, and then it friendly touched my head."
    # query_chinese = "昨晚做了一个梦，在动物园里给猴子剥橘子，猴子拿着剥好的橘子友好地摸了摸我的头。"
    # query_arabic = "حلمت الليلة الماضية ، كنت أقشر برتقالة في حديقة حيوانات من أجل قرد ، وأخذ القرد البرتقال المقشر ، ثم لمس رأسي بطريقة ودية."

    language_code = get_lang_code(query)
    print("language_code ", language_code)
    if language_code == False:
        ans = "Sorry, failed to detect language, please try again or use English."
    else:
        if language_code != 'en':
            print("translate to en")
            query = translate_to_dest(query)
    print("query ", query)
    db = load_db(persist_directory='data_en', embedding=OpenAIEmbeddings())
    retriever = load_retriever(db, k=4, distance_metric='cos')
    PROMPT = load_prompt_template()
    #=====================
    # core API all in here
    ans = openAPI_query(query, retriever, PROMPT)
    #=====================


    ans = ans.split("--------")
    output = ans[0]
    context = ans[1]
    print("output ", output)
    output_trans = translate_to_dest(output, dest=language_code)
    ans = output_trans+"\n\n"+"--------\n\n"+context
    return ans

if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.Markdown("explain your dream")
        with gr.Tab("Explain"):
            text_input = gr.Textbox()
            with gr.Row():
                text_button = gr.Button("generate")
                text_button_1 = gr.Button("save_conversation")
            # text_output = gr.Textbox(lines=5)
            text_output_1 = gr.Textbox(lines=10)
        text_button.click(process_text, inputs=text_input, outputs=text_output_1)
    demo.launch()
