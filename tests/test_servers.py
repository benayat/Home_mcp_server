"""
Tests for MCP servers.
"""

import pytest
import asyncio
from mcp_servers import MathServer, VisualizationServer


class TestMathServer:
    """Test cases for the Math MCP server."""
    
    @pytest.fixture
    def math_server(self):
        return MathServer()
    
    @pytest.mark.asyncio
    async def test_server_initialization(self, math_server):
        """Test that the math server initializes correctly."""
        assert math_server.name == "mcp-math-server"
        assert math_server.version == "1.0.0"
        assert not math_server._initialized
    
    @pytest.mark.asyncio
    async def test_list_tools(self, math_server):
        """Test that tools are listed correctly."""
        tools = await math_server.list_tools()
        assert len(tools) > 0
        
        tool_names = [tool["name"] for tool in tools]
        assert "basic_arithmetic" in tool_names
        assert "solve_equations" in tool_names
        assert "geometry" in tool_names
    
    @pytest.mark.asyncio
    async def test_basic_arithmetic(self, math_server):
        """Test basic arithmetic operations."""
        # Test addition
        result = await math_server.call_tool("basic_arithmetic", {
            "operation": "add",
            "a": 5,
            "b": 3
        })
        assert result["result"] == 8
        
        # Test division
        result = await math_server.call_tool("basic_arithmetic", {
            "operation": "divide", 
            "a": 10,
            "b": 2
        })
        assert result["result"] == 5
    
    @pytest.mark.asyncio
    async def test_equation_solving(self, math_server):
        """Test equation solving."""
        # Test linear equation: 2x + 4 = 0 -> x = -2
        result = await math_server.call_tool("solve_equations", {
            "equation_type": "linear",
            "a": 2,
            "b": 4
        })
        assert result["result"] == -2
        
        # Test quadratic equation: x^2 - 5x + 6 = 0 -> x = 2, 3
        result = await math_server.call_tool("solve_equations", {
            "equation_type": "quadratic",
            "a": 1,
            "b": -5,
            "c": 6
        })
        solutions = result["result"]
        assert 2 in solutions and 3 in solutions


class TestVisualizationServer:
    """Test cases for the Visualization MCP server."""
    
    @pytest.fixture
    def viz_server(self):
        return VisualizationServer()
    
    @pytest.mark.asyncio
    async def test_server_initialization(self, viz_server):
        """Test that the visualization server initializes correctly."""
        assert viz_server.name == "mcp-visualization-server"
        assert viz_server.version == "1.0.0"
        assert not viz_server._initialized
    
    @pytest.mark.asyncio
    async def test_list_tools(self, viz_server):
        """Test that tools are listed correctly."""
        tools = await viz_server.list_tools()
        assert len(tools) > 0
        
        tool_names = [tool["name"] for tool in tools]
        assert "create_chart" in tool_names
        assert "plot_function" in tool_names
        assert "visualize_geometry" in tool_names


if __name__ == "__main__":
    pytest.main([__file__])
