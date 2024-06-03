import requests
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain.schema.document import Document
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

    #text_splitter= RecursiveCharacterTextSplitter(chunk_size=128, chunk_overlap=30, length_function=len, is_separator_regex=False)
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

def create_chroma_vectorstore(chunks):
    embedding_function = OpenAIEmbeddings(model='text-embedding-3-large')
    
    return Chroma.from_documents(chunks, embedding_function)

def create_chroma_long_context_retriever(db, documents):
    reordered_docs = long_context_reorder(db)

# Function to create Chroma retriever with metadata filtering
def create_chroma_metadata_retriever(query, db, documents):
    filtered_docs = filter_by_metadata(documents, query)
    db.add_documents(filtered_docs)
    results = db.similarity_search_with_score(query, k=5)
    return results

# Function to create Chroma retriever with parent-child chunk retrieval
def create_chroma_parent_child_retriever(query, db, documents):
    enriched_docs = add_parent_child_chunks(documents)
    db.add_documents(enriched_docs)
    results = db.similarity_search_with_score(query, k=5)
    return results

# Function to create Chroma retriever with long-context reordering
def create_chroma_long_context_retriever(query, db, documents):
    reordered_docs = long_context_reorder(documents, query)
    db.add_documents(reordered_docs)
    results = db.similarity_search_with_score(query, k=5)
    return results

# Function to use Ensemble Retriever to combine results
def ensemble_retrieve(query, embeddings_model, documents):
    db = Chroma(embedding_function=embeddings_model)
    
    results_metadata = create_chroma_metadata_retriever(query, db, documents)
    results_parent_child = create_chroma_parent_child_retriever(query, db, documents)
    results_long_context = create_chroma_long_context_retriever(query, db, documents)
    
    combined_results = EnsembleRetriever(retrievers=[results_metadata, 
                                                     results_parent_child, 
                                                     results_long_context])
    
    return combined_results

# Main RAG function
def RagData(question):
    embeddings_model = OpenAIEmbeddings(model='text-embedding-3-large')
    
    documents = get_workspace()
    
    if documents is None:
        return "Failed to retrieve documents."
    
    # Use ensemble retrieval to get the final results
    results = ensemble_retrieve(question, embeddings_model, documents)
    
    # Format the retrieved documents
    def format_docs(result):
        return "\n\n---\n\n".join([doc.page_content for doc, _score in result])
    
    ragged_data = format_docs(results)
    return str(ragged_data).replace("\n", "")


# Example usage
if __name__ == "__main__":
    pass
