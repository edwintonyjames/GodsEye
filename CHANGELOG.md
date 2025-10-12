# Changelog

All notable changes to DefinitelyNotASpy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-12

### Added
- Initial release of DefinitelyNotASpy
- Go-based crawler service with Colly integration
- Python-based intelligence service with FastAPI
- Named Entity Recognition using spaCy
- Semantic embeddings with SentenceTransformers
- Neo4j knowledge graph integration
- Qdrant vector similarity search
- Redis job queue for crawler
- Docker Compose orchestration
- Comprehensive API documentation
- Health check endpoints
- REST APIs for both services
- Entity extraction and analysis
- Semantic search capabilities
- Entity comparison functionality
- Graph traversal and visualization
- Batch processing of crawled data
- Rate limiting and concurrent crawling
- Fact extraction from text
- Relationship discovery

### API Endpoints

#### Crawler Service (Port 8080)
- `GET /health` - Health check
- `POST /api/v1/crawl` - Start crawl job
- `GET /api/v1/status/:id` - Get job status
- `GET /api/v1/jobs` - List all jobs
- `DELETE /api/v1/job/:id` - Cancel job

#### Intel Service (Port 8000)
- `GET /health` - Health check
- `POST /api/v1/analyze` - Analyze text
- `POST /api/v1/compare` - Compare entities
- `POST /api/v1/process` - Process crawled data
- `GET /api/v1/graph/:entity` - Get entity graph
- `POST /api/v1/search` - Semantic search
- `GET /api/v1/graph/stats` - Graph statistics
- `POST /api/v1/graph/entity` - Create entity
- `POST /api/v1/graph/relationship` - Create relationship
- `GET /api/v1/graph/search` - Search graph

### Documentation
- README.md with comprehensive project overview
- QUICKSTART.md for fast setup
- ARCHITECTURE.md for system design details
- CONTRIBUTING.md for contributor guidelines
- API examples and usage documentation
- Makefile for common commands
- Startup scripts

### Infrastructure
- Docker containers for all services
- Neo4j database for knowledge graph
- Qdrant for vector storage
- Redis for job queue
- Health checks and monitoring
- CORS support
- Structured logging

## [Unreleased]

### Planned Features
- Authentication and authorization
- User management system
- Webhook notifications
- Scheduled crawls (cron jobs)
- CLI tool for management
- Web dashboard for visualization
- Export functionality (JSON, CSV, GraphML)
- LLM integration for summarization
- Multi-language support
- Custom NER model training
- Advanced graph algorithms
- Real-time streaming updates
- Kubernetes deployment manifests
- Monitoring and alerting setup
- Rate limiting per API key
- Caching layer for performance
- Incremental crawling
- Duplicate detection improvements
