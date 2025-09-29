"""Newsroom MCP Server - Main server implementation.

This module implements the main MCP server with Azure OAuth authentication,
integrating all MCP features (resources, tools, and prompts).
"""

import logging
from fastmcp import FastMCP
from fastmcp.server.auth.providers.azure import AzureProvider
from fastmcp.server.auth.oidc_proxy import OIDCProxy

from src.config import get_config
from src.mcp.resources.sample import register_resources
from src.mcp.tools.echo import register_tools as register_echo_tools
from src.mcp.tools.info import register_tools as register_info_tools
from src.mcp.prompts.greeting import register_prompts

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more verbose output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Also set FastMCP and auth loggers to DEBUG
logging.getLogger('fastmcp').setLevel(logging.DEBUG)
logging.getLogger('fastmcp.server.auth').setLevel(logging.DEBUG)


def create_server() -> FastMCP:
    """Create and configure the FastMCP server with Azure OAuth authentication.
    
    This function:
    1. Loads configuration from environment variables
    2. Sets up Azure OAuth authentication provider
    3. Initializes the FastMCP server
    4. Registers all MCP features (resources, tools, prompts)
    
    Returns:
        FastMCP: Configured FastMCP server instance ready to run.
        
    Raises:
        ValueError: If required configuration is missing or invalid.
    """
    logger.info("Starting Newsroom MCP server initialization...")
    
    # Load configuration
    try:
        config = get_config()
        logger.info(f"Configuration loaded successfully for {config.server.name} v{config.server.version}")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise
    
    # Configure Azure OIDC proxy
    # Using OIDCProxy directly instead of AzureProvider to avoid the 'resource' parameter
    # which causes AADSTS901002 error with Azure AD v2.0
    try:
        azure_oidc_config_url = (
            f"https://login.microsoftonline.com/{config.azure_oauth.tenant_id}/v2.0/"
            ".well-known/openid-configuration"
        )

        logger.info(f"Using Azure OIDC configuration URL: {azure_oidc_config_url}")

        auth_provider = OIDCProxy(
            config_url=azure_oidc_config_url,
            client_id=config.azure_oauth.client_id,
            client_secret=config.azure_oauth.client_secret,
            base_url=config.azure_oauth.base_url,
            redirect_path=config.azure_oauth.redirect_path,
            required_scopes=config.azure_oauth.required_scopes,
        )
        logger.info(f"Azure OIDC proxy configured with tenant: {config.azure_oauth.tenant_id}")
        logger.info(f"Redirect URI: {config.azure_oauth.redirect_uri}")
    except Exception as e:
        logger.error(f"Failed to configure Azure OIDC proxy: {e}")
        raise
    
    # Initialize FastMCP server with authentication
    mcp = FastMCP(
        name=config.server.name,
        auth=auth_provider
    )
    logger.info(f"FastMCP server '{config.server.name}' initialized with Azure OAuth authentication")
    
    # Register MCP features
    try:
        # Register resources
        register_resources(mcp)
        logger.info("✓ Resources registered: sample_data")
        
        # Register tools
        register_echo_tools(mcp)
        register_info_tools(mcp)
        logger.info("✓ Tools registered: echo, server_info")
        
        # Register prompts
        register_prompts(mcp)
        logger.info("✓ Prompts registered: greeting_template")
        
    except Exception as e:
        logger.error(f"Failed to register MCP features: {e}")
        raise
    
    logger.info("=" * 60)
    logger.info(f"🚀 {config.server.name} v{config.server.version} ready!")
    logger.info(f"   Authentication: Azure OAuth (Microsoft Entra ID)")
    logger.info(f"   Server will run on: {config.server.host}:{config.server.port}")
    logger.info(f"   OAuth Redirect URI: {config.azure_oauth.redirect_uri}")
    logger.info("=" * 60)
    
    return mcp


# Create the server instance
mcp = create_server()


if __name__ == "__main__":
    """Run the server when executed directly."""
    # Load configuration for runtime settings
    config = get_config()
    
    logger.info(f"Starting HTTP server on {config.server.host}:{config.server.port}...")
    logger.info("Press Ctrl+C to stop the server")
    
    # Run the server with HTTP transport (required for OAuth)
    mcp.run(
        transport="http",
        host=config.server.host,
        port=config.server.port
    )

