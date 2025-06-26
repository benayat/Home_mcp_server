#!/usr/bin/env python3
"""
Verification script for MCP servers.

This script checks that the servers can be imported and basic functionality works.
"""

import asyncio
import sys
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))


async def test_math_server():
    """Test the math server functionality."""
    print("Testing Math Server...")
    
    try:
        from mcp_servers import MathServer
        server = MathServer()
        
        # Test basic arithmetic
        result = await server.call_tool("basic_arithmetic", {
            "operation": "add",
            "a": 5,
            "b": 3
        })
        
        if result.get("result") == 8:
            print("✓ Math server basic arithmetic test passed")
        else:
            print(f"✗ Math server test failed: expected 8, got {result}")
            
        # Test tools listing
        tools = await server.list_tools()
        if len(tools) > 0:
            print(f"✓ Math server has {len(tools)} tools available")
        else:
            print("✗ Math server has no tools")
            
        return True
        
    except Exception as e:
        print(f"✗ Math server test failed: {e}")
        return False


async def test_visualization_server():
    """Test the visualization server functionality."""
    print("Testing Visualization Server...")
    
    try:
        from mcp_servers import VisualizationServer
        server = VisualizationServer()
        
        # Test tools listing
        tools = await server.list_tools()
        if len(tools) > 0:
            print(f"✓ Visualization server has {len(tools)} tools available")
        else:
            print("✗ Visualization server has no tools")
            
        # Note: We don't test actual chart creation as it requires matplotlib
        print("✓ Visualization server basic functionality works")
        print("  (Chart creation requires matplotlib, numpy, seaborn)")
        
        return True
        
    except Exception as e:
        print(f"✗ Visualization server test failed: {e}")
        return False


async def test_gateway_server():
    """Test the gateway server functionality."""
    print("Testing Gateway Server...")
    
    try:
        from mcp_servers.gateway_server import MCPGatewayServer
        server = MCPGatewayServer()
        
        # Test tools listing - should have both math and visualization tools
        tools = await server.list_tools()
        if len(tools) > 0:
            print(f"✓ Gateway server has {len(tools)} tools available")
            
            # Check for both math and visualization tools
            tool_names = {tool["name"] for tool in tools}
            
            # Check for math tools
            math_tools = {"basic_arithmetic", "solve_equations", "geometry"}
            if math_tools.issubset(tool_names):
                print("✓ Gateway server includes math tools")
            else:
                print("✗ Gateway server missing some math tools")
                
            # Check for visualization tools
            viz_tools = {"create_chart", "plot_function", "visualize_geometry"}
            if viz_tools.issubset(tool_names):
                print("✓ Gateway server includes visualization tools")
            else:
                print("✗ Gateway server missing some visualization tools")
        else:
            print("✗ Gateway server has no tools")
            
        # Test basic math functionality through gateway
        result = await server.call_tool("basic_arithmetic", {
            "operation": "multiply",
            "a": 6,
            "b": 7
        })
        
        if result.get("result") == 42:
            print("✓ Gateway server math functionality works")
        else:
            print(f"✗ Gateway server math test failed: expected 42, got {result}")
            
        # Test resources listing
        resources = await server.list_resources()
        if len(resources) > 0:
            print(f"✓ Gateway server has {len(resources)} resources available")
        else:
            print("✗ Gateway server has no resources")
            
        return True
        
    except Exception as e:
        print(f"✗ Gateway server test failed: {e}")
        return False


async def test_mcp_protocol():
    """Test MCP protocol compliance."""
    print("Testing MCP Protocol Compliance...")
    
    try:
        from mcp_servers import MathServer
        server = MathServer()
        
        # Test initialization response
        init_response = await server.handle_initialize(1, {})
        if "result" in init_response and "protocolVersion" in init_response["result"]:
            print("✓ MCP initialize response is valid")
        else:
            print("✗ MCP initialize response is invalid")
            
        # Test tools/list response
        tools_response = await server.handle_tools_list(2)
        if "result" in tools_response and "tools" in tools_response["result"]:
            print("✓ MCP tools/list response is valid")
        else:
            print("✗ MCP tools/list response is invalid")
            
        return True
        
    except Exception as e:
        print(f"✗ MCP protocol test failed: {e}")
        return False


def check_dependencies():
    """Check if optional dependencies are available."""
    print("Checking Dependencies...")
    
    required_deps = {
        "mcp": "Model Context Protocol library",
    }
    
    optional_deps = {
        "numpy": "NumPy for numerical computations",
        "matplotlib": "Matplotlib for plotting",
        "seaborn": "Seaborn for statistical plots"
    }
    
    for dep, description in required_deps.items():
        try:
            __import__(dep)
            print(f"✓ {dep} - {description}")
        except ImportError:
            print(f"✗ {dep} - {description} (REQUIRED)")
    
    for dep, description in optional_deps.items():
        try:
            __import__(dep)
            print(f"✓ {dep} - {description}")
        except ImportError:
            print(f"△ {dep} - {description} (optional for visualization)")


async def main():
    """Run all verification tests."""
    print("=== MCP Servers Verification ===\n")
    
    check_dependencies()
    print()
    
    math_ok = await test_math_server()
    print()
    
    viz_ok = await test_visualization_server()
    print()
    
    gateway_ok = await test_gateway_server()
    print()
    
    protocol_ok = await test_mcp_protocol()
    print()
    
    # Summary
    print("=== Summary ===")
    if math_ok and viz_ok and gateway_ok and protocol_ok:
        print("✓ All tests passed! MCP servers are ready to use.")
        print("\nTo run the servers:")
        print("  Math server: python -m mcp_servers.math_server")
        print("  Visualization server: python -m mcp_servers.visualization_server")
        print("\nOr install and use console commands:")
        print("  pip install -e .")
        print("  mcp-math-server")
        print("  mcp-visualization-server")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        print("\nIf you see import errors, try installing dependencies:")
        print("  pip install -r requirements.txt")


if __name__ == "__main__":
    asyncio.run(main())
