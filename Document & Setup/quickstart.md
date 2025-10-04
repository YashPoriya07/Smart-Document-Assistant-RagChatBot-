# 🚀 Quick Start Guide

Get your RAG chatbot running in 5 minutes!

## Prerequisites

- Python 3.9+
- Node.js 18+
- Pinecone account (free)
- Sarvam AI API key

## Step 1: Get API Keys (2 minutes)

### Pinecone
1. Go to [pinecone.io](https://www.pinecone.io/) and sign up
2. Create a project
3. Copy your API key from the dashboard

### Sarvam AI
1. Go to [sarvam.ai](https://www.sarvam.ai/) and sign up
2. Navigate to API section
3. Generate and copy your API key

## Step 2: Setup Backend (2 minutes)

```bash
# Clone and navigate to project
cd rag-chatbot/backend

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOL
PINECONE_API_KEY=your_pinecone_key_here
PINECONE_INDEX_NAME=rag-chatbot
SARVAM_API_KEY=your_sarvam_key_here
EOL

# Create directories
mkdir -p uploads processed

# Start server
python main.py
```

Backend will run on http://localhost:8000

## Step 3: Setup Frontend (1 minute)

Open a new terminal:

```bash
# Navigate to frontend
cd rag-chatbot/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on http://localhost:3000

## Step 4: Test It! (30 seconds)

1. Open http://localhost:3000 in your browser
2. Click "Get Started"
3. Upload 1-3 PDF files (test documents)
4. Wait for processing (watch the progress bar)
5. Start chatting with your documents!

## Troubleshooting

### "Module not found" error
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

### "Connection refused" error
Make sure backend is running on port 8000:
```bash
curl http://localhost:8000/health
```

### "Pinecone error"
- Check API key is correct
- Verify you have a free tier project

### "Sarvam AI error"
- Verify API key
- Check if you have API credits/access

## What's Next?

- Read [README.md](README.md) for detailed documentation
- Check [DEVELOPMENT.md](DEVELOPMENT.md) for development guide
- Customize chunk size in `document_processor.py`
- Adjust temperature in `rag_engine.py`

## Quick Commands Reference

```bash
# Backend
cd backend
source venv/bin/activate
python main.py

# Frontend
cd frontend
npm run dev

# Tests
cd backend
pytest

# Check API health
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs
```

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| Port 8000 in use | Kill process: `lsof -ti:8000 \| xargs kill -9` |
| Port 3000 in use | Use different port: `PORT=3001 npm run dev` |
| PDF upload fails | Check file size < 10MB and is valid PDF |
| Slow processing | Reduce chunk_size in document_processor.py |

## Architecture Overview

```
┌─────────────┐     ┌──────────────┐     ┌──────────┐
│   Next.js   │────▶│   FastAPI    │────▶│ Pinecone │
│  Frontend   │     │   Backend    │     │  Vector  │
└─────────────┘     └──────────────┘     │    DB    │
                           │              └──────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Sarvam AI   │
                    │     LLM      │
                    └──────────────┘
```

## File Structure

```
rag-chatbot/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── document_processor.py # PDF processing
│   ├── rag_engine.py        # RAG logic
│   ├── requirements.txt
│   └── .env                 # Your API keys
│
└── frontend/
    ├── app/
    │   ├── page.tsx         # Home page
    │   ├── upload/          # Upload interface
    │   └── chat/            # Chat interface
    └── package.json
```

## Testing Your Setup

### Test Backend API
```bash
# Health check
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","pinecone_connected":true,...}
```

### Test File Upload
```bash
# Upload a test PDF
curl -X POST http://localhost:8000/upload-files \
  -F "files=@test.pdf"
```

### Test Chat
```bash
# Send a chat message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What is this document about?"}'
```

## Environment Variables

### Required
- `PINECONE_API_KEY` - Your Pinecone API key
- `SARVAM_API_KEY` - Your Sarvam AI API key

### Optional
- `PINECONE_INDEX_NAME` - Index name (default: rag-chatbot)
- `HOST` - Backend host (default: 0.0.0.0)
- `PORT` - Backend port (default: 8000)

## Sample Test Data

Create a simple test PDF to verify everything works:

```bash
# Generate a test PDF (requires pandoc)
echo "# Test Document\n\nThis is a test document about AI and machine learning.\n\nAI is transforming the world." > test.md
pandoc test.md -o test.pdf
```

Or use any PDF you have handy!

## Performance Tips

- Start with 1-3 small PDFs (< 1MB each) for testing
- Processing time: ~10-30 seconds per MB
- First query may be slower (model loading)
- Subsequent queries are faster (cached embeddings)

## Need Help?

- 📖 Read [README.md](README.md) for full documentation
- 🐛 Check [GitHub Issues](https://github.com/yourusername/rag-chatbot/issues)
- 💬 Join our Discord community
- 📧 Email: support@example.com

---

**🎉 Congratulations! You're ready to chat with your documents!**
