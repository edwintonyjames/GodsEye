"""
Analysis router for text processing and entity extraction
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from loguru import logger

from app.models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    CompareRequest,
    CompareResponse,
    ProcessRequest,
    Entity
)
from app.services.nlp_service import NLPService
from app.services.neo4j_service import Neo4jService
from app.services.qdrant_service import QdrantService


router = APIRouter()

# Dependency injection
nlp_service = NLPService()
neo4j_service = Neo4jService()
qdrant_service = QdrantService()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest):
    """
    Analyze text and extract entities, generate embeddings, and optionally summarize
    """
    try:
        entities = []
        summary = None
        metadata = {}
        
        # Extract entities
        if request.extract_entities:
            entities = nlp_service.extract_entities(request.text)
            metadata["entity_count"] = len(entities)
        
        # Generate summary
        if request.generate_summary:
            summary = nlp_service.generate_summary(request.text)
        
        # Store in graph
        if request.store_in_graph and entities:
            for entity in entities:
                try:
                    # Store entity in Neo4j
                    await neo4j_service.create_entity(
                        entity_type=entity.label,
                        properties={
                            "name": entity.text,
                            "source": "analysis"
                        }
                    )
                    
                    # Generate and store embedding in Qdrant
                    embedding = nlp_service.generate_embedding(entity.text)
                    qdrant_service.store_embedding(
                        text=entity.text,
                        embedding=embedding,
                        metadata={
                            "label": entity.label,
                            "source": "analysis"
                        }
                    )
                except Exception as e:
                    logger.error(f"Failed to store entity {entity.text}: {e}")
        
        # Extract facts
        facts = nlp_service.extract_facts(request.text)
        if facts:
            metadata["facts_count"] = len(facts)
            # Store facts in graph
            if request.store_in_graph:
                await neo4j_service.store_facts(facts)
        
        return AnalyzeResponse(
            status="success",
            entities=entities,
            summary=summary,
            metadata=metadata
        )
        
    except Exception as e:
        logger.error(f"Error in analyze_text: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/compare", response_model=CompareResponse)
async def compare_entities(request: CompareRequest):
    """
    Compare two entities and determine similarity
    """
    try:
        entity1_text = request.entity1.get("text", "")
        entity2_text = request.entity2.get("text", "")
        
        if not entity1_text or not entity2_text:
            raise HTTPException(status_code=400, detail="Both entities must have 'text' field")
        
        # Calculate semantic similarity
        similarity = nlp_service.calculate_similarity(entity1_text, entity2_text)
        
        # Find matching and conflicting attributes
        matching_attributes = []
        conflicting_attributes = []
        
        for key in request.entity1.keys():
            if key in request.entity2:
                if request.entity1[key] == request.entity2[key]:
                    matching_attributes.append(key)
                else:
                    conflicting_attributes.append({
                        "attribute": key,
                        "entity1_value": request.entity1[key],
                        "entity2_value": request.entity2[key]
                    })
        
        # Determine verdict
        if similarity >= request.threshold:
            verdict = "match"
        elif similarity >= request.threshold * 0.7:
            verdict = "possible_match"
        else:
            verdict = "no_match"
        
        return CompareResponse(
            status="success",
            similarity=similarity,
            matching_attributes=matching_attributes,
            conflicting_attributes=conflicting_attributes,
            verdict=verdict
        )
        
    except Exception as e:
        logger.error(f"Error in compare_entities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process")
async def process_crawl_results(request: ProcessRequest):
    """
    Process crawled data from the crawler service
    """
    try:
        processed_count = 0
        entities_found = []
        
        for result in request.results:
            try:
                # Extract entities from content
                entities = nlp_service.extract_entities(result.content)
                
                # Store entities in Neo4j and Qdrant
                for entity in entities:
                    # Check if entity already exists
                    if entity.text not in [e.text for e in entities_found]:
                        entities_found.append(entity)
                        
                        # Store in Neo4j
                        await neo4j_service.create_entity(
                            entity_type=entity.label,
                            properties={
                                "name": entity.text,
                                "source_url": result.url,
                                "source_title": result.title,
                                "crawled_at": result.crawled_at.isoformat(),
                                "job_id": request.job_id
                            }
                        )
                        
                        # Generate and store embedding
                        embedding = nlp_service.generate_embedding(entity.text)
                        qdrant_service.store_embedding(
                            text=entity.text,
                            embedding=embedding,
                            metadata={
                                "label": entity.label,
                                "source_url": result.url,
                                "job_id": request.job_id
                            }
                        )
                
                # Extract and store facts
                facts = nlp_service.extract_facts(result.content)
                if facts:
                    await neo4j_service.store_facts(facts)
                
                processed_count += 1
                
            except Exception as e:
                logger.error(f"Failed to process result from {result.url}: {e}")
        
        logger.info(f"Processed {processed_count} crawl results, found {len(entities_found)} entities")
        
        return {
            "status": "success",
            "job_id": request.job_id,
            "processed_count": processed_count,
            "entities_found": len(entities_found),
            "message": f"Successfully processed {processed_count} pages"
        }
        
    except Exception as e:
        logger.error(f"Error in process_crawl_results: {e}")
        raise HTTPException(status_code=500, detail=str(e))
