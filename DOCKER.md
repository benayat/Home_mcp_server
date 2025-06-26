# Docker Deployment Guide

This guide covers deploying the MCP Gateway Server using Docker for production environments.

## 🐳 Overview

The MCP Gateway Server is containerized using Docker with the following features:

- **Multi-stage build** for optimized image size
- **Security hardened** with non-root user
- **Health checks** for monitoring
- **Resource limits** for stability  
- **Volume mounts** for data persistence
- **Environment configuration** support

## 📋 Prerequisites

- Docker Engine 20.10+ 
- Docker Compose 2.0+ (optional)
- At least 1GB RAM available
- 2GB disk space for images and data

## 🚀 Quick Start

### Option 1: Docker (Simple)

```bash
# Build and run the gateway server
./scripts/docker-deploy.sh all
```

### Option 2: Docker Compose (Recommended)

```bash
# Start the gateway server
./scripts/docker-compose-deploy.sh all
```

## 🔧 Manual Docker Commands

### Build Image

```bash
# Build the image
docker build -t mcp-gateway-server:latest .

# Build with custom version
docker build --build-arg VERSION=1.0.0 -t mcp-gateway-server:1.0.0 .
```

### Run Container

```bash
# Run gateway server
docker run -d \
  --name mcp-gateway-server \
  --restart unless-stopped \
  -v $(pwd)/logs:/app/logs:rw \
  -v $(pwd)/plots:/app/plots:rw \
  -e LOG_LEVEL=INFO \
  mcp-gateway-server:latest

# Run with custom configuration
docker run -d \
  --name mcp-gateway-server \
  --restart unless-stopped \
  --memory=1g \
  --cpus=0.5 \
  -v $(pwd)/logs:/app/logs:rw \
  -v $(pwd)/plots:/app/plots:rw \
  -e LOG_LEVEL=DEBUG \
  -e MCP_SERVER_TYPE=gateway \
  mcp-gateway-server:latest
```

### Manage Container

```bash
# Check status
docker ps --filter name=mcp-gateway-server

# View logs
docker logs -f mcp-gateway-server

# Execute commands inside container
docker exec -it mcp-gateway-server bash

# Stop container
docker stop mcp-gateway-server

# Remove container
docker rm mcp-gateway-server
```

## 🏗️ Docker Compose Deployment

### Basic Configuration

```yaml
# docker-compose.yml
version: '3.8'
services:
  mcp-gateway:
    image: mcp-gateway-server:latest
    container_name: mcp-gateway-server
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs:rw
      - ./plots:/app/plots:rw
    environment:
      - LOG_LEVEL=INFO
      - MCP_SERVER_TYPE=gateway
```

### Production Configuration

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  mcp-gateway:
    image: mcp-gateway-server:latest
    container_name: mcp-gateway-server
    restart: unless-stopped
    
    # Resource limits
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.1'
    
    # Volumes
    volumes:
      - mcp-logs:/app/logs:rw
      - mcp-plots:/app/plots:rw
    
    # Environment
    environment:
      - LOG_LEVEL=INFO
      - MCP_SERVER_TYPE=gateway
    
    # Health check
    healthcheck:
      test: ["CMD", "python", "-c", "from mcp_servers.gateway_server import MCPGatewayServer; print('healthy')"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  mcp-logs:
  mcp-plots:
```

### Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f mcp-gateway

# Scale services (if needed)
docker-compose up -d --scale mcp-gateway=2

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down --volumes
```

## 🔍 Monitoring & Health Checks

### Container Health

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' mcp-gateway-server

# View health check logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' mcp-gateway-server
```

### Resource Usage

```bash
# Monitor resource usage
docker stats mcp-gateway-server

# View detailed resource info
docker exec mcp-gateway-server top
```

### Application Logs

```bash
# View application logs
docker logs mcp-gateway-server

# Follow logs in real-time
docker logs -f mcp-gateway-server

# View last 100 lines
docker logs --tail 100 mcp-gateway-server
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `MCP_SERVER_TYPE` | `gateway` | Server type identifier |
| `PYTHONUNBUFFERED` | `1` | Disable Python output buffering |

### Volume Mounts

| Host Path | Container Path | Purpose |
|-----------|----------------|---------|
| `./logs` | `/app/logs` | Application logs |
| `./plots` | `/app/plots` | Generated visualization files |

### Resource Limits

Recommended resource limits:

- **Memory**: 1GB limit, 256MB reservation
- **CPU**: 0.5 CPU limit, 0.1 CPU reservation
- **Storage**: 2GB for images and data

## 🚨 Troubleshooting

### Common Issues

1. **Container won't start**
   ```bash
   # Check logs
   docker logs mcp-gateway-server
   
   # Check image
   docker images | grep mcp-gateway-server
   ```

2. **Permission errors**
   ```bash
   # Fix volume permissions
   sudo chown -R 1000:1000 ./logs ./plots
   ```

3. **Resource constraints**
   ```bash
   # Check available resources
   docker system df
   docker system prune -f
   ```

4. **Health check failures**
   ```bash
   # Test manually
   docker exec mcp-gateway-server python -c "from mcp_servers.gateway_server import MCPGatewayServer; print('OK')"
   ```

### Debugging

```bash
# Interactive shell
docker exec -it mcp-gateway-server bash

# Test functionality
docker exec mcp-gateway-server python -c "
import asyncio
from mcp_servers.gateway_server import MCPGatewayServer

async def test():
    server = MCPGatewayServer()
    tools = await server.list_tools()
    print(f'Tools: {len(tools)}')

asyncio.run(test())
"
```

## 🔒 Security Considerations

- Container runs as non-root user (`mcpuser`)
- Read-only filesystem except for mounted volumes
- No unnecessary packages in final image
- Regular security updates for base image
- Resource limits prevent resource exhaustion

## 📦 Multi-Architecture Support

Build for multiple architectures:

```bash
# Enable buildx
docker buildx create --use

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t mcp-gateway-server:latest \
  --push .
```

## 🚀 Production Deployment

For production environments:

1. Use Docker Compose with resource limits
2. Set up log rotation
3. Configure health checks
4. Use secrets management for sensitive data
5. Set up monitoring and alerting
6. Regular backups of volumes
7. Update strategy for zero-downtime deployments

## 📚 Additional Resources

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Container Security](https://docs.docker.com/engine/security/)
