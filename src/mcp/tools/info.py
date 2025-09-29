"""Server info tool implementation.

This module provides a tool that returns metadata about the MCP server
and its capabilities.
"""

from typing import Dict, Any


def get_server_info() -> Dict[str, Any]:
    """Get server information and capabilities.
    
    Returns:
        Dict[str, Any]: Server metadata including name, version, authentication,
                       and available features.
    """
    return {
        "name": "Newsroom MCP",
        "version": "1.0.0",
        "authentication": "Azure OAuth (Microsoft Entra ID)",
        "features": {
            "resources": ["sample_data"],
            "tools": ["echo", "server_info"],
            "prompts": ["greeting_template"]
        },
        "transport": "HTTP",
        "protocol": "MCP (Model Context Protocol)",
        "framework": "FastMCP"
    }


def register_tools(mcp):
    """Register all tools from this module with the MCP server.
    
    Args:
        mcp: FastMCP server instance to register tools with.
    """
    @mcp.tool(
        name="server_info",
        description="Returns metadata about the MCP server and its capabilities",
        annotations={
            "readOnlyHint": True,
            "idempotentHint": True
        }
    )
    def server_info() -> Dict[str, Any]:
        """Get information about the MCP server.
        
        This tool provides metadata about the server including its name,
        version, authentication method, and available features (resources,
        tools, and prompts).
        
        Returns:
            Dict[str, Any]: Server information object containing:
                - name: Server name
                - version: Server version
                - authentication: Authentication method used
                - features: Available resources, tools, and prompts
                - transport: Communication transport type
                - protocol: Protocol name and version
                - framework: Framework used to build the server
                
        Example:
            Input: {}
            Output: {
                "name": "Newsroom MCP",
                "version": "1.0.0",
                "authentication": "Azure OAuth (Microsoft Entra ID)",
                "features": {
                    "resources": ["sample_data"],
                    "tools": ["echo", "server_info"],
                    "prompts": ["greeting_template"]
                }
            }
        """
        return get_server_info()

