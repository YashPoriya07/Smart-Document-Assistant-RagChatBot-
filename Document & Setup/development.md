# Development Guide

## 🏗️ Architecture Overview

### System Flow

```
User → Next.js Frontend → FastAPI Backend → Document Processor → RAG Engine → Pinecone → Sarvam AI
```

### Key Components

1. **Document Processor** (`document_processor.py`)
   - Extracts text from PDFs
   - Cleans and normalizes text
   - Creates intelligent chunks with overlap
   - Preserves metadata

2. **RAG Engine** (`rag_engine.py`)
   - Manages Pinecone vector database
   - Generates embeddings using Sentence Transformers
   - Retrieves relevant context
   - Calls Sarvam AI for response generation

3. **FastAPI Server** (`main.py`)
   - Handles file uploads
   - Manages job processing
   - Provides chat endpoints
   - Maintains session state

4. **Next.js Frontend**
   - File upload interface
   - Real-time chat UI
   - Progress tracking
   - Source display

## 🔧 Development Setup

### Backend Development

```bash
cd backend
source venv/bin/activate

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest tests/ -v

# Run with coverage
pytest --cov=. --cov-report=html
```

### Frontend Development

```bash
cd frontend

# Development server
npm run dev

# Type checking
npm run type-check

# Linting
npm run lint

# Build for production
npm run build
npm run start
```

## 📝 Code Style

### Python

Follow PEP 8 guidelines:
- Use type hints
- Docstrings for all functions
- Maximum line length: 100 characters
- Use descriptive variable names

Example:
```python
def process_document(file_path: str, filename: str) -> List[Dict]:
    """
    Process a PDF document and return chunks.
    
    Args:
        file_path: Path to the PDF file
        filename: Original filename
        
    Returns:
        List of chunk dictionaries with text and metadata
        
    Raises:
        ValueError: If file cannot be processed
    """
    pass
```

### TypeScript/React

- Use functional components
- Implement proper TypeScript types
- Use hooks appropriately
- Follow React best practices

Example:
```typescript
interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

const ChatComponent: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  // ...
}
```

## 🧪 Testing Strategy

### Backend Tests

```python
# tests/test_document_processor.py
def test_chunk_creation():
    processor = DocumentProcessor()
    chunks = processor.create_chunks("test text", "file.pdf")
    assert len(chunks) > 0
    assert all("text" in c for c in chunks)
```

### Integration Tests

```python
# tests/test_api.py
from fastapi.testclient import TestClient

def test_upload_endpoint():
    client = TestClient(app)
    files = {"files": ("test.pdf", pdf_content, "application/pdf")}
    response = client.post("/upload-files", files=files)
    assert response.status_code == 200
```

## 🔌 API Integration

### Sarvam AI Integration

The `call_sarvam_ai` method in `rag_engine.py` handles Sarvam AI calls. Update this if the API format changes:

```python
def call_sarvam_ai(self, prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {self.sarvam_api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "sarvam-2b",  # Update model name
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]
```

### Pinecone Configuration

```python
# Initialize Pinecone
pc = Pinecone(api_key=api_key)

# Create index
pc.create_index(
    name="rag-chatbot",
    dimension=384,  # Must match embedding model
    metric='cosine',
    spec=ServerlessSpec(cloud='aws', region='us-east-1')
)
```

## 📊 Performance Optimization

### Backend Optimizations

1. **Batch Processing**
```python
# Process embeddings in batches
batch_size = 100
for i in range(0, len(vectors), batch_size):
    batch = vectors[i:i + batch_size]
    index.upsert(vectors=batch)
```

2. **Async Operations**
```python
@app.post("/upload-files")
async def upload_files(background_tasks: BackgroundTasks):
    # Add to background
    background_tasks.add_task(process_documents_task, job_id)
```

3. **Caching**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_embedding(text: str):
    return model.encode(text)
```

### Frontend Optimizations

1. **Lazy Loading**
```typescript
const ChatPage = dynamic(() => import('./chat/page'), {
  loading: () => <LoadingSpinner />,
});
```

2. **Debouncing**
```typescript
const debouncedSearch = useMemo(
  () => debounce((query) => performSearch(query), 300),
  []
);
```

## 🐛 Debugging

### Backend Debugging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def process_document(file_path: str):
    logger.debug(f"Processing file: {file_path}")
    # ...
```

### Frontend Debugging

```typescript
// Enable React DevTools
if (process.env.NODE_ENV === 'development') {
  console.log('Debug mode enabled');
}
```

## 📦 Adding New Features

### Adding a New Embedding Model

1. Update `rag_engine.py`:
```python
from sentence_transformers import SentenceTransformer

self.embedding_model = SentenceTransformer('new-model-name')
self.embedding_dimension = 768  # Update dimension
```

2. Delete existing Pinecone index or create new one
3. Reprocess all documents

### Adding File Type Support

1. Update `document_processor.py`:
```python
def extract_text_from_docx(self, file_path: str) -> str:
    import docx
    doc = docx.Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])
```

2. Update upload validation in `main.py`
3. Update frontend file type filter

### Adding Authentication

1. Install dependencies:
```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

2. Create auth module:
```python
from fastapi.security import HTTPBearer
from jose import jwt

security = HTTPBearer()

def verify_token(token: str):
    # Verify JWT token
    pass
```

3. Protect endpoints:
```python
@app.post("/chat")
async def chat(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Verify credentials
    pass
```

## 🚀 Deployment Checklist

### Pre-deployment

- [ ] Run all tests
- [ ] Update environment variables
- [ ] Check API rate limits
- [ ] Test with production data
- [ ] Review security settings
- [ ] Enable HTTPS
- [ ] Set up monitoring
- [ ] Configure backups

### Deployment Steps

1. **Backend (Railway/Render)**
   - Connect GitHub repo
   - Set environment variables
   - Configure build command: `pip install -r requirements.txt`
   - Configure start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Frontend (Vercel)**
   - Connect GitHub repo
   - Set environment variables
   - Deploy main branch

3. **Post-deployment**
   - Test all endpoints
   - Monitor logs
   - Check performance metrics

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Pinecone Guides](https://docs.pinecone.io/)
- [Sentence Transformers](https://www.sbert.net/)
- [Sarvam AI Documentation](https://sarvam.ai/docs)

## 🤝 Contributing Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make changes and add tests
4. Run tests: `pytest` and `npm test`
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Commit Message Format

```
type(scope): subject

body

footer
```

Types: feat, fix, docs, style, refactor, test, chore

Example:
```
feat(rag): add caching for embeddings

Implemented LRU cache for embedding generation to improve
response time for repeated queries.

Closes #123
```

## 📝 TODO

- [ ] Add user authentication
- [ ] Implement conversation export
- [ ] Add support for more file types
- [ ] Implement rate limiting
- [ ] Add Redis caching
- [ ] Create admin dashboard
- [ ] Add analytics tracking
- [ ] Implement A/B testing

---

For questions or issues, please open a GitHub issue or contact the maintainers.
