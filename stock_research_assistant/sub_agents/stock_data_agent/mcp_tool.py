import asyncio
import json
import os
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from functools import wraps

class PolygonMCPClient:
    """MCP Client for Polygon.io financial data"""
    
    def __init__(self, polygon_api_key: str):
        self.polygon_api_key = polygon_api_key
        self.session: Optional[ClientSession] = None
        self._client = None
        self._connected = False
        
        # Server parameters for the Polygon MCP server
        self.server_params = StdioServerParameters(
            command="uvx",
            args=[
                "--from", 
                "git+https://github.com/polygon-io/mcp_polygon@v0.4.0",
                "mcp_polygon"
            ],
            env={
                "POLYGON_API_KEY": polygon_api_key,
                "HOME": os.path.expanduser("~")
            }
        )
    
    async def connect(self):
        """Establish connection to MCP server"""
        if not self._connected:
            self._client = stdio_client(self.server_params)
            self.session, _ = await self._client.__aenter__()
            await self.session.initialize()
            self._connected = True
            print("Connected to Polygon MCP server")
    
    async def disconnect(self):
        """Disconnect from MCP server"""
        if self._connected and self._client:
            try:
                await self._client.__aexit__(None, None, None)
                self._connected = False
                self.session = None
                self._client = None
                print("Disconnected from Polygon MCP server")
            except Exception as e:
                print(f"Error disconnecting: {e}")
    
    async def call_mcp_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call MCP tool with automatic connection management"""
        if not self._connected:
            await self.connect()
        
        try:
            result = await self.session.call_tool(tool_name, arguments)
            
            if result.content and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, 'text'):
                    try:
                        return json.loads(content.text)
                    except json.JSONDecodeError:
                        return {"text": content.text}
                elif hasattr(content, 'data'):
                    return content.data
                else:
                    return {"content": str(content)}
            
            return {"warning": "No content returned from MCP server"}
            
        except Exception as e:
            return {"error": f"MCP tool call failed: {str(e)}"}

# Global MCP client instance
_mcp_client = None

def get_mcp_client():
    """Get or create MCP client instance"""
    global _mcp_client
    if _mcp_client is None:
        polygon_api_key = os.getenv("POLYGON_API_KEY")
        if not polygon_api_key:
            raise ValueError("POLYGON_API_KEY environment variable is required")
        _mcp_client = PolygonMCPClient(polygon_api_key)
    return _mcp_client

def mcp_tool(func):
    """Decorator to handle async MCP tool calls for sync agent functions"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Run the async function in the event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        if loop.is_running():
            # If event loop is already running, we need to create a task
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, func(*args, **kwargs))
                return future.result()
        else:
            return loop.run_until_complete(func(*args, **kwargs))
    
    return wrapper