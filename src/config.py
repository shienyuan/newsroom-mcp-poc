"""Configuration management for Newsroom MCP server.

This module handles environment variable loading, validation, and provides
centralized configuration for the MCP server and Azure OAuth authentication.
"""

import os
import logging
from dataclasses import dataclass, field
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


@dataclass
class AzureOAuthConfig:
    """Azure OAuth configuration settings.
    
    These settings are used by FastMCP's AzureProvider for authentication.
    All values are loaded from environment variables with the FASTMCP_SERVER_AUTH_AZURE_ prefix.
    """
    
    client_id: str
    client_secret: str
    tenant_id: str
    base_url: str = "http://localhost:8000"
    redirect_path: str = "/auth/callback"
    required_scopes: List[str] = field(default_factory=lambda: ["openid", "profile", "email"])
    timeout_seconds: int = 30
    
    @classmethod
    def from_env(cls) -> "AzureOAuthConfig":
        """Load Azure OAuth configuration from environment variables.
        
        Returns:
            AzureOAuthConfig: Configuration instance with values from environment.
            
        Raises:
            ValueError: If required environment variables are missing.
        """
        client_id = os.getenv("FASTMCP_SERVER_AUTH_AZURE_CLIENT_ID")
        client_secret = os.getenv("FASTMCP_SERVER_AUTH_AZURE_CLIENT_SECRET")
        tenant_id = os.getenv("FASTMCP_SERVER_AUTH_AZURE_TENANT_ID")
        
        # Validate required fields
        missing_vars = []
        if not client_id:
            missing_vars.append("FASTMCP_SERVER_AUTH_AZURE_CLIENT_ID")
        if not client_secret:
            missing_vars.append("FASTMCP_SERVER_AUTH_AZURE_CLIENT_SECRET")
        if not tenant_id:
            missing_vars.append("FASTMCP_SERVER_AUTH_AZURE_TENANT_ID")
            
        if missing_vars:
            raise ValueError(
                f"Missing required Azure OAuth environment variables: {', '.join(missing_vars)}. "
                "Please check your .env file."
            )
        
        # Load optional fields with defaults
        base_url = os.getenv("FASTMCP_SERVER_AUTH_AZURE_BASE_URL", "http://localhost:8000")
        redirect_path = os.getenv("FASTMCP_SERVER_AUTH_AZURE_REDIRECT_PATH", "/auth/callback")
        
        # Parse scopes (comma-separated string to list)
        scopes_str = os.getenv("FASTMCP_SERVER_AUTH_AZURE_REQUIRED_SCOPES", "openid,profile,email")
        required_scopes = [scope.strip() for scope in scopes_str.split(",") if scope.strip()]
        
        # Parse timeout
        timeout_str = os.getenv("FASTMCP_SERVER_AUTH_AZURE_TIMEOUT_SECONDS", "30")
        try:
            timeout_seconds = int(timeout_str)
        except ValueError:
            logger.warning(
                f"Invalid timeout value '{timeout_str}', using default 30 seconds"
            )
            timeout_seconds = 30
        
        return cls(
            client_id=client_id,
            client_secret=client_secret,
            tenant_id=tenant_id,
            base_url=base_url,
            redirect_path=redirect_path,
            required_scopes=required_scopes,
            timeout_seconds=timeout_seconds,
        )
    
    @property
    def redirect_uri(self) -> str:
        """Get the full redirect URI for OAuth callbacks.
        
        Returns:
            str: Complete redirect URI (base_url + redirect_path).
        """
        return f"{self.base_url.rstrip('/')}{self.redirect_path}"
    
    def validate(self) -> None:
        """Validate configuration values.
        
        Raises:
            ValueError: If configuration values are invalid.
        """
        if not self.client_id or len(self.client_id) < 10:
            raise ValueError("Invalid Azure client_id")
        
        if not self.client_secret or len(self.client_secret) < 10:
            raise ValueError("Invalid Azure client_secret")
        
        if not self.tenant_id or len(self.tenant_id) < 10:
            raise ValueError("Invalid Azure tenant_id")
        
        if not self.base_url.startswith(("http://", "https://")):
            raise ValueError("base_url must start with http:// or https://")
        
        if not self.redirect_path.startswith("/"):
            raise ValueError("redirect_path must start with /")
        
        if self.timeout_seconds < 1 or self.timeout_seconds > 300:
            raise ValueError("timeout_seconds must be between 1 and 300")
        
        if not self.required_scopes:
            raise ValueError("At least one OAuth scope is required")


@dataclass
class ServerConfig:
    """MCP server configuration settings."""
    
    name: str = "Newsroom MCP"
    version: str = "1.0.0"
    host: str = "localhost"
    port: int = 8000
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls) -> "ServerConfig":
        """Load server configuration from environment variables.
        
        Returns:
            ServerConfig: Configuration instance with values from environment.
        """
        name = os.getenv("MCP_SERVER_NAME", "Newsroom MCP")
        version = os.getenv("MCP_SERVER_VERSION", "1.0.0")
        host = os.getenv("MCP_SERVER_HOST", "localhost")
        
        # Parse port
        port_str = os.getenv("MCP_SERVER_PORT", "8000")
        try:
            port = int(port_str)
        except ValueError:
            logger.warning(f"Invalid port value '{port_str}', using default 8000")
            port = 8000
        
        log_level = os.getenv("MCP_LOG_LEVEL", "INFO").upper()
        
        return cls(
            name=name,
            version=version,
            host=host,
            port=port,
            log_level=log_level,
        )
    
    def validate(self) -> None:
        """Validate configuration values.
        
        Raises:
            ValueError: If configuration values are invalid.
        """
        if self.port < 1 or self.port > 65535:
            raise ValueError("port must be between 1 and 65535")
        
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level not in valid_log_levels:
            raise ValueError(f"log_level must be one of {valid_log_levels}")


@dataclass
class Config:
    """Main configuration container for the Newsroom MCP server."""
    
    server: ServerConfig
    azure_oauth: AzureOAuthConfig
    
    @classmethod
    def load(cls) -> "Config":
        """Load and validate all configuration from environment variables.
        
        Returns:
            Config: Complete configuration instance.
            
        Raises:
            ValueError: If configuration is invalid or required values are missing.
        """
        logger.info("Loading configuration from environment variables...")
        
        try:
            server_config = ServerConfig.from_env()
            azure_config = AzureOAuthConfig.from_env()
            
            # Validate configurations
            server_config.validate()
            azure_config.validate()
            
            config = cls(server=server_config, azure_oauth=azure_config)
            
            logger.info("Configuration loaded successfully")
            logger.debug(f"Server: {server_config.name} v{server_config.version}")
            logger.debug(f"Host: {server_config.host}:{server_config.port}")
            logger.debug(f"Azure Tenant: {azure_config.tenant_id}")
            logger.debug(f"Redirect URI: {azure_config.redirect_uri}")
            
            return config
            
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading configuration: {e}")
            raise


# Global configuration instance (lazy-loaded)
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance.
    
    This function provides lazy loading of configuration. The configuration
    is loaded once on first access and cached for subsequent calls.
    
    Returns:
        Config: The global configuration instance.
        
    Raises:
        ValueError: If configuration is invalid or required values are missing.
    """
    global _config
    if _config is None:
        _config = Config.load()
    return _config


def reload_config() -> Config:
    """Reload configuration from environment variables.
    
    This function forces a reload of the configuration, useful for testing
    or when environment variables have changed.
    
    Returns:
        Config: The newly loaded configuration instance.
    """
    global _config
    load_dotenv(override=True)  # Reload .env file
    _config = Config.load()
    return _config

