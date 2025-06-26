#!/bin/bash

# Docker Compose deployment script for MCP Servers
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
ENV_FILE="$PROJECT_DIR/.env.docker"

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

# Setup environment
setup_env() {
    log_info "Setting up environment..."
    
    cd "$PROJECT_DIR"
    
    # Create directories
    mkdir -p logs plots
    
    # Load environment variables
    if [ -f "$ENV_FILE" ]; then
        export $(grep -v '^#' "$ENV_FILE" | xargs)
        log_success "Environment variables loaded from $ENV_FILE"
    else
        log_warning "Environment file not found: $ENV_FILE"
    fi
}

# Build services
build_services() {
    log_info "Building MCP services with Docker Compose..."
    
    cd "$PROJECT_DIR"
    docker-compose build --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
    
    log_success "Services built successfully"
}

# Start services
start_services() {
    local profile="${1:-gateway}"
    
    log_info "Starting MCP services (profile: $profile)..."
    
    cd "$PROJECT_DIR"
    
    if [ "$profile" = "all" ]; then
        docker-compose --profile individual-servers up -d
    else
        docker-compose up -d
    fi
    
    log_success "Services started successfully"
    
    # Show running services
    docker-compose ps
}

# Stop services
stop_services() {
    log_info "Stopping MCP services..."
    
    cd "$PROJECT_DIR"
    docker-compose down
    
    log_success "Services stopped successfully"
}

# Show logs
show_logs() {
    local service="${1:-mcp-gateway}"
    
    log_info "Showing logs for service: $service"
    
    cd "$PROJECT_DIR"
    docker-compose logs -f "$service"
}

# Test services
test_services() {
    log_info "Testing MCP services..."
    
    cd "$PROJECT_DIR"
    
    # Test gateway server
    log_info "Testing gateway server..."
    docker-compose exec mcp-gateway python -c "
import sys
sys.path.insert(0, '.')
from mcp_servers.gateway_server import MCPGatewayServer
import asyncio

async def test():
    server = MCPGatewayServer()
    tools = await server.list_tools()
    print(f'✅ Gateway server: {len(tools)} tools available')
    
    result = await server.call_tool('basic_arithmetic', {'operation': 'multiply', 'a': 8, 'b': 7})
    print(f'✅ Math test: 8 × 7 = {result[\"result\"]}')
    
    resources = await server.list_resources()
    print(f'✅ Resources: {len(resources)} educational resources available')

asyncio.run(test())
"
    
    log_success "Service tests completed successfully"
}

# Monitor services
monitor_services() {
    log_info "Monitoring MCP services..."
    
    cd "$PROJECT_DIR"
    
    echo "=== Service Status ==="
    docker-compose ps
    
    echo -e "\n=== Service Health ==="
    for service in mcp-gateway mcp-math mcp-visualization; do
        if docker-compose ps -q "$service" >/dev/null 2>&1; then
            health=$(docker inspect --format='{{.State.Health.Status}}' "$(docker-compose ps -q "$service")" 2>/dev/null || echo "unknown")
            echo "$service: $health"
        fi
    done
    
    echo -e "\n=== Resource Usage ==="
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" $(docker-compose ps -q)
}

# Cleanup
cleanup() {
    log_info "Cleaning up MCP services and resources..."
    
    cd "$PROJECT_DIR"
    docker-compose down --volumes --remove-orphans
    docker system prune -f
    
    log_success "Cleanup completed"
}

# Usage function
usage() {
    echo "Usage: $0 {build|start|stop|logs|test|monitor|cleanup|all} [options]"
    echo ""
    echo "Commands:"
    echo "  build             - Build all services"
    echo "  start [profile]   - Start services (gateway|all, default: gateway)"
    echo "  stop              - Stop all services"
    echo "  logs [service]    - Show logs (default: mcp-gateway)"
    echo "  test              - Test running services"
    echo "  monitor           - Monitor service status and resources"
    echo "  cleanup           - Stop services and clean up resources"
    echo "  all               - Build, start, and test services"
    echo ""
    echo "Examples:"
    echo "  $0 start          - Start gateway server only"
    echo "  $0 start all      - Start all servers (gateway + individual)"
    echo "  $0 logs mcp-math  - Show math server logs"
}

# Main script logic
setup_env

case "${1:-}" in
    build)
        build_services
        ;;
    start)
        start_services "${2:-gateway}"
        ;;
    stop)
        stop_services
        ;;
    logs)
        show_logs "${2:-mcp-gateway}"
        ;;
    test)
        test_services
        ;;
    monitor)
        monitor_services
        ;;
    cleanup)
        cleanup
        ;;
    all)
        build_services
        start_services "gateway"
        sleep 10  # Wait for services to start
        test_services
        ;;
    *)
        usage
        exit 1
        ;;
esac
