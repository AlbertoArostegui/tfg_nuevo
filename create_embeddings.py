from langchain.text_splitter import RecursiveCharacterTextSplitter, TextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings

docs = open('documents/JQL_docs.txt', 'r', encoding='utf-8').read()
doc_splits = docs.split('\n\n')
doc_splits = [text for text in doc_splits if text.strip()]

vectorstore = Chroma.from_texts(
    texts=doc_splits,
    embedding=GPT4AllEmbeddings(),
    persist_directory='documents/rag-chroma',
)
