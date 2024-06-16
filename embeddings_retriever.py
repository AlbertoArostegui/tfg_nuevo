import templates
from redundant_filter_retriever import RedundantFilterRetriever
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
#from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def embeddings_retriever(texto_pregunta):

    local_model = "gpt-3.5-turbo"
    embeddings = OpenAIEmbeddings()

    db = Chroma(
        persist_directory = 'documents/rag-chroma-openai',
        embedding_function = embeddings
    )

    retriever = RedundantFilterRetriever(
        embeddings = embeddings,
        chroma = db
    )

    #chat = ChatOllama(model=local_model, base_url="http://127.0.0.1:11434")
    chat = ChatOpenAI(model=local_model)

    prompt = PromptTemplate(
        template = templates.template_traduccion,
        input_variables = ["question"],
    )

    question = texto_pregunta
    chain = prompt | chat | StrOutputParser()
    gen = chain.invoke({"question": question})

    relevant_documents = retriever.get_relevant_documents(gen)
    docs = ''
    for doc in relevant_documents:
        docs += doc.page_content + '\n\n'
    
    print(docs)
    return docs