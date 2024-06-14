from langchain.retrievers import EnsembleRetriever
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveJsonSplitter
#from langchain_elasticsearch import ElasticsearchStore
from langchain.retrievers.multi_query import MultiQueryRetriever
import os
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

def multi_query_retriever(retriever):
    llm = ChatOpenAI(
    temperature=0,
    max_tokens=800,
    model_kwargs={"top_p": 0, "frequency_penalty": 0, "presence_penalty": 0},
    )


    retriever = MultiQueryRetriever.from_llm(
        retriever=retriever, llm=llm
        )
    
    return retriever


def get_retriver(retrivers):
    ensemble_retriever = EnsembleRetriever(retrievers=retrivers)
    return ensemble_retriever


"""

def get_es_vectorstore():
    embeddings= OpenAIEmbeddings(model='text-embedding-3-large')
    db = ElasticsearchStore(es_cloud_id=os.getenv('ELASTICSEARCH_CLOUD_ID'),
    index_name="kleenestar",
    es_api_key= os.getenv('ELASTICSEARCH_API_KEY'),
    embedding=embeddings)
    return db
"""

"""
def add_documents_es(chunks):
    embeddings= OpenAIEmbeddings(model='text-embedding-3-large')

    elastic_vector_search = ElasticsearchStore.from_documents(documents=chunks,
    es_cloud_id=os.getenv('ELASTICSEARCH_CLOUD_ID'),
    index_name="kleenestar",
    embedding=embeddings,
    es_api_key= os.getenv('ELASTICSEARCH_API_KEY')
    )
"""



def RagData(question): #only for retrieving 
    documents= get_workspace()
    pinecone_vs= add_to_pinecone_vectorestore_openai(documents)
    self_querying= self_querying_retriever(pinecone_vs)
    #add_documents_es(chunks=documents)
    #elastic_vs= get_es_vectorstore()
    #elastic_vs.as_retriever()
    ensemble_retriever =get_retriver(retrivers=[pinecone_vs.as_retriever(), self_querying, ])

    retriever= multi_query_retriever(ensemble_retriever)
    
    documents = retriever.invoke(input=question)
    return documents