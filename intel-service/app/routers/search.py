"""
Search router for semantic search operations
"""
from fastapi import APIRouter, HTTPException, Query
from loguru import logger

from app.models.schemas import SearchRequest, SearchResponse, SearchResult
from app.services.nlp_service import NLPService
from app.services.qdrant_service import QdrantService


router = APIRouter()
nlp_service = NLPService()
qdrant_service = QdrantService()


@router.post("/search", response_model=SearchResponse)
async def semantic_search(request: SearchRequest):
    """
    Perform semantic search across stored entities
    """
    try:
        # Generate query embedding
        query_embedding = nlp_service.generate_embedding(request.query)
        
        # Search in Qdrant
        results = qdrant_service.search_similar(
            query_vector=query_embedding,
            top_k=request.top_k,
            score_threshold=request.threshold
        )
        
        # Format results
        search_results = [
            SearchResult(
                entity=result["text"],
                score=result["score"],
                metadata=result["metadata"]
            )
            for result in results
        ]
        
        logger.info(f"Semantic search for '{request.query}' found {len(search_results)} results")
        
        return SearchResponse(
            status="success",
            query=request.query,
            results=search_results,
            total=len(search_results)
        )
        
    except Exception as e:
        logger.error(f"Error in semantic_search: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/similar/{entity}")
async def find_similar_entities(
    entity: str,
    top_k: int = Query(default=10, ge=1, le=100),
    threshold: float = Query(default=0.5, ge=0.0, le=1.0)
):
    """
    Find entities similar to the given entity
    """
    try:
        # Generate embedding for the entity
        entity_embedding = nlp_service.generate_embedding(entity)
        
        # Search for similar entities
        results = qdrant_service.search_similar(
            query_vector=entity_embedding,
            top_k=top_k + 1,  # +1 to account for the entity itself
            score_threshold=threshold
        )
        
        # Filter out the entity itself
        filtered_results = [r for r in results if r["text"] != entity][:top_k]
        
        return {
            "status": "success",
            "entity": entity,
            "similar_entities": filtered_results,
            "total": len(filtered_results)
        }
        
    except Exception as e:
        logger.error(f"Error in find_similar_entities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/info")
async def get_search_info():
    """
    Get information about the vector search collection
    """
    try:
        info = qdrant_service.get_collection_info()
        return {
            "status": "success",
            "collection_info": info
        }
    except Exception as e:
        logger.error(f"Error in get_search_info: {e}")
        raise HTTPException(status_code=500, detail=str(e))
