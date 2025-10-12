"""
DefinitelyNotASpy Intel Service
Main application entry point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from loguru import logger
from app.routers import analysis, graph, search
from app.services.neo4j_service import Neo4jService
from app.services.qdrant_service import QdrantService
from app.services.nlp_service import NLPService


# Initialize services
neo4j_service = None
qdrant_service = None
nlp_service = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    global neo4j_service, qdrant_service, nlp_service
    
    logger.info("🚀 Starting Intel Service")
    
    # Initialize services
    try:
        neo4j_service = Neo4jService()
        await neo4j_service.connect()
        logger.info("✓ Neo4j connected")
    except Exception as e:
        logger.error(f"Failed to connect to Neo4j: {e}")
    
    try:
        qdrant_service = QdrantService()
        await qdrant_service.initialize()
        logger.info("✓ Qdrant initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Qdrant: {e}")
    
    try:
        nlp_service = NLPService()
        nlp_service.load_models()
        logger.info("✓ NLP models loaded")
    except Exception as e:
        logger.error(f"Failed to load NLP models: {e}")
    
    yield
    
    # Cleanup
    logger.info("Shutting down Intel Service")
    if neo4j_service:
        await neo4j_service.close()
    logger.info("Services closed")


# Create FastAPI app
app = FastAPI(
    title="DefinitelyNotASpy Intel Service",
    description="AI-powered intelligence service for entity analysis and knowledge graph building",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "intel",
        "neo4j": neo4j_service is not None and neo4j_service.is_connected(),
        "qdrant": qdrant_service is not None,
        "nlp": nlp_service is not None,
    }


# Include routers
app.include_router(analysis.router, prefix="/api/v1", tags=["analysis"])
app.include_router(graph.router, prefix="/api/v1", tags=["graph"])
app.include_router(search.router, prefix="/api/v1", tags=["search"])


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "DefinitelyNotASpy Intel Service",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("INTEL_PORT", "8000"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
