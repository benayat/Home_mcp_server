#!/usr/bin/env python3
"""
Example usage of the Math MCP Server.

This script demonstrates how to use the math server programmatically
(not through the MCP protocol, but directly).
"""

import asyncio
from mcp_servers import MathServer


async def main():
    """Demonstrate math server capabilities."""
    print("=== Math MCP Server Examples ===\n")
    
    # Create server instance
    server = MathServer()
    
    # Example 1: Basic arithmetic
    print("1. Basic Arithmetic:")
    result = await server.call_tool("basic_arithmetic", {
        "operation": "add",
        "a": 15,
        "b": 27
    })
    print(f"   15 + 27 = {result['result']}")
    print(f"   Explanation: {result['explanation']}\n")
    
    # Example 2: Quadratic equation
    print("2. Solving Quadratic Equation (x² - 5x + 6 = 0):")
    result = await server.call_tool("solve_equations", {
        "equation_type": "quadratic",
        "a": 1,
        "b": -5,
        "c": 6
    })
    print(f"   Solutions: {result['result']}")
    print(f"   Explanation: {result['explanation']}\n")
    
    # Example 3: Geometry
    print("3. Circle Area (radius = 5):")
    result = await server.call_tool("geometry", {
        "operation": "area_circle",
        "values": [5]
    })
    print(f"   Area: {result['result']:.2f}")
    print(f"   Explanation: {result['explanation']}\n")
    
    # Example 4: Trigonometry
    print("4. Trigonometry (sin(30°)):")
    result = await server.call_tool("trigonometry", {
        "function": "sin",
        "angle": 30,
        "unit": "degrees"
    })
    print(f"   sin(30°) = {result['result']:.4f}")
    print(f"   Explanation: {result['explanation']}\n")
    
    # Example 5: Expression evaluation
    print("5. Expression Evaluation:")
    result = await server.call_tool("evaluate_expression", {
        "expression": "2^3 + 4*5 - 10"
    })
    print(f"   2³ + 4×5 - 10 = {result['result']}")
    print(f"   Explanation: {result['explanation']}\n")
    
    # Example 6: Mathematical concept explanation
    print("6. Concept Explanation (Fractions - Middle School Level):")
    result = await server.call_tool("explain_concept", {
        "concept": "fractions",
        "level": "middle"
    })
    print(f"   Concept: {result['concept']}")
    print(f"   Explanation: {result['explanation']}")
    print(f"   Example: {result['example']}\n")


if __name__ == "__main__":
    asyncio.run(main())
