"""
MCP (Model Context Protocol) Servers

This package contains MCP servers for mathematical calculations and data visualization.
Each server provides specialized tools and capabilities:

- math_server: Mathematical calculations, equation solving, and concept explanations
- visualization_server: Chart generation, data visualization, and statistical plots

All servers follow MCP protocol standards and can be run independently as standalone servers.
"""

__version__ = "1.0.0"

from .math_server import MathServer
from .visualization_server import VisualizationServer

__all__ = ["MathServer", "VisualizationServer"]

# Available MCP servers
AVAILABLE_SERVERS = {
    "math": {
        "class": MathServer,
        "description": "Mathematical calculations, equation solving, and concept explanations",
        "capabilities": ["arithmetic", "algebra", "geometry", "trigonometry", "statistics"]
    },
    "visualization": {
        "class": VisualizationServer,
        "description": "Data visualization, chart generation, and statistical plots",
        "capabilities": ["charts", "plots", "functions", "geometry_viz", "statistics_viz"]
    }
}


def get_server_info(server_name: str) -> dict:
    """Get information about a specific MCP server."""
    return AVAILABLE_SERVERS.get(server_name, {})


def list_available_servers() -> list:
    """List all available MCP servers."""
    return list(AVAILABLE_SERVERS.keys())


def create_server(server_name: str):
    """Create a server instance by name."""
    if server_name not in AVAILABLE_SERVERS:
        raise ValueError(f"Unknown server: {server_name}")
    
    server_class = AVAILABLE_SERVERS[server_name]["class"]
    return server_class()
