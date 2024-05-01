from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
import dotenv

dotenv.load_dotenv()
docs = open('documents/JQL_docs.txt', 'r', encoding='utf-8').read()
doc_splits = docs.split('\n\n')
doc_splits = [text for text in doc_splits if text.strip()]

vectorstore = Chroma.from_texts(
    texts=doc_splits,
    embedding=OpenAIEmbeddings(),
    persist_directory='documents/rag-chroma-openai',
)
