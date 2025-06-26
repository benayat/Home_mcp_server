#!/bin/bash

# Docker deployment script for MCP Gateway Server
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
IMAGE_NAME="mcp-gateway-server"
VERSION="${VERSION:-latest}"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Build Docker image
build_image() {
    log_info "Building MCP Gateway Server Docker image..."
    
    cd "$PROJECT_DIR"
    
    # Build with build args
    docker build \
        --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
        --build-arg VERSION="$VERSION" \
        -t "$IMAGE_NAME:$VERSION" \
        -t "$IMAGE_NAME:latest" \
        .
    
    log_success "Docker image built successfully: $IMAGE_NAME:$VERSION"
}

# Run container
run_container() {
    log_info "Running MCP Gateway Server container..."
    
    # Stop existing container if running
    if docker ps -q -f name=mcp-gateway-server | grep -q .; then
        log_warning "Stopping existing container..."
        docker stop mcp-gateway-server
        docker rm mcp-gateway-server
    fi
    
    # Create directories for volumes
    mkdir -p "$PROJECT_DIR/logs" "$PROJECT_DIR/plots"
    
    # Run the container
    docker run -d \
        --name mcp-gateway-server \
        --restart unless-stopped \
        -v "$PROJECT_DIR/logs:/app/logs:rw" \
        -v "$PROJECT_DIR/plots:/app/plots:rw" \
        -e LOG_LEVEL=INFO \
        -e MCP_SERVER_TYPE=gateway \
        "$IMAGE_NAME:$VERSION"
    
    log_success "MCP Gateway Server container started successfully"
    
    # Show container status
    docker ps --filter name=mcp-gateway-server --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
}

# Test container
test_container() {
    log_info "Testing MCP Gateway Server container..."
    
    # Wait a moment for container to start
    sleep 3
    
    # Test if container is running
    if ! docker ps -q -f name=mcp-gateway-server | grep -q .; then
        log_error "Container is not running!"
        return 1
    fi
    
    # Test if health check passes
    health_status=$(docker inspect --format='{{.State.Health.Status}}' mcp-gateway-server 2>/dev/null || echo "unknown")
    if [ "$health_status" = "healthy" ]; then
        log_success "Container health check passed"
    else
        log_warning "Container health check status: $health_status"
    fi
    
    # Test basic functionality
    log_info "Testing basic functionality..."
    docker exec mcp-gateway-server python -c "
import sys
sys.path.insert(0, '.')
from mcp_servers.gateway_server import MCPGatewayServer
import asyncio

async def test():
    server = MCPGatewayServer()
    tools = await server.list_tools()
    print(f'✅ Gateway server has {len(tools)} tools available')
    
    result = await server.call_tool('basic_arithmetic', {'operation': 'add', 'a': 10, 'b': 5})
    print(f'✅ Math test: 10 + 5 = {result[\"result\"]}')

asyncio.run(test())
"
    
    log_success "Container functionality test passed"
}

# Show logs
show_logs() {
    log_info "Showing container logs..."
    docker logs -f mcp-gateway-server
}

# Stop container
stop_container() {
    log_info "Stopping MCP Gateway Server container..."
    docker stop mcp-gateway-server || true
    docker rm mcp-gateway-server || true
    log_success "Container stopped and removed"
}

# Clean up
cleanup() {
    log_info "Cleaning up Docker resources..."
    docker system prune -f
    log_success "Cleanup completed"
}

# Usage function
usage() {
    echo "Usage: $0 {build|run|test|logs|stop|cleanup|all}"
    echo ""
    echo "Commands:"
    echo "  build    - Build the Docker image"
    echo "  run      - Run the container"
    echo "  test     - Test the running container"
    echo "  logs     - Show container logs"
    echo "  stop     - Stop and remove the container"
    echo "  cleanup  - Clean up Docker resources"
    echo "  all      - Build, run, and test (recommended)"
    echo ""
    echo "Environment variables:"
    echo "  VERSION  - Docker image version (default: latest)"
}

# Main script logic
case "${1:-}" in
    build)
        build_image
        ;;
    run)
        run_container
        ;;
    test)
        test_container
        ;;
    logs)
        show_logs
        ;;
    stop)
        stop_container
        ;;
    cleanup)
        cleanup
        ;;
    all)
        build_image
        run_container
        test_container
        ;;
    *)
        usage
        exit 1
        ;;
esac
