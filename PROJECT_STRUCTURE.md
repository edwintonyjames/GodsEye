# Project Structure

Complete file and directory structure of DefinitelyNotASpy.

```
DefinitelyNotASpy/
│
├── 📄 README.md                          # Main project documentation
├── 📄 QUICKSTART.md                      # Quick start guide
├── 📄 ARCHITECTURE.md                    # System architecture details
├── 📄 CONTRIBUTING.md                    # Contribution guidelines
├── 📄 CHANGELOG.md                       # Version history
├── 📄 LICENSE                            # MIT License
├── 📄 Makefile                           # Common make commands
├── 📄 .gitignore                         # Git ignore rules
├── 📄 .env.example                       # Environment variables template
├── 📄 docker-compose.yml                 # Docker orchestration
├── 📄 start.sh                           # Startup script
│
├── 📁 crawler-service/                   # Go crawler microservice
│   ├── 📄 main.go                        # Entry point
│   ├── 📄 go.mod                         # Go dependencies
│   ├── 📄 go.sum                         # Go dependency checksums
│   ├── 📄 Dockerfile                     # Docker build config
│   │
│   └── 📁 internal/                      # Internal packages
│       ├── 📁 crawler/
│       │   └── 📄 crawler.go             # Crawling logic with Colly
│       │
│       ├── 📁 handlers/
│       │   └── 📄 handlers.go            # HTTP request handlers
│       │
│       ├── 📁 models/
│       │   └── 📄 models.go              # Data structures
│       │
│       └── 📁 database/
│           └── 📄 redis.go               # Redis connection
│
├── 📁 intel-service/                     # Python intelligence microservice
│   ├── 📄 main.py                        # FastAPI entry point
│   ├── 📄 requirements.txt               # Python dependencies
│   ├── 📄 Dockerfile                     # Docker build config
│   ├── 📄 pytest.ini                     # Pytest configuration
│   │
│   ├── 📁 app/
│   │   ├── 📄 __init__.py
│   │   │
│   │   ├── 📁 models/                    # Pydantic schemas
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 schemas.py
│   │   │
│   │   ├── 📁 services/                  # Business logic
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 nlp_service.py         # NER and NLP processing
│   │   │   ├── 📄 neo4j_service.py       # Graph database operations
│   │   │   └── 📄 qdrant_service.py      # Vector search operations
│   │   │
│   │   ├── 📁 routers/                   # API routes
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 analysis.py            # Analysis endpoints
│   │   │   ├── 📄 graph.py               # Graph endpoints
│   │   │   └── 📄 search.py              # Search endpoints
│   │   │
│   │   └── 📁 utils/                     # Utility functions
│   │       ├── 📄 __init__.py
│   │       └── 📄 helpers.py
│   │
│   └── 📁 tests/                         # Test suite
│       ├── 📄 __init__.py
│       └── 📄 test_nlp_service.py
│
└── 📁 examples/                          # Usage examples
    └── 📄 api_examples.md                # API usage examples
```

## File Descriptions

### Root Level Files

- **README.md**: Complete project overview, features, setup instructions
- **QUICKSTART.md**: 5-minute quick start guide
- **ARCHITECTURE.md**: Detailed system architecture and design decisions
- **CONTRIBUTING.md**: Guidelines for contributing to the project
- **CHANGELOG.md**: Version history and release notes
- **LICENSE**: MIT license
- **Makefile**: Common commands (build, up, down, logs, etc.)
- **.gitignore**: Files and directories to exclude from git
- **.env.example**: Template for environment variables
- **docker-compose.yml**: Multi-container Docker application configuration
- **start.sh**: Convenience script to start all services

### Crawler Service (Go)

#### Main Files
- **main.go**: HTTP server setup, middleware, routing
- **go.mod**: Go module definition and dependencies
- **Dockerfile**: Multi-stage Docker build for Go application

#### internal/crawler/
- **crawler.go**: Web crawling implementation using Colly
  - Concurrent crawling with goroutines
  - URL deduplication
  - Content extraction
  - Link following
  - Rate limiting

#### internal/handlers/
- **handlers.go**: HTTP request handlers
  - Health check
  - Start crawl
  - Get status
  - List jobs
  - Cancel job

#### internal/models/
- **models.go**: Data structures
  - CrawlRequest
  - CrawlJob
  - CrawlResult
  - JobStatus

#### internal/database/
- **redis.go**: Redis connection and operations

### Intel Service (Python)

