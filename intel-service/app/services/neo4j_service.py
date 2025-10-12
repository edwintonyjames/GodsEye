"""
Neo4j Service for knowledge graph management
"""
from neo4j import AsyncGraphDatabase
from typing import List, Dict, Any, Optional
import os
from loguru import logger


class Neo4jService:
    """Neo4j database service for knowledge graph"""
    
    def __init__(self):
        self.driver = None
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "definitelynotaspy123")
    
    async def connect(self):
        """Connect to Neo4j database"""
        try:
            self.driver = AsyncGraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password)
            )
            # Test connection
            async with self.driver.session() as session:
                result = await session.run("RETURN 1")
                await result.consume()
            logger.info(f"Connected to Neo4j at {self.uri}")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
    
    async def close(self):
        """Close Neo4j connection"""
        if self.driver:
            await self.driver.close()
            logger.info("Neo4j connection closed")
    
    def is_connected(self) -> bool:
        """Check if connected to Neo4j"""
        return self.driver is not None
    
    async def create_entity(self, entity_type: str, properties: Dict[str, Any]) -> str:
        """Create an entity node in the graph"""
        async with self.driver.session() as session:
            query = f"""
            MERGE (e:{entity_type} {{name: $name}})
            SET e += $properties
            RETURN e.name as name, id(e) as id
            """
            result = await session.run(
                query,
                name=properties.get("name", ""),
                properties=properties
            )
            record = await result.single()
            if record:
                logger.info(f"Created entity: {entity_type} - {record['name']}")
                return str(record["id"])
            return None
    
    async def create_relationship(
        self,
        from_entity: str,
        to_entity: str,
        relationship_type: str,
        properties: Dict[str, Any] = None
    ) -> bool:
        """Create a relationship between two entities"""
        async with self.driver.session() as session:
            query = """
            MATCH (a {name: $from_name})
            MATCH (b {name: $to_name})
            MERGE (a)-[r:""" + relationship_type + """]->(b)
            """
            
            if properties:
                query += " SET r += $properties"
            
            query += " RETURN r"
            
            result = await session.run(
                query,
                from_name=from_entity,
                to_name=to_entity,
                properties=properties or {}
            )
            
            record = await result.single()
            if record:
                logger.info(f"Created relationship: {from_entity} -{relationship_type}-> {to_entity}")
                return True
            return False
    
    async def get_entity_graph(self, entity_name: str, depth: int = 1) -> Dict[str, Any]:
        """Get entity and its relationships up to specified depth"""
        async with self.driver.session() as session:
            query = """
            MATCH path = (e {name: $name})-[*0..{depth}]-(related)
            RETURN e, related, relationships(path) as rels
            """.replace("{depth}", str(depth))
            
            result = await session.run(query, name=entity_name)
            
            nodes = []
            relationships = []
            
            async for record in result:
                # Add main entity
                if record["e"]:
                    node = dict(record["e"])
                    nodes.append({
                        "id": node.get("name", ""),
                        "label": list(record["e"].labels)[0] if record["e"].labels else "Entity",
                        "properties": node
                    })
                
                # Add related nodes
                if record["related"]:
                    node = dict(record["related"])
                    nodes.append({
                        "id": node.get("name", ""),
                        "label": list(record["related"].labels)[0] if record["related"].labels else "Entity",
                        "properties": node
                    })
                
                # Add relationships
                if record["rels"]:
                    for rel in record["rels"]:
                        relationships.append({
                            "source": rel.start_node.get("name", ""),
                            "target": rel.end_node.get("name", ""),
                            "type": rel.type,
                            "properties": dict(rel)
                        })
            
            # Remove duplicates
            unique_nodes = {node["id"]: node for node in nodes}.values()
            
            return {
                "nodes": list(unique_nodes),
                "relationships": relationships
            }
    
    async def search_entities(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for entities by name or properties"""
        async with self.driver.session() as session:
            cypher_query = """
            MATCH (e)
            WHERE e.name CONTAINS $query OR any(prop in keys(e) WHERE toString(e[prop]) CONTAINS $query)
            RETURN e, labels(e) as labels
            LIMIT $limit
            """
            
            result = await session.run(cypher_query, query=query, limit=limit)
            
            entities = []
            async for record in result:
                node = dict(record["e"])
                entities.append({
                    "name": node.get("name", ""),
                    "labels": record["labels"],
                    "properties": node
                })
            
            return entities
    
    async def store_facts(self, facts: List[Dict[str, Any]]):
        """Store extracted facts as graph relationships"""
        async with self.driver.session() as session:
            for fact in facts:
                try:
                    # Create subject and object nodes
                    await session.run(
                        "MERGE (s:Entity {name: $subject})",
                        subject=fact["subject"]
                    )
                    await session.run(
                        "MERGE (o:Entity {name: $object})",
                        object=fact["object"]
                    )
                    
                    # Create relationship
                    relationship_type = fact["predicate"].upper().replace(" ", "_")
                    query = f"""
                    MATCH (s:Entity {{name: $subject}})
                    MATCH (o:Entity {{name: $object}})
                    MERGE (s)-[r:{relationship_type}]->(o)
                    SET r.sentence = $sentence
                    """
                    
                    await session.run(
                        query,
                        subject=fact["subject"],
                        object=fact["object"],
                        sentence=fact.get("sentence", "")
                    )
                    
                except Exception as e:
                    logger.error(f"Failed to store fact: {e}")
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics"""
        async with self.driver.session() as session:
            # Count nodes
            result = await session.run("MATCH (n) RETURN count(n) as count")
            node_count = (await result.single())["count"]
            
            # Count relationships
            result = await session.run("MATCH ()-[r]->() RETURN count(r) as count")
            rel_count = (await result.single())["count"]
            
            # Get node labels
            result = await session.run("CALL db.labels()")
            labels = [record["label"] async for record in result]
            
            return {
                "nodes": node_count,
                "relationships": rel_count,
                "labels": labels
            }
