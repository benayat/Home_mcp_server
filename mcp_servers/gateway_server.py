#!/usr/bin/env python3
"""
MCP Gateway Server

A unified Model Context Protocol (MCP) server that provides both mathematical
calculations and data visualization capabilities through a single interface.
This serves as a gateway to all mathematical and visualization tools.
"""

import asyncio
import logging
from typing import Any, Dict, List

from .utils.base_server import BaseMCPServer, MCPError
from .utils.math_utils import MathSolver
from .utils.viz_utils import VisualizationHelper

logger = logging.getLogger(__name__)


class MCPGatewayServer(BaseMCPServer):
    """
    Unified MCP server providing both math and visualization capabilities.
    
    This gateway server consolidates all mathematical and visualization tools
    into a single MCP server interface, making it easier for clients to work
    with all capabilities through one connection.
    """
    
    def __init__(self):
        super().__init__("mcp-gateway-server", "1.0.0")
        self.math_solver = MathSolver()
        self.viz_helper = VisualizationHelper()
        
    def get_server_info(self) -> Dict[str, Any]:
        """Return server information."""
        return {
            "name": self.name,
            "version": self.version,
            "description": "Unified MCP server for mathematics and data visualization - your one-stop solution for mathematical calculations, problem solving, and data visualization"
        }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return server capabilities."""
        return {
            "tools": {"listChanged": False},
            "resources": {"subscribe": False, "listChanged": False}
        }
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Return list of all available tools (math + visualization)."""
        return [
            # === MATHEMATICAL TOOLS ===
            {
                "name": "basic_arithmetic",
                "description": "Perform basic arithmetic operations (add, subtract, multiply, divide)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["add", "subtract", "multiply", "divide"],
                            "description": "The arithmetic operation to perform"
                        },
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"}
                    },
                    "required": ["operation", "a", "b"]
                }
            },
            {
                "name": "advanced_operations",
                "description": "Perform advanced mathematical operations (power, sqrt, factorial, abs, round)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["power", "sqrt", "factorial", "abs", "round_number"],
                            "description": "The operation to perform"
                        },
                        "value": {"type": "number", "description": "Input value"},
                        "extra_param": {"type": "number", "description": "Extra parameter if needed (e.g., exponent for power, decimal places for rounding)", "default": 0}
                    },
                    "required": ["operation", "value"]
                }
            },
            {
                "name": "number_theory",
                "description": "Number theory operations (GCD, LCM, prime factors, primality test)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["gcd", "lcm", "prime_factors", "is_prime"],
                            "description": "The number theory operation"
                        },
                        "a": {"type": "integer", "description": "First integer"},
                        "b": {"type": "integer", "description": "Second integer (for GCD/LCM)", "default": 0}
                    },
                    "required": ["operation", "a"]
                }
            },
            {
                "name": "solve_equations",
                "description": "Solve linear and quadratic equations with step-by-step explanations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "equation_type": {
                            "type": "string",
                            "enum": ["linear", "quadratic"],
                            "description": "Type of equation to solve"
                        },
                        "a": {"type": "number", "description": "Coefficient a (for ax+b=0 or ax²+bx+c=0)"},
                        "b": {"type": "number", "description": "Coefficient b"},
                        "c": {"type": "number", "description": "Coefficient c (for quadratic only)", "default": 0}
                    },
                    "required": ["equation_type", "a", "b"]
                }
            },
            {
                "name": "geometry",
                "description": "Calculate geometric properties (areas, distances, slopes, etc.)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["area_circle", "area_rectangle", "area_triangle", "pythagorean", "distance", "slope", "midpoint"],
                            "description": "Geometric operation to perform"
                        },
                        "values": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Array of values needed for the operation (e.g., [radius] for circle, [x1,y1,x2,y2] for distance)"
                        }
                    },
                    "required": ["operation", "values"]
                }
            },
            {
                "name": "trigonometry",
                "description": "Trigonometric functions (sin, cos, tan) with support for degrees and radians",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "function": {
                            "type": "string",
                            "enum": ["sin", "cos", "tan"],
                            "description": "Trigonometric function"
                        },
                        "angle": {"type": "number", "description": "Angle value"},
                        "unit": {
                            "type": "string",
                            "enum": ["radians", "degrees"],
                            "description": "Angle unit",
                            "default": "radians"
                        }
                    },
                    "required": ["function", "angle"]
                }
            },
            {
                "name": "logarithms",
                "description": "Logarithmic functions (natural log, common log, custom base)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "log_type": {
                            "type": "string",
                            "enum": ["log", "log10"],
                            "description": "Type of logarithm"
                        },
                        "x": {"type": "number", "description": "Input value (must be positive)"},
                        "base": {"type": "number", "description": "Base for logarithm (default: e)", "default": 2.718281828459045}
                    },
                    "required": ["log_type", "x"]
                }
            },
            {
                "name": "fractions",
                "description": "Work with fractions (simplify, convert to/from decimal)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["simplify_fraction", "convert_to_decimal", "convert_to_fraction"],
                            "description": "Fraction operation"
                        },
                        "numerator": {"type": "integer", "description": "Numerator (for fraction operations)"},
                        "denominator": {"type": "integer", "description": "Denominator (for fraction operations)"},
                        "decimal": {"type": "number", "description": "Decimal value (for decimal to fraction conversion)"}
                    },
                    "required": ["operation"]
                }
            },
            {
                "name": "percentages",
                "description": "Calculate percentages and percentage relationships",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "part": {"type": "number", "description": "Part value"},
                        "whole": {"type": "number", "description": "Whole value"}
                    },
                    "required": ["part", "whole"]
                }
            },
            {
                "name": "evaluate_expression",
                "description": "Safely evaluate mathematical expressions with detailed steps",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression to evaluate (supports +, -, *, /, ^, parentheses)"
                        }
                    },
                    "required": ["expression"]
                }
            },
            {
                "name": "explain_concept",
                "description": "Explain mathematical concepts with examples at different educational levels",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "concept": {
                            "type": "string",
                            "description": "Mathematical concept to explain (e.g., 'fractions', 'quadratic equations', 'trigonometry')"
                        },
                        "level": {
                            "type": "string",
                            "enum": ["elementary", "middle", "high_school"],
                            "description": "Educational level for explanation",
                            "default": "middle"
                        }
                    },
                    "required": ["concept"]
                }
            },
            
            # === VISUALIZATION TOOLS ===
            {
                "name": "create_chart",
                "description": "Create various types of charts and graphs (line, bar, scatter, pie, histogram, box)",
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
                            "description": "Chart data (format depends on chart type)"
                        },
                        "title": {"type": "string", "description": "Chart title"},
                        "xlabel": {"type": "string", "description": "X-axis label"},
                        "ylabel": {"type": "string", "description": "Y-axis label"}
                    },
                    "required": ["chart_type", "data"]
                }
            },
            {
                "name": "plot_function",
                "description": "Plot mathematical functions with customizable ranges and styling",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression to plot (e.g., 'x**2 + 2*x + 1', 'sin(x)', 'exp(x)')"
                        },
                        "x_range": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Range for x values [min, max]",
                            "default": [-10, 10]
                        },
                        "num_points": {
                            "type": "integer",
                            "description": "Number of points to plot",
                            "default": 1000
                        },
                        "title": {"type": "string", "description": "Plot title"}
                    },
                    "required": ["expression"]
                }
            },
            {
                "name": "create_statistics_chart",
                "description": "Create comprehensive statistical visualizations and analysis",
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
                        "title": {"type": "string", "description": "Chart title"}
                    },
                    "required": ["data"]
                }
            },
            {
                "name": "visualize_geometry",
                "description": "Visualize geometric shapes and constructions",
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
                            "description": "Shape-specific parameters"
                        },
                        "title": {"type": "string", "description": "Visualization title"}
                    },
                    "required": ["shape_type", "parameters"]
                }
            }
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool (math or visualization) with given arguments."""
        
        try:
            # === MATHEMATICAL TOOLS ===
            if name == "basic_arithmetic":
                operation = arguments["operation"]
                a = arguments["a"]
                b = arguments["b"]
                return self.math_solver.operations[operation](a, b)
                
            elif name == "advanced_operations":
                operation = arguments["operation"]
                value = arguments["value"]
                extra_param = arguments.get("extra_param", 0)
                
                if operation in ["power"]:
                    return self.math_solver.operations[operation](value, extra_param)
                elif operation in ["round_number"]:
                    return self.math_solver.operations[operation](value, int(extra_param))
                else:
                    return self.math_solver.operations[operation](value)
                    
            elif name == "number_theory":
                operation = arguments["operation"]
                a = arguments["a"]
                b = arguments.get("b", 0)
                
                if operation in ["gcd", "lcm"]:
                    return self.math_solver.operations[operation](a, b)
                else:
                    return self.math_solver.operations[operation](a)
                    
            elif name == "solve_equations":
                equation_type = arguments["equation_type"]
                a = arguments["a"]
                b = arguments["b"]
                c = arguments.get("c", 0)
                
                if equation_type == "linear":
                    return self.math_solver.operations["solve_linear"](a, b)
                else:
                    return self.math_solver.operations["solve_quadratic"](a, b, c)
                    
            elif name == "geometry":
                operation = arguments["operation"]
                values = arguments["values"]
                
                if operation == "area_circle":
                    return self.math_solver.operations[operation](values[0])
                elif operation in ["area_rectangle", "pythagorean"]:
                    return self.math_solver.operations[operation](values[0], values[1])
                elif operation == "area_triangle":
                    return self.math_solver.operations[operation](values[0], values[1])
                elif operation in ["distance", "slope", "midpoint"]:
                    return self.math_solver.operations[operation](values[0], values[1], values[2], values[3])
                    
            elif name == "trigonometry":
                function = arguments["function"]
                angle = arguments["angle"]
                unit = arguments.get("unit", "radians")
                return self.math_solver.operations[function](angle, unit)
                
            elif name == "logarithms":
                import math
                log_type = arguments["log_type"]
                x = arguments["x"]
                base = arguments.get("base", math.e)
                
                if log_type == "log10":
                    return self.math_solver.operations["log10"](x)
                else:
                    return self.math_solver.operations["log"](x, base)
                    
            elif name == "fractions":
                operation = arguments["operation"]
                
                if operation == "simplify_fraction":
                    return self.math_solver.operations[operation](arguments["numerator"], arguments["denominator"])
                elif operation == "convert_to_decimal":
                    return self.math_solver.operations[operation](arguments["numerator"], arguments["denominator"])
                elif operation == "convert_to_fraction":
                    return self.math_solver.operations[operation](arguments["decimal"])
                    
            elif name == "percentages":
                return self.math_solver.operations["percentage"](arguments["part"], arguments["whole"])
                
            elif name == "evaluate_expression":
                return self.math_solver.operations["evaluate_expression"](arguments["expression"])
                
            elif name == "explain_concept":
                return await self.math_solver.explain_concept(arguments["concept"], arguments.get("level", "middle"))
            
            # === VISUALIZATION TOOLS ===
            elif name == "create_chart":
                chart_type = arguments["chart_type"]
                data = arguments["data"]
                title = arguments.get("title")
                xlabel = arguments.get("xlabel")
                ylabel = arguments.get("ylabel")
                
                return self.viz_helper.create_chart(chart_type, data, title, xlabel, ylabel)
                
            elif name == "plot_function":
                expression = arguments["expression"]
                x_range = arguments.get("x_range", (-10, 10))
                num_points = arguments.get("num_points", 1000)
                title = arguments.get("title")
                
                return self.viz_helper.plot_function(expression, tuple(x_range), num_points, title)
                
            elif name == "create_statistics_chart":
                data = arguments["data"]
                chart_type = arguments.get("chart_type", "all")
                title = arguments.get("title")
                
                return self.viz_helper.create_statistics_chart(data, chart_type, title)
                
            elif name == "visualize_geometry":
                shape_type = arguments["shape_type"]
                parameters = arguments["parameters"]
                title = arguments.get("title")
                
                return self.viz_helper.visualize_geometry(shape_type, parameters, title)
                
            else:
                raise MCPError(-32601, f"Unknown tool: {name}")
                
        except KeyError as e:
            raise MCPError(-32602, f"Missing required parameter: {e}")
        except Exception as e:
            logger.exception(f"Error executing tool {name}")
            raise MCPError(-32603, f"Tool execution error: {str(e)}")
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """Return list of available educational and reference resources."""
        return [
            {
                "uri": "math://concepts/elementary",
                "name": "Elementary Math Concepts",
                "description": "Basic arithmetic, place value, simple fractions",
                "mimeType": "text/plain"
            },
            {
                "uri": "math://concepts/middle",
                "name": "Middle School Math Concepts", 
                "description": "Fractions, decimals, percentages, basic algebra",
                "mimeType": "text/plain"
            },
            {
                "uri": "math://concepts/high_school",
                "name": "High School Math Concepts",
                "description": "Advanced algebra, geometry, trigonometry, pre-calculus",
                "mimeType": "text/plain"
            },
            {
                "uri": "math://formulas/geometry",
                "name": "Geometry Formulas",
                "description": "Common geometric formulas and equations",
                "mimeType": "text/plain"
            },
            {
                "uri": "math://formulas/algebra",
                "name": "Algebra Formulas",
                "description": "Algebraic formulas and identities",
                "mimeType": "text/plain"
            },
            {
                "uri": "viz://examples/charts",
                "name": "Chart Examples",
                "description": "Examples of different chart types and their data formats",
                "mimeType": "application/json"
            },
            {
                "uri": "viz://examples/functions",
                "name": "Function Plotting Examples",
                "description": "Examples of mathematical function expressions for plotting",
                "mimeType": "text/plain"
            }
        ]
    
    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """Read an educational or reference resource by URI."""
        
        # Math resources (inherited from math server)
        math_resources = {
            "math://concepts/elementary": {
                "contents": [
                    {
                        "type": "text",
                        "text": """Elementary Math Concepts

