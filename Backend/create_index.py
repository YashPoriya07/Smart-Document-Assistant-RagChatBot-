from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Pinecone
api_key = os.getenv("PINECONE_API_KEY")

if not api_key:
    print("❌ PINECONE_API_KEY not found in .env file!")
    exit(1)

print(f"✅ API Key found: {api_key[:10]}...")

pc = Pinecone(api_key=api_key)

# Check existing indexes
existing_indexes = [index.name for index in pc.list_indexes()]
print(f"Existing indexes: {existing_indexes}")

# Create index if it doesn't exist
index_name = "rag-chatbot"
if index_name in existing_indexes:
    print(f"✅ Index '{index_name}' already exists!")
else:
    print(f"Creating index '{index_name}'...")
    pc.create_index(
        name=index_name,
        dimension=384,  # Must match embedding model dimension
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )
    print("✅ Index created successfully!")
    print("⏳ Wait 1-2 minutes for initialization...")

# Test connection
try:
    index = pc.Index(index_name)
    stats = index.describe_index_stats()
    print(f"✅ Index stats: {stats}")
except Exception as e:
    print(f"❌ Error: {e}")
