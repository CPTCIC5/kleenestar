import json
import requests
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
from langchain_experimental.text_splitter import SemanticChunker
from langchain.schema.document import Document
from langchain_community.retrievers import BM25Retriever
from langchain_community.document_transformers import LongContextReorder
from langchain.retrievers import EnsembleRetriever

API_URL = "http://127.0.0.1:8000/api/channels/xyz/"

# Function to fetch workspace data
def get_workspace():
    response = requests.get(API_URL)
    if response.status_code == 200:
        response_data = response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return response.raise_for_status()

    text_splitter = SemanticChunker(OpenAIEmbeddings())
    documents = [Document(page_content=x) for x in text_splitter.split_text(str(response_data))]
    return documents

# Function to apply metadata filtering
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

# Function to reorder documents based on LongContextReorder
def long_context_reorder(documents, query):
    reorder_transformer = LongContextReorder()
    reordered_docs = reorder_transformer.transform_documents(documents, context=query)
    return reordered_docs

# Function to retrieve documents using Chroma
def retrieve_from_chroma(query, embeddings_model, documents):
    db = Chroma(embedding_function=embeddings_model)
    db.add_documents(documents)
    results = db.similarity_search_with_score(query, k=5)
    return results

# Function to retrieve documents using BM25
def retrieve_from_bm25(query, documents):
    retriever = BM25Retriever(docs=documents)
    retriever.from_documents(documents)  # Adding documents to the retriever
    print(retriever,'dy')
    results = retriever.get_relevant_documents(query)  # Performing the search with the query
    return results

# Function to retrieve documents using FAISS
def retrieve_from_faiss(query, embeddings_model, documents):
    db = FAISS(embedding_function=embeddings_model)
    db.add_documents(documents)
    results = db.similarity_search_with_score(query, k=5)
    return results

# Function to use Ensemble Retriever to combine results
def ensemble_retrieve(query, embeddings_model, documents):
    results_chroma = retrieve_from_chroma(query, embeddings_model, documents)
    results_bm25 = retrieve_from_bm25(query, documents)
    results_faiss = retrieve_from_faiss(query, embeddings_model, documents)
    
    combined_results = EnsembleRetriever(retrievers=[results_chroma, results_bm25, results_faiss])
    #combined_results = ensemble_retriever(retrievers)#[results_chroma, results_bm25, results_faiss])
    
    return combined_results

# Main RAG function
def RagData(question):
    embeddings_model = OpenAIEmbeddings(model='text-embedding-3-large')
    print(embeddings_model.model, 'xyz')
    
    documents = get_workspace()
    
    if documents is None:
        return "Failed to retrieve documents."
    
    # Apply metadata filtering
    filtered_docs = filter_by_metadata(documents, question)
    
    # Apply parent-child chunk retrieval
    enriched_docs = add_parent_child_chunks(filtered_docs)
    
    # Reorder documents using LongContextReorder
    reordered_docs = long_context_reorder(enriched_docs, question)
    
    # Use ensemble retrieval to get the final results
    results = ensemble_retrieve(question, embeddings_model, reordered_docs)
    
    # Format the retrieved documents
    def format_docs(result):
        return "\n\n---\n\n".join([doc.page_content for doc, _score in result])
    
    ragged_data = format_docs(results)
    return str(ragged_data).replace("\n", "")

# Example usage
if __name__ != "__main__":
    pass
