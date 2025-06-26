#!/usr/bin/env python3
"""
MCP Math Server

A comprehensive mathematics server implementing the Model Context Protocol (MCP).
Provides mathematical calculations, equation solving, and concept explanations
covering elementary to high school level topics.
"""

import asyncio
import logging
import math
from typing import Any, Dict, List

from .utils.base_server import BaseMCPServer, MCPError
from .utils.math_utils import MathSolver

logger = logging.getLogger(__name__)


class MathServer(BaseMCPServer):
    """MCP server for mathematical calculations and problem solving."""
    
    def __init__(self):
        super().__init__("mcp-math-server", "1.0.0")
        self.solver = MathSolver()
        
    def get_server_info(self) -> Dict[str, Any]:
        """Return server information."""
        return {
            "name": self.name,
            "version": self.version,
            "description": "Expert mathematics server covering elementary to high school level topics"
        }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return server capabilities."""
        return {
            "tools": {"listChanged": False},
            "resources": {"subscribe": False, "listChanged": False}
        }
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Return list of available math tools."""
        return [
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
                "description": "Perform advanced mathematical operations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["power", "sqrt", "factorial", "abs", "round_number"],
                            "description": "The operation to perform"
                        },
                        "value": {"type": "number", "description": "Input value"},
                        "extra_param": {"type": "number", "description": "Extra parameter if needed", "default": 0}
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
                "description": "Solve linear and quadratic equations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "equation_type": {
                            "type": "string",
                            "enum": ["linear", "quadratic"],
                            "description": "Type of equation to solve"
                        },
                        "a": {"type": "number", "description": "Coefficient a"},
                        "b": {"type": "number", "description": "Coefficient b"},
                        "c": {"type": "number", "description": "Coefficient c (for quadratic)", "default": 0}
                    },
                    "required": ["equation_type", "a", "b"]
                }
            },
            {
                "name": "geometry",
                "description": "Calculate areas, distances, and other geometric properties",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "enum": ["area_circle", "area_rectangle", "area_triangle", "pythagorean", "distance", "slope", "midpoint"],
                            "description": "Geometric operation"
                        },
                        "values": {
                            "type": "array",
                            "items": {"type": "number"},
                            "description": "Array of values needed for the operation"
                        }
                    },
                    "required": ["operation", "values"]
                }
            },
            {
                "name": "trigonometry",
                "description": "Trigonometric functions (sin, cos, tan)",
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
                "description": "Logarithmic functions",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "log_type": {
                            "type": "string",
                            "enum": ["log", "log10"],
                            "description": "Type of logarithm"
                        },
                        "x": {"type": "number", "description": "Input value"},
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
                "description": "Calculate percentages",
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
                "description": "Safely evaluate mathematical expressions",
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
                "description": "Explain mathematical concepts with examples",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "concept": {
                            "type": "string",
                            "description": "Mathematical concept to explain"
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
            }
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a math tool with given arguments."""
        
        try:
            if name == "basic_arithmetic":
                operation = arguments["operation"]
                a = arguments["a"]
                b = arguments["b"]
                return self.solver.operations[operation](a, b)
                
            elif name == "advanced_operations":
                operation = arguments["operation"]
                value = arguments["value"]
                extra_param = arguments.get("extra_param", 0)
                
                if operation in ["power"]:
                    return self.solver.operations[operation](value, extra_param)
                elif operation in ["round_number"]:
                    return self.solver.operations[operation](value, int(extra_param))
                else:
                    return self.solver.operations[operation](value)
                    
            elif name == "number_theory":
                operation = arguments["operation"]
                a = arguments["a"]
                b = arguments.get("b", 0)
                
                if operation in ["gcd", "lcm"]:
                    return self.solver.operations[operation](a, b)
                else:
                    return self.solver.operations[operation](a)
                    
            elif name == "solve_equations":
                equation_type = arguments["equation_type"]
                a = arguments["a"]
                b = arguments["b"]
                c = arguments.get("c", 0)
                
                if equation_type == "linear":
                    return self.solver.operations["solve_linear"](a, b)
                else:
                    return self.solver.operations["solve_quadratic"](a, b, c)
                    
            elif name == "geometry":
                operation = arguments["operation"]
                values = arguments["values"]
                
                if operation == "area_circle":
                    return self.solver.operations[operation](values[0])
                elif operation in ["area_rectangle", "pythagorean"]:
                    return self.solver.operations[operation](values[0], values[1])
                elif operation == "area_triangle":
                    return self.solver.operations[operation](values[0], values[1])
                elif operation in ["distance", "slope", "midpoint"]:
                    return self.solver.operations[operation](values[0], values[1], values[2], values[3])
                    
            elif name == "trigonometry":
                function = arguments["function"]
                angle = arguments["angle"]
                unit = arguments.get("unit", "radians")
                return self.solver.operations[function](angle, unit)
                
            elif name == "logarithms":
                log_type = arguments["log_type"]
                x = arguments["x"]
                base = arguments.get("base", math.e)
                
                if log_type == "log10":
                    return self.solver.operations["log10"](x)
                else:
                    return self.solver.operations["log"](x, base)
                    
            elif name == "fractions":
                operation = arguments["operation"]
                
                if operation == "simplify_fraction":
                    return self.solver.operations[operation](arguments["numerator"], arguments["denominator"])
                elif operation == "convert_to_decimal":
                    return self.solver.operations[operation](arguments["numerator"], arguments["denominator"])
                elif operation == "convert_to_fraction":
                    return self.solver.operations[operation](arguments["decimal"])
                    
            elif name == "percentages":
                return self.solver.operations["percentage"](arguments["part"], arguments["whole"])
                
            elif name == "evaluate_expression":
                return self.solver.operations["evaluate_expression"](arguments["expression"])
                
            elif name == "explain_concept":
                return await self.solver.explain_concept(arguments["concept"], arguments.get("level", "middle"))
                
            else:
                raise MCPError(-32601, f"Unknown tool: {name}")
                
        except KeyError as e:
            raise MCPError(-32602, f"Missing required parameter: {e}")
        except Exception as e:
            logger.exception(f"Error executing tool {name}")
            raise MCPError(-32603, f"Tool execution error: {str(e)}")
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """Return list of available mathematical resources."""
        return [
            {
                "uri": "math://concepts/elementary",
                "name": "Elementary Math Concepts",
                "description": "Basic arithmetic and foundational concepts",
                "mimeType": "text/plain"
            },
            {
                "uri": "math://concepts/middle",
                "name": "Middle School Math Concepts", 
                "description": "Fractions, decimals, basic algebra",
                "mimeType": "text/plain"
            },
            {
                "uri": "math://concepts/high_school",
                "name": "High School Math Concepts",
                "description": "Advanced algebra, geometry, trigonometry",
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
            }
        ]
    
    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """Read a mathematical resource by URI."""
        
        resources = {
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
        
        if uri not in resources:
            raise MCPError(-32601, f"Resource not found: {uri}")
        
        return resources[uri]


def main():
    """Main entry point for the math server."""
    logging.basicConfig(level=logging.INFO)
    server = MathServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
