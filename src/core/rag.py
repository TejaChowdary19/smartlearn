from __future__ import annotations
from typing import List, Dict, Optional, Tuple, Union
import os
import re
from pathlib import Path
from sentence_transformers import SentenceTransformer
from langchain_chroma import Chroma  # Updated import
from langchain.embeddings.base import Embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import chromadb
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import fitz  # PyMuPDF for PDF processing
from PIL import Image
import pytesseract
import json

class STEmbedding(Embeddings):
    """LangChain-compatible wrapper for sentence-transformers."""
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name  # Store the model name for access

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        # Convert numpy arrays to lists
        if len(embeddings.shape) == 1:
            embeddings = embeddings.reshape(1, -1)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        embedding = self.model.encode([text], convert_to_numpy=True)
        return embedding[0].tolist()

class AdvancedDocumentProcessor:
    """Enhanced document processing with multi-modal support."""
    
    @staticmethod
    def load_text_file(file_path: str) -> str:
        """Load text from a text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading text file {file_path}: {e}")
            return ""
    
    @staticmethod
    def load_markdown_file(file_path: str) -> str:
        """Load text from a markdown file."""
        return AdvancedDocumentProcessor.load_text_file(file_path)
    
    @staticmethod
    def load_pdf_file(file_path: str) -> str:
        """Extract text from PDF files."""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            print(f"Error loading PDF file {file_path}: {e}")
            return ""
    
    @staticmethod
    def extract_text_from_image(image_path: str) -> str:
        """Extract text from images using OCR."""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            print(f"Error extracting text from image {image_path}: {e}")
            return ""
    
    @staticmethod
    def split_text_adaptive(text: str, content_type: str = "general") -> List[str]:
        """Adaptive text splitting based on content type."""
        if content_type == "code":
            # For code, split by functions/classes
            chunk_size = 800
            chunk_overlap = 100
        elif content_type == "academic":
            # For academic papers, split by sections
            chunk_size = 1200
            chunk_overlap = 200
        elif content_type == "conversation":
            # For conversations, split by turns
            chunk_size = 600
            chunk_overlap = 100
        else:
            # Default settings
            chunk_size = 1000
            chunk_overlap = 200
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        return text_splitter.split_text(text)

class HybridSearchEngine:
    """Combines semantic and keyword search for better retrieval."""
    
    def __init__(self, documents: List[str]):
        self.documents = documents
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.tfidf_matrix = None
        self._build_tfidf_index()
    
    def _build_tfidf_index(self):
        """Build TF-IDF index for keyword search."""
        try:
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.documents)
        except Exception as e:
            print(f"Error building TF-IDF index: {e}")
            self.tfidf_matrix = None
    
    def keyword_search(self, query: str, top_k: int = 5) -> List[Tuple[int, float]]:
        """Perform keyword-based search using TF-IDF."""
        if self.tfidf_matrix is None:
            return []
        
        try:
            query_vector = self.tfidf_vectorizer.transform([query])
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            # Get top-k results
            top_indices = similarities.argsort()[-top_k:][::-1]
            results = [(idx, similarities[idx]) for idx in top_indices if similarities[idx] > 0]
            return results
        except Exception as e:
            print(f"Error in keyword search: {e}")
            return []
    
    def hybrid_search(self, query: str, semantic_scores: List[float], 
                     alpha: float = 0.7, top_k: int = 5) -> List[Tuple[int, float]]:
        """Combine semantic and keyword search scores."""
        if not semantic_scores:
            return []
        
        # Get keyword search scores
        keyword_results = self.keyword_search(query, top_k=len(semantic_scores))
        keyword_scores = [0.0] * len(semantic_scores)
        
        for idx, score in keyword_results:
            if idx < len(keyword_scores):
                keyword_scores[idx] = score
        
        # Normalize scores
        if max(semantic_scores) > 0:
            semantic_scores = [s / max(semantic_scores) for s in semantic_scores]
        if max(keyword_scores) > 0:
            keyword_scores = [s / max(keyword_scores) for s in keyword_scores]
        
        # Combine scores
        hybrid_scores = []
        for i in range(len(semantic_scores)):
            hybrid_score = alpha * semantic_scores[i] + (1 - alpha) * keyword_scores[i]
            hybrid_scores.append((i, hybrid_score))
        
        # Sort by hybrid score and return top-k
        hybrid_scores.sort(key=lambda x: x[1], reverse=True)
        return hybrid_scores[:top_k]

class QueryExpander:
    """Expands queries to improve retrieval."""
    
    def __init__(self):
        self.synonyms = {
            "math": ["mathematics", "mathematical", "calculation", "computation"],
            "programming": ["coding", "software development", "computer programming"],
            "physics": ["physical science", "mechanics", "dynamics"],
            "chemistry": ["chemical science", "molecular science"],
            "biology": ["biological science", "life science"],
            "study": ["learn", "research", "investigate", "examine"],
            "understand": ["comprehend", "grasp", "fathom", "realize"],
            "practice": ["exercise", "drill", "rehearse", "train"]
        }
    
    def expand_query(self, query: str) -> List[str]:
        """Expand a query with synonyms and related terms."""
        expanded_queries = [query]
        
        # Add synonyms
        for word in query.lower().split():
            if word in self.synonyms:
                for synonym in self.synonyms[word]:
                    expanded_queries.append(query.replace(word, synonym))
        
        # Add related terms
        if "derivative" in query.lower():
            expanded_queries.extend([
                query + " calculus",
                query + " differentiation",
                query + " rate of change"
            ])
        
        if "algorithm" in query.lower():
            expanded_queries.extend([
                query + " computer science",
                query + " programming",
                query + " data structure"
            ])
        
        return list(set(expanded_queries))  # Remove duplicates

class EnhancedRAG:
    """Enhanced RAG system with advanced features."""
    
    def __init__(self, persist_path: str | None = None, 
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        persist_path = persist_path or os.getenv("RAG_DB_PATH", ".smartlearn/chroma_db")
        os.makedirs(persist_path, exist_ok=True)
        
        self.emb = STEmbedding(model_name=embedding_model)
        self.persist_path = persist_path
        self.vs = None
        self.processor = AdvancedDocumentProcessor()
        self.documents_loaded = False
        self.documents = []
        self.hybrid_search_engine = None
        self.query_expander = QueryExpander()
        
        # Initialize vector store
        self._init_vector_store()
    
    def _init_vector_store(self):
        """Initialize the vector store with proper configuration."""
        try:
            # Create ChromaDB client
            client = chromadb.PersistentClient(path=self.persist_path)
            
            # Initialize Chroma vector store
            self.vs = Chroma(
                collection_name="smartlearn",
                embedding_function=self.emb,
                client=client
            )
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            # Fallback to in-memory store
            self.vs = Chroma(
                collection_name="smartlearn",
                embedding_function=self.emb
            )
        
    def load_knowledge_base(self, knowledge_base_path: str) -> bool:
        """Load documents from the knowledge base directory with multi-modal support."""
        try:
            kb_path = Path(knowledge_base_path)
            if not kb_path.exists():
                print(f"Knowledge base path not found: {knowledge_base_path}")
                return False
            
            # Clear existing documents - use safer method
            if hasattr(self.vs, '_collection') and self.vs._collection:
                try:
                    # Try to get existing documents first
                    existing = self.vs._collection.get()
                    if existing and 'ids' in existing and existing['ids']:
                        # Delete by IDs if they exist
                        self.vs._collection.delete(ids=existing['ids'])
                        print("✅ Cleared existing documents")
                except Exception as e:
                    print(f"⚠️ Warning: Could not clear existing documents: {e}")
                    # Continue anyway
            
            documents = []
            chunk_id = 0
            
            # Process different file types
            for file_path in kb_path.rglob("*"):
                if file_path.is_file():
                    content = ""
                    content_type = "general"
                    
                    # Determine content type and load accordingly
                    if file_path.suffix.lower() == '.md':
                        content = self.processor.load_markdown_file(str(file_path))
                        content_type = "academic"
                    elif file_path.suffix.lower() == '.txt':
                        content = self.processor.load_text_file(str(file_path))
                    elif file_path.suffix.lower() == '.pdf':
                        content = self.processor.load_pdf_file(str(file_path))
                        content_type = "academic"
                    elif file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                        content = self.processor.extract_text_from_image(str(file_path))
                        content_type = "image"
                    elif file_path.suffix.lower() == '.py':
                        content = self.processor.load_text_file(str(file_path))
                        content_type = "code"
                    
                    if content.strip():
                        # Split content adaptively
                        chunks = self.processor.split_text_adaptive(content, content_type)
                        
                        for i, chunk in enumerate(chunks):
                            if chunk.strip():
                                # Create document with metadata
                                doc = Document(
                                    page_content=chunk,
                                    metadata={
                                        "source": str(file_path),
                                        "chunk_id": chunk_id,
                                        "content_type": content_type,
                                        "chunk_index": i,
                                        "total_chunks": len(chunks)
                                    }
                                )
                                documents.append(doc)
                                chunk_id += 1
            
            if documents:
                # Add documents to vector store
                self.vs.add_documents(documents)
                self.documents = [doc.page_content for doc in documents]
                
                # Initialize hybrid search engine
                self.hybrid_search_engine = HybridSearchEngine(self.documents)
                
                self.documents_loaded = True
                print(f"✅ Loaded {len(documents)} document chunks from knowledge base")
                return True
            else:
                print("❌ No documents found in knowledge base")
                return False
                
        except Exception as e:
            print(f"❌ Error loading knowledge base: {e}")
            return False
    
    def retrieve_relevant_context(self, query: str, k: int = 3, 
                                use_hybrid: bool = True, alpha: float = 0.7) -> Tuple[str, List[Dict]]:
        """Retrieve relevant context using enhanced search."""
        try:
            if not self.documents_loaded:
                return "", []
            
            # Expand query
            expanded_queries = self.query_expander.expand_query(query)
            
            # Get semantic search results
            semantic_results = []
            for exp_query in expanded_queries:
                results = self.vs.similarity_search_with_score(exp_query, k=k)
                semantic_results.extend(results)
            
            # Remove duplicates and get top results
            unique_results = {}
            for doc, score in semantic_results:
                if doc.metadata.get('chunk_id') not in unique_results:
                    unique_results[doc.metadata.get('chunk_id')] = (doc, score)
            
            # Sort by score and get top-k
            sorted_results = sorted(unique_results.values(), key=lambda x: x[1], reverse=True)[:k]
            
            if use_hybrid and self.hybrid_search_engine:
                # Use hybrid search
                semantic_scores = [score for _, score in sorted_results]
                hybrid_results = self.hybrid_search_engine.hybrid_search(
                    query, semantic_scores, alpha=alpha, top_k=k
                )
                
                # Reorder results based on hybrid scores
                final_results = []
                for idx, hybrid_score in hybrid_results:
                    if idx < len(sorted_results):
                        doc, _ = sorted_results[idx]
                        final_results.append((doc, hybrid_score))
                sorted_results = final_results
            
            # Format results
            context = "\n\n".join([doc.page_content for doc, _ in sorted_results])
            sources = []
            
            for doc, score in sorted_results:
                sources.append({
                    "source": doc.metadata.get("source", "Unknown"),
                    "chunk_id": doc.metadata.get("chunk_id", "Unknown"),
                    "content_type": doc.metadata.get("content_type", "general"),
                    "relevance_score": float(score),
                    "chunk_index": doc.metadata.get("chunk_index", 0),
                    "total_chunks": doc.metadata.get("total_chunks", 1)
                })
            
            return context, sources
            
        except Exception as e:
            print(f"❌ Error retrieving context: {e}")
            return "", []
    
    def get_knowledge_base_stats(self) -> Dict:
        """Get comprehensive statistics about the loaded knowledge base."""
        try:
            if not self.documents_loaded:
                return {"status": "No documents loaded", "count": 0}
            
            # Get collection info
            if hasattr(self.vs, '_collection') and self.vs._collection:
                count = self.vs._collection.count()
            else:
                count = "Unknown"
            
            # Analyze content types
            content_types = {}
            if hasattr(self.vs, '_collection') and self.vs._collection:
                try:
                    results = self.vs._collection.get()
                    if results and 'metadatas' in results:
                        for metadata in results['metadatas']:
                            if metadata and 'content_type' in metadata:
                                content_type = metadata['content_type']
                                content_types[content_type] = content_types.get(content_type, 0) + 1
                except Exception as e:
                    print(f"Warning: Could not analyze content types: {e}")
            
            return {
                "status": "Documents loaded",
                "count": count,
                "embedding_model": self.emb.model_name,
                "content_types": content_types,
                "hybrid_search": self.hybrid_search_engine is not None,
                "query_expansion": True
            }
            
        except Exception as e:
            return {"status": f"Error: {e}", "count": 0}
    
    def search_similar_documents(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar documents with enhanced metadata."""
        try:
            if not self.documents_loaded:
                return []
            
            # Use hybrid search if available
            if self.hybrid_search_engine:
                context, sources = self.retrieve_relevant_context(query, k=k, use_hybrid=True)
            else:
                context, sources = self.retrieve_relevant_context(query, k=k, use_hybrid=False)
            
            return sources
            
        except Exception as e:
            print(f"❌ Error searching documents: {e}")
            return []
    
    def get_document_summary(self, source: str) -> Dict:
        """Get summary information about a specific document."""
        try:
            if not self.documents_loaded:
                return {}
            
            # Find all chunks from this source
            source_chunks = []
            if hasattr(self.vs, '_collection') and self.vs._collection:
                try:
                    results = self.vs._collection.get(
                        where={"source": source}
                    )
                    if results and 'metadatas' in results:
                        source_chunks = results['metadatas']
                except Exception as e:
                    print(f"Warning: Could not get source chunks: {e}")
            
            if not source_chunks:
                return {}
            
            # Analyze the document
            total_chunks = len(source_chunks)
            content_types = set()
            chunk_sizes = []
            
            for chunk in source_chunks:
                if chunk and 'content_type' in chunk:
                    content_types.add(chunk['content_type'])
                if chunk and 'chunk_index' in chunk:
                    chunk_sizes.append(chunk.get('chunk_index', 0))
            
            return {
                "source": source,
                "total_chunks": total_chunks,
                "content_types": list(content_types),
                "chunk_range": f"{min(chunk_sizes)} - {max(chunk_sizes)}" if chunk_sizes else "Unknown",
                "estimated_pages": max(1, total_chunks // 3)  # Rough estimate
            }
            
        except Exception as e:
            print(f"❌ Error getting document summary: {e}")
            return {}

class SimpleRAG:
    """Backward compatibility wrapper for EnhancedRAG."""
    
    def __init__(self, persist_path: str | None = None, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.enhanced_rag = EnhancedRAG(persist_path, embedding_model)

    def add_documents(self, docs: List[str]):
        """Add documents to the knowledge base."""
        # This is a simplified interface for backward compatibility
        pass

    def retrieve(self, query: str, k: int = 3) -> str:
        """Retrieve relevant context."""
        context, _ = self.enhanced_rag.retrieve_relevant_context(query, k)
        return context
