from redundant_filter_retriever import RedundantFilterRetriever
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma

embeddings = GPT4AllEmbeddings()

db = Chroma(
    persist_directory = 'documents/rag-chroma',
    embedding_function = embeddings
)

retriever = RedundantFilterRetriever(
    embeddings = embeddings,
    chroma = db
)

relevant_documents = retriever.invoke('Which issues where closed during August 2023?')
for doc in relevant_documents:
    print(doc.page_content + '\n\n')