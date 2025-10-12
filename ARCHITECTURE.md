# Architecture Documentation

## System Overview

DefinitelyNotASpy is a microservices-based system for web crawling, entity extraction, and knowledge graph construction.

## High-Level Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ├─────────────────────────────────┐
       │                                 │
       ▼                                 ▼
┌─────────────────┐            ┌─────────────────┐
│ Crawler Service │            │  Intel Service  │
│     (Go)        │───────────▶│    (Python)     │
└────────┬────────┘            └────────┬────────┘
         │                              │
         │                              ├──────────┐
         │                              │          │
         ▼                              ▼          ▼
    ┌────────┐                   ┌─────────┐ ┌────────┐
    │ Redis  │                   │  Neo4j  │ │ Qdrant │
    └────────┘                   └─────────┘ └────────┘
```

## Service Details

### 1. Crawler Service (Go)

**Purpose**: High-performance web crawling and content extraction

**Technology Stack**:
- Go 1.21+
- Fiber (HTTP framework)
- Colly (web scraping)
- Redis (job queue)

**Responsibilities**:
- Accept crawl requests via REST API
- Manage crawl jobs and queue
- Perform concurrent web crawling
- Extract HTML content and links
- Send data to Intel Service for processing
- Store job metadata

**Key Components**:
- `main.go`: Entry point and HTTP server setup
- `internal/handlers/`: HTTP request handlers
- `internal/crawler/`: Crawling logic and Colly integration
- `internal/models/`: Data structures
- `internal/database/`: Redis connection management

**API Endpoints**:
- `POST /api/v1/crawl`: Start crawl job
- `GET /api/v1/status/:id`: Get job status
- `GET /api/v1/jobs`: List all jobs
- `DELETE /api/v1/job/:id`: Cancel job

### 2. Intel Service (Python)

**Purpose**: NLP processing, entity extraction, and knowledge management

**Technology Stack**:
- Python 3.11+
- FastAPI (HTTP framework)
- spaCy (NER)
- SentenceTransformers (embeddings)
- Neo4j (graph database)
- Qdrant (vector database)

**Responsibilities**:
- Extract named entities from text
- Generate semantic embeddings
- Store entities in knowledge graph
- Perform semantic search
- Compare entities
- Extract facts and relationships

**Key Components**:
- `main.py`: Entry point and FastAPI app
- `app/routers/`: API route handlers
- `app/services/nlp_service.py`: NLP and entity extraction
- `app/services/neo4j_service.py`: Graph database operations
- `app/services/qdrant_service.py`: Vector search operations
- `app/models/`: Pydantic schemas

**API Endpoints**:
- `POST /api/v1/analyze`: Analyze text and extract entities
- `POST /api/v1/compare`: Compare two entities
- `POST /api/v1/process`: Process crawled data
- `GET /api/v1/graph/:entity`: Get entity graph
- `POST /api/v1/search`: Semantic search
- `GET /api/v1/graph/stats`: Graph statistics

## Data Flow

### Crawl Flow

1. **User Request**
   ```
   POST /api/v1/crawl
   {
     "query": "elon musk",
     "max_pages": 50,
     "max_depth": 2
   }
   ```

2. **Crawler Service**
   - Creates job with unique ID
   - Queues job in Redis
   - Performs search query
   - Crawls discovered URLs concurrently
   - Extracts content and links

3. **Intel Service Processing**
   - Receives crawled data
   - Extracts entities using spaCy
   - Generates embeddings
   - Stores in Neo4j (relationships)
   - Stores in Qdrant (vectors)

4. **Response**
   ```json
   {
     "job_id": "uuid",
     "status": "completed",
     "entities_found": 25,
     "pages_crawled": 50
   }
   ```

### Analysis Flow

1. **User Request**
   ```
   POST /api/v1/analyze
   {
     "text": "Sample text",
     "extract_entities": true
   }
   ```

2. **Entity Extraction**
   - spaCy NER processes text
   - Identifies PERSON, ORG, GPE, etc.
   - Extracts confidence scores

3. **Embedding Generation**
   - SentenceTransformer creates vectors
   - Stores in Qdrant with metadata

4. **Graph Storage**
   - Creates entity nodes in Neo4j
   - Establishes relationships
   - Stores source attribution

## Database Schemas

### Neo4j Graph Model

**Node Types**:
- `PERSON`: People entities
- `ORG`: Organizations
- `GPE`: Geopolitical entities (countries, cities)
- `Entity`: Generic entity

**Relationship Types**:
- `WORKS_FOR`
- `LOCATED_IN`
- `FOUNDED`
- `RELATED_TO`
- Custom relationships from fact extraction

**Node Properties**:
```cypher
(:PERSON {
  name: string,
  source: string,
  source_url: string,
  crawled_at: datetime
})
```

### Qdrant Collections

**Collection**: `entities`

**Vector Config**:
- Size: 384 (all-MiniLM-L6-v2)
- Distance: Cosine

**Payload Structure**:
```json
{
  "text": "Entity text",
  "label": "PERSON",
  "source": "crawl",
  "source_url": "https://...",
  "job_id": "uuid"
}
```

## Scaling Considerations

### Horizontal Scaling

**Crawler Service**:
- Stateless design allows multiple instances
- Redis for shared job queue
- Load balancer for request distribution

**Intel Service**:
- Stateless processing
- Multiple workers for parallel processing
- Neo4j cluster for high availability

### Vertical Scaling

**Resource Allocation**:
- Crawler: CPU-intensive (increase cores)
- Intel: Memory-intensive (increase RAM for models)
- Neo4j: Disk I/O (SSD recommended)
- Qdrant: Memory for vectors (RAM based on collection size)

## Performance Optimization

### Crawler Service
- Concurrent goroutines (configurable)
- Rate limiting per domain
- Request timeout controls
- Connection pooling

### Intel Service
- Model caching in memory
- Batch processing for embeddings
- Async Neo4j operations
- Connection pooling

### Database
- Neo4j indexes on frequently queried properties
- Qdrant HNSW index for fast similarity search
- Redis persistence configuration

## Security Considerations

### API Security
- Add authentication middleware (JWT)
- Rate limiting per client
- Input validation and sanitization
- CORS configuration

### Data Security
- Environment variables for secrets
- Encrypted database connections
- Secure Neo4j credentials
- Network isolation between services

### Crawling Ethics
- Respect robots.txt
- Implement rate limiting
- Add user-agent identification
- Handle GDPR/privacy requirements

## Monitoring & Observability

### Metrics to Track
- Crawl job completion rate
- Average crawl time per page
- Entity extraction accuracy
- API response times
- Database query performance
- Error rates

### Logging
- Structured JSON logs
- Centralized log aggregation
- Error tracking and alerting
- Debug mode for development

### Health Checks
- `/health` endpoints on all services
- Database connectivity checks
- Resource utilization monitoring

## Future Enhancements

### Planned Features
- Authentication and user management
- Job scheduling (cron-based crawls)
- Webhook notifications
- Export functionality (JSON, CSV, GraphML)
- Web dashboard for visualization
- CLI tool for management

### Advanced Features
- Multi-language support
- Custom NER models
- LLM integration for summarization
- Advanced graph algorithms
- Real-time streaming updates
- Distributed crawling across multiple nodes

## Technology Decisions

### Why Go for Crawler?
- Excellent concurrency with goroutines
- Fast execution speed
- Low memory footprint
- Strong standard library
- Easy deployment (single binary)

### Why Python for Intel?
- Rich NLP ecosystem (spaCy, Transformers)
- Easy integration with ML models
- Rapid development
- Extensive library support
- Strong typing with Pydantic

### Why Neo4j?
- Native graph database
- Cypher query language
- ACID compliance
- Good performance for graph queries
- Excellent visualization tools

### Why Qdrant?
- Purpose-built for vector similarity
- High performance
- Easy to use API
- Supports filtering
- Good documentation

## Deployment Options

### Docker Compose (Development)
- Single machine deployment
- Easy setup and teardown
- Good for development and testing

### Kubernetes (Production)
- Container orchestration
- Auto-scaling
- High availability
- Rolling updates
- Service discovery

### Cloud Providers
- AWS: ECS/EKS, RDS, ElastiCache
- GCP: GKE, Cloud SQL, Memorystore
- Azure: AKS, Azure Database, Redis Cache