**Addition & Subtraction**
- Addition: Combining numbers to find a total
- Subtraction: Taking away or finding the difference
- Number line: Visual tool for understanding operations

**Multiplication & Division**
- Multiplication: Repeated addition or groups of equal size
- Division: Sharing equally or finding how many groups
- Times tables: Foundation for mental math

**Place Value**
- Ones, tens, hundreds places
- Reading and writing numbers
- Comparing numbers using <, >, =

**Basic Fractions**
- Parts of a whole
- Simple fraction addition/subtraction
- Comparing fractions"""
                    }
                ]
            },
            "math://concepts/middle": {
                "contents": [
                    {
                        "type": "text",
                        "text": """Middle School Math Concepts

**Fractions & Decimals**
- Equivalent fractions
- Adding/subtracting fractions with different denominators
- Converting between fractions and decimals
- Ordering fractions and decimals

**Percentages**
- Understanding percent as "out of 100"
- Converting between fractions, decimals, and percentages
- Finding percentages of numbers
- Percentage increase/decrease

**Basic Algebra**
- Variables and expressions
- Solving simple equations
- Graphing linear relationships
- Order of operations (PEMDAS)

**Geometry**
- Area and perimeter
- Volume of simple shapes
- Coordinate graphing
- Basic angle relationships"""
                    }
                ]
            },
            "math://concepts/high_school": {
                "contents": [
                    {
                        "type": "text",
                        "text": """High School Math Concepts

