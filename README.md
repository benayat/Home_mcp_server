# MCP Servers

A unified Model Context Protocol (MCP) server system providing comprehensive mathematical calculations and data visualization capabilities through a single, easy-to-use interface.

## 🌟 Gateway Server (Recommended)

**Use the Gateway Server for the best client experience** - it provides all mathematical and visualization tools through a single MCP connection, eliminating the need to manage multiple server connections.

### Key Benefits
- ✅ **15 unified tools** (11 math + 4 visualization)
- ✅ **7 educational resources**
- ✅ **Single connection point** - easier client integration
- ✅ **Full MCP protocol compliance**
- ✅ **Rich explanations** with step-by-step solutions

## Overview

This package provides three MCP servers:

- **🎯 Gateway Server** (`mcp-gateway-server`): **Recommended** - All math and visualization tools in one unified interface
- **Math Server** (`mcp-math-server`): Mathematical calculations covering elementary to high school topics  
- **Visualization Server** (`mcp-visualization-server`): Data visualization and chart generation tools

## 📚 Documentation

- **[MCP Client Guide](MCP_CLIENT_GUIDE.md)** - Complete guide for consuming the MCP servers via the MCP protocol
- **[API Documentation](API.md)** - Detailed API reference for all servers and tools
- **[Docker Guide](DOCKER.md)** - Docker deployment and container management
- **[OpenAPI Guide](OPENAPI.md)** - REST API interface and OpenAPI 3.0 specification

## Features

### Gateway Server (All Features Combined)
All math and visualization features are available through the gateway server:

### Math Tools
- Basic arithmetic operations (add, subtract, multiply, divide)
- Advanced operations (power, square root, factorial, absolute value)
- Number theory (GCD, LCM, prime factorization, primality testing)
- Equation solving (linear and quadratic equations)
- Geometry calculations (areas, distances, slopes, midpoints)
- Trigonometric functions (sin, cos, tan)
- Logarithmic functions (natural log, common log)
- Fraction operations (simplify, convert to/from decimal)
- Percentage calculations
- Expression evaluation
- Mathematical concept explanations

### Visualization Tools
- Chart creation (line, bar, scatter, pie, histogram, box plots)
- Mathematical function plotting
- Statistical visualizations
- Geometric shape visualization
- Data analysis charts

## Installation

```bash
pip install -e .
```

For development:
```bash
pip install -e ".[dev]"
```

## Quick Start

### Gateway Server (Recommended)

The gateway server provides all functionality through a single connection:

## Quick Start

### Gateway Server (Recommended)

The gateway server provides all functionality through a single connection:

```bash
# Run the unified gateway server
python -m mcp_servers.gateway_server

# Or after installation:
mcp-gateway-server
```

### Individual Servers (If Needed)

```bash
# Math server only
python -m mcp_servers.math_server
# Or: mcp-math-server

# Visualization server only
python -m mcp_servers.visualization_server  
# Or: mcp-visualization-server
```

### Integration with MCP Clients

**Recommended**: Use the gateway server for simplified client configuration:

```json
{
  "mcpServers": {
    "gateway": {
      "command": "mcp-gateway-server"
    }
  }
}
```

**Alternative**: Individual servers (if you need only specific functionality):

```json
{
  "mcpServers": {
    "math": {
      "command": "mcp-math-server"
    },
    "visualization": {
      "command": "mcp-visualization-server"
    }
  }
}
```

### Building Custom MCP Clients

For developers building custom MCP clients, see the **[MCP Client Guide](MCP_CLIENT_GUIDE.md)** for:
- Complete MCP protocol details and JSON-RPC examples
- All 15 available tools with input/output schemas
- Usage patterns for educational and data analysis workflows  
- Client implementation examples in Python and JavaScript
- Best practices, error handling, and troubleshooting
    "visualization": {
      "command": "mcp-visualization-server"
    }
  }
}
```

### Example Tool Calls

#### Gateway Server Examples (All Tools Available)

**Basic Math:**
```json
{
  "name": "basic_arithmetic",
  "arguments": {
    "operation": "add",
    "a": 15,
    "b": 27
  }
}
```

**Equation Solving:**
```json
{
  "name": "solve_equations",
  "arguments": {
    "equation_type": "quadratic",
    "a": 1,
    "b": -5,
    "c": 6
  }
}
```

**Visualization:**
```json
{
  "name": "create_chart",
  "arguments": {
    "chart_type": "line",
    "data": {
      "x": [1, 2, 3, 4, 5],
      "y": [2, 4, 6, 8, 10]
    },
    "title": "Linear Function"
  }
}
```
    "b": 27
  }
}
```

