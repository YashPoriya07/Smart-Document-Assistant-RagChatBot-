import pdfplumber
from typing import List, Dict
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    """
    Handles PDF text extraction and intelligent chunking
    """
    
    def __init__(self, chunk_size: int = 1500, chunk_overlap: int = 300):
        self.chunk_size = chunk_size  # Increased from 1000
        self.chunk_overlap = chunk_overlap  # Increased from 200
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF file
        """
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n\n--- Page {page_num} ---\n\n"
                        text += page_text
            
            if not text.strip():
                raise ValueError("No text could be extracted from PDF")
            
            return self.clean_text(text)
        
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def clean_text(self, text: str) -> str:
        """
        Clean extracted text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\"\']+', '', text)
        # Fix spacing around punctuation
        text = re.sub(r'\s+([\.!\?,;:])', r'\1', text)
        
        return text.strip()
    
    def create_chunks(self, text: str, source_file: str) -> List[Dict]:
        """
        Create intelligent chunks with context preservation
        """
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create chunk objects with metadata
        chunk_objects = []
        for idx, chunk in enumerate(chunks):
            chunk_obj = {
                "text": chunk,
                "metadata": {
                    "source": source_file,
                    "chunk_id": idx,
                    "total_chunks": len(chunks),
                    "char_count": len(chunk)
                }
            }
            chunk_objects.append(chunk_obj)
        
        return chunk_objects
    
    def process_pdf(self, pdf_path: str, filename: str) -> List[Dict]:
        """
        Main processing pipeline: extract, clean, and chunk
        """
        try:
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            
            # Create chunks
            chunks = self.create_chunks(text, filename)
            
            return chunks
        
        except Exception as e:
            raise Exception(f"Error processing PDF {filename}: {str(e)}")
    
    def get_chunk_statistics(self, chunks: List[Dict]) -> Dict:
        """
        Get statistics about chunks
        """
        if not chunks:
            return {}
        
        char_counts = [chunk["metadata"]["char_count"] for chunk in chunks]
        
        return {
            "total_chunks": len(chunks),
            "avg_chunk_size": sum(char_counts) / len(char_counts),
            "min_chunk_size": min(char_counts),
            "max_chunk_size": max(char_counts),
            "total_characters": sum(char_counts)
        }
