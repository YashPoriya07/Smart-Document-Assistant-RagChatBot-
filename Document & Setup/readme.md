# RAG-Based Document Chatbot

A full-stack application that processes PDF documents and creates an intelligent chatbot using Retrieval-Augmented Generation (RAG) with Sarvam AI.

## 🚀 Features

- **Multi-file PDF Upload**: Upload up to 15 PDF files (max 10MB each)
- **Intelligent Document Processing**: Automatic text extraction and chunking
- **Vector Search**: Powered by Pinecone for fast semantic search
- **AI Responses**: Context-aware answers using Sarvam AI
- **Source Citations**: Every answer includes document references
- **Chat History**: Maintains conversation context
- **Modern UI**: Beautiful, responsive interface built with Next.js

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance API framework
- **Pinecone**: Vector database for embeddings
- **Sentence Transformers**: Local embedding generation
- **Sarvam AI**: LLM for response generation
- **pdfplumber**: PDF text extraction

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- Pinecone account (free tier)
- Sarvam AI API key

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd rag-chatbot
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the backend directory:

```bash
# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=rag-chatbot

# Sarvam AI Configuration
SARVAM_API_KEY=your_sarvam_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create environment file (optional)
# For API URL configuration
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

## 🚀 Running the Application

### Start Backend Server

```bash
cd backend
python main.py

# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

The application will be available at `http://localhost:3000`

## 📁 Project Structure

```
rag-chatbot/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── document_processor.py   # PDF processing & chunking
│   ├── rag_engine.py           # RAG implementation
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables
│   ├── uploads/                # Uploaded files directory
│   └── processed/              # Processed metadata directory
│
└── frontend/
    ├── app/
    │   ├── page.tsx            # Home page
    │   ├── upload/
    │   │   └── page.tsx        # Upload interface
    │   ├── chat/
    │   │   └── page.tsx        # Chat interface
    │   ├── layout.tsx          # Root layout
    │   └── globals.css         # Global styles
    ├── package.json
    ├── tailwind.config.ts
    └── tsconfig.json
```

## 🔑 Getting API Keys

### Pinecone

1. Sign up at [pinecone.io](https://www.pinecone.io/)
2. Create a new project
3. Go to API Keys section
4. Copy your API key
5. The free tier includes:
   - 1 index
   - 100K vectors
   - Sufficient for this project

### Sarvam AI

1. Sign up at [sarvam.ai](https://www.sarvam.ai/)
2. Navigate to API section
3. Generate an API key
4. Check their documentation for:
   - Available models
   - Rate limits
   - Pricing (if applicable)

**Note**: If Sarvam AI requires a different endpoint or model format, update the `call_sarvam_ai` method in `rag_engine.py` accordingly.

## 📝 API Endpoints

### File Upload
- `POST /upload-files` - Upload multiple PDF files
- `GET /upload-status/{job_id}` - Check processing status

### Chat
- `POST /chat` - Send message and get response
- `GET /chat/history/{session_id}` - Retrieve chat history
- `DELETE /chat/clear/{session_id}` - Clear conversation

### Health
- `GET /health` - System health check

## 🎯 Usage Flow

1. **Upload Documents**: Navigate to upload page and select 1-15 PDF files
2. **Wait for Processing**: The system extracts text, creates chunks, and generates embeddings
3. **Start Chatting**: Once processing is complete, you're redirected to the chat interface
4. **Ask Questions**: Type your questions and receive AI-generated answers with source citations

## ⚙️ Configuration Options

### Document Processing

In `document_processor.py`:
```python
chunk_size = 1000        # Characters per chunk
chunk_overlap = 200      # Overlap between chunks
```

### RAG Settings

In `rag_engine.py`:
```python
top_k = 5               # Number of context chunks to retrieve
embedding_model = 'all-MiniLM-L6-v2'  # Embedding model
```

### Sarvam AI Parameters

```python
temperature = 0.7       # Response creativity
max_tokens = 1000       # Maximum response length
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest
```

### API Testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Upload file
curl -X POST "http://localhost:8000/upload-files" \
  -F "files=@document.pdf"
```

## 🐛 Troubleshooting

### Common Issues

1. **Pinecone Connection Error**
   - Verify API key is correct
   - Check if index exists
   - Ensure region matches

2. **Sarvam AI API Error**
   - Verify API key
   - Check rate limits
   - Confirm endpoint URL is correct

3. **PDF Processing Fails**
   - Ensure PDF is not corrupted
   - Check if PDF contains extractable text
   - Verify file size is under 10MB

4. **Frontend Can't Connect to Backend**
   - Ensure backend is running on port 8000
   - Check CORS settings in `main.py`
   - Verify API URL in frontend

## 🚢 Deployment

### Backend Deployment (Railway/Render)

1. Create a new project
2. Connect GitHub repository
3. Set environment variables
4. Deploy

### Frontend Deployment (Vercel)

```bash
cd frontend
npm run build
vercel --prod
```

## 📊 Performance Optimization

- **Batch Processing**: Embeddings are generated in batches of 100
- **Async Operations**: Background tasks for document processing
- **Caching**: Consider adding Redis for frequent queries
- **Database**: Add PostgreSQL for persistent storage

## 🔒 Security Considerations

- Validate file types and sizes
- Sanitize user inputs
- Implement rate limiting
- Add authentication (JWT tokens)
- Use HTTPS in production
- Store API keys securely

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation at `/docs`
- Open an issue on GitHub

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [RAG Concepts](https://www.pinecone.io/learn/retrieval-augmented-generation/)

---

**Built with ❤️ using FastAPI, Next.js, and Sarvam AI**
