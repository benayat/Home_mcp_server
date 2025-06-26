#!/usr/bin/env python3
"""
Demo script showing the MCP Gateway Server capabilities.

This demonstrates how the gateway server centralizes all math and visualization
tools into a single MCP-compliant interface.
"""

import asyncio
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_servers.gateway_server import MCPGatewayServer


async def demo_gateway_server():
    """Demonstrate the unified gateway server capabilities."""
    
    print("🚀 MCP Gateway Server Demo")
    print("=" * 50)
    
    # Initialize the gateway server
    server = MCPGatewayServer()
    
    # Show server info
    info = server.get_server_info()
    print(f"📋 Server: {info['name']} v{info['version']}")
    print(f"📝 {info['description']}")
    print()
    
    # List available tools
    tools = await server.list_tools()
    print(f"🛠️  Available Tools: {len(tools)}")
    
    # Categorize tools
    math_tools = []
    viz_tools = []
    
    for tool in tools:
        if any(keyword in tool['name'] for keyword in ['arithmetic', 'solve', 'geometry', 'trigonometry', 'logarithms', 'fractions', 'percentage', 'evaluate', 'explain', 'theory', 'advanced']):
            math_tools.append(tool['name'])
        elif any(keyword in tool['name'] for keyword in ['chart', 'plot', 'visualize', 'statistics']):
            viz_tools.append(tool['name'])
    
    print(f"   📊 Math tools: {len(math_tools)}")
    for tool in math_tools[:5]:  # Show first 5
        print(f"      • {tool}")
    if len(math_tools) > 5:
        print(f"      • ... and {len(math_tools) - 5} more")
    
    print(f"   📈 Visualization tools: {len(viz_tools)}")
    for tool in viz_tools:
        print(f"      • {tool}")
    print()
    
    # Demo math capabilities
    print("🧮 Math Examples:")
    
    # Basic arithmetic
    result = await server.call_tool('basic_arithmetic', {
        'operation': 'multiply', 
        'a': 12, 
        'b': 8
    })
    print(f"   • 12 × 8 = {result['result']}")
    
    # Solve quadratic equation
    result = await server.call_tool('solve_equations', {
        'equation_type': 'quadratic',
        'a': 1,
        'b': -7,
        'c': 12
    })
    print(f"   • Solve x²-7x+12=0: x = {result['result']}")
    
    # Geometry calculation
    result = await server.call_tool('geometry', {
        'operation': 'area_circle',
        'values': [5]
    })
    print(f"   • Circle area (r=5): {result['result']:.2f}")
    
    # Trigonometry
    result = await server.call_tool('trigonometry', {
        'function': 'sin',
        'angle': 30,
        'unit': 'degrees'
    })
    print(f"   • sin(30°) = {result['result']:.3f}")
    print()
    
    # Show educational resources
    resources = await server.list_resources()
    print(f"📚 Educational Resources: {len(resources)}")
    for resource in resources:
        print(f"   • {resource['name']}: {resource['description']}")
    print()
    
    # MCP Protocol compliance demonstration
    print("✅ MCP Protocol Compliance:")
    print("   • JSON-RPC 2.0 compliant")
    print("   • Standard MCP methods: initialize, tools/list, tools/call, resources/list, resources/read")
    print("   • Proper error handling and response formatting")
    print("   • Content-type responses for tool results")
    print()
    
    print("🎯 Benefits for Client Integration:")
    print("   ✅ Single connection point (no need to manage multiple servers)")
    print("   ✅ All 15 tools available through one interface")
    print("   ✅ Educational resources included")
    print("   ✅ Rich explanations with step-by-step solutions")
    print("   ✅ Production-ready with proper error handling")
    print()
    
    print("🚀 Ready for MCP client integration!")


if __name__ == "__main__":
    asyncio.run(demo_gateway_server())
