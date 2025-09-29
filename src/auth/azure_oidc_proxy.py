"""Custom Azure OIDC Proxy that fixes the 'resource' parameter issue.

Azure AD v2.0 doesn't support the 'resource' parameter in OAuth authorization requests,
which causes AADSTS901002 errors. This custom proxy removes that parameter.
"""

import logging

from fastmcp.server.auth.oauth_proxy import OAuthProxy
from fastmcp.server.auth.providers.jwt import JWTVerifier

logger = logging.getLogger(__name__)


class AzureOIDCProxy(OAuthProxy):
    """Custom OAuth Proxy for Azure that removes the unsupported 'resource' parameter.

    Azure AD v2.0 endpoints don't support the 'resource' parameter in authorization
    requests. This proxy extends OAuthProxy to prevent that parameter from being added.
    """

    def __init__(self, config_url: str, **kwargs):
        """Initialize the Azure OIDC Proxy.

        Args:
            config_url: Azure OIDC configuration URL
            **kwargs: Additional arguments passed to OAuthProxy
        """
        # Fetch OIDC configuration
        import httpx

        logger.debug(f"Fetching OIDC configuration from {config_url}")
        response = httpx.get(config_url, timeout=5.0)
        response.raise_for_status()
        oidc_config = response.json()

        # Extract OAuth endpoints and JWKS URI
        authorization_endpoint = oidc_config['authorization_endpoint']
        token_endpoint = oidc_config['token_endpoint']
        jwks_uri = oidc_config['jwks_uri']
        issuer = oidc_config['issuer']

        logger.debug(f"Authorization endpoint: {authorization_endpoint}")
        logger.debug(f"Token endpoint: {token_endpoint}")
        logger.debug(f"JWKS URI: {jwks_uri}")
        logger.debug(f"Issuer: {issuer}")

        # Get required scopes
        required_scopes = kwargs.get('required_scopes', ['openid', 'profile', 'email'])
        scope_string = ' '.join(required_scopes)

        logger.debug(f"Using scopes: {scope_string}")

        # Create JWT verifier for Azure tokens
        # Azure uses the client_id as the audience
        token_verifier = JWTVerifier(
            jwks_uri=jwks_uri,
            issuer=issuer,
            audience=kwargs.get('client_id'),
        )

        logger.debug("JWT verifier configured for Azure tokens")

        # Initialize parent with OAuth endpoints
        # Note: We pass scope through extra_authorize_params to ensure it's used correctly
        super().__init__(
            upstream_authorization_endpoint=authorization_endpoint,
            upstream_token_endpoint=token_endpoint,
            upstream_client_id=kwargs.get('client_id'),
            upstream_client_secret=kwargs.get('client_secret'),
            token_verifier=token_verifier,
            base_url=kwargs.get('base_url'),
            redirect_path=kwargs.get('redirect_path', '/auth/callback'),
            extra_authorize_params={
                'scope': scope_string,
            },
        )

        logger.info("Azure OIDC Proxy initialized")

    def _build_upstream_authorization_params(self, *args, **kwargs):
        """Override to remove the 'resource' parameter that Azure AD v2.0 doesn't support."""
        # Call parent method to get base parameters
        params = super()._build_upstream_authorization_params(*args, **kwargs)

        # Remove the 'resource' parameter if it exists
        if 'resource' in params:
            logger.debug("Removing 'resource' parameter from authorization request")
            del params['resource']

        return params

