#!/usr/bin/env python3
"""
MCP Visualization Server

A comprehensive visualization server implementing the Model Context Protocol (MCP).
Provides data visualization, chart generation, and statistical plotting capabilities.
"""

import asyncio
import logging
from typing import Any, Dict, List

from .utils.base_server import BaseMCPServer, MCPError
from .utils.viz_utils import VisualizationHelper

logger = logging.getLogger(__name__)


class VisualizationServer(BaseMCPServer):
    """MCP server for data visualization and chart generation."""
    
    def __init__(self):
        super().__init__("mcp-visualization-server", "1.0.0")
        self.viz_helper = VisualizationHelper()
        
    def get_server_info(self) -> Dict[str, Any]:
        """Return server information."""
        return {
            "name": self.name,
            "version": self.version,
            "description": "Data visualization and chart generation server"
        }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return server capabilities."""
        return {
            "tools": {"listChanged": False}
        }
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Return list of available visualization tools."""
        return [
            {
                "name": "create_chart",
                "description": "Create various types of charts and graphs",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "chart_type": {
                            "type": "string",
                            "enum": ["line", "bar", "scatter", "pie", "histogram", "box"],
                            "description": "Type of chart to create"
                        },
                        "data": {
                            "type": "object",
                            "description": "Data for the chart (x, y values or categories)"
                        },
                        "title": {
                            "type": "string",
                            "description": "Chart title"
                        },
                        "xlabel": {
                            "type": "string",
                            "description": "X-axis label"
                        },
                        "ylabel": {
                            "type": "string",
                            "description": "Y-axis label"
                        }
                    },
                    "required": ["chart_type", "data"]
                }
            },
            {
                "name": "plot_function",
                "description": "Plot mathematical functions",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression to plot (e.g., 'x**2', 'sin(x)')"
                        },
                        "x_range": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 2,
                            "maxItems": 2,
                            "description": "Range for x values [min, max]",
                            "default": [-10, 10]
                        },
                        "num_points": {
                            "type": "integer",
                            "description": "Number of points to plot",
                            "default": 1000,
                            "minimum": 10,
                            "maximum": 10000
                        },
                        "title": {
                            "type": "string",
                            "description": "Plot title"
                        }
                    },
                    "required": ["expression"]
                }
            },
            {
                "name": "create_statistics_chart",
                "description": "Create statistical visualizations for data analysis",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "data": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Numerical data for statistical analysis"
                        },
                        "chart_type": {
                            "type": "string",
                            "enum": ["all"],
                            "description": "Type of statistical visualization",
                            "default": "all"
                        },
                        "title": {
                            "type": "string",
                            "description": "Chart title"
                        }
                    },
                    "required": ["data"]
                }
            },
            {
                "name": "visualize_geometry",
                "description": "Visualize geometric shapes",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "shape_type": {
                            "type": "string",
                            "enum": ["circle", "rectangle", "triangle", "polygon"],
                            "description": "Type of geometric shape to visualize"
                        },
                        "parameters": {
                            "type": "object",
                            "description": "Shape-specific parameters (e.g., radius for circle, vertices for polygon)"
                        },
                        "title": {
                            "type": "string",
                            "description": "Visualization title"
                        }
                    },
                    "required": ["shape_type", "parameters"]
                }
            }
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a visualization tool with given arguments."""
        
        try:
            if name == "create_chart":
                chart_type = arguments["chart_type"]
                data = arguments["data"]
                title = arguments.get("title")
                xlabel = arguments.get("xlabel")
                ylabel = arguments.get("ylabel")
                
                return self.viz_helper.create_chart(
                    chart_type=chart_type,
                    data=data,
                    title=title,
                    xlabel=xlabel,
                    ylabel=ylabel
                )
                
            elif name == "plot_function":
                expression = arguments["expression"]
                x_range = tuple(arguments.get("x_range", [-10, 10]))
                num_points = arguments.get("num_points", 1000)
                title = arguments.get("title")
                
                return self.viz_helper.plot_function(
                    expression=expression,
                    x_range=x_range,
                    num_points=num_points,
                    title=title
                )
                
            elif name == "create_statistics_chart":
                data = arguments["data"]
                chart_type = arguments.get("chart_type", "all")
                title = arguments.get("title")
                
                return self.viz_helper.create_statistics_chart(
                    data=data,
                    chart_type=chart_type,
                    title=title
                )
                
            elif name == "visualize_geometry":
                shape_type = arguments["shape_type"]
                parameters = arguments["parameters"]
                title = arguments.get("title")
                
                return self.viz_helper.visualize_geometry(
                    shape_type=shape_type,
                    parameters=parameters,
                    title=title
                )
                
            else:
                raise MCPError(-32601, f"Unknown tool: {name}")
                
        except KeyError as e:
            raise MCPError(-32602, f"Missing required parameter: {e}")
        except Exception as e:
            logger.exception(f"Error executing tool {name}")
            raise MCPError(-32603, f"Tool execution error: {str(e)}")


def main():
    """Main entry point for the visualization server."""
    logging.basicConfig(level=logging.INFO)
    server = VisualizationServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
