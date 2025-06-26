# MCP Gateway Server - Client Integration Guide

> **Complete guide for consuming the MCP Gateway Server via the Model Context Protocol**

## Table of Contents
- [Overview](#overview)
- [MCP Protocol Basics](#mcp-protocol-basics)
- [Server Connection](#server-connection)
- [Available Tools](#available-tools)
- [Mathematical Tools](#mathematical-tools)
- [Visualization Tools](#visualization-tools)
- [Usage Patterns](#usage-patterns)
- [Error Handling](#error-handling)
- [Code Examples](#code-examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

The MCP Gateway Server is a unified Model Context Protocol (MCP) server that provides comprehensive mathematical calculations and data visualization capabilities through a single interface. This guide covers everything you need to integrate with and consume the server via the MCP protocol.

### Key Benefits for Clients
- ✅ **15+ unified tools** accessible through one connection
- ✅ **Full MCP protocol compliance** (JSON-RPC 2.0)
- ✅ **Rich responses** with explanations and step-by-step solutions
- ✅ **Type-safe schemas** for all tool inputs and outputs
- ✅ **Educational content** suitable for elementary to high school levels

## MCP Protocol Basics

The Model Context Protocol (MCP) is a JSON-RPC 2.0 based protocol. All communication happens over standard input/output (stdio) or other transport mechanisms.

### Protocol Structure
```json
{
  "jsonrpc": "2.0",
  "id": "request-id",
  "method": "method_name",
  "params": { ... }
}
```

### Required Headers
All requests must include:
- `jsonrpc`: Always "2.0"
- `id`: Unique identifier for the request
- `method`: The MCP method name

## Server Connection

### Server Information
- **Name**: `mcp-gateway-server`
- **Version**: `1.0.0`
- **Protocol**: MCP (Model Context Protocol)
- **Transport**: stdio, TCP, or WebSocket

### Starting the Server
```bash
# Direct execution
python -m mcp_servers.gateway_server

# Or using the entry point
mcp-gateway-server
```

### Initial Handshake
1. **Initialize**: Send `initialize` request
2. **Get Capabilities**: Server returns supported features
3. **Start Session**: Send `initialized` notification

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "clientInfo": {
      "name": "your-client",
      "version": "1.0.0"
    }
  }
}
```

## Available Tools

The gateway server provides **15 tools** across mathematical and visualization domains:

### Tool Categories
- **Mathematical Tools** (11): Core math operations and problem solving
- **Visualization Tools** (4): Chart creation and data visualization

### Getting Tool List
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

## Mathematical Tools

### 1. `basic_arithmetic`
Perform basic arithmetic operations.

**Input Schema:**
```json
{
  "operation": "add|subtract|multiply|divide",
  "a": number,
  "b": number
}
```

**Example:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "basic_arithmetic",
    "arguments": {
      "operation": "add",
      "a": 15,
      "b": 27
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Result: 42\nExplanation: Adding 15 and 27 gives us 42."
      }
    ]
  }
}
```

### 2. `advanced_operations`
Perform advanced mathematical operations.

**Input Schema:**
```json
{
  "operation": "power|sqrt|factorial|abs|round_number",
  "value": number,
  "extra_param": number  // Optional: exponent for power, decimal places for rounding
}
```

**Examples:**
```json
// Square root
{
  "operation": "sqrt",
  "value": 16
}

// Power operation
{
  "operation": "power",
  "value": 2,
  "extra_param": 8
}

// Factorial
{
  "operation": "factorial",
  "value": 5
}
```

### 3. `number_theory`
Number theory operations and properties.

**Input Schema:**
```json
{
  "operation": "gcd|lcm|prime_factors|is_prime",
  "a": integer,
  "b": integer  // Optional: for GCD/LCM operations
}
```

**Examples:**
```json
// Greatest Common Divisor
{
  "operation": "gcd",
  "a": 48,
  "b": 18
}

// Prime factorization
{
  "operation": "prime_factors",
  "a": 60
}

// Primality test
{
  "operation": "is_prime",
  "a": 17
}
```

### 4. `solve_equations`
Solve linear and quadratic equations with step-by-step explanations.

**Input Schema:**
```json
{
  "equation_type": "linear|quadratic",
  "a": number,  // Coefficient of highest degree term
  "b": number,  // Coefficient of middle term
  "c": number   // Constant term (quadratic only)
}
```

**Examples:**
```json
// Linear equation: 3x + 6 = 0
{
  "equation_type": "linear",
  "a": 3,
  "b": 6
}

// Quadratic equation: x² - 5x + 6 = 0
{
  "equation_type": "quadratic",
  "a": 1,
  "b": -5,
  "c": 6
}
```

### 5. `geometry`
Calculate geometric properties and relationships.

**Input Schema:**
```json
{
  "operation": "area_circle|area_rectangle|area_triangle|pythagorean|distance|slope|midpoint",
  "values": [number, ...]  // Array of values specific to operation
}
```

**Examples:**
```json
// Circle area (radius = 5)
{
  "operation": "area_circle",
  "values": [5]
}

// Rectangle area (width = 4, height = 6)
{
  "operation": "area_rectangle",
  "values": [4, 6]
}

// Distance between points (x1=0, y1=0, x2=3, y2=4)
{
  "operation": "distance",
  "values": [0, 0, 3, 4]
}

// Triangle area (base = 8, height = 6)
{
  "operation": "area_triangle",
  "values": [8, 6]
}
```

### 6. `trigonometry`
Trigonometric functions with degree/radian support.

**Input Schema:**
```json
{
  "function": "sin|cos|tan",
  "angle": number,
  "unit": "degrees|radians"  // Default: radians
}
```

**Examples:**
```json
// Sine of 30 degrees
{
  "function": "sin",
  "angle": 30,
  "unit": "degrees"
}

// Cosine of π/4 radians
{
  "function": "cos",
  "angle": 0.7853981633974483,
  "unit": "radians"
}
```

### 7. `logarithms`
Logarithmic functions with different bases.

**Input Schema:**
```json
{
  "log_type": "log|log10",
  "x": number,      // Must be positive
  "base": number    // Optional: custom base (default: e for log, 10 for log10)
}
```

**Examples:**
```json
// Natural logarithm
{
  "log_type": "log",
  "x": 2.718281828
}

// Common logarithm (base 10)
{
  "log_type": "log10",
  "x": 100
}
```

### 8. `fractions`
Work with fractions and decimal conversions.

**Input Schema:**
```json
{
  "operation": "simplify_fraction|convert_to_decimal|convert_to_fraction",
  "numerator": integer,    // For fraction operations
  "denominator": integer,  // For fraction operations
  "decimal": number        // For decimal to fraction conversion
}
```

**Examples:**
```json
// Simplify fraction 8/12
{
  "operation": "simplify_fraction",
  "numerator": 8,
  "denominator": 12
}

// Convert 0.75 to fraction
{
  "operation": "convert_to_fraction",
  "decimal": 0.75
}
```

### 9. `percentages`
Calculate percentages and relationships.

**Input Schema:**
```json
{
  "part": number,   // Part value
  "whole": number   // Whole value
}
```

**Example:**
```json
// What percentage is 25 of 200?
{
  "part": 25,
  "whole": 200
}
```

### 10. `evaluate_expression`
Safely evaluate mathematical expressions.

**Input Schema:**
```json
{
  "expression": string  // Mathematical expression
}
```

**Example:**
```json
{
  "expression": "2^3 + 4*5 - 10"
}
```

**Supported Operations:**
- Basic arithmetic: `+`, `-`, `*`, `/`
- Exponentiation: `^` or `**`
- Parentheses: `(`, `)`
- Mathematical functions: `sin`, `cos`, `tan`, `sqrt`, `log`

### 11. `explain_concept`
Get educational explanations of mathematical concepts.

**Input Schema:**
```json
{
  "concept": string,
  "level": "elementary|middle|high_school"  // Default: middle
}
```

**Examples:**
```json
// Explain fractions for middle school
{
  "concept": "fractions",
  "level": "middle"
}

// Explain quadratic equations for high school
{
  "concept": "quadratic equations",
  "level": "high_school"
}
```

## Visualization Tools

### 1. `create_chart`
Create various types of charts and graphs.

**Input Schema:**
```json
{
  "chart_type": "line|bar|scatter|pie|histogram|box",
  "data": object,           // Chart-specific data format
  "title": string,          // Optional
  "xlabel": string,         // Optional
  "ylabel": string          // Optional
}
```

**Data Formats by Chart Type:**

**Line Chart:**
```json
{
  "chart_type": "line",
  "data": {
    "x": [1, 2, 3, 4, 5],
    "y": [2, 4, 6, 8, 10]
  },
  "title": "Linear Growth",
  "xlabel": "Time",
  "ylabel": "Value"
}
```

**Bar Chart:**
```json
{
  "chart_type": "bar",
  "data": {
    "categories": ["A", "B", "C", "D"],
    "values": [10, 25, 15, 30]
  },
  "title": "Category Comparison"
}
```

**Pie Chart:**
```json
{
  "chart_type": "pie",
  "data": {
    "labels": ["Red", "Blue", "Green", "Yellow"],
    "sizes": [30, 25, 20, 25]
  },
  "title": "Color Distribution"
}
```

**Scatter Plot:**
```json
{
  "chart_type": "scatter",
  "data": {
    "x": [1, 2, 3, 4, 5],
    "y": [2, 5, 3, 8, 7]
  },
  "title": "Data Points"
}
```

**Histogram:**
```json
{
  "chart_type": "histogram",
  "data": {
    "values": [1, 2, 2, 3, 3, 3, 4, 4, 5]
  },
  "title": "Distribution"
}
```

### 2. `plot_function`
Plot mathematical functions.

**Input Schema:**
```json
{
  "expression": string,           // Mathematical expression
  "x_range": [number, number],    // Optional: [min, max], default: [-10, 10]
  "num_points": integer,          // Optional: default 1000
  "title": string                 // Optional
}
```

**Examples:**
```json
// Plot quadratic function
{
  "expression": "x**2 + 2*x + 1",
  "x_range": [-5, 3],
  "title": "Quadratic Function"
}

// Plot sine wave
{
  "expression": "sin(x)",
  "x_range": [-6.28, 6.28],
  "title": "Sine Wave"
}

// Plot exponential function
{
  "expression": "exp(x)",
  "x_range": [-2, 2],
  "title": "Exponential Growth"
}
```

### 3. `create_statistics_chart`
Create comprehensive statistical visualizations.

**Input Schema:**
```json
{
  "data": [number, ...],    // Array of numerical data
  "chart_type": "all",      // Currently only supports "all"
  "title": string           // Optional
}
```

**Example:**
```json
{
  "data": [1, 2, 3, 4, 5, 5, 6, 7, 8, 9, 10],
  "chart_type": "all",
  "title": "Dataset Analysis"
}
```

**Output:** Creates multiple charts showing:
- Histogram with statistics
- Box plot
- Statistical summary (mean, median, mode, std dev)

### 4. `visualize_geometry`
Visualize geometric shapes and constructions.

**Input Schema:**
```json
{
  "shape_type": "circle|rectangle|triangle|polygon",
  "parameters": object,     // Shape-specific parameters
  "title": string          // Optional
}
```

**Examples:**

**Circle:**
```json
{
  "shape_type": "circle",
  "parameters": {
    "center": [0, 0],
    "radius": 5
  },
  "title": "Circle with radius 5"
}
```

**Rectangle:**
```json
{
  "shape_type": "rectangle",
  "parameters": {
    "corner": [0, 0],
    "width": 6,
    "height": 4
  },
  "title": "Rectangle 6x4"
}
```

**Triangle:**
```json
{
  "shape_type": "triangle",
  "parameters": {
    "vertices": [[0, 0], [4, 0], [2, 3]]
  },
  "title": "Triangle"
}
```

## Usage Patterns

### 1. Educational Workflow
```json
// Step 1: Get concept explanation
{
  "method": "tools/call",
  "params": {
    "name": "explain_concept",
    "arguments": {
      "concept": "quadratic equations",
      "level": "high_school"
    }
  }
}

// Step 2: Solve a specific example
{
  "method": "tools/call",
  "params": {
    "name": "solve_equations",
    "arguments": {
      "equation_type": "quadratic",
      "a": 1,
      "b": -5,
      "c": 6
    }
  }
}

// Step 3: Visualize the function
{
  "method": "tools/call",
  "params": {
    "name": "plot_function",
    "arguments": {
      "expression": "x**2 - 5*x + 6",
      "x_range": [-1, 6],
      "title": "y = x² - 5x + 6"
    }
  }
}
```

### 2. Data Analysis Workflow
```json
// Step 1: Create statistical visualization
{
  "method": "tools/call",
  "params": {
    "name": "create_statistics_chart",
    "arguments": {
      "data": [23, 45, 56, 78, 32, 67, 89, 12, 34, 56],
      "title": "Sample Data Analysis"
    }
  }
}

// Step 2: Create specific chart
{
  "method": "tools/call",
  "params": {
    "name": "create_chart",
    "arguments": {
      "chart_type": "histogram",
      "data": {
        "values": [23, 45, 56, 78, 32, 67, 89, 12, 34, 56]
      },
      "title": "Data Distribution"
    }
  }
}
```

### 3. Geometry Problem Solving
```json
// Step 1: Calculate area
{
  "method": "tools/call",
  "params": {
    "name": "geometry",
    "arguments": {
      "operation": "area_circle",
      "values": [5]
    }
  }
}

// Step 2: Visualize the shape
{
  "method": "tools/call",
  "params": {
    "name": "visualize_geometry",
    "arguments": {
      "shape_type": "circle",
      "parameters": {
        "center": [0, 0],
        "radius": 5
      },
      "title": "Circle with area calculation"
    }
  }
}
```

## Error Handling

### Standard MCP Errors
The server returns standard JSON-RPC 2.0 error responses:

```json
{
  "jsonrpc": "2.0",
  "id": "request-id",
  "error": {
    "code": -32600,
    "message": "Invalid Request",
    "data": "Additional error details"
  }
}
```

### Common Error Codes
- `-32700`: Parse error (invalid JSON)
- `-32600`: Invalid request
- `-32601`: Method not found
- `-32602`: Invalid params
- `-32603`: Internal error

### Tool-Specific Errors
```json
{
  "jsonrpc": "2.0",
  "id": "request-id",
  "error": {
    "code": -32000,
    "message": "Tool execution error",
    "data": {
      "tool": "basic_arithmetic",
      "error": "Division by zero"
    }
  }
}
```

### Error Handling Best Practices
1. **Always check for errors** in responses
2. **Validate inputs** before sending requests
3. **Handle network errors** gracefully
4. **Provide meaningful error messages** to users

## Code Examples

### Python Client Example
```python
import json
import subprocess
import asyncio

class MCPGatewayClient:
    def __init__(self):
        self.process = None
        self.request_id = 0
    
    async def start_server(self):
        """Start the MCP gateway server."""
        self.process = subprocess.Popen(
            ['python', '-m', 'mcp_servers.gateway_server'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    
    def get_next_id(self):
        """Get next request ID."""
        self.request_id += 1
        return self.request_id
    
    async def send_request(self, method, params=None):
        """Send MCP request and get response."""
        request = {
            "jsonrpc": "2.0",
            "id": self.get_next_id(),
            "method": method,
            "params": params or {}
        }
        
        # Send request
        request_json = json.dumps(request) + '\n'
        self.process.stdin.write(request_json)
        self.process.stdin.flush()
        
        # Read response
        response_line = self.process.stdout.readline()
        return json.loads(response_line)
    
    async def initialize(self):
        """Initialize MCP connection."""
        response = await self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "clientInfo": {"name": "python-client", "version": "1.0.0"}
        })
        
        # Send initialized notification
        await self.send_request("initialized")
        return response
    
    async def list_tools(self):
        """Get list of available tools."""
        return await self.send_request("tools/list")
    
    async def call_tool(self, name, arguments):
        """Call a specific tool."""
        return await self.send_request("tools/call", {
            "name": name,
            "arguments": arguments
        })

# Usage example
async def main():
    client = MCPGatewayClient()
    
    try:
        # Start server and initialize
        await client.start_server()
        await client.initialize()
        
        # List available tools
        tools_response = await client.list_tools()
        print("Available tools:", len(tools_response["result"]["tools"]))
        
        # Call a math tool
        result = await client.call_tool("basic_arithmetic", {
            "operation": "add",
            "a": 15,
            "b": 27
        })
        print("Math result:", result["result"]["content"][0]["text"])
        
        # Call a visualization tool
        result = await client.call_tool("create_chart", {
            "chart_type": "line",
            "data": {
                "x": [1, 2, 3, 4, 5],
                "y": [2, 4, 6, 8, 10]
            },
            "title": "Linear Growth"
        })
        print("Chart created:", result["result"]["content"][0]["text"])
        
    finally:
        if client.process:
            client.process.terminate()

if __name__ == "__main__":
    asyncio.run(main())
```

### JavaScript/Node.js Client Example
```javascript
const { spawn } = require('child_process');
const { Readable, Writable } = require('stream');

class MCPGatewayClient {
    constructor() {
        this.process = null;
        this.requestId = 0;
    }
    
    async startServer() {
        this.process = spawn('python', ['-m', 'mcp_servers.gateway_server'], {
            stdio: ['pipe', 'pipe', 'pipe']
        });
    }
    
    getNextId() {
        return ++this.requestId;
    }
    
    async sendRequest(method, params = {}) {
        const request = {
            jsonrpc: "2.0",
            id: this.getNextId(),
            method: method,
            params: params
        };
        
        return new Promise((resolve, reject) => {
            // Send request
            this.process.stdin.write(JSON.stringify(request) + '\n');
            
            // Read response
            let responseData = '';
            const onData = (data) => {
                responseData += data.toString();
                if (responseData.includes('\n')) {
                    this.process.stdout.removeListener('data', onData);
                    try {
                        const response = JSON.parse(responseData.trim());
                        resolve(response);
                    } catch (error) {
                        reject(error);
                    }
                }
            };
            
            this.process.stdout.on('data', onData);
        });
    }
    
    async initialize() {
        const response = await this.sendRequest('initialize', {
            protocolVersion: "2024-11-05",
            capabilities: { tools: {} },
            clientInfo: { name: "js-client", version: "1.0.0" }
        });
        
        await this.sendRequest('initialized');
        return response;
    }
    
    async listTools() {
        return await this.sendRequest('tools/list');
    }
    
    async callTool(name, arguments) {
        return await this.sendRequest('tools/call', {
            name: name,
            arguments: arguments
        });
    }
}

// Usage example
async function main() {
    const client = new MCPGatewayClient();
    
    try {
        await client.startServer();
        await client.initialize();
        
        // List tools
        const toolsResponse = await client.listTools();
        console.log('Available tools:', toolsResponse.result.tools.length);
        
        // Call math tool
        const mathResult = await client.callTool('basic_arithmetic', {
            operation: 'multiply',
            a: 12,
            b: 8
        });
        console.log('Math result:', mathResult.result.content[0].text);
        
        // Call visualization tool
        const vizResult = await client.callTool('plot_function', {
            expression: 'x**2',
            x_range: [-5, 5],
            title: 'Parabola'
        });
        console.log('Visualization result:', vizResult.result.content[0].text);
        
    } finally {
        if (client.process) {
            client.process.kill();
        }
    }
}

main().catch(console.error);
```

## Best Practices

### 1. Connection Management
- **Initialize once**: Call `initialize` only once per session
- **Handle errors**: Always check for error responses
- **Clean shutdown**: Properly terminate the server process
- **Reconnection logic**: Implement reconnection for production use

### 2. Tool Usage
- **Validate inputs**: Check required parameters before calling tools
- **Handle responses**: Parse both success and error responses
- **Batch operations**: Group related calls when possible
- **Cache results**: Store expensive calculations for reuse

### 3. Educational Applications
- **Progressive difficulty**: Start with basic concepts, advance gradually
- **Visual reinforcement**: Use visualization tools to support explanations
- **Step-by-step**: Break complex problems into smaller steps
- **Interactive feedback**: Provide immediate feedback on student responses

### 4. Performance Optimization
- **Minimize calls**: Combine operations when possible
- **Streaming**: Use appropriate transport for your use case
- **Error recovery**: Implement robust error handling and retry logic
- **Resource management**: Monitor memory and CPU usage

### 5. User Experience
- **Clear feedback**: Show progress for long operations
- **Error messages**: Provide user-friendly error explanations
- **Input validation**: Validate user inputs before sending to server
- **Help system**: Integrate tool descriptions into your UI

## Troubleshooting

### Common Issues

#### 1. Server Won't Start
**Symptoms:** Process fails to start or exits immediately
**Solutions:**
- Check Python installation and path
- Verify dependencies are installed: `pip install -r requirements.txt`
- Check for port conflicts if using TCP transport
- Review error logs in stderr

#### 2. JSON-RPC Errors
**Symptoms:** Receiving -32600, -32601, or -32602 errors
**Solutions:**
- Validate JSON format
- Check method names (use `tools/list`, `tools/call`, etc.)
- Verify required parameters are included
- Ensure parameter types match schema

#### 3. Tool Execution Errors
**Symptoms:** Tools return error responses
**Solutions:**
- Validate input parameters against schemas
- Check for mathematical errors (division by zero, negative square roots)
- Ensure data formats match expected schemas for visualization tools
- Review error messages for specific guidance

#### 4. Connection Issues
**Symptoms:** Hanging requests or communication failures
**Solutions:**
- Check stdio pipes are properly configured
- Ensure proper line termination (\n) for messages
- Verify server process is still running
- Implement timeout mechanisms

#### 5. Visualization Problems
**Symptoms:** Charts fail to generate or display incorrectly
**Solutions:**
- Verify data array formats
- Check for empty or invalid data sets
- Ensure chart type matches data structure
- Review matplotlib/plotting library installation

### Debugging Tips

1. **Enable logging**: Set up proper logging in your client
2. **Message inspection**: Log all JSON-RPC messages for debugging
3. **Server logs**: Monitor server stderr for error messages
4. **Tool validation**: Test tools individually before complex workflows
5. **Protocol compliance**: Use MCP protocol validators if available

### Getting Help

1. **Documentation**: Review this guide and the API documentation
2. **Examples**: Check the provided example clients
3. **Error messages**: Read error messages carefully for specific guidance
4. **Testing**: Use the provided test scripts to verify functionality

---

## Summary

The MCP Gateway Server provides a powerful, unified interface for mathematical calculations and data visualization through the Model Context Protocol. This guide covers:

- ✅ **15 tools** for comprehensive math and visualization capabilities
- ✅ **Complete protocol details** with JSON-RPC examples
- ✅ **Real-world usage patterns** for different application types
- ✅ **Production-ready examples** in Python and JavaScript
- ✅ **Best practices** for robust client implementations
- ✅ **Troubleshooting guide** for common issues

For additional resources, see:
- `README.md` - General project overview
- `API.md` - Detailed API documentation
- `examples/` - Sample client implementations
- `tests/` - Test scripts and validation

**Ready to integrate?** Start with the provided examples and adapt them to your specific use case. The MCP Gateway Server is designed to be developer-friendly while providing production-grade reliability and performance.
