# Multi-stage Docker build for MCP Gateway Server
FROM python:3.11-slim as builder

# Set build arguments
ARG BUILD_DATE
ARG VERSION=1.0.0

# Add metadata
LABEL maintainer="MCP Servers" \
      description="Unified MCP Gateway Server for Mathematics and Visualization" \
      version="${VERSION}" \
      build-date="${BUILD_DATE}"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    MCP_SERVER_TYPE=gateway

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # For matplotlib backend
    libfreetype6-dev \
    libpng-dev \
    # For numerical computations
    libblas3 \
    liblapack3 \
    # Cleanup
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

# Create app directory and set ownership
WORKDIR /app
RUN chown -R mcpuser:mcpuser /app

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=mcpuser:mcpuser . .

# Install the package
RUN pip install -e .

# Switch to non-root user
USER mcpuser

# Create directory for logs and plots (if needed)
RUN mkdir -p /app/logs /app/plots

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.path.insert(0, '.'); from mcp_servers.gateway_server import MCPGatewayServer; print('healthy')" || exit 1

# Expose port for REST API
EXPOSE 8080

# Default command - run the gateway server (MCP protocol)
# To run REST API: CMD ["python", "-m", "uvicorn", "mcp_servers.rest_api:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["python", "-m", "mcp_servers.gateway_server"]
