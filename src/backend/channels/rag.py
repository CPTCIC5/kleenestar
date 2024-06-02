import json, requests
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain.schema.document import Document
from langchain_community.document_transformers import LongContextReorder

API_URL = "http://127.0.0.1:8000/api/channels/xyz/"

# Function to fetch workspace data
def get_workspace():
    response = requests.get(API_URL)
    if response.status_code == 200:
        ResponseData = response.json()
    else:
        print("Failed to fetch data:", response.status_code)
        return response.raise_for_status()

    #text_splitter= RecursiveCharacterTextSplitter(chunk_size=128, chunk_overlap=30, length_function=len, is_separator_regex=False)
    text_splitter= SemanticChunker(OpenAIEmbeddings())
    documents = [Document(page_content=x) for x in text_splitter.split_text(str(ResponseData))]
    return documents

# Function to apply metadata filtering
def filter_by_metadata(documents, query):
    # Placeholder: filter based on 'relevance' metadata
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


# Function to simulate multiple document agents
def retrieve_from_agents(query, embeddings_model, documents, db):
    db.add_documents(documents)
    results = db.similarity_search_with_score(query, k=5)
    return results

# Main RAG function
def RagData(question):
    embeddings_model = OpenAIEmbeddings(model='text-embedding-3-large')
    print(embeddings_model.model , 'xyz')
    documents = get_workspace()
    
    if documents is None:
        return "Failed to retrieve documents."
    
    # Apply metadata filtering
    filtered_docs = filter_by_metadata(documents, question)
    
    # Apply parent-child chunk retrieval
    enriched_docs = add_parent_child_chunks(filtered_docs)
    
    # Reorder documents using LongContextReorder
    reordered_docs = long_context_reorder(enriched_docs, question)
    
    db = Chroma(embedding_function=embeddings_model)
    
    # Simulate multiple document agents
    results = retrieve_from_agents(question, embeddings_model, reordered_docs, db)
    
    # Format the retrieved documents
    def format_docs(result):
        return "\n\n---\n\n".join([doc.page_content for doc, _score in result])
    
    RaggedData = format_docs(results)
    return str(RaggedData).replace("\n", "")

# Example usage
if __name__ != "__main__":
    pass