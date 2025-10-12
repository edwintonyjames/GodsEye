"""
Qdrant Service for vector similarity search
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from typing import List, Dict, Any, Optional
import os
from loguru import logger
import uuid


class QdrantService:
    """Qdrant vector database service"""
    
    def __init__(self):
        self.client = None
        self.host = os.getenv("QDRANT_HOST", "localhost")
        self.port = int(os.getenv("QDRANT_PORT", "6333"))
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "entities")
        self.vector_size = 384  # Size for all-MiniLM-L6-v2
    
    async def initialize(self):
        """Initialize Qdrant client and create collection"""
        try:
            self.client = QdrantClient(host=self.host, port=self.port)
            
            # Create collection if it doesn't exist
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name not in collection_names:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Qdrant collection exists: {self.collection_name}")
                
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant: {e}")
            raise
    
    def store_embedding(
        self,
        text: str,
        embedding: List[float],
        metadata: Dict[str, Any]
    ) -> str:
        """Store text embedding in Qdrant"""
        point_id = str(uuid.uuid4())
        
        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "text": text,
                **metadata
            }
        )
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )
        
        logger.info(f"Stored embedding with ID: {point_id}")
        return point_id
    
    def search_similar(
        self,
        query_vector: List[float],
        top_k: int = 10,
        score_threshold: float = 0.5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar embeddings"""
        search_params = {
            "collection_name": self.collection_name,
            "query_vector": query_vector,
            "limit": top_k,
            "score_threshold": score_threshold,
        }
        
        # Add filters if provided
        if filters:
            filter_conditions = []
            for key, value in filters.items():
                filter_conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )
            if filter_conditions:
                search_params["query_filter"] = Filter(must=filter_conditions)
        
        results = self.client.search(**search_params)
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "score": result.score,
                "text": result.payload.get("text", ""),
                "metadata": {k: v for k, v in result.payload.items() if k != "text"}
            })
        
        logger.info(f"Found {len(formatted_results)} similar results")
        return formatted_results
    
    def delete_by_id(self, point_id: str) -> bool:
        """Delete a point by ID"""
        try:
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=[point_id]
            )
            logger.info(f"Deleted point: {point_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete point {point_id}: {e}")
            return False
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get collection information"""
        try:
            info = self.client.get_collection(collection_name=self.collection_name)
            return {
                "name": self.collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return {}
    
    def batch_store_embeddings(
        self,
        embeddings: List[tuple[str, List[float], Dict[str, Any]]]
    ) -> List[str]:
        """Store multiple embeddings at once"""
        points = []
        point_ids = []
        
        for text, embedding, metadata in embeddings:
            point_id = str(uuid.uuid4())
            point_ids.append(point_id)
            
            points.append(PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "text": text,
                    **metadata
                }
            ))
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        logger.info(f"Stored {len(points)} embeddings")
        return point_ids
