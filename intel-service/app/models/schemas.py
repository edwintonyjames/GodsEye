"""
Data models and schemas for the Intel Service
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class Entity(BaseModel):
    """Entity extracted from text"""
    text: str
    label: str
    start: int
    end: int
    confidence: Optional[float] = None


class AnalyzeRequest(BaseModel):
    """Request to analyze text"""
    text: str = Field(..., description="Text to analyze")
    extract_entities: bool = Field(default=True, description="Extract named entities")
    generate_summary: bool = Field(default=False, description="Generate summary")
    store_in_graph: bool = Field(default=True, description="Store entities in graph")


class AnalyzeResponse(BaseModel):
    """Response from text analysis"""
    status: str
    entities: List[Entity]
    summary: Optional[str] = None
    metadata: Dict[str, Any] = {}


class CompareRequest(BaseModel):
    """Request to compare two entities"""
    entity1: Dict[str, Any]
    entity2: Dict[str, Any]
    threshold: float = Field(default=0.7, ge=0.0, le=1.0)


class CompareResponse(BaseModel):
    """Response from entity comparison"""
    status: str
    similarity: float
    matching_attributes: List[str]
    conflicting_attributes: List[Dict[str, Any]]
    verdict: str


class GraphNode(BaseModel):
    """Node in the knowledge graph"""
    id: str
    label: str
    properties: Dict[str, Any]


class GraphRelationship(BaseModel):
    """Relationship in the knowledge graph"""
    source: str
    target: str
    type: str
    properties: Dict[str, Any] = {}


class GraphResponse(BaseModel):
    """Response containing graph data"""
    status: str
    entity: str
    depth: int
    nodes: List[GraphNode]
    relationships: List[GraphRelationship]


class SearchRequest(BaseModel):
    """Request for semantic search"""
    query: str = Field(..., description="Search query")
    top_k: int = Field(default=10, ge=1, le=100, description="Number of results")
    threshold: float = Field(default=0.5, ge=0.0, le=1.0)


class SearchResult(BaseModel):
    """Individual search result"""
    entity: str
    score: float
    metadata: Dict[str, Any]


class SearchResponse(BaseModel):
    """Response from semantic search"""
    status: str
    query: str
    results: List[SearchResult]
    total: int


class CrawlResult(BaseModel):
    """Result from crawler service"""
    url: str
    title: str
    content: str
    links: List[str]
    crawled_at: datetime
    status_code: int
    error: Optional[str] = None


class ProcessRequest(BaseModel):
    """Request to process crawled data"""
    job_id: str
    results: List[CrawlResult]