**Advanced Algebra**
- Quadratic equations and graphing
- Systems of equations
- Exponential and logarithmic functions
- Polynomial operations

**Geometry & Trigonometry**
- Pythagorean theorem applications
- Trigonometric ratios (sin, cos, tan)
- Circle theorems
- Volume and surface area

**Statistics & Probability**
- Mean, median, mode, range
- Standard deviation
- Probability calculations
- Data analysis and interpretation

**Pre-Calculus**
- Function composition
- Inverse functions
- Limits (introduction)
- Sequences and series"""
                    }
                ]
            },
            "math://formulas/geometry": {
                "contents": [
                    {
                        "type": "text",
                        "text": """Geometry Formulas

**Area Formulas**
- Rectangle: A = length × width
- Circle: A = π × r²
- Triangle: A = ½ × base × height
- Parallelogram: A = base × height
- Trapezoid: A = ½ × (base₁ + base₂) × height

**Volume Formulas**
- Rectangular prism: V = length × width × height
- Cylinder: V = π × r² × height
- Sphere: V = ⁴⁄₃ × π × r³
- Cone: V = ⅓ × π × r² × height

**Distance & Slope**
- Distance formula: d = √[(x₂-x₁)² + (y₂-y₁)²]
- Slope formula: m = (y₂-y₁)/(x₂-x₁)
- Midpoint formula: ((x₁+x₂)/2, (y₁+y₂)/2)

