from langchain.retrievers import EnsembleRetriever
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveJsonSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
import requests
import json

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

 
    text_splitter= RecursiveJsonSplitter(max_chunk_size=128)
    documents = text_splitter.create_documents(texts=response_data)

    for i, document in enumerate(documents):
        
        if 'channel' in document.page_content:
            document.metadata['channel'] = json.loads(document.page_content)['channel']

        else:
            document.metadata['channel'] = documents[i-1].metadata['channel']

    return documents

"""
#Later on someday
def get_pinecone_vectorstore():
    embeddings = OpenAIEmbeddings(model='text-embedding-3-large')# aryan recommened
    vectorstore = PineconeVectorStore(  embedding=embeddings,
                                        index_name="kleenestar",
                                        )

    return vectorstore
"""

def add_to_pinecone_vectorestore_openai(documents): 
    embeddings= OpenAIEmbeddings(model='text-embedding-3-large')
    pinecone_vs = PineconeVectorStore.from_documents(embedding=embeddings, index_name='kleenestar', documents=documents)

    return pinecone_vs 

 
def self_querying_retriever(vectorstore):
    llm = ChatOpenAI(temperature=0.1)
    metadata_field_info = []
    document_content_description = "marketing channel data in real-time"
    retriever = SelfQueryRetriever.from_llm(
    llm= llm,
    vectorstore= vectorstore,
    metadata_field_info=metadata_field_info,
    document_contents= document_content_description
        )
    return retriever

def get_retriver(retrivers):
    ensemble_retriever = EnsembleRetriever(retrievers=retrivers)
    return ensemble_retriever

def get_FAISS_vectorstore(chunks):
    embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
    faiss_vectorstore = FAISS.from_documents(chunks, embeddings)

    return faiss_vectorstore

def get_bm25_vectorstore(chunks):
    bm25_retriever = BM25Retriever.from_documents(documents=chunks)

    bm25_retriever.k = 5

    return bm25_retriever

def RagData(question): #only for retrieving 
    documents= get_workspace()
    pinecone_vs= add_to_pinecone_vectorestore_openai(documents)
    self_querying= self_querying_retriever(pinecone_vs)
    bm25_vs= get_bm25_vectorstore(documents)
    faiss_vs= get_FAISS_vectorstore(documents)
    retriever =get_retriver(retrivers=[pinecone_vs.as_retriever(), self_querying, bm25_vs, faiss_vs.as_retriever()])

    documents = retriever.invoke(input=question)
    return documents