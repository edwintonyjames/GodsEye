"""
NLP Service for entity extraction and text analysis
"""
import spacy
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
from loguru import logger

from app.models.schemas import Entity


class NLPService:
    """Natural Language Processing service"""
    
    def __init__(self):
        self.nlp = None
        self.embedder = None
        
    def load_models(self):
        """Load NLP models"""
        try:
            # Load spaCy model for NER
            logger.info("Loading spaCy model...")
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("✓ spaCy model loaded")
            
            # Load sentence transformer for embeddings
            logger.info("Loading SentenceTransformer model...")
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✓ SentenceTransformer model loaded")
            
        except Exception as e:
            logger.error(f"Failed to load NLP models: {e}")
            raise
    
    def extract_entities(self, text: str) -> List[Entity]:
        """Extract named entities from text"""
        if not self.nlp:
            raise RuntimeError("NLP model not loaded")
        
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entity = Entity(
                text=ent.text,
                label=ent.label_,
                start=ent.start_char,
                end=ent.end_char,
                confidence=None  # spaCy doesn't provide confidence scores by default
            )
            entities.append(entity)
        
        logger.info(f"Extracted {len(entities)} entities from text")
        return entities
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text"""
        if not self.embedder:
            raise RuntimeError("Embedder model not loaded")
        
        embedding = self.embedder.encode(text, convert_to_tensor=False)
        return embedding.tolist()
    
    def generate_summary(self, text: str, max_length: int = 150) -> str:
        """Generate a summary of the text"""
        if not self.nlp:
            raise RuntimeError("NLP model not loaded")
        
        # Simple extractive summarization
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
        
        if len(sentences) <= 3:
            return text
        
        # Take first few sentences as summary
        summary_sentences = sentences[:3]
        summary = " ".join(summary_sentences)
        
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."
        
        return summary
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        if not self.embedder:
            raise RuntimeError("Embedder model not loaded")
        
        embeddings = self.embedder.encode([text1, text2])
        
        # Calculate cosine similarity
        from numpy import dot
        from numpy.linalg import norm
        
        similarity = dot(embeddings[0], embeddings[1]) / (norm(embeddings[0]) * norm(embeddings[1]))
        return float(similarity)
    
    def extract_facts(self, text: str) -> List[Dict[str, Any]]:
        """Extract facts and relationships from text"""
        if not self.nlp:
            raise RuntimeError("NLP model not loaded")
        
        doc = self.nlp(text)
        facts = []
        
        # Extract subject-verb-object triples
        for sent in doc.sents:
            for token in sent:
                if token.dep_ in ("nsubj", "nsubjpass"):
                    subject = token.text
                    verb = token.head.text
                    
                    # Find object
                    obj = None
                    for child in token.head.children:
                        if child.dep_ in ("dobj", "attr", "prep"):
                            obj = child.text
                            break
                    
                    if obj:
                        fact = {
                            "subject": subject,
                            "predicate": verb,
                            "object": obj,
                            "sentence": sent.text
                        }
                        facts.append(fact)
        
        logger.info(f"Extracted {len(facts)} facts from text")
        return facts
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        # Simple sentiment analysis using spaCy
        # For production, use a dedicated sentiment model
        if not self.nlp:
            raise RuntimeError("NLP model not loaded")
        
        doc = self.nlp(text)
        
        # Placeholder sentiment analysis
        # In production, use models like VADER, TextBlob, or transformers
        return {
            "polarity": 0.0,
            "subjectivity": 0.0,
            "label": "neutral"
        }
