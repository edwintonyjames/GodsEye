# 🧠 GodsEye

A hybrid AI data retrieval and intelligence system that crawls the internet, extracts and structures information about people, places, or entities, and builds a comprehensive knowledge graph with semantic analysis capabilities.

## 🏗️ Architecture

This project uses a **microservices architecture** with two primary services:

### 1. **Crawler Service** (Go)
- High-performance concurrent web crawling using goroutines
- Google dork / search query integration
- HTML parsing and content extraction
- URL deduplication and rate limiting
- Job queue management with Redis
- REST API for crawl orchestration

### 2. **Intel Service** (Python)
- Named Entity Recognition (NER) using spaCy
- Fact extraction and comparison
- Semantic embeddings with SentenceTransformers
- Knowledge graph creation and enrichment (Neo4j)
- Vector similarity search (Qdrant)
- Text summarization and analysis

## 🛠️ Tech Stack

### Go Service
- **Framework**: Fiber (high-performance HTTP)
- **Scraping**: Colly
- **Logging**: Logrus
- **Database**: PostgreSQL (metadata), Redis (job queue)

### Python Service
- **Framework**: FastAPI
- **NER**: spaCy
- **Embeddings**: SentenceTransformers
- **Graph DB**: Neo4j
- **Vector DB**: Qdrant
- **Logging**: Loguru

### Infrastructure
- **Orchestration**: Docker Compose
- **Message Queue**: Redis
- **Graph Database**: Neo4j
- **Vector Database**: Qdrant

## 📁 Project Structure

```
GodsEye/
├── crawler-service/           # Go-based web crawler
│   ├── main.go
│   ├── go.mod
│   ├── go.sum
│   ├── Dockerfile
│   └── internal/
│       ├── crawler/          # Crawling logic
│       ├── models/           # Data models
│       ├── handlers/         # HTTP handlers
│       └── database/         # DB connections
│
├── intel-service/            # Python-based intelligence API
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── app/
│       ├── models/           # Pydantic models
│       ├── services/         # Business logic
│       ├── routers/          # API routes
│       └── utils/            # Utilities
│
├── docker-compose.yml        # Service orchestration
├── .env.example             # Environment variables template
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Go 1.21+ (for local development)
- Python 3.11+ (for local development)

### Running with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd GodsEye
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**
   ```bash
   docker-compose up --build
   ```

4. **Access the services**
   - Crawler API: http://localhost:8080
   - Intel API: http://localhost:8000
   - Neo4j Browser: http://localhost:7474 (user: neo4j, pass: GodsEye123)
   - Qdrant Dashboard: http://localhost:6333/dashboard

### Local Development

#### Crawler Service (Go)
```bash
cd crawler-service
go mod download
go run main.go
```

#### Intel Service (Python)
```bash
cd intel-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn main:app --reload --port 8000
```

## 📡 API Endpoints

### Crawler Service (Port 8080)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/crawl` | Start a new crawl job |
| GET | `/status/:id` | Get crawl job status |
| GET | `/jobs` | List all crawl jobs |

**Example: Start a crawl**
```bash
curl -X POST http://localhost:8080/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "query": "elon musk spacex",
    "max_pages": 50,
    "max_depth": 2
  }'
```

### Intel Service (Port 8000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/analyze` | Analyze text and extract entities |
| POST | `/compare` | Compare two entities |
| GET | `/graph/{entity}` | Get entity relationship graph |
| POST | `/search` | Semantic search across entities |

**Example: Analyze text**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Elon Musk is the CEO of SpaceX and Tesla.",
    "extract_entities": true
  }'
```

## 🔄 Data Flow

1. **User initiates crawl** → `POST /crawl?query=elon+musk`
2. **Crawler service**:
   - Performs Google dork search
   - Crawls discovered URLs
   - Extracts raw HTML content
3. **Content sent to Intel service** for processing
4. **Intel service**:
   - Cleans and preprocesses text
   - Extracts named entities (people, organizations, locations)
   - Generates embeddings
   - Stores in Neo4j (relationships) and Qdrant (vectors)
5. **User queries** → `/analyze` or `/compare` → receives structured data with:
   - Extracted entities
   - Confidence scores
   - Source URLs
   - Relationship graph

## 🔧 Configuration

### Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `CRAWLER_PORT`: Port for crawler service (default: 8080)
- `INTEL_PORT`: Port for intel service (default: 8000)
- `NEO4J_URI`: Neo4j connection string
- `QDRANT_HOST`: Qdrant host
- `OPENAI_API_KEY`: Optional, for LLM-based summarization
- `MAX_CONCURRENT_CRAWLS`: Max parallel crawl jobs

## 🧪 Testing

### Run tests for Go service
```bash
cd crawler-service
go test ./...
```

### Run tests for Python service
```bash
cd intel-service
pytest
```

## 📊 Monitoring

- **Crawler logs**: `docker-compose logs -f crawler-service`
- **Intel logs**: `docker-compose logs -f intel-service`
- **Neo4j queries**: Access Neo4j Browser at http://localhost:7474
- **Qdrant collections**: Access Qdrant dashboard at http://localhost:6333/dashboard

## 🔐 Security Notes

- Never commit `.env` file with real credentials
- Use environment-specific API keys
- Implement rate limiting for production use
- Add authentication/authorization for API endpoints
- Review and sanitize all crawled content

## 🚧 Roadmap

- [ ] Add authentication and API keys
- [ ] Implement webhook notifications
- [ ] Add scheduled crawls (cron jobs)
- [ ] Implement LLM-based summarization
- [ ] Add CLI tool for management
- [ ] Create web dashboard
- [ ] Add export functionality (JSON, CSV, GraphML)
- [ ] Implement caching layer
- [ ] Add support for more search engines
- [ ] Create Kubernetes manifests

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please read CONTRIBUTING.md for guidelines.

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Ensure you comply with:
- Website terms of service
- `robots.txt` files
- Rate limiting best practices
- Data privacy regulations
- Copyright laws

Always obtain proper authorization before crawling websites.
