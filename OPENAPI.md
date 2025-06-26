# OpenAPI & REST API Integration

This document describes the OpenAPI specification and REST API interface for the MCP Gateway Server, making it easy to consume the server functionality via standard HTTP requests.

## 🌟 Overview

The MCP Gateway Server now provides **two interfaces**:

1. **MCP Protocol** (stdin/stdout) - For MCP clients
2. **REST API** (HTTP) - For standard web applications and tools

The REST API implements a comprehensive OpenAPI 3.0 specification, providing:
- ✅ **Interactive API documentation** (Swagger UI)
- ✅ **Standard HTTP endpoints** for all tools
- ✅ **Request/response validation** with Pydantic
- ✅ **CORS support** for web applications
- ✅ **Health checks** and monitoring
- ✅ **Error handling** with proper HTTP status codes

## 📋 OpenAPI Specification

The complete OpenAPI specification is available in `openapi.yaml` and includes:

- **15 tool endpoints** (math + visualization)
- **Educational resources** access
- **Server information** and health checks
- **Request/response schemas** with validation
- **Examples** for all endpoints

### Key Features:
- **OpenAPI 3.0.3** compliant
- **Comprehensive schemas** for all data types
- **Rich documentation** with examples
- **Error response** standardization
- **Multiple server** configurations

## 🚀 Running the REST API

### Option 1: Direct Python
```bash
# Start the REST API server
python -m uvicorn mcp_servers.rest_api:app --host 0.0.0.0 --port 8080

# Or use the convenience script
./scripts/start-rest-api.sh

# Or use Make
make run-rest-api
```

### Option 2: Docker
```bash
# Run REST API in Docker
docker-compose --profile rest-api up -d

# Or use Make
make docker-rest-api
```

### Option 3: Console Command (after installation)
```bash
# Install with REST API support
pip install -e ".[api]"

# Run the server
mcp-rest-api
```

## 📚 API Documentation

Once the server is running, access the interactive documentation:

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc  
- **OpenAPI JSON**: http://localhost:8080/openapi.json
- **Raw YAML**: ./openapi.yaml

## 🔗 API Endpoints

### Server Management
- `GET /health` - Health check
- `GET /info` - Server information and capabilities
- `GET /tools` - List all available tools

### Math Tools
- `POST /tools/basic_arithmetic` - Basic arithmetic operations
- `POST /tools/solve_equations` - Solve linear/quadratic equations
- `POST /tools/geometry` - Geometric calculations
- `POST /tools/trigonometry` - Trigonometric functions
- `POST /tools/advanced_operations` - Advanced math operations
- `POST /tools/evaluate_expression` - Expression evaluation

### Visualization Tools
- `POST /tools/create_chart` - Create charts and graphs
- `POST /tools/plot_function` - Plot mathematical functions
- `POST /tools/visualize_geometry` - Visualize geometric shapes
- `POST /tools/create_statistics_chart` - Statistical visualizations

### Educational Resources
- `GET /resources` - List all educational resources
- `GET /resources/{resource_id}` - Get specific resource content

### Utility Endpoints
- `GET /tools/math` - List only math tools
- `GET /tools/visualization` - List only visualization tools

## 💡 Usage Examples

### Using curl

```bash
# Health check
curl http://localhost:8080/health

# Basic arithmetic
curl -X POST http://localhost:8080/tools/basic_arithmetic \
  -H "Content-Type: application/json" \
  -d '{"operation": "add", "a": 15, "b": 27}'

# Solve quadratic equation
curl -X POST http://localhost:8080/tools/solve_equations \
  -H "Content-Type: application/json" \
  -d '{"equation_type": "quadratic", "a": 1, "b": -5, "c": 6}'

# Create a line chart
curl -X POST http://localhost:8080/tools/create_chart \
  -H "Content-Type: application/json" \
  -d '{
    "chart_type": "line",
    "data": {"x": [1,2,3,4,5], "y": [1,4,9,16,25]},
    "title": "Square Function",
    "xlabel": "x",
    "ylabel": "x²"
  }'

# List educational resources
curl http://localhost:8080/resources

# Get elementary math concepts
curl "http://localhost:8080/resources/math%3A%2F%2Fconcepts%2Felementary"
```

### Using Python (requests)

```python
import requests

base_url = "http://localhost:8080"

# Health check
response = requests.get(f"{base_url}/health")
print(response.json())

# Basic arithmetic
response = requests.post(f"{base_url}/tools/basic_arithmetic", json={
    "operation": "multiply",
    "a": 7,
    "b": 6
})
result = response.json()
print(f"7 × 6 = {result['result']}")

# Solve equation
response = requests.post(f"{base_url}/tools/solve_equations", json={
    "equation_type": "quadratic",
    "a": 1,
    "b": -5,
    "c": 6
})
result = response.json()
print(f"Solutions: {result['result']}")
```

### Using Python (aiohttp async)

