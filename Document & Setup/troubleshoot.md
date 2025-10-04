# 🔧 Troubleshooting Guide

Common issues and their solutions.

## Table of Contents
- [Installation Issues](#installation-issues)
- [Backend Issues](#backend-issues)
- [Frontend Issues](#frontend-issues)
- [API Integration Issues](#api-integration-issues)
- [Performance Issues](#performance-issues)
- [Deployment Issues](#deployment-issues)

---

## Installation Issues

### Python Version Error

**Problem:** `Python 3.9 or higher required`

**Solution:**
```bash
# Check Python version
python --version

# Install Python 3.9+ from python.org
# Or use pyenv
pyenv install 3.11
pyenv local 3.11
```

### pip Install Fails

**Problem:** `ERROR: Could not install packages`

**Solution:**
```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose logging
pip install -r requirements.txt -v

# If specific package fails, install separately
pip install pdfplumber
pip install pinecone-client
```

### Virtual Environment Issues

**Problem:** `venv not activating`

**Solution:**
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# If still fails, recreate venv
rm -rf venv
python -m venv venv
```

### Node.js Installation

**Problem:** `npm: command not found`

**Solution:**
```bash
# Install Node.js from nodejs.org
# Or use nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

---

## Backend Issues

### Port Already in Use

**Problem:** `Address already in use: 8000`

**Solution:**
```bash
# Find process using port 8000
lsof -ti:8000

# Kill the process
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

### Module Import Errors

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check if package is installed
pip list | grep fastapi
```

### Pinecone Connection Error

**Problem:** `PineconeException: Invalid API key`

**Solution:**
```bash
# Verify API key in .env
cat backend/.env | grep PINECONE

# Test API key
python -c "from pinecone import Pinecone; pc = Pinecone(api_key='your_key'); print(pc.list_indexes())"

# Regenerate API key from Pinecone dashboard
```

### Pinecone Index Error

**Problem:** `Index 'rag-chatbot' not found`

**Solution:**
```python
# The app will auto-create the index, but if it fails:
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="your_key")
pc.create_index(
    name="rag-chatbot",
    dimension=384,
    metric='cosine',
    spec=ServerlessSpec(cloud='aws', region='us-east-1')
)
```

### PDF Processing Fails

**Problem:** `Error extracting text from PDF`

**Solution:**
```bash
# Install additional dependencies
pip install pdfplumber pypdf2

# Test PDF manually
python -c "import pdfplumber; pdf = pdfplumber.open('test.pdf'); print(pdf.pages[0].extract_text())"

# If PDF is image-based, need OCR
pip install pytesseract
# Install tesseract: brew install tesseract (Mac) or apt-get install tesseract-ocr (Linux)
```

### File Upload Limit Exceeded

**Problem:** `413 Request Entity Too Large`

**Solution:**
```python
# Increase limit in main.py
from fastapi import FastAPI

app = FastAPI()
app.max_request_size = 50 * 1024 * 1024  # 50MB

# Or configure nginx if deployed
client_max_body_size 50M;
```

### Sarvam AI API Error

**Problem:** `401 Unauthorized` or `429 Rate Limit`

**Solution:**
```bash
# Verify API key
echo $SARVAM_API_KEY

# Check API status
curl -H "Authorization: Bearer $SARVAM_API_KEY" https://api.sarvam.ai/v1/health

# If rate limited, implement retry logic
import time
from tenacity import retry, wait_exponential

@retry(wait=wait_exponential(multiplier=1, min=4, max=10))
def call_api():
    # Your API call
```

### Memory Error During Processing

**Problem:** `MemoryError` when processing large PDFs

**Solution:**
```python
# Reduce chunk size in document_processor.py
processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)

# Process files in smaller batches
for i in range(0, len(files), 5):
    batch = files[i:i+5]
    process_batch(batch)

# Increase system memory or use swap
```

---

## Frontend Issues

### npm Install Fails

**Problem:** `npm ERR! code ERESOLVE`

**Solution:**
```bash
# Clear cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install

# Use legacy peer deps if needed
npm install --legacy-peer-deps
```

### Port 3000 in Use

**Problem:** `Port 3000 is already in use`

**Solution:**
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 npm run dev
```

### TypeScript Errors

**Problem:** `Type 'X' is not assignable to type 'Y'`

**Solution:**
```bash
# Check TypeScript version
npm list typescript

# Update TypeScript
npm install --save-dev typescript@latest

# Regenerate types
npm run build
```

### CORS Error

**Problem:** `Access to fetch blocked by CORS policy`

**Solution:**
```python
# Update CORS settings in backend/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Connection Refused

**Problem:** `Failed to fetch` or `Connection refused`

**Solution:**
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check API URL in frontend
# Update next.config.js if needed
env: {
  NEXT_PUBLIC_API_URL: 'http://localhost:8000',
}

# Check browser console for detailed error
```

### Build Errors

**Problem:** `Error: Cannot find module` during build

**Solution:**
```bash
# Clean build cache
rm -rf .next

# Rebuild
npm run build

# If module missing, install it
npm install missing-package
```

---

## API Integration Issues

### Sarvam AI Model Not Found

**Problem:** `Model 'sarvam-2b' not found`

**Solution:**
```python
# Check available models in Sarvam AI dashboard
# Update model name in rag_engine.py
payload = {
    "model": "correct-model-name",  # Update this
    # ...
}
```

### Embedding Dimension Mismatch

**Problem:** `Dimension mismatch: expected 384, got 768`

**Solution:**
```python
# Check embedding model dimension
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
print(model.get_sentence_embedding_dimension())  # Should be 384

# Update Pinecone index dimension to match
# Or change embedding model to match existing index
```

### Rate Limiting

**Problem:** `429 Too Many Requests`

**Solution:**
```python
# Implement rate limiting
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/chat")
@limiter.limit("10/minute")
async def chat():
    # ...

# Or implement exponential backoff
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        response = api_call()
        break
    except RateLimitError:
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)
```

---

## Performance Issues

### Slow PDF Processing

**Problem:** Documents take too long to process

**Solution:**
```python
# 1. Reduce chunk size
processor = DocumentProcessor(chunk_size=500)

# 2. Process in parallel
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(process_pdf, pdf_files)

# 3. Use faster PDF library
# Try pypdf2 instead of pdfplumber for text-only PDFs
```

### Slow Chat Responses

**Problem:** Responses take 10+ seconds

**Solution:**
```python
# 1. Reduce context chunks
contexts = self.retrieve_context(query, top_k=3)  # Reduce from 5 to 3

# 2. Cache embeddings
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_embedding(text: str):
    return model.encode(text)

# 3. Use faster embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Faster than larger models

# 4. Reduce max_tokens in API call
max_tokens = 500  # Reduce from 1000
```

### High Memory Usage

**Problem:** Application uses too much RAM

**Solution:**
```python
# 1. Use model quantization
model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

# 2. Clear cache periodically
import gc
gc.collect()

# 3. Limit batch size
batch_size = 50  # Reduce from 100

# 4. Use streaming for large responses
from fastapi.responses import StreamingResponse
```

### Database Connection Issues

**Problem:** Too many Pinecone connections

**Solution:**
```python
# Use connection pooling
class RAGEngine:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize once
        return cls._instance
```

---

## Deployment Issues

### Docker Build Fails

**Problem:** `Error building Docker image`

**Solution:**
```dockerfile
# Use specific versions
FROM python:3.11-slim

# Add build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Build with verbose logging
docker build --progress=plain -t rag-chatbot .
```

### Environment Variables Not Loading

**Problem:** `KeyError: 'PINECONE_API_KEY'`

**Solution:**
```bash
# Check env vars are set
docker run --env-file .env rag-chatbot env

# Use docker-compose for easier management
docker-compose up

# Or set explicitly
docker run -e PINECONE_API_KEY=your_key rag-chatbot
```

### Vercel Deployment Issues

**Problem:** Build fails on Vercel

**Solution:**
```json
// package.json
{
  "engines": {
    "node": "18.x",
    "npm": "9.x"
  }
}

// next.config.js
module.exports = {
  output: 'standalone',
  // Disable type checking during build if needed
  typescript: {
    ignoreBuildErrors: true,
  },
}
```

### Railway/Render Backend Issues

**Problem:** Backend crashes in production

**Solution:**
```bash
# Check logs
railway logs
# or
render logs

# Ensure all dependencies in requirements.txt
pip freeze > requirements.txt

# Set worker timeout
web: uvicorn main:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 120
```

---

## Getting Help

If you're still stuck:

1. **Check Logs**
   ```bash
   # Backend logs
   tail -f backend.log
   
   # Frontend logs
   npm run dev -- --verbose
   ```

2. **Enable Debug Mode**
   ```python
   # backend/main.py
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

3. **Test Components Individually**
   ```bash
   # Test Pinecone
   python -c "from rag_engine import RAGEngine; rag = RAGEngine(); print(rag.is_connected())"
   
   # Test PDF processing
   python -c "from document_processor import DocumentProcessor; dp = DocumentProcessor(); print(dp.extract_text_from_pdf('test.pdf'))"
   ```

4. **Search Issues**
   - Check GitHub Issues
   - Search Stack Overflow
   - Read API documentation

5. **Report Bug**
   - Include error message
   - Provide steps to reproduce
   - Share relevant logs
   - Mention environment (OS, Python version, etc.)

---

## Prevention Tips

- Always use virtual environments
- Keep dependencies updated
- Test with small datasets first
- Monitor API usage/costs
- Implement proper error handling
- Add logging throughout code
- Use type hints for better debugging
- Write tests for critical functions

---

**Still need help?** Open an issue on GitHub with:
- Error message
- Steps to reproduce
- Environment details
- What you've tried
