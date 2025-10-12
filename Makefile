.PHONY: help build up down logs clean test restart

help:
	@echo "DefinitelyNotASpy - Available commands:"
	@echo "  make build     - Build all Docker images"
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make logs      - View logs from all services"
	@echo "  make clean     - Clean up containers and volumes"
	@echo "  make test      - Run tests"
	@echo "  make restart   - Restart all services"
	@echo "  make crawler   - View crawler service logs"
	@echo "  make intel     - View intel service logs"

build:
	@echo "📦 Building Docker images..."
	docker-compose build

up:
	@echo "🚀 Starting services..."
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "Crawler API: http://localhost:8080"
	@echo "Intel API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

down:
	@echo "🛑 Stopping services..."
	docker-compose down

logs:
	docker-compose logs -f

crawler:
	docker-compose logs -f crawler-service

intel:
	docker-compose logs -f intel-service

clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	docker system prune -f

restart:
	@echo "🔄 Restarting services..."
	docker-compose restart

test:
	@echo "🧪 Running tests..."
	cd crawler-service && go test ./...
	cd intel-service && pytest

dev-crawler:
	@echo "🔧 Starting crawler service in dev mode..."
	cd crawler-service && go run main.go

dev-intel:
	@echo "🔧 Starting intel service in dev mode..."
	cd intel-service && uvicorn main:app --reload --port 8000

status:
	@echo "📊 Service Status:"
	docker-compose ps