**Circle Properties**
- Circumference: C = 2πr
- Arc length: s = rθ (θ in radians)
- Sector area: A = ½r²θ"""
                    }
                ]
            },
            "math://formulas/algebra": {
                "contents": [
                    {
                        "type": "text",
                        "text": """Algebra Formulas

**Quadratic Formula**
- x = (-b ± √(b²-4ac))/(2a)
- For equations of the form ax² + bx + c = 0

**Exponent Rules**
- x^a × x^b = x^(a+b)
- x^a ÷ x^b = x^(a-b)
- (x^a)^b = x^(ab)
- x^0 = 1
- x^(-a) = 1/x^a

**Logarithm Properties**
- log(xy) = log(x) + log(y)
- log(x/y) = log(x) - log(y)
- log(x^n) = n × log(x)
- log_b(b^x) = x

**Factoring Patterns**
- Difference of squares: a² - b² = (a+b)(a-b)
- Perfect square trinomial: a² + 2ab + b² = (a+b)²
- Sum/difference of cubes: a³ ± b³ = (a ± b)(a² ∓ ab + b²)"""
                    }
                ]
            }
        }
        
        # Visualization resources
        viz_resources = {
            "viz://examples/charts": {
                "contents": [
                    {
                        "type": "text",
                        "text": """Chart Data Format Examples

