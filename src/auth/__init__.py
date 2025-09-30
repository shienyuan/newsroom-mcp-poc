"""Authentication providers for Newsroom MCP server."""

from src.auth.patched_azure_provider import PatchedAzureProvider

__all__ = ["PatchedAzureProvider"]

