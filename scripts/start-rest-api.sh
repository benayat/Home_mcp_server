#!/bin/bash

# REST API Server startup script for MCP Gateway Server
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-8080}"
WORKERS="${WORKERS:-1}"
LOG_LEVEL="${LOG_LEVEL:-info}"

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

# Check dependencies
check_dependencies() {
    log_info "Checking dependencies..."
    
    # Check if Python packages are installed
    python3 -c "
import sys
try:
    import fastapi
    import uvicorn
    import pydantic
    print('✅ FastAPI dependencies available')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    print('Please install: pip install fastapi uvicorn[standard] pydantic')
    sys.exit(1)

# Check MCP server
try:
    from mcp_servers.gateway_server import MCPGatewayServer
    print('✅ MCP Gateway Server available')
except ImportError as e:
    print(f'❌ MCP server not available: {e}')
    sys.exit(1)
"
    
    if [ $? -ne 0 ]; then
        log_error "Dependency check failed"
        exit 1
    fi
}

# Start the server
start_server() {
    log_info "Starting MCP Gateway REST API Server..."
    log_info "Configuration:"
    log_info "  Host: $HOST"
    log_info "  Port: $PORT"
    log_info "  Workers: $WORKERS"
    log_info "  Log Level: $LOG_LEVEL"
    
    # Start the server
    python3 -m uvicorn mcp_servers.rest_api:app \
        --host "$HOST" \
        --port "$PORT" \
        --workers "$WORKERS" \
        --log-level "$LOG_LEVEL" \
        --access-log
}

# Show server info
show_info() {
    log_success "MCP Gateway REST API Server is starting!"
    echo ""
    echo "📋 API Documentation:"
    echo "  Swagger UI: http://${HOST}:${PORT}/docs"
    echo "  ReDoc:      http://${HOST}:${PORT}/redoc"
    echo "  OpenAPI:    http://${HOST}:${PORT}/openapi.json"
    echo ""
    echo "🔗 API Endpoints:"
    echo "  Health:     GET  http://${HOST}:${PORT}/health"
    echo "  Info:       GET  http://${HOST}:${PORT}/info"
    echo "  Tools:      GET  http://${HOST}:${PORT}/tools"
    echo "  Execute:    POST http://${HOST}:${PORT}/tools/{tool_name}"
    echo "  Resources:  GET  http://${HOST}:${PORT}/resources"
    echo ""
    echo "🧮 Math Examples:"
    echo "  curl -X POST http://${HOST}:${PORT}/tools/basic_arithmetic \\"
    echo "    -H 'Content-Type: application/json' \\"
    echo "    -d '{\"operation\": \"add\", \"a\": 15, \"b\": 27}'"
    echo ""
    echo "📊 Visualization Examples:"
    echo "  curl -X POST http://${HOST}:${PORT}/tools/create_chart \\"
    echo "    -H 'Content-Type: application/json' \\"
    echo "    -d '{\"chart_type\": \"line\", \"data\": {\"x\": [1,2,3], \"y\": [1,4,9]}}'"
    echo ""
}

# Usage
usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -h, --host HOST      Host to bind to (default: 0.0.0.0)"
    echo "  -p, --port PORT      Port to listen on (default: 8080)"
    echo "  -w, --workers N      Number of workers (default: 1)"
    echo "  -l, --log-level LVL  Log level (default: info)"
    echo "  --help               Show this help message"
    echo ""
    echo "Environment variables:"
    echo "  HOST, PORT, WORKERS, LOG_LEVEL"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--host)
            HOST="$2"
            shift 2
            ;;
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -w|--workers)
            WORKERS="$2"
            shift 2
            ;;
        -l|--log-level)
            LOG_LEVEL="$2"
            shift 2
            ;;
        --help)
            usage
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Main execution
log_info "🚀 MCP Gateway REST API Server"
log_info "================================"

check_dependencies
show_info
start_server
