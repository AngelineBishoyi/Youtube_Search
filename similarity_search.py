from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize Qdrant client
client = QdrantClient(url="http://localhost:6333")

# Initialize SentenceTransformer model
model = SentenceTransformer('sentence-t5-base')

# Define the URL and data of the query chunk
query_url = "https://www.youtube.com/watch?v=HFfXvfFe9F8"
query_data = "Google Germany projects"

# Encode the query chunk
query_embedding = model.encode([query_data])[0]



# Perform similarity search with distance metric
search_results = client.search(
      collection_name="genai-docs",
      query_vector=query_embedding.tolist(),  # Convert to list
      limit=3,  # Retrieve top 3 similar chunks
    
)

# Print search results
print("Similar Chunks:")
for result in search_results:
     print("Document ID:", result.id)
     print("Similarity Score:", result.score)
     print("Chunk URL:", result.payload["URL"])
     print("Chunk Data:", result.payload["data"])
     print()
     