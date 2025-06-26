# MCP Servers API Documentation

## Overview

This package provides a unified Model Context Protocol (MCP) server system with both mathematical and visualization capabilities.

## 🚀 Centralized Gateway Server (Recommended)

The **MCP Gateway Server** provides a unified interface combining all mathematical and visualization capabilities in one MCP-compliant server. This is the **recommended approach for client integration**.

### Key Benefits:
- ✅ **Single connection point** - Connect to one server instead of multiple
- ✅ **15 unified tools** (math + visualization)
- ✅ **MCP protocol compliant** - Ready for any MCP client
- ✅ **Educational resources** - Built-in learning materials
- ✅ **Production ready** - Proper error handling and logging

### Quick Start:
```bash
# Run the gateway server
python -m mcp_servers.gateway_server

# Or after installation:
mcp-gateway-server
```

## Legacy Individual Servers

You can also use individual servers if needed:
1. **Math Server** - Mathematical calculations only
2. **Visualization Server** - Data visualization only

---

# Available Tools & Capabilities

## Math Server

### Available Tools

#### `basic_arithmetic`
Perform basic arithmetic operations.

**Parameters:**
- `operation` (string): "add", "subtract", "multiply", or "divide"
- `a` (number): First number
- `b` (number): Second number

**Example:**
```json
{
  "name": "basic_arithmetic",
  "arguments": {
    "operation": "add",
    "a": 15,
    "b": 27
  }
}
```

#### `advanced_operations`
Perform advanced mathematical operations.

**Parameters:**
- `operation` (string): "power", "sqrt", "factorial", "abs", or "round_number"
- `value` (number): Input value
- `extra_param` (number, optional): Extra parameter for operations like power or rounding

**Example:**
```json
{
  "name": "advanced_operations",
  "arguments": {
    "operation": "power",
    "value": 2,
    "extra_param": 10
  }
}
```

#### `number_theory`
Number theory operations.

**Parameters:**
- `operation` (string): "gcd", "lcm", "prime_factors", or "is_prime"
- `a` (integer): First integer
- `b` (integer, optional): Second integer (for GCD/LCM)

#### `solve_equations`
Solve linear and quadratic equations.

**Parameters:**
- `equation_type` (string): "linear" or "quadratic"
- `a` (number): Coefficient a
- `b` (number): Coefficient b
- `c` (number, optional): Coefficient c (for quadratic)

**Example:**
```json
{
  "name": "solve_equations",
  "arguments": {
    "equation_type": "quadratic",
    "a": 1,
    "b": -5,
    "c": 6
  }
}
```

#### `geometry`
Calculate geometric properties.

**Parameters:**
- `operation` (string): "area_circle", "area_rectangle", "area_triangle", "pythagorean", "distance", "slope", "midpoint"
- `values` (array): Array of numeric values needed for the operation

**Example:**
```json
{
  "name": "geometry",
  "arguments": {
    "operation": "area_circle",
    "values": [5]
  }
}
```

#### `trigonometry`
Trigonometric functions.

**Parameters:**
- `function` (string): "sin", "cos", or "tan"
- `angle` (number): Angle value
- `unit` (string, optional): "radians" or "degrees" (default: "radians")

#### `logarithms`
Logarithmic functions.

**Parameters:**
- `log_type` (string): "log" or "log10"
- `x` (number): Input value
- `base` (number, optional): Base for logarithm (default: e)

#### `fractions`
Work with fractions.

**Parameters:**
- `operation` (string): "simplify_fraction", "convert_to_decimal", "convert_to_fraction"
- `numerator` (integer): Numerator
- `denominator` (integer): Denominator
- `decimal` (number): Decimal value (for conversion)

#### `percentages`
Calculate percentages.

**Parameters:**
- `part` (number): Part value
- `whole` (number): Whole value

#### `evaluate_expression`
Safely evaluate mathematical expressions.

**Parameters:**
- `expression` (string): Mathematical expression (supports +, -, *, /, ^, parentheses)

#### `explain_concept`
Explain mathematical concepts.

**Parameters:**
- `concept` (string): Mathematical concept to explain
- `level` (string, optional): "elementary", "middle", or "high_school" (default: "middle")

### Resources

The math server provides educational resources:
- `math://concepts/elementary` - Elementary math concepts
- `math://concepts/middle` - Middle school concepts
- `math://concepts/high_school` - High school concepts
- `math://formulas/geometry` - Geometry formulas
- `math://formulas/algebra` - Algebra formulas

## Visualization Server

### Available Tools

#### `create_chart`
Create various types of charts.

