"""Authentication module for Newsroom MCP.

This module contains custom authentication providers and utilities.
"""

from src.auth.azure_oidc_proxy import AzureOIDCProxy

__all__ = ['AzureOIDCProxy']

