# 🚀 Quick Start Guide

Get DefinitelyNotASpy up and running in 5 minutes!

## Prerequisites

- Docker Desktop installed and running
- At least 4GB of available RAM
- Ports 8080, 8000, 7474, 7687, 6333, 6379 available

## Step 1: Clone or Navigate to Project

```bash
cd /Users/we/Documents/DefinitelyNotASpy
```

## Step 2: Environment Setup

```bash
# Copy environment template
cp .env.example .env

# (Optional) Edit .env if you want to customize settings
nano .env
```

## Step 3: Start Services

### Option A: Using the start script
```bash
./start.sh
```

### Option B: Using Make
```bash
make up
```

### Option C: Using Docker Compose directly
```bash
docker-compose up -d
```

## Step 4: Wait for Services to Initialize

This takes about 30-60 seconds. Check status:

```bash
docker-compose ps
```

All services should show "Up" status.

## Step 5: Verify Everything is Running

### Check Health Endpoints

```bash
# Crawler service
curl http://localhost:8080/health

# Intel service
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "crawler" // or "intel"
}
```

## Step 6: Run Your First Crawl

```bash
curl -X POST http://localhost:8080/api/v1/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "query": "artificial intelligence",
    "max_pages": 10,
    "max_depth": 1
  }'
```

Save the `job_id` from the response.

## Step 7: Check Crawl Status

```bash
curl http://localhost:8080/api/v1/status/YOUR_JOB_ID
```

## Step 8: Analyze Some Text

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "OpenAI created ChatGPT in San Francisco. Sam Altman is the CEO.",
    "extract_entities": true,
    "store_in_graph": true
  }'
```

## Step 9: Explore the APIs

### Interactive API Documentation
- Intel Service: http://localhost:8000/docs
- Try out endpoints directly in the browser!

### Neo4j Browser
- URL: http://localhost:7474
- Username: `neo4j`
- Password: `definitelynotaspy123`

Run a Cypher query:
```cypher
MATCH (n) RETURN n LIMIT 25
```

### Qdrant Dashboard
- URL: http://localhost:6333/dashboard
- View your vector collections

## Common Commands

```bash
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f crawler-service
docker-compose logs -f intel-service

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Stop and remove all data
docker-compose down -v
```

## Example Workflow

### 1. Start a crawl about a person
```bash
curl -X POST http://localhost:8080/api/v1/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Elon Musk Tesla",
    "max_pages": 20,
    "max_depth": 2
  }'
```

### 2. Wait for completion (check status periodically)
```bash
curl http://localhost:8080/api/v1/status/YOUR_JOB_ID
```

### 3. Search the knowledge graph
```bash
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "electric vehicles",
    "top_k": 5,
    "threshold": 0.6
  }'
```

### 4. Visualize in Neo4j
Open http://localhost:7474 and run:
```cypher
MATCH (p:PERSON)-[r]->(o:ORG)
RETURN p, r, o
LIMIT 50
```

## Troubleshooting

### Services won't start
```bash
# Check Docker is running
docker info

# Check port conflicts
lsof -i :8080
lsof -i :8000

# View detailed logs
docker-compose logs
```

### Connection errors
```bash
# Restart all services
docker-compose restart

# Or restart specific service
docker-compose restart crawler-service
```

### Out of memory
```bash
# Check Docker memory allocation
docker stats

# Increase Docker Desktop memory in settings
# Recommended: 6GB+
```

### Neo4j connection fails
```bash
# Check Neo4j logs
docker-compose logs neo4j

# Wait longer (Neo4j takes 20-30 seconds to start)
# Check health: curl http://localhost:7474
```

## Next Steps

1. **Explore the APIs**: Check out `/docs` endpoint for interactive documentation
2. **Read the full README**: Learn about all features
3. **Check examples**: See `examples/api_examples.md` for more use cases
4. **Review architecture**: Understand the system in `ARCHITECTURE.md`
5. **Contribute**: See `CONTRIBUTING.md` for contribution guidelines

## Getting Help

- Check logs: `docker-compose logs -f`
- Read troubleshooting: See README.md
- Open an issue: GitHub Issues
- Review documentation: All .md files in project root

## Clean Up

When you're done experimenting:

```bash
# Stop services (keeps data)
docker-compose down

# Stop and remove all data
docker-compose down -v

# Remove Docker images
docker-compose down --rmi all -v
```

---

**That's it!** You now have a fully functional AI-powered web intelligence system running locally. Happy crawling! 🕷️
