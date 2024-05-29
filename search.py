from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.search(
    collection_name="genai-docs",
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="URL",
                match=models.MatchValue(
                    value="https://www.youtube.com/watch?v=HFfXvfFe9F8",
                ),
            )
        ]
    ),
    search_params=models.SearchParams(hnsw_ef=128, exact=False),
    query_vector=[]
)
print("succesful")