"""
Mathematical utilities and calculation functions.

This module contains the core mathematical solver functions used by the math MCP server.
"""

import math
import re
from decimal import Decimal, getcontext
from fractions import Fraction
from typing import Any, Dict, List, Union

# Set high precision for decimal calculations
getcontext().prec = 50


class MathSolver:
    """Comprehensive math problem solver with detailed explanations."""
    
    def __init__(self):
        self.operations = {
            'add': self._add,
            'subtract': self._subtract,
            'multiply': self._multiply,
            'divide': self._divide,
            'power': self._power,
            'sqrt': self._sqrt,
            'factorial': self._factorial,
            'gcd': self._gcd,
            'lcm': self._lcm,
            'prime_factors': self._prime_factors,
            'is_prime': self._is_prime,
            'solve_linear': self._solve_linear,
            'solve_quadratic': self._solve_quadratic,
            'percentage': self._percentage,
            'area_circle': self._area_circle,
            'area_rectangle': self._area_rectangle,
            'area_triangle': self._area_triangle,
            'pythagorean': self._pythagorean,
            'distance': self._distance,
            'slope': self._slope,
            'midpoint': self._midpoint,
            'evaluate_expression': self._evaluate_expression,
            'simplify_fraction': self._simplify_fraction,
            'convert_to_decimal': self._convert_to_decimal,
            'convert_to_fraction': self._convert_to_fraction,
            'sin': self._sin,
            'cos': self._cos,
            'tan': self._tan,
            'log': self._log,
            'log10': self._log10,
            'abs': self._abs,
            'round_number': self._round_number
        }

    def _add(self, a: float, b: float) -> Dict[str, Any]:
        result = a + b
        return {
            'result': result,
            'explanation': f"Addition: {a} + {b} = {result}",
            'steps': [f"Add {a} and {b}", f"Result: {result}"]
        }

    def _subtract(self, a: float, b: float) -> Dict[str, Any]:
        result = a - b
        return {
            'result': result,
            'explanation': f"Subtraction: {a} - {b} = {result}",
            'steps': [f"Subtract {b} from {a}", f"Result: {result}"]
        }

    def _multiply(self, a: float, b: float) -> Dict[str, Any]:
        result = a * b
        return {
            'result': result,
            'explanation': f"Multiplication: {a} × {b} = {result}",
            'steps': [f"Multiply {a} by {b}", f"Result: {result}"]
        }

    def _divide(self, a: float, b: float) -> Dict[str, Any]:
        if b == 0:
            return {
                'error': 'Division by zero is undefined',
                'explanation': 'Cannot divide by zero'
            }
        result = a / b
        return {
            'result': result,
            'explanation': f"Division: {a} ÷ {b} = {result}",
            'steps': [f"Divide {a} by {b}", f"Result: {result}"]
        }

    def _power(self, base: float, exponent: float) -> Dict[str, Any]:
        try:
            result = base ** exponent
            return {
                'result': result,
                'explanation': f"Exponentiation: {base}^{exponent} = {result}",
                'steps': [f"Raise {base} to the power of {exponent}", f"Result: {result}"]
            }
        except (OverflowError, ValueError) as e:
            return {
                'error': f'Error in power calculation: {str(e)}',
                'explanation': 'Power calculation resulted in an error'
            }

    def _sqrt(self, n: float) -> Dict[str, Any]:
        if n < 0:
            return {
                'error': 'Square root of negative number is not real',
                'explanation': 'Cannot take square root of negative numbers in real numbers'
            }
        result = math.sqrt(n)
        return {
            'result': result,
            'explanation': f"Square root: √{n} = {result}",
            'steps': [f"Calculate square root of {n}", f"Result: {result}"]
        }

    def _factorial(self, n: float) -> Dict[str, Any]:
        if n < 0 or n != int(n):
            return {
                'error': 'Factorial is only defined for non-negative integers',
                'explanation': 'Factorial requires a non-negative integer'
            }
        
        n = int(n)
        if n > 170:  # Prevent overflow
            return {
                'error': 'Number too large for factorial calculation',
                'explanation': 'Factorial of numbers > 170 causes overflow'
            }
        
        result = math.factorial(n)
        return {
            'result': result,
            'explanation': f"Factorial: {n}! = {result}",
            'steps': [f"Calculate {n}!", f"Result: {result}"]
        }

    def _gcd(self, a: int, b: int) -> Dict[str, Any]:
        a, b = int(a), int(b)
        result = math.gcd(abs(a), abs(b))
        return {
            'result': result,
            'explanation': f"Greatest Common Divisor of {a} and {b} is {result}",
            'steps': [f"Find GCD of {a} and {b}", f"Result: {result}"]
        }

    def _lcm(self, a: int, b: int) -> Dict[str, Any]:
        a, b = int(a), int(b)
        if a == 0 or b == 0:
            return {
                'result': 0,
                'explanation': 'LCM with zero is zero',
                'steps': ['One number is zero', 'LCM = 0']
            }
        
        gcd_val = math.gcd(abs(a), abs(b))
        result = abs(a * b) // gcd_val
        return {
            'result': result,
            'explanation': f"Least Common Multiple of {a} and {b} is {result}",
            'steps': [
                f"LCM = |a × b| / GCD(a, b)",
                f"GCD({a}, {b}) = {gcd_val}",
                f"LCM = |{a} × {b}| / {gcd_val} = {result}"
            ]
        }

    def _prime_factors(self, n: int) -> Dict[str, Any]:
        n = int(abs(n))
        if n < 2:
            return {
                'result': [],
                'explanation': f"{n} has no prime factors",
                'steps': ['Numbers less than 2 have no prime factors']
            }
        
        factors = []
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors.append(d)
                n //= d
            d += 1
        if n > 1:
            factors.append(n)
        
        return {
            'result': factors,
            'explanation': f"Prime factors: {factors}",
            'steps': [f"Factor {int(abs(n))}", f"Prime factors: {factors}"]
        }

    def _is_prime(self, n: float) -> Dict[str, Any]:
        n = int(n)
        if n < 2:
            return {
                'result': False,
                'explanation': f"{n} is not prime (numbers < 2 are not prime)",
                'steps': [f"Check if {n} is prime", "Numbers less than 2 are not prime"]
            }
        
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return {
                    'result': False,
                    'explanation': f"{n} is not prime (divisible by {i})",
                    'steps': [f"Check divisors of {n}", f"Found divisor: {i}", "Therefore not prime"]
                }
        
        return {
            'result': True,
            'explanation': f"{n} is prime",
            'steps': [f"Check all divisors up to √{n}", "No divisors found", "Therefore prime"]
        }

    def _solve_linear(self, a: float, b: float) -> Dict[str, Any]:
        """Solve linear equation ax + b = 0"""
        if a == 0:
            if b == 0:
                return {
                    'result': 'infinite solutions',
                    'explanation': '0x + 0 = 0 is always true',
                    'steps': ['The equation 0 = 0 is always true', 'Therefore infinite solutions']
                }
            else:
                return {
                    'result': 'no solution',
                    'explanation': f'0x + {b} = 0 is impossible',
                    'steps': [f'The equation {b} = 0 is false', 'Therefore no solution']
                }
        
        result = -b / a
        return {
            'result': result,
            'explanation': f"Linear equation: {a}x + {b} = 0, solution: x = {result}",
            'steps': [
                f"{a}x + {b} = 0",
                f"{a}x = {-b}",
                f"x = {-b}/{a} = {result}"
            ]
        }

    def _solve_quadratic(self, a: float, b: float, c: float) -> Dict[str, Any]:
        """Solve quadratic equation ax² + bx + c = 0"""
        if a == 0:
            return self._solve_linear(b, c)
        
        discriminant = b**2 - 4*a*c
        
        if discriminant < 0:
            return {
                'result': 'no real solutions',
                'explanation': f"Discriminant = {discriminant} < 0, no real solutions",
                'steps': [
                    f"For {a}x² + {b}x + {c} = 0",
                    f"Discriminant = b² - 4ac = {b}² - 4({a})({c}) = {discriminant}",
                    "Since discriminant < 0, no real solutions"
                ]
            }
        elif discriminant == 0:
            x = -b / (2*a)
            return {
                'result': [x],
                'explanation': f"One solution (repeated root): x = {x}",
                'steps': [
                    f"For {a}x² + {b}x + {c} = 0",
                    f"Discriminant = {discriminant} = 0",
                    f"x = -b/(2a) = {-b}/(2×{a}) = {x}"
                ]
            }
        else:
            sqrt_discriminant = math.sqrt(discriminant)
            x1 = (-b + sqrt_discriminant) / (2*a)
            x2 = (-b - sqrt_discriminant) / (2*a)
            return {
                'result': [x1, x2],
                'explanation': f"Two solutions: x₁ = {x1}, x₂ = {x2}",
                'steps': [
                    f"For {a}x² + {b}x + {c} = 0",
                    f"Discriminant = {discriminant}",
                    f"x = (-b ± √discriminant)/(2a)",
                    f"x₁ = ({-b} + √{discriminant})/(2×{a}) = {x1}",
                    f"x₂ = ({-b} - √{discriminant})/(2×{a}) = {x2}"
                ]
            }

    def _percentage(self, part: float, whole: float) -> Dict[str, Any]:
        if whole == 0:
            return {
                'error': 'Cannot calculate percentage with zero as whole',
                'explanation': 'Division by zero in percentage calculation'
            }
        
        result = (part / whole) * 100
        return {
            'result': result,
            'explanation': f"{part} is {result}% of {whole}",
            'steps': [
                f"Percentage = (part/whole) × 100",
                f"Percentage = ({part}/{whole}) × 100 = {result}%"
            ]
        }

    def _area_circle(self, radius: float) -> Dict[str, Any]:
        area = math.pi * radius**2
        return {
            'result': area,
            'explanation': f"Area of circle with radius {radius} is {area}",
            'steps': [
                f"Area = π × r²",
                f"Area = π × {radius}² = {area}"
            ]
        }

    def _area_rectangle(self, length: float, width: float) -> Dict[str, Any]:
        area = length * width
        return {
            'result': area,
            'explanation': f"Area of rectangle with length {length} and width {width} is {area}",
            'steps': [
                f"Area = length × width",
                f"Area = {length} × {width} = {area}"
            ]
        }

    def _area_triangle(self, base: float, height: float) -> Dict[str, Any]:
        area = 0.5 * base * height
        return {
            'result': area,
            'explanation': f"Area of triangle with base {base} and height {height} is {area}",
            'steps': [
                f"Area = ½ × base × height",
                f"Area = ½ × {base} × {height} = {area}"
            ]
        }

    def _pythagorean(self, a: float, b: float) -> Dict[str, Any]:
        c = math.sqrt(a**2 + b**2)
        return {
            'result': c,
            'explanation': f"Hypotenuse of right triangle with legs {a} and {b} is {c}",
            'steps': [
                f"Pythagorean theorem: c² = a² + b²",
                f"c² = {a}² + {b}² = {a**2} + {b**2} = {a**2 + b**2}",
                f"c = √{a**2 + b**2} = {c}"
            ]
        }

    def _distance(self, x1: float, y1: float, x2: float, y2: float) -> Dict[str, Any]:
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return {
            'result': distance,
            'explanation': f"Distance between ({x1}, {y1}) and ({x2}, {y2}) is {distance}",
            'steps': [
                f"Distance formula: d = √[(x₂-x₁)² + (y₂-y₁)²]",
                f"d = √[({x2}-{x1})² + ({y2}-{y1})²]",
                f"d = √[{x2-x1}² + {y2-y1}²] = √[{(x2-x1)**2} + {(y2-y1)**2}] = {distance}"
            ]
        }

    def _slope(self, x1: float, y1: float, x2: float, y2: float) -> Dict[str, Any]:
        if x2 - x1 == 0:
            return {
                'result': 'undefined',
                'explanation': 'Slope is undefined (vertical line)',
                'steps': ['x₂ - x₁ = 0', 'Division by zero', 'Slope is undefined']
            }
        
        slope = (y2 - y1) / (x2 - x1)
        return {
            'result': slope,
            'explanation': f"Slope between ({x1}, {y1}) and ({x2}, {y2}) is {slope}",
            'steps': [
                f"Slope formula: m = (y₂-y₁)/(x₂-x₁)",
                f"m = ({y2}-{y1})/({x2}-{x1}) = {y2-y1}/{x2-x1} = {slope}"
            ]
        }

    def _midpoint(self, x1: float, y1: float, x2: float, y2: float) -> Dict[str, Any]:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        return {
            'result': [mid_x, mid_y],
            'explanation': f"Midpoint between ({x1}, {y1}) and ({x2}, {y2}) is ({mid_x}, {mid_y})",
            'steps': [
                f"Midpoint formula: ((x₁+x₂)/2, (y₁+y₂)/2)",
                f"Midpoint = (({x1}+{x2})/2, ({y1}+{y2})/2) = ({mid_x}, {mid_y})"
            ]
        }

    def _evaluate_expression(self, expression: str) -> Dict[str, Any]:
        """Safely evaluate mathematical expressions"""
        try:
            # Remove spaces and validate expression
            expression = expression.replace(' ', '')
            
            # Only allow safe mathematical operations
            allowed_chars = set('0123456789+-*/().^')
            if not all(c in allowed_chars for c in expression):
                return {
                    'error': 'Invalid characters in expression',
                    'explanation': 'Only numbers and basic operators (+, -, *, /, ^, parentheses) are allowed'
                }
            
            # Replace ^ with ** for Python exponentiation
            expression = expression.replace('^', '**')
            
            # Evaluate the expression
            result = eval(expression, {"__builtins__": {}}, {})
            
            return {
                'result': result,
                'explanation': f"Expression evaluation: {expression} = {result}",
                'steps': [f"Evaluate: {expression}", f"Result: {result}"]
            }
        except Exception as e:
            return {
                'error': f'Error evaluating expression: {str(e)}',
                'explanation': 'Invalid mathematical expression'
            }

    def _simplify_fraction(self, numerator: int, denominator: int) -> Dict[str, Any]:
        if denominator == 0:
            return {
                'error': 'Denominator cannot be zero',
                'explanation': 'Division by zero is undefined'
            }
        
        fraction = Fraction(int(numerator), int(denominator))
        return {
            'result': [fraction.numerator, fraction.denominator],
            'explanation': f"Simplified fraction: {numerator}/{denominator} = {fraction.numerator}/{fraction.denominator}",
            'steps': [
                f"Original fraction: {numerator}/{denominator}",
                f"GCD of {numerator} and {denominator} is {math.gcd(abs(int(numerator)), abs(int(denominator)))}",
                f"Simplified: {fraction.numerator}/{fraction.denominator}"
            ]
        }

    def _convert_to_decimal(self, numerator: int, denominator: int) -> Dict[str, Any]:
        if denominator == 0:
            return {
                'error': 'Denominator cannot be zero',
                'explanation': 'Division by zero is undefined'
            }
        
        decimal = float(numerator) / float(denominator)
        return {
            'result': decimal,
            'explanation': f"Fraction to decimal: {numerator}/{denominator} = {decimal}",
            'steps': [f"Divide {numerator} by {denominator}", f"Result: {decimal}"]
        }

    def _convert_to_fraction(self, decimal: float) -> Dict[str, Any]:
        fraction = Fraction(decimal).limit_denominator(1000)
        return {
            'result': [fraction.numerator, fraction.denominator],
            'explanation': f"Decimal to fraction: {decimal} = {fraction.numerator}/{fraction.denominator}",
            'steps': [f"Convert {decimal} to fraction", f"Result: {fraction.numerator}/{fraction.denominator}"]
        }

    def _sin(self, angle: float, unit: str = 'radians') -> Dict[str, Any]:
        if unit == 'degrees':
            angle_rad = math.radians(angle)
            result = math.sin(angle_rad)
            explanation = f"sin({angle}°) = {result}"
        else:
            result = math.sin(angle)
            explanation = f"sin({angle}) = {result}"
        
        return {
            'result': result,
            'explanation': explanation,
            'steps': [f"Calculate sine of {angle} {unit}", f"Result: {result}"]
        }

    def _cos(self, angle: float, unit: str = 'radians') -> Dict[str, Any]:
        if unit == 'degrees':
            angle_rad = math.radians(angle)
            result = math.cos(angle_rad)
            explanation = f"cos({angle}°) = {result}"
        else:
            result = math.cos(angle)
            explanation = f"cos({angle}) = {result}"
        
        return {
            'result': result,
            'explanation': explanation,
            'steps': [f"Calculate cosine of {angle} {unit}", f"Result: {result}"]
        }

    def _tan(self, angle: float, unit: str = 'radians') -> Dict[str, Any]:
        if unit == 'degrees':
            angle_rad = math.radians(angle)
            # Check for undefined values
            if abs(math.cos(angle_rad)) < 1e-10:
                return {
                    'result': 'undefined',
                    'explanation': f"tan({angle}°) is undefined (cosine is zero)",
                    'steps': [f"tan({angle}°) = sin({angle}°)/cos({angle}°)", "cos is zero", "Therefore undefined"]
                }
            result = math.tan(angle_rad)
            explanation = f"tan({angle}°) = {result}"
        else:
            if abs(math.cos(angle)) < 1e-10:
                return {
                    'result': 'undefined',
                    'explanation': f"tan({angle}) is undefined (cosine is zero)",
                    'steps': [f"tan({angle}) = sin({angle})/cos({angle})", "cos is zero", "Therefore undefined"]
                }
            result = math.tan(angle)
            explanation = f"tan({angle}) = {result}"
        
        return {
            'result': result,
            'explanation': explanation,
            'steps': [f"Calculate tangent of {angle} {unit}", f"Result: {result}"]
        }

    def _log(self, x: float, base: float = math.e) -> Dict[str, Any]:
        if x <= 0:
            return {
                'error': 'Logarithm undefined for non-positive numbers',
                'explanation': 'Logarithm is only defined for positive real numbers'
            }
        if base <= 0 or base == 1:
            return {
                'error': 'Invalid logarithm base',
                'explanation': 'Logarithm base must be positive and not equal to 1'
            }
        
        if base == math.e:
            result = math.log(x)
            explanation = f"Natural logarithm: ln({x}) = {result}"
        else:
            result = math.log(x) / math.log(base)
            explanation = f"Logarithm base {base}: log_{base}({x}) = {result}"
        
        return {
            'result': result,
            'explanation': explanation,
            'steps': [f"Calculate logarithm of {x}", f"Result: {result}"]
        }

    def _log10(self, x: float) -> Dict[str, Any]:
        if x <= 0:
            return {
                'error': 'Logarithm undefined for non-positive numbers',
                'explanation': 'Logarithm is only defined for positive real numbers'
            }
        
        result = math.log10(x)
        return {
            'result': result,
            'explanation': f"Common logarithm: log₁₀({x}) = {result}",
            'steps': [f"Calculate log base 10 of {x}", f"Result: {result}"]
        }

    def _abs(self, x: float) -> Dict[str, Any]:
        result = abs(x)
        return {
            'result': result,
            'explanation': f"Absolute value: |{x}| = {result}",
            'steps': [f"Take absolute value of {x}", f"Result: {result}"]
        }

    def _round_number(self, x: float, decimals: int = 0) -> Dict[str, Any]:
        result = round(x, decimals)
        return {
            'result': result,
            'explanation': f"Round {x} to {decimals} decimal places: {result}",
            'steps': [f"Round {x} to {decimals} decimal places", f"Result: {result}"]
        }

    async def explain_concept(self, concept: str, level: str = "middle") -> Dict[str, Any]:
        """Explain mathematical concepts at appropriate level"""
        explanations = {
            "elementary": {
                "addition": {
                    "explanation": "Addition means putting numbers together to find the total.",
                    "example": "If you have 3 apples and get 2 more, you add: 3 + 2 = 5 apples total.",
                    "steps": ["Count the first group", "Count the second group", "Count them all together"]
                },
                "subtraction": {
                    "explanation": "Subtraction means taking away or finding the difference.",
                    "example": "If you have 8 cookies and eat 3, you subtract: 8 - 3 = 5 cookies left.",
                    "steps": ["Start with the bigger number", "Take away the smaller number", "Count what's left"]
                },
                "multiplication": {
                    "explanation": "Multiplication is repeated addition or groups of equal size.",
                    "example": "3 groups of 4 objects each: 3 × 4 = 4 + 4 + 4 = 12",
                    "steps": ["Count the number of groups", "Count how many in each group", "Add all groups together"]
                },
                "division": {
                    "explanation": "Division means sharing equally or finding how many groups.",
                    "example": "12 candies shared among 3 children: 12 ÷ 3 = 4 candies each",
                    "steps": ["Start with the total", "Decide how many groups", "Share equally among groups"]
                }
            },
            "middle": {
                "fractions": {
                    "explanation": "Fractions represent parts of a whole, written as numerator/denominator.",
                    "example": "3/4 means 3 parts out of 4 equal parts total",
                    "steps": ["Denominator shows total parts", "Numerator shows parts we have", "Can be simplified by dividing by GCD"]
                },
                "decimals": {
                    "explanation": "Decimals are another way to write fractions using place value.",
                    "example": "0.75 = 75/100 = 3/4",
                    "steps": ["Each place represents a power of 10", "Can convert to/from fractions", "Useful for precise calculations"]
                },
                "percentages": {
                    "explanation": "Percentages mean 'out of 100' and show parts of a whole.",
                    "example": "25% = 25/100 = 0.25 = 1/4",
                    "steps": ["Percent means per hundred", "Multiply by 100 to convert from decimal", "Divide by 100 to convert to decimal"]
                },
                "algebra_basics": {
                    "explanation": "Algebra uses letters (variables) to represent unknown numbers.",
                    "example": "If x + 5 = 12, then x = 7",
                    "steps": ["Variables represent unknown values", "Equations show relationships", "Solve by isolating the variable"]
                }
            },
            "high_school": {
                "quadratic_equations": {
                    "explanation": "Quadratic equations have the form ax² + bx + c = 0 and can have 0, 1, or 2 real solutions.",
                    "example": "x² - 5x + 6 = 0 has solutions x = 2 and x = 3",
                    "steps": ["Use quadratic formula: x = (-b ± √(b²-4ac))/(2a)", "Check discriminant b²-4ac", "If positive: 2 solutions, if zero: 1 solution, if negative: no real solutions"]
                },
                "trigonometry": {
                    "explanation": "Trigonometry studies relationships between angles and sides in triangles.",
                    "example": "In a right triangle, sin(θ) = opposite/hypotenuse",
                    "steps": ["SOH: Sin = Opposite/Hypotenuse", "CAH: Cos = Adjacent/Hypotenuse", "TOA: Tan = Opposite/Adjacent"]
                },
                "logarithms": {
                    "explanation": "Logarithms are the inverse of exponential functions.",
                    "example": "If 2³ = 8, then log₂(8) = 3",
                    "steps": ["log_b(x) asks 'what power gives x?'", "Natural log (ln) uses base e", "Common log uses base 10"]
                },
                "functions": {
                    "explanation": "Functions are rules that assign exactly one output to each input.",
                    "example": "f(x) = 2x + 1 assigns f(3) = 7",
                    "steps": ["Domain: all possible inputs", "Range: all possible outputs", "Can be linear, quadratic, exponential, etc."]
                }
            }
        }
        
        concept_lower = concept.lower()
        level_explanations = explanations.get(level, explanations["middle"])
        
        # Find matching concept
        for key, explanation in level_explanations.items():
            if concept_lower in key or key in concept_lower:
                return {
                    "concept": concept,
                    "level": level,
                    "explanation": explanation["explanation"],
                    "example": explanation["example"],
                    "steps": explanation["steps"]
                }
        
        return {
            "concept": concept,
            "level": level,
            "explanation": f"Concept '{concept}' not found in {level} level explanations. Available concepts: {', '.join(level_explanations.keys())}",
            "example": "Please try a different concept or level.",
            "steps": []
        }
