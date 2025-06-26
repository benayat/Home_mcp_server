# Quick Start Guide

## Installation

### From Source
```bash
# Clone the repository (if you have it in a git repo)
# git clone <repository-url>
# cd mcp-servers

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### Verify Installation
```bash
python verify.py
```

## Running the Servers

### As Standalone MCP Servers (Recommended)
```bash
# Math server
mcp-math-server

# Visualization server (in another terminal)
mcp-visualization-server
```

### For Development/Testing
```bash
# Math server
python -m mcp_servers.math_server

# Visualization server
python -m mcp_servers.visualization_server
```

## Testing Examples

### Run Math Examples
```bash
PYTHONPATH=. python examples/math_examples.py
```

### Run Visualization Examples
```bash
PYTHONPATH=. python examples/visualization_examples.py
```

## MCP Client Configuration

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "math": {
      "command": "mcp-math-server"
    },
    "visualization": {
      "command": "mcp-visualization-server"
    }
  }
}
```

## Development

### Install Development Dependencies
```bash
make install-dev
# or
pip install -e ".[dev]"
```

### Run Tests
```bash
make test
# or
python -m pytest tests/ -v
```

### Format Code
```bash
make format
# or
black mcp_servers/ tests/
isort mcp_servers/ tests/
```

### Lint Code
```bash
make lint
# or
flake8 mcp_servers/
mypy mcp_servers/
```

## Troubleshooting

### Import Errors
If you get import errors, make sure you have the project directory in your Python path:
```bash
export PYTHONPATH=/path/to/mcp-servers:$PYTHONPATH
```

### Missing Dependencies
For visualization features, install the full requirements:
```bash
pip install -r requirements.txt
```

### Permission Issues
Make sure the scripts are executable:
```bash
chmod +x examples/*.py
```

## Project Structure

```
mcp-servers/
├── mcp_servers/                 # Main package
│   ├── __init__.py             # Package initialization
│   ├── math_server.py          # Math MCP server
│   ├── visualization_server.py # Visualization MCP server
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── base_server.py      # Base MCP server class
│       ├── math_utils.py       # Math calculation utilities
│       └── viz_utils.py        # Visualization utilities
├── tests/                      # Test files
├── examples/                   # Usage examples
├── docs/                       # Documentation
├── requirements.txt            # Dependencies
├── pyproject.toml             # Project configuration
├── setup.py                   # Setup script
└── README.md                  # Main documentation
```
