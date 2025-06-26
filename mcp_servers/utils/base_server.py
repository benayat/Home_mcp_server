"""
Base MCP Server implementation.

Provides common functionality for all MCP servers including:
- JSON-RPC message handling
- Standard MCP protocol methods
- Error handling
- Stdin/stdout communication
"""

import asyncio
import json
import logging
import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class MCPError(Exception):
    """Base exception for MCP errors."""
    
    def __init__(self, code: int, message: str, data: Optional[Any] = None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(message)


class BaseMCPServer(ABC):
    """
    Base class for MCP servers.
    
    Handles the MCP protocol communication and provides abstract methods
    for server-specific functionality.
    """
    
    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.protocol_version = "2024-11-05"
        self._initialized = False
        
    @abstractmethod
    def get_server_info(self) -> Dict[str, Any]:
        """Return server information for the initialize response."""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """Return server capabilities for the initialize response."""
        pass
    
    @abstractmethod
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools."""
        pass
    
    @abstractmethod
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool with given arguments."""
        pass
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """Return list of available resources. Override if resources are supported."""
        return []
    
    async def read_resource(self, uri: str) -> Dict[str, Any]:
        """Read a resource by URI. Override if resources are supported."""
        raise MCPError(-32601, f"Resource not found: {uri}")
    
    def create_response(self, request_id: Optional[Union[str, int]], result: Any) -> Dict[str, Any]:
        """Create a successful JSON-RPC response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
    
    def create_error_response(
        self, 
        request_id: Optional[Union[str, int]], 
        code: int, 
        message: str, 
        data: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Create an error JSON-RPC response."""
        error = {"code": code, "message": message}
        if data is not None:
            error["data"] = data
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": error
        }
    
    async def handle_initialize(self, request_id: Optional[Union[str, int]], params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request."""
        self._initialized = True
        
        return self.create_response(request_id, {
            "protocolVersion": self.protocol_version,
            "capabilities": self.get_capabilities(),
            "serverInfo": self.get_server_info()
        })
    
    async def handle_tools_list(self, request_id: Optional[Union[str, int]]) -> Dict[str, Any]:
        """Handle tools/list request."""
        if not self._initialized:
            return self.create_error_response(request_id, -32002, "Server not initialized")
        
        tools = await self.list_tools()
        return self.create_response(request_id, {"tools": tools})
    
    async def handle_tools_call(self, request_id: Optional[Union[str, int]], params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request."""
        if not self._initialized:
            return self.create_error_response(request_id, -32002, "Server not initialized")
        
        try:
            name = params.get("name")
            arguments = params.get("arguments", {})
            
            if not name:
                return self.create_error_response(request_id, -32602, "Missing tool name")
            
            # Parse arguments if they're a string
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    return self.create_error_response(request_id, -32602, "Invalid arguments format")
            
            result = await self.call_tool(name, arguments)
            
            # Format result as MCP content
            content = []
            if isinstance(result, dict):
                content.append({
                    "type": "text",
                    "text": json.dumps(result, indent=2, ensure_ascii=False)
                })
            elif isinstance(result, str):
                content.append({
                    "type": "text", 
                    "text": result
                })
            else:
                content.append({
                    "type": "text",
                    "text": str(result)
                })
            
            return self.create_response(request_id, {"content": content})
            
        except MCPError as e:
            return self.create_error_response(request_id, e.code, e.message, e.data)
        except Exception as e:
            logger.exception(f"Error executing tool {params.get('name', 'unknown')}")
            return self.create_error_response(request_id, -32603, f"Internal error: {str(e)}")
    
    async def handle_resources_list(self, request_id: Optional[Union[str, int]]) -> Dict[str, Any]:
        """Handle resources/list request."""
        if not self._initialized:
            return self.create_error_response(request_id, -32002, "Server not initialized")
        
        try:
            resources = await self.list_resources()
            return self.create_response(request_id, {"resources": resources})
        except Exception as e:
            logger.exception("Error listing resources")
            return self.create_error_response(request_id, -32603, f"Internal error: {str(e)}")
    
    async def handle_resources_read(self, request_id: Optional[Union[str, int]], params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle resources/read request."""
        if not self._initialized:
            return self.create_error_response(request_id, -32002, "Server not initialized")
        
        try:
            uri = params.get("uri")
            if not uri:
                return self.create_error_response(request_id, -32602, "Missing resource URI")
            
            result = await self.read_resource(uri)
            return self.create_response(request_id, result)
            
        except MCPError as e:
            return self.create_error_response(request_id, e.code, e.message, e.data)
        except Exception as e:
            logger.exception(f"Error reading resource {params.get('uri', 'unknown')}")
            return self.create_error_response(request_id, -32603, f"Internal error: {str(e)}")
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle an incoming JSON-RPC request."""
        try:
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            if method == "initialize":
                return await self.handle_initialize(request_id, params)
            elif method == "tools/list":
                return await self.handle_tools_list(request_id)
            elif method == "tools/call":
                return await self.handle_tools_call(request_id, params)
            elif method == "resources/list":
                return await self.handle_resources_list(request_id)
            elif method == "resources/read":
                return await self.handle_resources_read(request_id, params)
            else:
                return self.create_error_response(request_id, -32601, f"Method not found: {method}")
                
        except Exception as e:
            logger.exception("Error handling request")
            return self.create_error_response(
                request.get("id"), 
                -32603, 
                f"Internal error: {str(e)}"
            )
    
    async def run(self) -> None:
        """Run the MCP server, reading from stdin and writing to stdout."""
        logger.info(f"Starting {self.name} MCP server")
        
        try:
            # Set up stdin/stdout for line-buffered I/O
            sys.stdout.reconfigure(line_buffering=True)
            
            # Main message loop
            while True:
                try:
                    # Read line from stdin
                    line = await asyncio.get_event_loop().run_in_executor(
                        None, sys.stdin.readline
                    )
                    
                    if not line:  # EOF
                        break
                    
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Parse JSON-RPC request
                    try:
                        request = json.loads(line)
                    except json.JSONDecodeError as e:
                        error_response = self.create_error_response(
                            None, -32700, f"Parse error: {str(e)}"
                        )
                        print(json.dumps(error_response), flush=True)
                        continue
                    
                    # Handle request
                    response = await self.handle_request(request)
                    
                    # Send response
                    print(json.dumps(response), flush=True)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logger.exception("Error in main loop")
                    error_response = self.create_error_response(
                        None, -32603, f"Internal error: {str(e)}"
                    )
                    print(json.dumps(error_response), flush=True)
                    
        except Exception as e:
            logger.exception(f"Fatal error in {self.name} server")
            sys.exit(1)
        
        logger.info(f"{self.name} MCP server stopped")
