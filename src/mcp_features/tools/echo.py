"""Echo tool implementation.

This module provides a simple echo tool that returns the input message,
demonstrating basic MCP tool functionality.
"""


def register_tools(mcp):
    """Register all tools from this module with the MCP server.
    
    Args:
        mcp: FastMCP server instance to register tools with.
    """
    @mcp.tool(
        name="echo",
        description="A simple echo tool that returns the input message",
        annotations={
            "readOnlyHint": True,
            "idempotentHint": True
        }
    )
    def echo(message: str) -> str:
        """Echo back the provided message.
        
        This tool demonstrates the basic pattern for MCP tools. It accepts
        a message string and returns it unchanged, useful for testing and
        demonstrating tool functionality.
        
        Args:
            message: The message to echo back.
            
        Returns:
            str: The same message that was provided as input.
            
        Example:
            Input: {"message": "Hello, MCP!"}
            Output: "Echo: Hello, MCP!"
        """
        return f"Echo: {message}"

