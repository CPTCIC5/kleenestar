import requests
from langchain_text_splitters import RecursiveJsonSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS



load_dotenv()

API_URL = "http://127.0.0.1:8000/api/channels/xyz/"


# Function to fetch workspace data
def get_workspace():
    response = requests.get(API_URL)
    if response.status_code == 200:
        response_data = response.json()

    else:
        print("Failed to fetch data:", response.status_code)
        return response.raise_for_status()

 
    text_splitter= RecursiveJsonSplitter(max_chunk_size=80)
    documents = text_splitter.create_documents(texts=response_data)

    return documents



def add_to_pinecone_vectorestore_openai(): 
    embeddings= OpenAIEmbeddings(model='text-embedding-3-large')
    pinecone_vs = PineconeVectorStore.from_documents(embedding=embeddings, index_name='kleenestar', documents=get_workspace())

    return pinecone_vs 

def get_FAISS_vectorstore(chunks):
    embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
    faiss_vectorstore = FAISS.from_documents(chunks, embeddings)

    return faiss_vectorstore


def get_bm25_vectorstore(chunks):
    bm25_retriever = BM25Retriever.from_documents(documents=chunks)
    
    bm25_retriever.k = 2

    return bm25_retriever

if __name__ == '__main__':
    pass