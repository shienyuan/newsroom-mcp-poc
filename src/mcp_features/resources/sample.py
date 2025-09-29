"""Sample MCP resource implementation.

This module provides a simple example resource that returns static JSON data,
demonstrating how to expose data and content for AI context using FastMCP.
"""

from datetime import datetime
from typing import Dict, Any


def get_sample_data() -> Dict[str, Any]:
    """Sample data resource that returns static JSON data.
    
    This resource demonstrates the basic pattern for exposing data through MCP.
    It returns a static JSON object with sample information including a message,
    timestamp, and nested data structure.
    
    Returns:
        Dict[str, Any]: Static JSON object with sample information.
        
    Example:
        When accessed via URI "sample://data", returns:
        {
            "message": "This is sample data from an MCP resource",
            "timestamp": "2024-01-15T10:30:00Z",
            "data": {
                "id": 1,
                "name": "Sample Resource",
                "type": "demonstration"
            }
        }
    """
    return {
        "message": "This is sample data from an MCP resource",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "data": {
            "id": 1,
            "name": "Sample Resource",
            "type": "demonstration",
            "features": [
                "Static data exposure",
                "JSON serialization",
                "MCP resource pattern"
            ]
        },
        "metadata": {
            "version": "1.0.0",
            "source": "Newsroom MCP Server",
            "read_only": True
        }
    }


def register_resources(mcp):
    """Register all resources from this module with the MCP server.
    
    Args:
        mcp: FastMCP server instance to register resources with.
    """
    @mcp.resource(
        uri="sample://data",
        name="sample_data",
        description="A simple resource that returns sample JSON data for demonstration purposes",
        mime_type="application/json",
        annotations={
            "readOnlyHint": True,
            "idempotentHint": True
        }
    )
    def sample_data_resource() -> Dict[str, Any]:
        """Provides sample data as a read-only MCP resource."""
        return get_sample_data()

