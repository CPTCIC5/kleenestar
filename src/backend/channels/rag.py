from langchain.retrievers import EnsembleRetriever
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from dotenv import load_dotenv


load_dotenv()


def get_pinecone_vectorstore():
    embeddings = OpenAIEmbeddings(model='text-embedding-3-large')# aryan recommened
    vectorstore = PineconeVectorStore(  embedding=embeddings,
                                        index_name="kleenestar",
                                        )

    return vectorstore



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

def RagData(question): #only for retrieving 
    pinecone_vs = get_pinecone_vectorstore()
    self_querying = self_querying_retriever(pinecone_vs)
    retriever =get_retriver(retrivers=[pinecone_vs.as_retriever(), self_querying])

    documents = retriever.invoke(input=question)
    return documents