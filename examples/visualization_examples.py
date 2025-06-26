#!/usr/bin/env python3
"""
Example usage of the Visualization MCP Server.

This script demonstrates how to use the visualization server programmatically.
Note: This requires matplotlib and related dependencies to be installed.
"""

import asyncio
from mcp_servers import VisualizationServer


async def main():
    """Demonstrate visualization server capabilities."""
    print("=== Visualization MCP Server Examples ===\n")
    
    # Create server instance
    server = VisualizationServer()
    
    try:
        # Example 1: Line chart
        print("1. Creating Line Chart:")
        result = await server.call_tool("create_chart", {
            "chart_type": "line",
            "data": {
                "x": [1, 2, 3, 4, 5],
                "y": [2, 4, 6, 8, 10]
            },
            "title": "Linear Function y = 2x",
            "xlabel": "x",
            "ylabel": "y"
        })
        
        if "error" in result:
            print(f"   Error: {result['error']}")
        else:
            print(f"   Success: {result['description']}")
            print(f"   File: {result['filename']}\n")
        
        # Example 2: Bar chart
        print("2. Creating Bar Chart:")
        result = await server.call_tool("create_chart", {
            "chart_type": "bar",
            "data": {
                "categories": ["A", "B", "C", "D"],
                "values": [23, 45, 56, 78]
            },
            "title": "Sample Data",
            "xlabel": "Categories",
            "ylabel": "Values"
        })
        
        if "error" in result:
            print(f"   Error: {result['error']}")
        else:
            print(f"   Success: {result['description']}")
            print(f"   File: {result['filename']}\n")
        
        # Example 3: Function plotting
        print("3. Plotting Mathematical Function:")
        result = await server.call_tool("plot_function", {
            "expression": "x**2 - 4*x + 3",
            "x_range": [-2, 6],
            "title": "Quadratic Function: y = x² - 4x + 3"
        })
        
        if "error" in result:
            print(f"   Error: {result['error']}")
        else:
            print(f"   Success: {result['description']}")
            print(f"   File: {result['filename']}\n")
        
        # Example 4: Statistical visualization
        print("4. Statistical Analysis:")
        import random
        data = [random.gauss(50, 15) for _ in range(100)]  # Generate sample data
        
        result = await server.call_tool("create_statistics_chart", {
            "data": data,
            "title": "Statistical Analysis of Sample Data"
        })
        
        if "error" in result:
            print(f"   Error: {result['error']}")
        else:
            print(f"   Success: {result['description']}")
            print(f"   File: {result['filename']}\n")
        
        # Example 5: Geometric visualization
        print("5. Geometric Shape Visualization:")
        result = await server.call_tool("visualize_geometry", {
            "shape_type": "triangle",
            "parameters": {
                "vertices": [[0, 0], [4, 0], [2, 3]]
            },
            "title": "Right Triangle"
        })
        
        if "error" in result:
            print(f"   Error: {result['error']}")
        else:
            print(f"   Success: {result['description']}")
            print(f"   File: {result['filename']}\n")
    
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Note: Visualization examples require matplotlib, numpy, and seaborn to be installed.")
        print("Install with: pip install matplotlib numpy seaborn")


if __name__ == "__main__":
    asyncio.run(main())
