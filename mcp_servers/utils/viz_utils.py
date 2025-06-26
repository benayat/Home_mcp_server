"""
Visualization utilities for creating charts and graphs.

This module contains helper functions for the visualization MCP server.
"""

import base64
import io
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Set style for better looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class VisualizationHelper:
    """Helper class for creating various types of visualizations."""
    
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path("visualizations")
        self.output_dir.mkdir(exist_ok=True)
        
    def create_chart(
        self,
        chart_type: str,
        data: Dict[str, Any],
        title: Optional[str] = None,
        xlabel: Optional[str] = None,
        ylabel: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Create a chart based on the specified type and data."""
        
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if chart_type == "line":
                return self._create_line_chart(ax, data, title, xlabel, ylabel, **kwargs)
            elif chart_type == "bar":
                return self._create_bar_chart(ax, data, title, xlabel, ylabel, **kwargs)
            elif chart_type == "scatter":
                return self._create_scatter_chart(ax, data, title, xlabel, ylabel, **kwargs)
            elif chart_type == "pie":
                return self._create_pie_chart(ax, data, title, **kwargs)
            elif chart_type == "histogram":
                return self._create_histogram(ax, data, title, xlabel, ylabel, **kwargs)
            elif chart_type == "box":
                return self._create_box_plot(ax, data, title, xlabel, ylabel, **kwargs)
            else:
                return {
                    "error": f"Unsupported chart type: {chart_type}",
                    "supported_types": ["line", "bar", "scatter", "pie", "histogram", "box"]
                }
                
        except Exception as e:
            return {
                "error": f"Error creating chart: {str(e)}",
                "chart_type": chart_type
            }
        finally:
            plt.close(fig)
    
    def _create_line_chart(
        self, ax, data: Dict[str, Any], title: str, xlabel: str, ylabel: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a line chart."""
        
        x = data.get("x", [])
        y = data.get("y", [])
        
        if not x or not y:
            return {"error": "Line chart requires 'x' and 'y' data arrays"}
        
        if len(x) != len(y):
            return {"error": "x and y arrays must have the same length"}
        
        ax.plot(x, y, marker='o', linewidth=2, markersize=6)
        
        if title:
            ax.set_title(title, fontsize=16, fontweight='bold')
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=12)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=12)
        
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return self._save_chart(ax.figure, "line_chart")
    
    def _create_bar_chart(
        self, ax, data: Dict[str, Any], title: str, xlabel: str, ylabel: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a bar chart."""
        
        categories = data.get("categories", data.get("x", []))
        values = data.get("values", data.get("y", []))
        
        if not categories or not values:
            return {"error": "Bar chart requires 'categories' and 'values' data arrays"}
        
        if len(categories) != len(values):
            return {"error": "categories and values arrays must have the same length"}
        
        bars = ax.bar(categories, values, alpha=0.8)
        
        # Color bars with a gradient
        colors = plt.cm.viridis(np.linspace(0, 1, len(bars)))
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        
        if title:
            ax.set_title(title, fontsize=16, fontweight='bold')
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=12)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=12)
        
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        return self._save_chart(ax.figure, "bar_chart")
    
    def _create_scatter_chart(
        self, ax, data: Dict[str, Any], title: str, xlabel: str, ylabel: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a scatter plot."""
        
        x = data.get("x", [])
        y = data.get("y", [])
        
        if not x or not y:
            return {"error": "Scatter plot requires 'x' and 'y' data arrays"}
        
        if len(x) != len(y):
            return {"error": "x and y arrays must have the same length"}
        
        # Optional color and size data
        colors = data.get("colors", None)
        sizes = data.get("sizes", 50)
        
        scatter = ax.scatter(x, y, c=colors, s=sizes, alpha=0.7, edgecolors='w', linewidth=0.5)
        
        if title:
            ax.set_title(title, fontsize=16, fontweight='bold')
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=12)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=12)
        
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return self._save_chart(ax.figure, "scatter_plot")
    
    def _create_pie_chart(
        self, ax, data: Dict[str, Any], title: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a pie chart."""
        
        labels = data.get("labels", [])
        values = data.get("values", [])
        
        if not labels or not values:
            return {"error": "Pie chart requires 'labels' and 'values' data arrays"}
        
        if len(labels) != len(values):
            return {"error": "labels and values arrays must have the same length"}
        
        # Create pie chart with better colors
        colors = plt.cm.Set3(np.linspace(0, 1, len(values)))
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=labels, 
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            explode=[0.05] * len(values)  # Slightly separate all slices
        )
        
        # Improve text formatting
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        if title:
            ax.set_title(title, fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        
        return self._save_chart(ax.figure, "pie_chart")
    
    def _create_histogram(
        self, ax, data: Dict[str, Any], title: str, xlabel: str, ylabel: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a histogram."""
        
        values = data.get("values", data.get("x", []))
        bins = data.get("bins", 30)
        
        if not values:
            return {"error": "Histogram requires 'values' data array"}
        
        n, bins, patches = ax.hist(values, bins=bins, alpha=0.7, edgecolor='black', linewidth=0.5)
        
        # Color bars with a gradient
        colors = plt.cm.viridis(np.linspace(0, 1, len(patches)))
        for patch, color in zip(patches, colors):
            patch.set_facecolor(color)
        
        if title:
            ax.set_title(title, fontsize=16, fontweight='bold')
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=12)
        if ylabel:
            ax.set_ylabel(ylabel or "Frequency", fontsize=12)
        
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        return self._save_chart(ax.figure, "histogram")
    
    def _create_box_plot(
        self, ax, data: Dict[str, Any], title: str, xlabel: str, ylabel: str, **kwargs
    ) -> Dict[str, Any]:
        """Create a box plot."""
        
        values = data.get("values", [])
        labels = data.get("labels", None)
        
        if not values:
            return {"error": "Box plot requires 'values' data"}
        
        # Handle both single dataset and multiple datasets
        if isinstance(values[0], (int, float)):
            # Single dataset
            box_data = [values]
            box_labels = labels or ["Data"]
        else:
            # Multiple datasets
            box_data = values
            box_labels = labels or [f"Dataset {i+1}" for i in range(len(values))]
        
        bp = ax.boxplot(box_data, labels=box_labels, patch_artist=True)
        
        # Color the boxes
        colors = plt.cm.Set2(np.linspace(0, 1, len(box_data)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        if title:
            ax.set_title(title, fontsize=16, fontweight='bold')
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=12)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=12)
        
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        
        return self._save_chart(ax.figure, "box_plot")
    
    def plot_function(
        self,
        expression: str,
        x_range: Tuple[float, float] = (-10, 10),
        num_points: int = 1000,
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """Plot a mathematical function."""
        
        try:
            x_min, x_max = x_range
            x = np.linspace(x_min, x_max, num_points)
            
            # Prepare safe evaluation environment
            safe_dict = {
                "x": x,
                "np": np,
                "sin": np.sin,
                "cos": np.cos,
                "tan": np.tan,
                "exp": np.exp,
                "log": np.log,
                "sqrt": np.sqrt,
                "abs": np.abs,
                "pi": np.pi,
                "e": np.e,
                "__builtins__": {}
            }
            
            # Evaluate the expression
            y = eval(expression, safe_dict)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(x, y, linewidth=2, color='blue')
            
            ax.set_title(title or f"Plot of y = {expression}", fontsize=16, fontweight='bold')
            ax.set_xlabel("x", fontsize=12)
            ax.set_ylabel("y", fontsize=12)
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='k', linewidth=0.5)
            ax.axvline(x=0, color='k', linewidth=0.5)
            
            plt.tight_layout()
            
            result = self._save_chart(fig, "function_plot")
            plt.close(fig)
            
            return result
            
        except Exception as e:
            return {
                "error": f"Error plotting function '{expression}': {str(e)}",
                "suggestion": "Check that the expression uses valid mathematical operations"
            }
    
    def create_statistics_chart(
        self,
        data: List[float],
        chart_type: str = "all",
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create statistical visualizations for a dataset."""
        
        if not data:
            return {"error": "No data provided for statistical analysis"}
        
        try:
            data_array = np.array(data)
            
            if chart_type == "all":
                # Create a multi-panel statistical summary
                fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
                
                # Histogram
                ax1.hist(data_array, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
                ax1.set_title("Distribution", fontweight='bold')
                ax1.set_xlabel("Value")
                ax1.set_ylabel("Frequency")
                ax1.grid(True, alpha=0.3)
                
                # Box plot
                ax2.boxplot(data_array, vert=True)
                ax2.set_title("Box Plot", fontweight='bold')
                ax2.set_ylabel("Value")
                ax2.grid(True, alpha=0.3)
                
                # Q-Q plot approximation
                sorted_data = np.sort(data_array)
                n = len(sorted_data)
                theoretical_quantiles = np.linspace(0, 1, n)
                ax3.scatter(theoretical_quantiles, sorted_data, alpha=0.7)
                ax3.plot([0, 1], [np.min(sorted_data), np.max(sorted_data)], 'r--')
                ax3.set_title("Quantile Plot", fontweight='bold')
                ax3.set_xlabel("Theoretical Quantiles")
                ax3.set_ylabel("Sample Quantiles")
                ax3.grid(True, alpha=0.3)
                
                # Statistics summary
                stats_text = self._calculate_statistics(data_array)
                ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes, fontsize=10,
                        verticalalignment='top', fontfamily='monospace')
                ax4.set_title("Statistics Summary", fontweight='bold')
                ax4.axis('off')
                
                if title:
                    fig.suptitle(title, fontsize=16, fontweight='bold')
                
                plt.tight_layout()
                result = self._save_chart(fig, "statistics_summary")
                plt.close(fig)
                
                return result
            
            else:
                return {"error": f"Unsupported statistics chart type: {chart_type}"}
                
        except Exception as e:
            return {
                "error": f"Error creating statistics chart: {str(e)}",
                "data_sample": data[:5] if len(data) > 5 else data
            }
    
    def visualize_geometry(
        self,
        shape_type: str,
        parameters: Dict[str, Any],
        title: Optional[str] = None
    ) -> Dict[str, Any]:
        """Visualize geometric shapes."""
        
        try:
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.set_aspect('equal')
            
            if shape_type == "circle":
                return self._draw_circle(ax, parameters, title)
            elif shape_type == "rectangle":
                return self._draw_rectangle(ax, parameters, title)
            elif shape_type == "triangle":
                return self._draw_triangle(ax, parameters, title)
            elif shape_type == "polygon":
                return self._draw_polygon(ax, parameters, title)
            else:
                return {
                    "error": f"Unsupported shape type: {shape_type}",
                    "supported_shapes": ["circle", "rectangle", "triangle", "polygon"]
                }
                
        except Exception as e:
            return {
                "error": f"Error visualizing {shape_type}: {str(e)}",
                "parameters": parameters
            }
        finally:
            if 'fig' in locals():
                plt.close(fig)
    
    def _draw_circle(self, ax, params: Dict[str, Any], title: str) -> Dict[str, Any]:
        """Draw a circle."""
        radius = params.get("radius", 1)
        center = params.get("center", [0, 0])
        
        circle = plt.Circle(center, radius, fill=False, color='blue', linewidth=2)
        ax.add_patch(circle)
        
        # Add center point
        ax.plot(center[0], center[1], 'ro', markersize=5)
        
        # Set limits
        margin = radius * 0.2
        ax.set_xlim(center[0] - radius - margin, center[0] + radius + margin)
        ax.set_ylim(center[1] - radius - margin, center[1] + radius + margin)
        
        ax.set_title(title or f"Circle (radius={radius})", fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return self._save_chart(ax.figure, "circle")
    
    def _draw_rectangle(self, ax, params: Dict[str, Any], title: str) -> Dict[str, Any]:
        """Draw a rectangle."""
        width = params.get("width", 2)
        height = params.get("height", 1)
        center = params.get("center", [0, 0])
        
        x = center[0] - width/2
        y = center[1] - height/2
        
        rect = plt.Rectangle((x, y), width, height, fill=False, color='blue', linewidth=2)
        ax.add_patch(rect)
        
        # Add center point
        ax.plot(center[0], center[1], 'ro', markersize=5)
        
        # Set limits
        margin = max(width, height) * 0.2
        ax.set_xlim(x - margin, x + width + margin)
        ax.set_ylim(y - margin, y + height + margin)
        
        ax.set_title(title or f"Rectangle ({width}×{height})", fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return self._save_chart(ax.figure, "rectangle")
    
    def _draw_triangle(self, ax, params: Dict[str, Any], title: str) -> Dict[str, Any]:
        """Draw a triangle."""
        vertices = params.get("vertices", [[0, 0], [1, 0], [0.5, 1]])
        
        if len(vertices) != 3:
            return {"error": "Triangle requires exactly 3 vertices"}
        
        # Close the triangle
        triangle_x = [v[0] for v in vertices] + [vertices[0][0]]
        triangle_y = [v[1] for v in vertices] + [vertices[0][1]]
        
        ax.plot(triangle_x, triangle_y, 'b-', linewidth=2)
        ax.fill(triangle_x[:-1], triangle_y[:-1], alpha=0.3, color='lightblue')
        
        # Mark vertices
        for i, vertex in enumerate(vertices):
            ax.plot(vertex[0], vertex[1], 'ro', markersize=5)
            ax.annotate(f'V{i+1}', (vertex[0], vertex[1]), xytext=(5, 5), 
                       textcoords='offset points')
        
        # Set limits
        all_x = [v[0] for v in vertices]
        all_y = [v[1] for v in vertices]
        margin = max(max(all_x) - min(all_x), max(all_y) - min(all_y)) * 0.2
        ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
        ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
        
        ax.set_title(title or "Triangle", fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return self._save_chart(ax.figure, "triangle")
    
    def _draw_polygon(self, ax, params: Dict[str, Any], title: str) -> Dict[str, Any]:
        """Draw a polygon."""
        vertices = params.get("vertices", [])
        
        if len(vertices) < 3:
            return {"error": "Polygon requires at least 3 vertices"}
        
        # Close the polygon
        polygon_x = [v[0] for v in vertices] + [vertices[0][0]]
        polygon_y = [v[1] for v in vertices] + [vertices[0][1]]
        
        ax.plot(polygon_x, polygon_y, 'b-', linewidth=2)
        ax.fill(polygon_x[:-1], polygon_y[:-1], alpha=0.3, color='lightblue')
        
        # Mark vertices
        for i, vertex in enumerate(vertices):
            ax.plot(vertex[0], vertex[1], 'ro', markersize=5)
            ax.annotate(f'V{i+1}', (vertex[0], vertex[1]), xytext=(5, 5), 
                       textcoords='offset points')
        
        # Set limits
        all_x = [v[0] for v in vertices]
        all_y = [v[1] for v in vertices]
        margin = max(max(all_x) - min(all_x), max(all_y) - min(all_y)) * 0.2
        ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
        ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
        
        ax.set_title(title or f"Polygon ({len(vertices)} vertices)", fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return self._save_chart(ax.figure, "polygon")
    
    def _calculate_statistics(self, data: np.ndarray) -> str:
        """Calculate basic statistics for a dataset."""
        stats = {
            "Count": len(data),
            "Mean": np.mean(data),
            "Median": np.median(data),
            "Std Dev": np.std(data),
            "Min": np.min(data),
            "Max": np.max(data),
            "Q1": np.percentile(data, 25),
            "Q3": np.percentile(data, 75)
        }
        
        text = ""
        for key, value in stats.items():
            if key == "Count":
                text += f"{key}: {value}\n"
            else:
                text += f"{key}: {value:.3f}\n"
        
        return text
    
    def _save_chart(self, figure, chart_name: str) -> Dict[str, Any]:
        """Save chart and return result with image data."""
        
        # Save to file
        timestamp = int(plt.time.time() * 1000)
        filename = f"{chart_name}_{timestamp}.png"
        filepath = self.output_dir / filename
        
        figure.savefig(filepath, dpi=300, bbox_inches='tight', 
                      facecolor='white', edgecolor='none')
        
        # Convert to base64 for inline display
        buffer = io.BytesIO()
        figure.savefig(buffer, format='png', dpi=150, bbox_inches='tight',
                      facecolor='white', edgecolor='none')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        buffer.close()
        
        return {
            "success": True,
            "chart_type": chart_name,
            "file_path": str(filepath),
            "filename": filename,
            "image_base64": image_base64,
            "description": f"Chart saved as {filename}"
        }
