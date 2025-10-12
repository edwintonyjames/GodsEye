#!/bin/bash

# DefinitelyNotASpy - Installation Validation Script

echo "🔍 Validating DefinitelyNotASpy Installation..."
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SUCCESS=0
WARNINGS=0
ERRORS=0

# Check Docker
echo "Checking Docker..."
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker is installed"
    if docker info &> /dev/null; then
        echo -e "${GREEN}✓${NC} Docker daemon is running"
        ((SUCCESS++))
    else
        echo -e "${RED}✗${NC} Docker daemon is not running"
        ((ERRORS++))
    fi
else
    echo -e "${RED}✗${NC} Docker is not installed"
    ((ERRORS++))
fi

echo ""

# Check Docker Compose
echo "Checking Docker Compose..."
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker Compose is installed"
    ((SUCCESS++))
else
    echo -e "${RED}✗${NC} Docker Compose is not installed"
    ((ERRORS++))
fi

echo ""

# Check environment file
echo "Checking environment configuration..."
if [ -f .env ]; then
    echo -e "${GREEN}✓${NC} .env file exists"
    ((SUCCESS++))
else
    echo -e "${YELLOW}⚠${NC} .env file not found (will use .env.example)"
    ((WARNINGS++))
fi

echo ""

# Check services
echo "Checking services status..."

check_service() {
    local service=$1
    local url=$2
    
    if curl -s -f "$url" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $service is responding"
        return 0
    else
        echo -e "${RED}✗${NC} $service is not responding at $url"
        return 1
    fi
}

# Check if containers are running
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}✓${NC} Docker containers are running"
    
    sleep 2
    
    if check_service "Crawler Service" "http://localhost:8080/health"; then
        ((SUCCESS++))
    else
        ((ERRORS++))
    fi
    
    if check_service "Intel Service" "http://localhost:8000/health"; then
        ((SUCCESS++))
    else
        ((ERRORS++))
    fi
    
    if check_service "Neo4j" "http://localhost:7474"; then
        ((SUCCESS++))
    else
        ((ERRORS++))
    fi
    
    if check_service "Qdrant" "http://localhost:6333/dashboard"; then
        ((SUCCESS++))
    else
        ((ERRORS++))
    fi
else
    echo -e "${YELLOW}⚠${NC} Services are not running. Start with: make up"
    ((WARNINGS++))
fi

echo ""

# Check ports
echo "Checking port availability..."
check_port() {
    local port=$1
    local service=$2
    
    if lsof -i :$port > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Port $port ($service) is in use"
    else
        echo -e "${YELLOW}⚠${NC} Port $port ($service) is not in use"
    fi
}

check_port 8080 "Crawler"
check_port 8000 "Intel"
check_port 7474 "Neo4j"
check_port 6333 "Qdrant"

echo ""
echo "═══════════════════════════════════════"
echo "Validation Summary:"
echo -e "${GREEN}✓ Successful checks: $SUCCESS${NC}"
echo -e "${YELLOW}⚠ Warnings: $WARNINGS${NC}"
echo -e "${RED}✗ Errors: $ERRORS${NC}"
echo "═══════════════════════════════════════"

if [ $ERRORS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All checks passed! System is ready.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. View API docs: http://localhost:8000/docs"
    echo "  2. Check examples: cat examples/api_examples.md"
    echo "  3. Run a test crawl: make test"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Some checks failed. Please fix the errors above.${NC}"
    echo ""
    echo "Common fixes:"
    echo "  - Start Docker Desktop"
    echo "  - Run: make up"
    echo "  - Check logs: docker-compose logs"
    exit 1
fi
