import json
import requests
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
#from langchain_experimental.text_splitter import SemanticChunker
from langchain.schema.document import Document
from langchain_community.retrievers import BM25Retriever
#from langchain_community.document_transformers import LongContextReorder
from langchain.retrievers import EnsembleRetriever
#from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveJsonSplitter
from langchain.retrievers.self_query.base import SelfQueryRetriever
#from langchain.chains.query_constructor.base import AttributeInfo
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain_community.document_transformers.openai_functions import (
    create_metadata_tagger,
)
#from langchain_experimental.openai_assistant import OpenAIAssistantRunnable
from dotenv import load_dotenv


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


    #text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=30, length_function=len, is_separator_regex=False)
    #text_splitter = SemanticChunker(OpenAIEmbeddings())
    #documents = [Document(page_content=x) for x in text_splitter.split_text(str(response_data))]
    #return documents

# Function to apply metadata filtering
def get_pinecone_vectorestore(documents):
    embeddings= OpenAIEmbeddings('text-embedding-3-large')
    #Creates a pinecone vector record
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

"""
#NOT CALLING IT ANYWHERE--> USELESS
def filter_by_metadata(documents, query):
    return sorted(documents, key=lambda x: x.metadata.get('relevance', 0), reverse=True)

# Function to apply parent-child chunk retrieval
def add_parent_child_chunks(documents):
    enhanced_docs = []
    for doc in documents:
        enhanced_docs.append(doc)
        if 'child_ids' in doc.metadata:
            for child_id in doc.metadata['child_ids']:
                child_doc = next((d for d in documents if d.metadata['id'] == child_id), None)
                if child_doc:
                    enhanced_docs.append(child_doc)
    return enhanced_docs
"""
# Function to reorder documents based on LongContextReorder



def get_chroma_vectorestore( documents):
    embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
    db = Chroma(embedding_function=embeddings)
    db.add_documents(documents)
    return db

def get_FAISS_vectorstore(chunks):
    embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
    faiss_vectorstore = FAISS.from_documents(chunks, embeddings)

    return faiss_vectorstore

def get_retriver(retrivers):
    ensemble_retriever = EnsembleRetriever(retrievers=retrivers)
    return ensemble_retriever


def get_bm25_vectorstore(chunks):
    bm25_retriever = BM25Retriever.from_documents(documents=chunks)
    
    bm25_retriever.k = 2

    return bm25_retriever


def RagData(question):
    
    documents = get_workspace()
    
    if documents is None:
        return "Failed to retrieve documents."
    
    faiss_vs = get_FAISS_vectorstore(documents)
    bm25_vs = get_bm25_vectorstore(documents)
    chroma_vs = get_chroma_vectorestore(documents=documents)
    vectores = chroma_vs.get(include=['metadatas', 'documents', 'embeddings'])

    faiss_vs= FAISS

    retriever = get_retriver([faiss_vs.as_retriever(),bm25_vs, chroma_vs.as_retriever(), self_querying_retriever(chroma_vs)])
    return retriever.get_relevant_documents(query=question)
    
    # Format the retrieved documents
    def format_docs(result):
        return "\n\n---\n\n".join([doc.page_content for doc, _score in result])
    
    ragged_data = format_docs(results)
    return str(ragged_data).replace("\n", "")

# Example usage
if __name__ != "__main__":
    pass