```json
{
  "name": "solve_equations",
  "arguments": {
    "equation_type": "quadratic",
    "a": 1,
    "b": -5,
    "c": 6
  }
}
```

```json
{
  "name": "geometry",
  "arguments": {
    "operation": "area_circle",
    "values": [5]
  }
}
```

#### Visualization Server Examples

```json
{
  "name": "create_chart",
  "arguments": {
    "chart_type": "line",
    "data": {
      "x": [1, 2, 3, 4, 5],
      "y": [2, 4, 6, 8, 10]
    },
    "title": "Linear Function",
    "xlabel": "x",
    "ylabel": "y"
  }
}
```

## Development

### Project Structure

```
mcp_servers/
├── __init__.py           # Package initialization
├── math_server.py        # Math MCP server
├── visualization_server.py # Visualization MCP server
└── utils/               # Shared utilities
    ├── __init__.py
    ├── base_server.py   # Base MCP server class
    ├── math_utils.py    # Math calculation utilities
    └── viz_utils.py     # Visualization utilities
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black mcp_servers/
isort mcp_servers/
```

### Type Checking

```bash
mypy mcp_servers/
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## Protocol Compliance

These servers implement the Model Context Protocol (MCP) specification:
- Protocol version: 2024-11-05
- Communication: stdin/stdout JSON-RPC
- Capabilities: tools, resources (math server only)
- Error handling: Standard JSON-RPC error codes

## 🐳 Docker Deployment

For production deployment, the MCP Gateway Server is available as a Docker container.

### Quick Start with Docker

```bash
# Build and run the gateway server
./scripts/docker-deploy.sh all

# Or using Docker Compose
./scripts/docker-compose-deploy.sh all
```

### Docker Commands

```bash
# Build the Docker image
docker build -t mcp-gateway-server .

# Run the container
docker run -d \
  --name mcp-gateway-server \
  --restart unless-stopped \
  -v $(pwd)/logs:/app/logs:rw \
  -v $(pwd)/plots:/app/plots:rw \
  mcp-gateway-server

# Check container status
docker ps --filter name=mcp-gateway-server

# View logs
docker logs -f mcp-gateway-server

# Test functionality
docker exec mcp-gateway-server python -c "
from mcp_servers.gateway_server import MCPGatewayServer
import asyncio
asyncio.run(MCPGatewayServer().list_tools())
"
```

### Docker Compose (Recommended)

```bash
# Start gateway server
docker-compose up -d

# Start all servers (gateway + individual)
docker-compose --profile individual-servers up -d

# Monitor services
docker-compose ps

# View logs
docker-compose logs -f mcp-gateway

# Stop services
docker-compose down
```

### Production Configuration

The Docker container includes:
- ✅ **Multi-stage build** for optimized image size
- ✅ **Non-root user** for security
- ✅ **Health checks** for monitoring
- ✅ **Resource limits** for stability
- ✅ **Volume mounts** for persistence
- ✅ **Environment configuration** support

## 🌐 REST API Interface

For easy integration with web applications and standard HTTP clients, the gateway server also provides a **REST API interface** with full OpenAPI 3.0 specification.

### Quick Start REST API

```bash
# Start the REST API server
./scripts/start-rest-api.sh

# Or with Docker
make docker-rest-api

# Access interactive documentation
# Swagger UI: http://localhost:8080/docs
# ReDoc: http://localhost:8080/redoc
```

### REST API Examples

```bash
# Health check
curl http://localhost:8080/health

# Basic arithmetic via REST
curl -X POST http://localhost:8080/tools/basic_arithmetic \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 15, "b": 27}'

# Create a chart via REST  
curl -X POST http://localhost:8080/tools/create_chart \
  -H "Content-Type: application/json" \
  -d '{"chart_type": "line", "data": {"x": [1,2,3], "y": [1,4,9]}}'
```

See [`OPENAPI.md`](OPENAPI.md) for complete REST API documentation.
