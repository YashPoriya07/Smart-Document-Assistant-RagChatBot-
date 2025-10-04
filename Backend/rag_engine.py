import os
from typing import List, Dict, Tuple
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class RAGEngine:
    """
    Retrieval-Augmented Generation engine using Pinecone and Sarvam AI
    """
    
    def __init__(self):
        # Initialize Pinecone
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "rag-chatbot")
        
        # Initialize embedding model (local)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dimension = 384  # Dimension for all-MiniLM-L6-v2
        
        # Create or connect to index
        self._setup_index()
    
    def _setup_index(self):
        """
        Setup Pinecone index
        """
        try:
            # Check if index exists
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                # Create new index
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.embedding_dimension,
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
            
            # Connect to index
            self.index = self.pc.Index(self.index_name)
            
        except Exception as e:
            raise Exception(f"Error setting up Pinecone index: {str(e)}")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using SentenceTransformer
        """
        try:
            embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
            return embeddings.tolist()
        except Exception as e:
            raise Exception(f"Error generating embeddings: {str(e)}")
    
    async def store_embeddings(self, chunks: List[Dict], job_id: str):
        """
        Store embeddings in Pinecone
        """
        try:
            # Prepare texts for embedding
            texts = [chunk["text"] for chunk in chunks]
            
            # Generate embeddings
            embeddings = self.generate_embeddings(texts)
            
            # Prepare vectors for upsert
            vectors = []
            for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                vector_id = f"{job_id}_{chunk['metadata']['source']}_{idx}"
                vectors.append({
                    "id": vector_id,
                    "values": embedding,
                    "metadata": {
                        "text": chunk["text"],
                        "source": chunk["metadata"]["source"],
                        "chunk_id": chunk["metadata"]["chunk_id"],
                        "job_id": job_id
                    }
                })
            
            # Upsert in batches
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)
            
        except Exception as e:
            raise Exception(f"Error storing embeddings: {str(e)}")
    
    def retrieve_context(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Retrieve relevant context from Pinecone
        """
        try:
            # Generate query embedding
            query_embedding = self.generate_embeddings([query])[0]
            
            # Search in Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Extract and format results
            contexts = []
            for match in results.matches:
                contexts.append({
                    "text": match.metadata.get("text", ""),
                    "source": match.metadata.get("source", ""),
                    "score": match.score,
                    "chunk_id": match.metadata.get("chunk_id", 0)
                })
            
            return contexts
        
        except Exception as e:
            raise Exception(f"Error retrieving context: {str(e)}")
    
    def call_llm_api(self, prompt: str) -> str:
        """
        Call Sarvam AI for text generation
        """
        try:
            sarvam_key = os.getenv("SARVAM_API_KEY")
            if not sarvam_key:
                raise Exception("SARVAM_API_KEY not found in environment variables")
            
            headers = {
                "api-subscription-key": sarvam_key,
                "Content-Type": "application/json"
            }
            
            # Sarvam AI chat endpoint
            url = "https://api.sarvam.ai/v1/chat/completions"
            
            # Truncate prompt if too long (Sarvam has limits)
            max_length = 2500
            if len(prompt) > max_length:
                # Intelligently truncate from the middle, keep question intact
                question_start = prompt.rfind("Question:")
                if question_start > 0:
                    context_part = prompt[:question_start]
                    question_part = prompt[question_start:]
                    available_space = max_length - len(question_part) - 100
                    context_part = context_part[:available_space] + "\n...[truncated]...\n"
                    prompt = context_part + question_part
                else:
                    prompt = prompt[:max_length]
            
            payload = {
                "model": "sarvam-m",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.4,
                "max_tokens": 1000,
                "top_p": 0.9
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=45)
            
            # Debug logging
            print(f"Sarvam Response Status: {response.status_code}")
            if response.status_code != 200:
                print(f"Sarvam Error Response: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            
            # Extract response from Sarvam AI format
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            elif "response" in result:
                return result["response"]
            else:
                print(f"Unexpected Sarvam response format: {result}")
                raise Exception("Unexpected response format from Sarvam AI")
        
        except requests.exceptions.RequestException as e:
            error_msg = f"Sarvam AI API error: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f"\nResponse: {e.response.text}"
            raise Exception(error_msg)
        except (KeyError, IndexError) as e:
            raise Exception(f"Error parsing Sarvam AI response: {str(e)}")
    
    async def get_response(self, query: str, history: List[Dict]) -> Tuple[str, List[Dict]]:
        """
        Generate response using RAG
        """
        try:
            # Retrieve relevant context
            contexts = self.retrieve_context(query, top_k=5)
            
            if not contexts:
                return "I don't have enough information to answer that question based on the uploaded documents.", []
            
            # Build context string
            context_text = "\n\n".join([
                f"[Source: {ctx['source']}, Relevance: {ctx['score']:.2f}]\n{ctx['text']}"
                for ctx in contexts
            ])
            
            # Build conversation history
            history_text = ""
            if history:
                recent_history = history[-4:]  # Last 2 exchanges
                history_text = "\n".join([
                    f"{msg['role'].upper()}: {msg['content']}"
                    for msg in recent_history
                ])
            
            # Create prompt for Sarvam AI
            prompt = f"""You are a helpful AI assistant answering questions based on provided documents.

Context from documents:
{context_text}

{f"Previous conversation:{chr(10)}{history_text}{chr(10)}{chr(10)}" if history_text else ""}User Question: {query}

Instructions:
1. Answer the question based ONLY on the provided context
2. Be specific and cite sources when possible
3. If the context doesn't contain the answer, say so
4. Keep your answer concise and relevant
5. Maintain conversation continuity if there's previous context
6. No special characters and response should be in plain text
Answer:"""
            
            # Get response from LLM
            response = self.call_llm_api(prompt)
            
            # Prepare source information
            sources = [
                {
                    "source": ctx["source"],
                    "excerpt": ctx["text"][:200] + "...",
                    "relevance_score": ctx["score"]
                }
                for ctx in contexts[:3]  # Top 3 sources
            ]
            
            return response, sources
        
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
    
    def is_connected(self) -> bool:
        """
        Check if connected to Pinecone
        """
        try:
            self.index.describe_index_stats()
            return True
        except:
            return False
    
    def delete_job_data(self, job_id: str):
        """
        Delete all vectors associated with a job
        """
        try:
            self.index.delete(filter={"job_id": job_id})
        except Exception as e:
            raise Exception(f"Error deleting job data: {str(e)}")