**Line Chart:**
{
  "chart_type": "line",
  "data": {
    "x": [1, 2, 3, 4, 5],
    "y": [2, 4, 6, 8, 10]
  }
}

**Bar Chart:**
{
  "chart_type": "bar", 
  "data": {
    "categories": ["A", "B", "C"],
    "values": [10, 20, 15]
  }
}

**Scatter Plot:**
{
  "chart_type": "scatter",
  "data": {
    "x": [1, 2, 3, 4, 5],
    "y": [2, 4, 6, 8, 10],
    "colors": [1, 2, 3, 4, 5],
    "sizes": [20, 40, 60, 80, 100]
  }
}

**Pie Chart:**
{
  "chart_type": "pie",
  "data": {
    "labels": ["Category A", "Category B", "Category C"],
    "values": [30, 45, 25]
  }
}

**Histogram:**
{
  "chart_type": "histogram",
  "data": {
    "values": [1, 2, 2, 3, 3, 3, 4, 4, 5],
    "bins": 10
  }
}"""
                    }
                ]
            },
            "viz://examples/functions": {
                "contents": [
                    {
                        "type": "text",
                        "text": """Mathematical Function Examples for Plotting

**Linear Functions:**
- "x" - Simple line
- "2*x + 3" - Line with slope and intercept
- "-0.5*x + 4" - Negative slope

**Quadratic Functions:**
- "x**2" - Basic parabola
- "x**2 - 4*x + 3" - Parabola with roots
- "-2*x**2 + 8*x - 6" - Downward parabola

**Trigonometric Functions:**
- "sin(x)" - Sine wave
- "cos(x)" - Cosine wave
- "tan(x)" - Tangent function
- "2*sin(3*x)" - Amplitude and frequency modulation

**Exponential Functions:**
- "exp(x)" - Natural exponential
- "2**x" - Base 2 exponential
- "exp(-x**2)" - Gaussian function

**Logarithmic Functions:**
- "log(x)" - Natural logarithm
- "log(abs(x))" - Logarithm with absolute value

**Combined Functions:**
- "x*sin(x)" - Product of linear and sine
- "exp(-x**2)*cos(5*x)" - Modulated Gaussian
- "sqrt(abs(x))" - Square root function

**Note:** Use numpy functions: sin, cos, tan, exp, log, sqrt, abs, pi"""
                    }
                ]
            }
        }
        
        # Combine all resources
        all_resources = {**math_resources, **viz_resources}
        
        if uri not in all_resources:
            raise MCPError(-32601, f"Resource not found: {uri}")
        
        return all_resources[uri]


def main():
    """Main entry point for the unified MCP gateway server."""
    logging.basicConfig(level=logging.INFO)
    server = MCPGatewayServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
