from langchain.retrievers import EnsembleRetriever
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from dotenv import load_dotenv
#from langchain_elasticsearch import ElasticsearchStore
from langchain.retrievers.multi_query import MultiQueryRetriever
from pinecone import Pinecone
import os

load_dotenv()

"""
#Later on someday
def get_pinecone_vectorstore():
    embeddings = OpenAIEmbeddings(model='text-embedding-3-large')# aryan recommened
    vectorstore = PineconeVectorStore(  embedding=embeddings,
                                        index_name="kleenestar",
                                        )

    return vectorstore
"""

def get_pinecone_vectorestore_openai(namespace): 
    embeddings= OpenAIEmbeddings(model='text-embedding-3-large')
    pinecone_vs = PineconeVectorStore(embedding=embeddings, index_name='kleenestar',namespace=namespace)

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


"""
RagData function fetches the latest embeddings from the pinecone vector store,
to give rag context to the prompt
"""

def RagData(question, namespace): #only for retrieving 
    print(namespace)
    pinecone_vs= get_pinecone_vectorestore_openai(namespace)
    self_querying= self_querying_retriever(pinecone_vs)
    #add_documents_es(chunks=documents)
    #elastic_vs= get_es_vectorstore()
    #elastic_vs.as_retriever()
    ensemble_retriever =get_retriver(retrivers=[pinecone_vs.as_retriever(), self_querying, ])

    retriever= multi_query_retriever(ensemble_retriever)
    
    documents = retriever.invoke(input=question)
    return documents




def stats():
    pc= Pinecone(api_key=os.environ['PINECONE_API_KEY'])
    index= pc.Index("kleenestar")
    return index.describe_index_stats()

def delete_vectores(namespace):
    pc= Pinecone(api_key=os.environ['PINECONE_API_KEY'])
    index= pc.Index("kleenestar")
    index.delete(delete_all=True, namespace=namespace)

def add_to_pinecone_vectorestore_openai(documents, namespace):
    embeddings= OpenAIEmbeddings(model='text-embedding-3-large')
    pinecone_vs = PineconeVectorStore.from_documents(embedding=embeddings, index_name='kleenestar', namespace=namespace, documents=documents)


