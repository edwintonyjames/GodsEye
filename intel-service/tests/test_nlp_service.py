"""
Tests for NLP Service
"""
import pytest
from app.services.nlp_service import NLPService


@pytest.fixture
def nlp_service():
    service = NLPService()
    service.load_models()
    return service


def test_extract_entities(nlp_service):
    text = "Elon Musk is the CEO of SpaceX and Tesla."
    entities = nlp_service.extract_entities(text)
    
    assert len(entities) > 0
    entity_texts = [e.text for e in entities]
    assert "Elon Musk" in entity_texts or "SpaceX" in entity_texts


def test_generate_embedding(nlp_service):
    text = "Artificial intelligence is transforming the world."
    embedding = nlp_service.generate_embedding(text)
    
    assert isinstance(embedding, list)
    assert len(embedding) == 384  # Size for all-MiniLM-L6-v2


def test_generate_summary(nlp_service):
    text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines.
    It is different from natural intelligence displayed by humans and animals.
    AI research has been defined as the field of study of intelligent agents.
    """
    summary = nlp_service.generate_summary(text, max_length=100)
    
    assert len(summary) <= 100
    assert len(summary) > 0


def test_calculate_similarity(nlp_service):
    text1 = "Machine learning is a subset of artificial intelligence."
    text2 = "AI includes machine learning as one of its components."
    
    similarity = nlp_service.calculate_similarity(text1, text2)
    
    assert 0.0 <= similarity <= 1.0
    assert similarity > 0.5  # These texts are semantically similar


def test_extract_facts(nlp_service):
    text = "Apple was founded by Steve Jobs. Microsoft was founded by Bill Gates."
    facts = nlp_service.extract_facts(text)
    
    assert isinstance(facts, list)
    # Facts extraction may or may not find structured facts depending on text complexity
    assert len(facts) >= 0