**Parameters:**
- `chart_type` (string): "line", "bar", "scatter", "pie", "histogram", "box"
- `data` (object): Chart data (format depends on chart type)
- `title` (string, optional): Chart title
- `xlabel` (string, optional): X-axis label
- `ylabel` (string, optional): Y-axis label

**Example:**
```json
{
  "name": "create_chart",
  "arguments": {
    "chart_type": "line",
    "data": {
      "x": [1, 2, 3, 4, 5],
      "y": [2, 4, 6, 8, 10]
    },
    "title": "Linear Function",
    "xlabel": "x",
    "ylabel": "y"
  }
}
```

#### `plot_function`
Plot mathematical functions.

**Parameters:**
- `expression` (string): Mathematical expression to plot
- `x_range` (array, optional): Range for x values [min, max] (default: [-10, 10])
- `num_points` (integer, optional): Number of points to plot (default: 1000)
- `title` (string, optional): Plot title

**Example:**
```json
{
  "name": "plot_function",
  "arguments": {
    "expression": "x**2 - 4*x + 3",
    "x_range": [-2, 6],
    "title": "Quadratic Function"
  }
}
```

#### `create_statistics_chart`
Create statistical visualizations.

**Parameters:**
- `data` (array): Numerical data for analysis
- `chart_type` (string, optional): "all" (default)
- `title` (string, optional): Chart title

#### `visualize_geometry`
Visualize geometric shapes.

**Parameters:**
- `shape_type` (string): "circle", "rectangle", "triangle", "polygon"
- `parameters` (object): Shape-specific parameters
- `title` (string, optional): Visualization title

**Example:**
```json
{
  "name": "visualize_geometry",
  "arguments": {
    "shape_type": "circle",
    "parameters": {
      "radius": 5,
      "center": [0, 0]
    },
    "title": "Circle Visualization"
  }
}
```

## Chart Data Formats

### Line Chart
```json
{
  "x": [1, 2, 3, 4, 5],
  "y": [2, 4, 6, 8, 10]
}
```

### Bar Chart
```json
{
  "categories": ["A", "B", "C"],
  "values": [10, 20, 15]
}
```

### Scatter Plot
```json
{
  "x": [1, 2, 3, 4, 5],
  "y": [2, 4, 6, 8, 10],
  "colors": [1, 2, 3, 4, 5],
  "sizes": [20, 40, 60, 80, 100]
}
```

### Pie Chart
```json
{
  "labels": ["Category A", "Category B", "Category C"],
  "values": [30, 45, 25]
}
```

### Histogram
```json
{
  "values": [1, 2, 2, 3, 3, 3, 4, 4, 5],
  "bins": 10
}
```

### Box Plot
```json
{
  "values": [1, 2, 3, 4, 5, 6, 7, 8, 9],
  "labels": ["Dataset 1"]
}
```

## Geometric Shape Parameters

### Circle
```json
{
  "radius": 5,
  "center": [0, 0]
}
```

### Rectangle
```json
{
  "width": 4,
  "height": 3,
  "center": [0, 0]
}
```

### Triangle
```json
{
  "vertices": [[0, 0], [3, 0], [1.5, 2]]
}
```

### Polygon
```json
{
  "vertices": [[0, 0], [2, 0], [3, 1], [2, 2], [0, 2]]
}
```

## Error Handling

All tools return standardized error responses when issues occur:

```json
{
  "error": "Error description",
  "explanation": "Detailed explanation of the error"
}
```

Common error scenarios:
- Division by zero
- Invalid input parameters
- Mathematical domain errors (e.g., square root of negative numbers)
- Invalid expressions or syntax
- Missing required parameters

## Running the Servers

### Gateway Server (Recommended)
```bash
# Run the unified gateway server that includes all tools
python -m mcp_servers.gateway_server

# Or after installation:
mcp-gateway-server
```

### Individual Servers (If Needed)
```bash
# Math server only
python -m mcp_servers.math_server
# Or: mcp-math-server

# Visualization server only  
python -m mcp_servers.visualization_server
# Or: mcp-visualization-server
```

### Programmatic Usage
```python
import asyncio
from mcp_servers.gateway_server import MCPGatewayServer

async def main():
    # Use the gateway server for all functionality
    server = MCPGatewayServer()
    
    # Math example
    result = await server.call_tool("basic_arithmetic", {
        "operation": "add",
        "a": 15,
        "b": 27
    })
    print(result)  # {'result': 42, 'explanation': 'Addition: 15 + 27 = 42', 'steps': [...]}
    
    # Equation solving example
    result = await server.call_tool("solve_equations", {
        "equation_type": "quadratic",
        "a": 1,
        "b": -5,
        "c": 6
    })
    print(result)  # {'result': [3.0, 2.0], 'explanation': 'Two solutions...', 'steps': [...]}

asyncio.run(main())
```
