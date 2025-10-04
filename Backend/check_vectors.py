import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-chatbot")

stats = index.describe_index_stats()
print(f"Total vectors: {stats['total_vector_count']}")
print(f"Namespaces: {stats.get('namespaces', {})}")

if stats['total_vector_count'] == 0:
    print("❌ No vectors found! Re-upload your PDF.")
else:
    print("✅ Vectors found!")
