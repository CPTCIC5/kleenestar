from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key='e6aab546-8b50-400c-8f92-b55cdea339ad')

index_name = "docs-quickstart-index"

pc.create_index(
    name=index_name,
    dimension=8,
    metric="cosine",
    spec=ServerlessSpec(
        cloud='aws', 
        region='us-east-1'
    ) 
) 

index = pc.Index(index_name)

index.upsert(
    vectors=[
        {"id": "vec1", "values": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]},
        {"id": "vec2", "values": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]},
        {"id": "vec3", "values": [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]},
        {"id": "vec4", "values": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]}
    ],
    namespace="ns1"
)

index.upsert(
    vectors=[
        {"id": "vec5", "values": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]},
        {"id": "vec6", "values": [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]},
        {"id": "vec7", "values": [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]},
        {"id": "vec8", "values": [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]}
    ],
    namespace="ns2"
)

print(index.describe_index_stats())


