"""
Graph router for knowledge graph operations
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from loguru import logger

from app.models.schemas import GraphResponse, GraphNode, GraphRelationship
from app.services.neo4j_service import Neo4jService


router = APIRouter()
neo4j_service = Neo4jService()


@router.get("/graph/{entity}", response_model=GraphResponse)
async def get_entity_graph(
    entity: str,
    depth: int = Query(default=1, ge=1, le=3, description="Depth of graph traversal")
):
    """
    Get knowledge graph for a specific entity
    """
    try:
        # Get graph data from Neo4j
        graph_data = await neo4j_service.get_entity_graph(entity, depth)
        
        # Convert to response format
        nodes = [
            GraphNode(
                id=node["id"],
                label=node["label"],
                properties=node["properties"]
            )
            for node in graph_data["nodes"]
        ]
        
        relationships = [
            GraphRelationship(
                source=rel["source"],
                target=rel["target"],
                type=rel["type"],
                properties=rel.get("properties", {})
            )
            for rel in graph_data["relationships"]
        ]
        
        return GraphResponse(
            status="success",
            entity=entity,
            depth=depth,
            nodes=nodes,
            relationships=relationships
        )
        
    except Exception as e:
        logger.error(f"Error in get_entity_graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/graph/stats")
async def get_graph_statistics():
    """
    Get statistics about the knowledge graph
    """
    try:
        stats = await neo4j_service.get_statistics()
        return {
            "status": "success",
            "statistics": stats
        }
    except Exception as e:
        logger.error(f"Error in get_graph_statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/graph/entity")
async def create_entity(
    entity_type: str,
    name: str,
    properties: Optional[dict] = None
):
    """
    Create a new entity in the graph
    """
    try:
        props = properties or {}
        props["name"] = name
        
        entity_id = await neo4j_service.create_entity(entity_type, props)
        
        return {
            "status": "success",
            "entity_id": entity_id,
            "message": f"Created entity: {name}"
        }
    except Exception as e:
        logger.error(f"Error in create_entity: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/graph/relationship")
async def create_relationship(
    from_entity: str,
    to_entity: str,
    relationship_type: str,
    properties: Optional[dict] = None
):
    """
    Create a relationship between two entities
    """
    try:
        success = await neo4j_service.create_relationship(
            from_entity,
            to_entity,
            relationship_type,
            properties
        )
        
        if success:
            return {
                "status": "success",
                "message": f"Created relationship: {from_entity} -{relationship_type}-> {to_entity}"
            }
        else:
            raise HTTPException(status_code=404, detail="One or both entities not found")
            
    except Exception as e:
        logger.error(f"Error in create_relationship: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/graph/search")
async def search_graph(
    query: str = Query(..., description="Search query"),
    limit: int = Query(default=10, ge=1, le=100)
):
    """
    Search for entities in the graph
    """
    try:
        results = await neo4j_service.search_entities(query, limit)
        
        return {
            "status": "success",
            "query": query,
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        logger.error(f"Error in search_graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))
