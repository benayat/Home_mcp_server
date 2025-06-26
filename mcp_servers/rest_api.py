#!/usr/bin/env python3
"""
HTTP REST API wrapper for MCP Gateway Server.

This provides a REST API interface that implements the OpenAPI specification,
making it easy for HTTP clients to consume the MCP server functionality.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib.parse import unquote

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

from mcp_servers.gateway_server import MCPGatewayServer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for request/response validation
class BasicArithmeticRequest(BaseModel):
    operation: str = Field(..., pattern="^(add|subtract|multiply|divide)$")
    a: float
    b: float

class SolveEquationRequest(BaseModel):
    equation_type: str = Field(..., pattern="^(linear|quadratic)$")
    a: float
    b: float
    c: Optional[float] = 0

class GeometryRequest(BaseModel):
    operation: str = Field(..., pattern="^(area_circle|area_rectangle|area_triangle|pythagorean|distance|slope|midpoint)$")
    values: List[float]

class CreateChartRequest(BaseModel):
    chart_type: str = Field(..., pattern="^(line|bar|scatter|pie|histogram|box)$")
    data: Dict[str, Any]
    title: Optional[str] = None
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None

class PlotFunctionRequest(BaseModel):
    expression: str
    x_range: Optional[List[float]] = [-10, 10]
    num_points: Optional[int] = 1000
    title: Optional[str] = None

class ToolResponse(BaseModel):
    result: Any
    explanation: Optional[str] = None
    steps: Optional[List[str]] = None

class ErrorResponse(BaseModel):
    error: str
    code: int
    details: Optional[str] = None

class ServerInfo(BaseModel):
    name: str
    version: str
    description: str
    protocolVersion: str
    capabilities: Dict[str, Any]

# FastAPI app
app = FastAPI(
    title="MCP Gateway Server API",
    description="REST API interface for the Model Context Protocol (MCP) Gateway Server",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MCP server
mcp_server = MCPGatewayServer()

@app.on_event("startup")
async def startup_event():
    """Initialize the MCP server on startup."""
    logger.info("Starting MCP Gateway REST API server")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down MCP Gateway REST API server")

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.exception(f"Unhandled error in {request.url.path}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "code": 500,
            "details": str(exc)
        }
    )

# Health and info endpoints
@app.get("/health", tags=["Server"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/info", response_model=ServerInfo, tags=["Server"])
async def get_server_info():
    """Get server information and capabilities."""
    info = mcp_server.get_server_info()
    capabilities = mcp_server.get_capabilities()
    
    return ServerInfo(
        name=info["name"],
        version=info["version"],
        description=info["description"],
        protocolVersion=mcp_server.protocol_version,
        capabilities=capabilities
    )

@app.get("/tools", tags=["Server"])
async def list_tools():
    """List all available tools."""
    tools = await mcp_server.list_tools()
    return {"tools": tools}

@app.post("/tools/{tool_name}", response_model=ToolResponse, tags=["Math", "Visualization"])
async def execute_tool(tool_name: str, arguments: Dict[str, Any]):
    """Execute a specific tool with provided arguments."""
    try:
        result = await mcp_server.call_tool(tool_name, arguments)
        return ToolResponse(**result) if isinstance(result, dict) else ToolResponse(result=result)
    except Exception as e:
        logger.exception(f"Error executing tool {tool_name}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": f"Tool execution error: {str(e)}",
                "code": 400,
                "details": f"Failed to execute tool '{tool_name}'"
            }
        )

# Math tool endpoints
@app.post("/tools/basic_arithmetic", response_model=ToolResponse, tags=["Math"])
async def basic_arithmetic(request: BasicArithmeticRequest):
    """Perform basic arithmetic operations."""
    try:
        result = await mcp_server.call_tool("basic_arithmetic", request.dict())
        return ToolResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tools/solve_equations", response_model=ToolResponse, tags=["Math"])
async def solve_equations(request: SolveEquationRequest):
    """Solve linear and quadratic equations."""
    try:
        result = await mcp_server.call_tool("solve_equations", request.dict())
        return ToolResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tools/geometry", response_model=ToolResponse, tags=["Math"])
async def geometry_calculations(request: GeometryRequest):
    """Perform geometry calculations."""
    try:
        result = await mcp_server.call_tool("geometry", request.dict())
        return ToolResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tools/trigonometry", response_model=ToolResponse, tags=["Math"])
async def trigonometry(function: str, angle: float, unit: str = "radians"):
    """Perform trigonometric calculations."""
    try:
        arguments = {"function": function, "angle": angle, "unit": unit}
        result = await mcp_server.call_tool("trigonometry", arguments)
        return ToolResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tools/advanced_operations", response_model=ToolResponse, tags=["Math"])
async def advanced_operations(operation: str, value: float, extra_param: Optional[float] = 0):
    """Perform advanced mathematical operations."""
    try:
        arguments = {"operation": operation, "value": value, "extra_param": extra_param}
        result = await mcp_server.call_tool("advanced_operations", arguments)
        return ToolResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tools/evaluate_expression", response_model=ToolResponse, tags=["Math"])
async def evaluate_expression(expression: str):
    """Safely evaluate mathematical expressions."""
    try:
        result = await mcp_server.call_tool("evaluate_expression", {"expression": expression})
        return ToolResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Visualization tool endpoints
@app.post("/tools/create_chart", response_model=ToolResponse, tags=["Visualization"])
async def create_chart(request: CreateChartRequest):
    """Create various types of charts and graphs."""
    try:
        result = await mcp_server.call_tool("create_chart", request.dict())
        return ToolResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tools/plot_function", response_model=ToolResponse, tags=["Visualization"])
async def plot_function(request: PlotFunctionRequest):
    """Plot mathematical functions."""
    try:
        result = await mcp_server.call_tool("plot_function", request.dict())
        return ToolResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tools/visualize_geometry", response_model=ToolResponse, tags=["Visualization"])
async def visualize_geometry(shape_type: str, parameters: Dict[str, Any], title: Optional[str] = None):
    """Visualize geometric shapes."""
    try:
        arguments = {"shape_type": shape_type, "parameters": parameters}
        if title:
            arguments["title"] = title
        result = await mcp_server.call_tool("visualize_geometry", arguments)
        return ToolResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/tools/create_statistics_chart", response_model=ToolResponse, tags=["Visualization"])
async def create_statistics_chart(data: List[float], chart_type: str = "all", title: Optional[str] = None):
    """Create statistical visualizations."""
    try:
        arguments = {"data": data, "chart_type": chart_type}
        if title:
            arguments["title"] = title
        result = await mcp_server.call_tool("create_statistics_chart", arguments)
        return ToolResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Resource endpoints
@app.get("/resources", tags=["Resources"])
async def list_resources():
    """List all available educational resources."""
    resources = await mcp_server.list_resources()
    return {"resources": resources}

@app.get("/resources/{resource_id:path}", tags=["Resources"])
async def get_resource(resource_id: str):
    """Get content of a specific educational resource."""
    try:
        # URL decode the resource ID
        decoded_id = unquote(resource_id)
        result = await mcp_server.read_resource(decoded_id)
        return result
    except Exception as e:
        logger.exception(f"Error reading resource {resource_id}")
        raise HTTPException(
            status_code=404,
            detail={
                "error": f"Resource not found: {resource_id}",
                "code": 404,
                "details": str(e)
            }
        )

# Additional utility endpoints
@app.get("/tools/math", tags=["Math"])
async def list_math_tools():
    """List only mathematical tools."""
    all_tools = await mcp_server.list_tools()
    math_keywords = ['arithmetic', 'solve', 'geometry', 'trigonometry', 'logarithms', 
                     'fractions', 'percentage', 'evaluate', 'explain', 'theory', 'advanced']
    
    math_tools = [
        tool for tool in all_tools 
        if any(keyword in tool['name'] for keyword in math_keywords)
    ]
    return {"tools": math_tools}

@app.get("/tools/visualization", tags=["Visualization"])
async def list_visualization_tools():
    """List only visualization tools."""
    all_tools = await mcp_server.list_tools()
    viz_keywords = ['chart', 'plot', 'visualize', 'statistics']
    
    viz_tools = [
        tool for tool in all_tools 
        if any(keyword in tool['name'] for keyword in viz_keywords)
    ]
    return {"tools": viz_tools}

def main():
    """Main entry point for the REST API server."""
    uvicorn.run(
        "mcp_servers.rest_api:app",
        host="0.0.0.0",
        port=8080,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
