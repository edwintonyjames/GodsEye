#!/bin/bash

# DefinitelyNotASpy - API Test Script

echo "🧪 Testing DefinitelyNotASpy APIs..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Base URLs
CRAWLER_URL="http://localhost:8080"
INTEL_URL="http://localhost:8000"

# Test counter
PASSED=0
FAILED=0

# Helper function for tests
test_endpoint() {
    local name=$1
    local method=$2
    local url=$3
    local data=$4
    
    echo -n "Testing $name... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$url" 2>/dev/null)
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$url" \
            -H "Content-Type: application/json" \
            -d "$data" 2>/dev/null)
    fi
    
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)
    
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
        echo -e "${GREEN}✓ PASSED${NC} (HTTP $http_code)"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} (HTTP $http_code)"
        ((FAILED++))
        return 1
    fi
}

# Test Crawler Service
echo -e "${BLUE}═══ Crawler Service Tests ═══${NC}"
echo ""

test_endpoint "Health Check" "GET" "$CRAWLER_URL/health"

crawl_data='{
  "query": "artificial intelligence",
  "max_pages": 5,
  "max_depth": 1
}'

if test_endpoint "Start Crawl" "POST" "$CRAWLER_URL/api/v1/crawl" "$crawl_data"; then
    # Extract job ID from response (simplified - assumes job_id is in response)
    echo "  Crawl job started successfully"
fi

test_endpoint "List Jobs" "GET" "$CRAWLER_URL/api/v1/jobs"

echo ""

# Test Intel Service
echo -e "${BLUE}═══ Intel Service Tests ═══${NC}"
echo ""

test_endpoint "Health Check" "GET" "$INTEL_URL/health"

analyze_data='{
  "text": "Elon Musk is the CEO of SpaceX and Tesla. The companies are based in California.",
  "extract_entities": true,
  "generate_summary": false,
  "store_in_graph": true
}'

test_endpoint "Analyze Text" "POST" "$INTEL_URL/api/v1/analyze" "$analyze_data"

compare_data='{
  "entity1": {
    "text": "SpaceX is a space exploration company",
    "name": "SpaceX"
  },
  "entity2": {
    "text": "SpaceX develops rockets",
    "name": "SpaceX"
  },
  "threshold": 0.7
}'

test_endpoint "Compare Entities" "POST" "$INTEL_URL/api/v1/compare" "$compare_data"

search_data='{
  "query": "space technology",
  "top_k": 5,
  "threshold": 0.5
}'

test_endpoint "Semantic Search" "POST" "$INTEL_URL/api/v1/search" "$search_data"

test_endpoint "Graph Stats" "GET" "$INTEL_URL/api/v1/graph/stats"

echo ""

# Summary
echo "═══════════════════════════════════════"
echo -e "Test Results: ${GREEN}$PASSED passed${NC}, ${RED}$FAILED failed${NC}"
echo "═══════════════════════════════════════"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi
