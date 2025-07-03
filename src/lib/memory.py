import chromadb
from sentence_transformers import SentenceTransformer

# Initialize
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("memories")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Add memory
def add_memory(user, content):
    embedding = embedder.encode(content).tolist()
    collection.add(documents=[content], embeddings=[embedding], metadatas=[{"user": user}])

# Retrieve relevant memories
def get_relevant_memories(user, query, top_k=3):
    query_embedding = embedder.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k, where={"user": user})
    return results["documents"][0]