```python
import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        # Health check
        async with session.get("http://localhost:8080/health") as response:
            health = await response.json()
            print(f"Status: {health['status']}")
        
        # Math operation
        async with session.post("http://localhost:8080/tools/basic_arithmetic", 
                              json={"operation": "add", "a": 10, "b": 5}) as response:
            result = await response.json()
            print(f"10 + 5 = {result['result']}")

asyncio.run(main())
```

### Using JavaScript (fetch)

```javascript
// Health check
fetch('http://localhost:8080/health')
  .then(response => response.json())
  .then(data => console.log('Health:', data.status));

// Basic arithmetic
fetch('http://localhost:8080/tools/basic_arithmetic', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    operation: 'multiply',
    a: 8,
    b: 7
  })
})
.then(response => response.json())
.then(data => console.log('8 × 7 =', data.result));

// Create chart
fetch('http://localhost:8080/tools/create_chart', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    chart_type: 'line',
    data: {
      x: [1, 2, 3, 4, 5],
      y: [2, 4, 6, 8, 10]
    },
    title: 'Linear Function'
  })
})
.then(response => response.json())
.then(data => console.log('Chart:', data.result));
```

## 🏗️ Request/Response Schemas

### Request Examples

#### Basic Arithmetic
```json
{
  "operation": "add|subtract|multiply|divide",
  "a": 15,
  "b": 27
}
```

#### Solve Equations
```json
{
  "equation_type": "linear|quadratic",
  "a": 1,
  "b": -5,
  "c": 6
}
```

#### Create Chart
```json
{
  "chart_type": "line|bar|scatter|pie|histogram|box",
  "data": {
    "x": [1, 2, 3, 4, 5],
    "y": [2, 4, 6, 8, 10]
  },
  "title": "Chart Title",
  "xlabel": "X Label",
  "ylabel": "Y Label"
}
```

### Response Format

All successful responses follow this structure:

```json
{
  "result": "actual_result_data",
  "explanation": "Human-readable explanation",
  "steps": ["step1", "step2", "step3"]
}
```

### Error Responses

```json
{
  "error": "Error description",
  "code": 400,
  "details": "Additional error details"
}
```

## 🔧 Configuration

### Environment Variables

- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8080)
- `LOG_LEVEL` - Logging level (default: INFO)
- `WORKERS` - Number of workers (default: 1)

### CORS Configuration

The server includes CORS middleware configured for development. For production:

```python
# Update CORS settings in rest_api.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 🚨 Error Handling

The REST API provides comprehensive error handling:

- **400 Bad Request** - Invalid input parameters
- **404 Not Found** - Tool or resource not found
- **422 Unprocessable Entity** - Validation errors
- **500 Internal Server Error** - Server errors

All errors include:
- Error message
- HTTP status code  
- Additional details when available

## 📊 Monitoring & Health Checks

### Health Check Endpoint
```bash
curl http://localhost:8080/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-01T12:00:00Z",
  "version": "1.0.0"
}
```

### Docker Health Checks

The Docker container includes built-in health checks:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
```

## 🔒 Security Considerations

- **Input validation** with Pydantic schemas
- **CORS configuration** for web security
- **Rate limiting** (implement as needed)
- **Authentication** (implement as needed)
- **HTTPS** (configure reverse proxy)

## 🚀 Production Deployment

For production environments:

1. **Use a reverse proxy** (nginx, Apache)
2. **Configure HTTPS** with SSL certificates
3. **Set up rate limiting**
4. **Configure proper CORS** origins
5. **Implement authentication** if needed
6. **Use multiple workers** for scalability
7. **Set up monitoring** and logging

### Example nginx configuration:

```nginx
server {
    listen 443 ssl;
    server_name api.yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📈 Performance

The FastAPI-based REST API provides:

- **High performance** with async/await
- **Automatic validation** with minimal overhead
- **JSON serialization** optimization
- **Connection pooling** for database operations
- **Horizontal scaling** with multiple workers

## 🔄 Migration from MCP Protocol

If you're currently using the MCP protocol directly, you can migrate to the REST API:

### Before (MCP Protocol)
```python
from mcp_servers.gateway_server import MCPGatewayServer
import asyncio

async def main():
    server = MCPGatewayServer()
    result = await server.call_tool("basic_arithmetic", {
        "operation": "add", "a": 5, "b": 3
    })
    print(result)

asyncio.run(main())
```

### After (REST API)
```python
import requests

response = requests.post("http://localhost:8080/tools/basic_arithmetic", 
                        json={"operation": "add", "a": 5, "b": 3})
result = response.json()
print(result)
```

## 🎯 Integration Examples

The REST API makes it easy to integrate with:

- **Web applications** (JavaScript/TypeScript)
- **Mobile apps** (React Native, Flutter)
- **Data science tools** (Jupyter, Python scripts)
- **Business applications** (Excel, Power BI)
- **API testing tools** (Postman, Insomnia)
- **CI/CD pipelines** (automated testing)

See `examples/rest_api_client.py` for a complete Python client implementation.

---

**The MCP Gateway Server now provides both MCP protocol and REST API interfaces, making it accessible to any application that can make HTTP requests!** 🎉
