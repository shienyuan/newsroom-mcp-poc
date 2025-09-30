"""Patched Azure OAuth Provider for FastMCP.

This module provides a workaround for the Azure OAuth v2.0 'resource' parameter issue.
See: https://github.com/jlowin/fastmcp/issues/1846

The standard AzureProvider adds a 'resource' parameter to the OAuth authorization URL,
but Azure AD v2.0 doesn't support this parameter and returns an error.

This patched provider removes the 'resource' parameter to ensure compatibility with
Azure AD v2.0 endpoints.
"""

from fastmcp.server.auth.providers.azure import AzureProvider


class PatchedAzureProvider(AzureProvider):
    """Azure OAuth provider with v2.0 compatibility fix.
    
    This class extends FastMCP's AzureProvider to remove the 'resource' parameter
    from OAuth authorization requests, which is not supported by Azure AD v2.0.
    
    The issue occurs because:
    1. MCP clients send a 'resource' parameter per RFC 8707 (Resource Indicators)
    2. FastMCP's OAuth proxy forwards this to Azure
    3. Azure AD v2.0 doesn't support this parameter and fails with AADSTS901002
    
    This workaround:
    1. Overrides _get_resource_url() to return None (forces v2.0 behavior)
    2. Strips the 'resource' parameter from authorization requests
    
    Usage:
        auth_provider = PatchedAzureProvider(
            client_id="your-client-id",
            client_secret="your-client-secret",
            tenant_id="your-tenant-id",
            base_url="http://localhost:8000",
            required_scopes=["User.Read", "email", "openid", "profile"],
        )
        
        mcp = FastMCP(name="My Server", auth=auth_provider)
    
    References:
        - GitHub Issue: https://github.com/jlowin/fastmcp/issues/1846
        - Azure AD v2.0 Docs: https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow
    """
    
    def _get_resource_url(self, mcp_path: str) -> None:
        """Override to return None and force Azure AD v2.0 behavior.
        
        The parent class returns a resource URL that gets added to the OAuth
        authorization request. Azure AD v2.0 doesn't support the 'resource'
        parameter, so we return None to prevent it from being added.
        
        Args:
            mcp_path: The MCP endpoint path (ignored)
            
        Returns:
            None: Forces v2.0 behavior without resource parameter
        """
        return None
    
    def authorize(self, *args, **kwargs):
        """Override authorize to strip the 'resource' parameter.
        
        This ensures that even if the resource parameter is passed in kwargs,
        it will be removed before calling the parent's authorize method.
        
        Args:
            *args: Positional arguments passed to parent authorize
            **kwargs: Keyword arguments passed to parent authorize
            
        Returns:
            The result from the parent's authorize method
        """
        # Remove 'resource' parameter if present
        kwargs.pop("resource", None)
        return super().authorize(*args, **kwargs)