#### Main Files
- **main.py**: FastAPI application with lifecycle management
- **requirements.txt**: Python package dependencies
- **Dockerfile**: Python application container
- **pytest.ini**: Test configuration

#### app/models/
- **schemas.py**: Pydantic models for request/response validation
  - Entity
  - AnalyzeRequest/Response
  - CompareRequest/Response
  - GraphResponse
  - SearchRequest/Response

#### app/services/
- **nlp_service.py**: NLP operations
  - Entity extraction with spaCy
  - Embedding generation with SentenceTransformers
  - Text summarization
  - Similarity calculation
  - Fact extraction

- **neo4j_service.py**: Graph database operations
  - Entity creation
  - Relationship creation
  - Graph traversal
  - Search entities
  - Store facts

- **qdrant_service.py**: Vector search operations
  - Store embeddings
  - Similarity search
  - Collection management
  - Batch operations

#### app/routers/
- **analysis.py**: Analysis endpoints
  - Analyze text
  - Compare entities
  - Process crawled data

- **graph.py**: Graph endpoints
  - Get entity graph
  - Create entities/relationships
  - Search graph
  - Get statistics

- **search.py**: Search endpoints
  - Semantic search
  - Find similar entities
  - Collection info

#### app/utils/
- **helpers.py**: Utility functions
  - Text cleaning
  - URL parsing
  - Text truncation

### Tests
- **test_nlp_service.py**: Unit tests for NLP service

### Examples
- **api_examples.md**: Complete API usage examples in various languages

## Technology Stack Summary

### Go Crawler Service
- **Framework**: Fiber v2.51
- **Scraping**: Colly v2.1
- **Logging**: Logrus v1.9
- **Database**: Redis v8
- **UUID**: Google UUID v1.5

### Python Intel Service
- **Framework**: FastAPI 0.104
- **NLP**: spaCy 3.7
- **Embeddings**: SentenceTransformers 2.2
- **Graph DB**: Neo4j 5.14
- **Vector DB**: Qdrant Client 1.6
- **Logging**: Loguru 0.7

### Infrastructure
- **Docker**: Multi-container orchestration
- **Neo4j**: 5.12 (Graph database)
- **Qdrant**: Latest (Vector database)
- **Redis**: 7-alpine (Job queue)

## API Structure

### Crawler Service (Port 8080)
```
/health
/api/v1/
  ├── /crawl        (POST)
  ├── /status/:id   (GET)
  ├── /jobs         (GET)
  └── /job/:id      (DELETE)
```

### Intel Service (Port 8000)
```
/health
/docs (Swagger UI)
/api/v1/
  ├── /analyze      (POST)
  ├── /compare      (POST)
  ├── /process      (POST)
  ├── /search       (POST)
  └── /graph/
      ├── /:entity         (GET)
      ├── /stats           (GET)
      ├── /entity          (POST)
      ├── /relationship    (POST)
      └── /search          (GET)
```

## Data Flow

1. **User → Crawler**: Submit crawl request
2. **Crawler → Web**: Fetch pages concurrently
3. **Crawler → Intel**: Send extracted content
4. **Intel → NLP**: Extract entities and embeddings
5. **Intel → Neo4j**: Store entities and relationships
6. **Intel → Qdrant**: Store vector embeddings
7. **User → Intel**: Query for analysis/search
8. **Intel → User**: Return results with confidence scores

## Port Mapping

| Service | Port | Purpose |
|---------|------|---------|
| Crawler | 8080 | HTTP API |
| Intel | 8000 | HTTP API |
| Neo4j Browser | 7474 | Web UI |
| Neo4j Bolt | 7687 | Database |
| Qdrant HTTP | 6333 | HTTP API & Dashboard |
| Qdrant gRPC | 6334 | gRPC API |
| Redis | 6379 | Cache/Queue |

## Environment Variables

See `.env.example` for complete list. Key variables:
- `CRAWLER_PORT`: Crawler service port
- `INTEL_PORT`: Intel service port
- `NEO4J_URI`: Neo4j connection string
- `QDRANT_HOST`: Qdrant host
- `LOG_LEVEL`: Logging level

## Volume Mounts

- `neo4j_data`: Persistent Neo4j graph data
- `neo4j_logs`: Neo4j logs
- `qdrant_data`: Qdrant vector storage
- `redis_data`: Redis persistence

## Network

All services communicate through `app-network` bridge network for isolation and service discovery.
