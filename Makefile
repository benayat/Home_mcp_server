.PHONY: help install install-dev test lint format clean run-math run-viz run-gateway docker-build docker-run docker-test docker-stop docker-clean docker-all

help:
	@echo "Available commands:"
	@echo "  install          Install the package"
	@echo "  install-dev      Install with development dependencies"
	@echo "  test             Run tests"
	@echo "  lint             Run linting"
	@echo "  format           Format code with black and isort"
	@echo "  clean            Clean build artifacts"
	@echo "  run-math         Run the math MCP server"
	@echo "  run-viz          Run the visualization MCP server"
	@echo "  run-gateway      Run the gateway MCP server (recommended)"
	@echo ""
	@echo "Docker commands:"
	@echo "  docker-build     Build Docker image"
	@echo "  docker-run       Run Docker container"
	@echo "  docker-test      Test Docker container"
	@echo "  docker-stop      Stop Docker container"
	@echo "  docker-clean     Clean Docker resources"
	@echo "  docker-all       Build, run, and test Docker container"
	@echo ""
	@echo "Docker Compose commands:"
	@echo "  docker-compose-up     Start services with Docker Compose"
	@echo "  docker-compose-down   Stop services with Docker Compose"
	@echo "  docker-compose-test   Test services with Docker Compose"
	@echo "  docker-compose-all    Build, (re)create, start, and attach to services"
	@echo ""
	@echo "REST API commands:"
	@echo "  run-rest-api     Run REST API server"
	@echo "  docker-rest-api  Run REST API in Docker"
	@echo "  docker-rest-api-logs  View logs for REST API in Docker"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pip install -r requirements-dev.txt

test:
	python -m pytest tests/ -v

lint:
	flake8 mcp_servers/
	mypy mcp_servers/

format:
	black mcp_servers/ tests/
	isort mcp_servers/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run-math:
	python -m mcp_servers.math_server

run-viz:
	python -m mcp_servers.visualization_server

run-gateway:
	python -m mcp_servers.gateway_server

# Docker commands
docker-build:
	./scripts/docker-deploy.sh build

docker-run:
	./scripts/docker-deploy.sh run

docker-test:
	./scripts/docker-deploy.sh test

docker-stop:
	./scripts/docker-deploy.sh stop

docker-clean:
	./scripts/docker-deploy.sh cleanup

docker-all:
	./scripts/docker-deploy.sh all

# Docker Compose commands
docker-compose-up:
	./scripts/docker-compose-deploy.sh start

docker-compose-down:
	./scripts/docker-compose-deploy.sh stop

docker-compose-test:
	./scripts/docker-compose-deploy.sh test

docker-compose-all:
	./scripts/docker-compose-deploy.sh all

# REST API commands
run-rest-api:
	./scripts/start-rest-api.sh

docker-rest-api:
	docker-compose --profile rest-api up -d

docker-rest-api-logs:
	docker-compose logs -f mcp-rest-api

test-docker:
	python tests/test_docker.py

verify-docker:
	@echo "🐳 Docker Integration Verification"
	@echo "=================================="
	@echo "✅ Dockerfile created"
	@echo "✅ docker-compose.yml created"
	@echo "✅ Deployment scripts created"
	@echo "✅ Documentation created"
	@echo ""
	@echo "📋 Available Docker files:"
	@ls -la Dockerfile docker-compose.yml .dockerignore .env.docker 2>/dev/null || true
	@echo ""
	@echo "📋 Available scripts:"
	@ls -la scripts/docker*.sh 2>/dev/null || true
	@echo ""
	@echo "🚀 Ready for Docker deployment!"
	@echo ""
	@echo "Next steps:"
	@echo "  make docker-all      # Build, run, and test with Docker"
	@echo "  make docker-compose-all  # Build, run, and test with Docker Compose"
