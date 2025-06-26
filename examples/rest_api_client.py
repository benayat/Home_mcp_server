#!/usr/bin/env python3
"""
Example REST API client for MCP Gateway Server.

This demonstrates how to use the REST API to interact with the
MCP Gateway Server using standard HTTP requests.
"""

import asyncio
import json
import sys
from typing import Any, Dict

import aiohttp


class MCPRestClient:
    """REST API client for MCP Gateway Server."""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url.rstrip('/')
        
    async def health_check(self) -> Dict[str, Any]:
        """Check server health."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/health") as response:
                return await response.json()
    
    async def get_server_info(self) -> Dict[str, Any]:
        """Get server information."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/info") as response:
                return await response.json()
    
    async def list_tools(self) -> Dict[str, Any]:
        """List all available tools."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/tools") as response:
                return await response.json()
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific tool."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/tools/{tool_name}",
                json=arguments,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"HTTP {response.status}: {error_text}")
    
    async def basic_arithmetic(self, operation: str, a: float, b: float) -> Dict[str, Any]:
        """Perform basic arithmetic."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/tools/basic_arithmetic",
                json={"operation": operation, "a": a, "b": b},
                headers={"Content-Type": "application/json"}
            ) as response:
                return await response.json()
    
    async def solve_equation(self, equation_type: str, a: float, b: float, c: float = 0) -> Dict[str, Any]:
        """Solve equations."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/tools/solve_equations",
                json={"equation_type": equation_type, "a": a, "b": b, "c": c},
                headers={"Content-Type": "application/json"}
            ) as response:
                return await response.json()
    
    async def create_chart(self, chart_type: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Create a chart."""
        chart_data = {"chart_type": chart_type, "data": data}
        chart_data.update(kwargs)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/tools/create_chart",
                json=chart_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                return await response.json()
    
    async def list_resources(self) -> Dict[str, Any]:
        """List educational resources."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/resources") as response:
                return await response.json()
    
    async def get_resource(self, resource_id: str) -> Dict[str, Any]:
        """Get a specific resource."""
        # URL encode the resource ID
        import urllib.parse
        encoded_id = urllib.parse.quote(resource_id, safe='')
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/resources/{encoded_id}") as response:
                return await response.json()


async def demo_math_operations(client: MCPRestClient):
    """Demonstrate math operations."""
    print("🧮 Math Operations Demo")
    print("=" * 30)
    
    # Basic arithmetic
    print("1. Basic Arithmetic:")
    result = await client.basic_arithmetic("multiply", 7, 6)
    print(f"   7 × 6 = {result['result']} - {result.get('explanation', '')}")
    
    # Equation solving
    print("\n2. Equation Solving:")
    result = await client.solve_equation("quadratic", 1, -5, 6)
    print(f"   x²-5x+6=0 → x = {result['result']}")
    print(f"   Explanation: {result.get('explanation', '')}")
    
    # Geometry
    print("\n3. Geometry:")
    result = await client.execute_tool("geometry", {
        "operation": "area_circle",
        "values": [3]
    })
    print(f"   Circle area (r=3) = {result['result']:.2f}")
    
    # Expression evaluation
    print("\n4. Expression Evaluation:")
    result = await client.execute_tool("evaluate_expression", {
        "expression": "2^3 + 4*5 - 6"
    })
    print(f"   2³ + 4×5 - 6 = {result['result']}")


async def demo_visualization(client: MCPRestClient):
    """Demonstrate visualization operations."""
    print("\n📊 Visualization Demo")
    print("=" * 30)
    
    # Line chart
    print("1. Line Chart:")
    try:
        result = await client.create_chart("line", {
            "x": [1, 2, 3, 4, 5],
            "y": [1, 4, 9, 16, 25]
        }, title="Square Function", xlabel="x", ylabel="x²")
        print(f"   Chart created: {result.get('result', {}).get('message', 'Success')}")
    except Exception as e:
        print(f"   Chart creation: {e} (requires matplotlib)")
    
    # Function plotting
    print("\n2. Function Plotting:")
    try:
        result = await client.execute_tool("plot_function", {
            "expression": "x**2 - 4*x + 3",
            "x_range": [-1, 5],
            "title": "Quadratic Function"
        })
        print(f"   Function plot: {result.get('result', {}).get('message', 'Success')}")
    except Exception as e:
        print(f"   Function plotting: {e} (requires matplotlib)")


async def demo_resources(client: MCPRestClient):
    """Demonstrate educational resources."""
    print("\n📚 Educational Resources Demo")
    print("=" * 30)
    
    # List resources
    resources = await client.list_resources()
    print(f"Available resources: {len(resources['resources'])}")
    
    for resource in resources['resources'][:3]:
        print(f"   • {resource['name']}: {resource['description']}")
    
    # Get a specific resource
    print("\n📖 Elementary Math Concepts:")
    try:
        content = await client.get_resource("math://concepts/elementary")
        text_content = content['contents'][0]['text']
        # Show first few lines
        lines = text_content.split('\n')[:8]
        for line in lines:
            if line.strip():
                print(f"   {line}")
        print("   ...")
    except Exception as e:
        print(f"   Error accessing resource: {e}")


async def main():
    """Main demo function."""
    print("🚀 MCP Gateway Server REST API Demo")
    print("=" * 50)
    
    # Initialize client
    client = MCPRestClient()
    
    try:
        # Health check
        health = await client.health_check()
        print(f"✅ Server Status: {health['status']}")
        
        # Server info
        info = await client.get_server_info()
        print(f"📋 Server: {info['name']} v{info['version']}")
        print(f"📝 Description: {info['description']}")
        
        # List tools
        tools = await client.list_tools()
        print(f"🛠️  Available Tools: {len(tools['tools'])}")
        
        # Run demos
        await demo_math_operations(client)
        await demo_visualization(client)
        await demo_resources(client)
        
        print("\n✅ Demo completed successfully!")
        print("\n🔗 Try the interactive API documentation:")
        print("   Swagger UI: http://localhost:8080/docs")
        print("   ReDoc:      http://localhost:8080/redoc")
        
    except aiohttp.ClientConnectorError:
        print("❌ Cannot connect to server. Make sure the REST API is running:")
        print("   make run-rest-api")
        print("   # or")
        print("   ./scripts/start-rest-api.sh")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Check if aiohttp is available
    try:
        import aiohttp
    except ImportError:
        print("❌ aiohttp not found. Install it with: pip install aiohttp")
        sys.exit(1)
    
    asyncio.run(main())
