# API Examples

This document provides examples of how to use the DefinitelyNotASpy APIs.

## Crawler Service API

### 1. Start a Crawl Job

```bash
curl -X POST http://localhost:8080/api/v1/crawl \
  -H "Content-Type: application/json" \
  -d '{
    "query": "elon musk spacex",
    "max_pages": 20,
    "max_depth": 2
  }'
```

Response:
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "pending",
  "message": "Crawl job created successfully",
  "job": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "query": "elon musk spacex",
    "status": "pending",
    "max_pages": 20,
    "max_depth": 2,
    "pages_crawled": 0,
    "urls_found": 0,
    "started_at": "2025-10-12T09:00:00Z"
  }
}
```

### 2. Check Crawl Status

```bash
curl http://localhost:8080/api/v1/status/123e4567-e89b-12d3-a456-426614174000
```

Response:
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "running",
  "pages_crawled": 15,
  "urls_found": 87,
  "progress": 75.0,
  "started_at": "2025-10-12T09:00:00Z"
}
```

### 3. List All Jobs

```bash
curl http://localhost:8080/api/v1/jobs
```

## Intel Service API

### 1. Analyze Text

```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Elon Musk is the CEO of SpaceX and Tesla. He was born in South Africa and moved to the United States.",
    "extract_entities": true,
    "generate_summary": true,
    "store_in_graph": true
  }'
```

Response:
```json
{
  "status": "success",
  "entities": [
    {
      "text": "Elon Musk",
      "label": "PERSON",
      "start": 0,
      "end": 9,
      "confidence": null
    },
    {
      "text": "SpaceX",
      "label": "ORG",
      "start": 24,
      "end": 30,
      "confidence": null
    },
    {
      "text": "Tesla",
      "label": "ORG",
      "start": 35,
      "end": 40,
      "confidence": null
    },
    {
      "text": "South Africa",
      "label": "GPE",
      "start": 58,
      "end": 70,
      "confidence": null
    },
    {
      "text": "United States",
      "label": "GPE",
      "start": 88,
      "end": 101,
      "confidence": null
    }
  ],
  "summary": "Elon Musk is the CEO of SpaceX and Tesla. He was born in South Africa and moved to the United States.",
  "metadata": {
    "entity_count": 5,
    "facts_count": 2
  }
}
```

### 2. Compare Entities

```bash
curl -X POST http://localhost:8000/api/v1/compare \
  -H "Content-Type: application/json" \
  -d '{
    "entity1": {
      "text": "Elon Musk, CEO of Tesla and SpaceX",
      "name": "Elon Musk",
      "role": "CEO"
    },
    "entity2": {
      "text": "Elon Musk, founder of SpaceX",
      "name": "Elon Musk",
      "role": "Founder"
    },
    "threshold": 0.7
  }'
```

Response:
```json
{
  "status": "success",
  "similarity": 0.92,
  "matching_attributes": ["name"],
  "conflicting_attributes": [
    {
      "attribute": "role",
      "entity1_value": "CEO",
      "entity2_value": "Founder"
    }
  ],
  "verdict": "match"
}
```

### 3. Get Entity Graph

```bash
curl http://localhost:8000/api/v1/graph/Elon%20Musk?depth=2
```

Response:
```json
{
  "status": "success",
  "entity": "Elon Musk",
  "depth": 2,
  "nodes": [
    {
      "id": "Elon Musk",
      "label": "PERSON",
      "properties": {
        "name": "Elon Musk",
        "source": "analysis"
      }
    },
    {
      "id": "SpaceX",
      "label": "ORG",
      "properties": {
        "name": "SpaceX"
      }
    }
  ],
  "relationships": [
    {
      "source": "Elon Musk",
      "target": "SpaceX",
      "type": "CEO_OF",
      "properties": {}
    }
  ]
}
```

### 4. Semantic Search

```bash
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "space exploration companies",
    "top_k": 5,
    "threshold": 0.6
  }'
```

Response:
```json
{
  "status": "success",
  "query": "space exploration companies",
  "results": [
    {
      "entity": "SpaceX",
      "score": 0.89,
      "metadata": {
        "label": "ORG",
        "source": "analysis"
      }
    },
    {
      "entity": "NASA",
      "score": 0.82,
      "metadata": {
        "label": "ORG",
        "source": "crawl"
      }
    }
  ],
  "total": 2
}
```

### 5. Search Graph

```bash
curl "http://localhost:8000/api/v1/graph/search?query=Tesla&limit=10"
```

### 6. Get Graph Statistics

```bash
curl http://localhost:8000/api/v1/graph/stats
```

Response:
```json
{
  "status": "success",
  "statistics": {
    "nodes": 150,
    "relationships": 230,
    "labels": ["PERSON", "ORG", "GPE", "Entity"]
  }
}
```

## Python Examples

### Using Python requests library

```python
import requests
import json

# Start a crawl
crawl_data = {
    "query": "artificial intelligence",
    "max_pages": 30,
    "max_depth": 2
}

response = requests.post(
    "http://localhost:8080/api/v1/crawl",
    json=crawl_data
)
job = response.json()
job_id = job["job_id"]

print(f"Started crawl job: {job_id}")

# Check status
status_response = requests.get(
    f"http://localhost:8080/api/v1/status/{job_id}"
)
print(status_response.json())

# Analyze text
analyze_data = {
    "text": "OpenAI released GPT-4 in March 2023.",
    "extract_entities": True,
    "store_in_graph": True
}

intel_response = requests.post(
    "http://localhost:8000/api/v1/analyze",
    json=analyze_data
)
print(intel_response.json())
```

## JavaScript/Node.js Examples

```javascript
// Start a crawl
const crawlData = {
  query: "machine learning",
  max_pages: 20,
  max_depth: 2
};

fetch("http://localhost:8080/api/v1/crawl", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(crawlData)
})
  .then(response => response.json())
  .then(data => console.log("Job ID:", data.job_id))
  .catch(error => console.error("Error:", error));

// Analyze text
const analyzeData = {
  text: "Microsoft acquired GitHub in 2018.",
  extract_entities: true,
  store_in_graph: true
};

fetch("http://localhost:8000/api/v1/analyze", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(analyzeData)
})
  .then(response => response.json())
  .then(data => console.log("Entities:", data.entities))
  .catch(error => console.error("Error:", error));
```
