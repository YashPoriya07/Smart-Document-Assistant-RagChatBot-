import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

# Test Pinecone
try:
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    indexes = pc.list_indexes()
    print("✅ Pinecone connected!")
    print(f"Indexes: {[idx.name for idx in indexes]}")
except Exception as e:
    print(f"❌ Pinecone error: {e}")

# Test Sarvam AI
import requests
try:
    headers = {"Authorization": f"Bearer {os.getenv('SARVAM_API_KEY')}"}
    # Test endpoint (adjust if needed)
    print("✅ Sarvam AI key loaded")
    print(f"Key starts with: {os.getenv('SARVAM_API_KEY')[:10]}...")
except Exception as e:
    print(f"❌ Sarvam AI error: {e}")
