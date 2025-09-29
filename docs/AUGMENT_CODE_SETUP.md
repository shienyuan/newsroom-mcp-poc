# Using Newsroom MCP with Augment Code

This guide explains how to connect the Newsroom MCP server to Augment Code with Azure OAuth authentication.

## Prerequisites

1. **Server is running**: The Newsroom MCP server must be running on `http://localhost:8000`
2. **Azure App Registration**: You have configured Azure OAuth credentials in `.env`
3. **Augment Code**: You have Augment Code installed and configured

## Configuration

### 1. Add Server to Augment Code

Add the following configuration to your Augment Code MCP servers configuration:

```json
{
  "mcpServers": {
    "newsroom-mcp": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "auth": "oauth"
    }
  }
}
```

### 2. Start the Server

Make sure the Newsroom MCP server is running:

```bash
# From the project root
source venv/bin/activate
python run_server.py
```

You should see:
```
🚀 Newsroom MCP v1.0.0 ready!
   Authentication: Azure OAuth (Microsoft Entra ID)
   Server will run on: localhost:8000
   OAuth Redirect URI: http://localhost:8000/auth/callback
```

### 3. Connect from Augment Code

When Augment Code first connects to the server:

1. **OAuth Discovery**: Augment Code will discover the OAuth configuration at:
   - `http://localhost:8000/.well-known/oauth-protected-resource`
   - `http://localhost:8000/.well-known/oauth-authorization-server`

2. **Browser Authentication**: Augment Code will open your browser to:
   - `http://localhost:8000/authorize`
   - This redirects to Azure's login page
   - You'll log in with your Microsoft account

3. **Token Exchange**: After successful login:
   - Azure redirects back to the server with an authorization code
   - The server exchanges the code for an access token
   - Augment Code receives and caches the token

4. **Authenticated Access**: All subsequent requests will use the cached token

## OAuth Flow Details

### Endpoints Exposed by the Server

The server exposes these OAuth endpoints:

| Endpoint | Purpose |
|----------|---------|
| `/.well-known/oauth-protected-resource` | OAuth resource metadata |
| `/.well-known/oauth-authorization-server` | OAuth server metadata |
| `/authorize` | OAuth authorization endpoint (proxies to Azure) |
| `/token` | OAuth token endpoint (proxies to Azure) |
| `/register` | Dynamic client registration |
| `/auth/callback` | OAuth callback handler |
| `/mcp` | Protected MCP endpoint |

### What Happens Behind the Scenes

1. **Server acts as OAuth Proxy**: The Newsroom MCP server proxies OAuth requests to Azure AD
2. **Azure handles authentication**: Users log in through Microsoft's secure login page
3. **Token validation**: The server validates tokens from Azure before allowing MCP access
4. **Scopes requested**: `openid`, `profile`, `email` (configurable in `.env`)

## Troubleshooting

### "401 Unauthorized" Errors

This is normal before authentication! The server requires OAuth authentication for all MCP requests.

**What you'll see in logs:**
```
INFO:     127.0.0.1:xxxxx - "POST /mcp HTTP/1.1" 401 Unauthorized
```

**Solution**: Complete the OAuth flow in your browser when prompted by Augment Code.

### "404 Not Found" for OIDC Endpoints

You might see these in the logs:
```
INFO:     127.0.0.1:xxxxx - "GET /.well-known/openid-configuration HTTP/1.1" 404 Not Found
```

**This is OK!** Augment Code tries multiple discovery methods. The important endpoints (oauth-authorization-server) return 200 OK.

### Browser Doesn't Open

If Augment Code doesn't automatically open your browser:

1. Check the Augment Code logs for the authorization URL
2. Manually copy and paste the URL into your browser
3. Complete the Azure login
4. The browser will redirect back to complete the flow

### Token Expired

OAuth tokens expire after a certain time. If you get authentication errors:

1. Augment Code should automatically refresh the token
2. If not, you may need to re-authenticate through the browser
3. Check that your Azure App Registration allows refresh tokens

## Testing the Server

### Manual OAuth Flow Test

You can test the OAuth flow manually:

1. **Get the authorization URL**:
   ```bash
   curl http://localhost:8000/.well-known/oauth-authorization-server
   ```

2. **Check OAuth metadata**:
   ```bash
   curl http://localhost:8000/.well-known/oauth-protected-resource
   ```

3. **Verify MCP endpoint requires auth**:
   ```bash
   curl http://localhost:8000/mcp
   # Should return: {"error": "invalid_token", "error_description": "Authentication required"}
   ```

### Using the Test Client

The project includes a test client that demonstrates the OAuth flow:

```bash
source venv/bin/activate
python test_client.py
```

**Note**: This requires a graphical environment to open the browser for authentication.

## Available MCP Features

Once authenticated, you can access:

### Resources
- **sample_data** (`sample://data`): Returns sample JSON data with timestamp

### Tools
- **echo**: Echoes back your message
- **server_info**: Returns server metadata and capabilities

### Prompts
- **greeting_template**: Generates personalized greetings (formal/casual)

## Security Notes

1. **HTTPS in Production**: Always use HTTPS in production environments
2. **Secure Credentials**: Never commit `.env` file with real credentials
3. **Token Storage**: Augment Code caches tokens securely on your machine
4. **Scope Limitation**: Only request the minimum required OAuth scopes
5. **Azure App Registration**: Ensure redirect URIs match exactly in Azure portal

## Support

For issues:
1. Check server logs for detailed error messages
2. Verify Azure App Registration configuration
3. Ensure all environment variables are set correctly in `.env`
4. Test OAuth endpoints manually with curl

## References

- [Augment Code Remote MCP Authentication](https://www.augmentcode.com/changelog/remote-mcp-authentication)
- [FastMCP Azure OAuth Documentation](https://gofastmcp.com/docs/integrations/azure)
- [Microsoft Identity Platform OAuth 2.0](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)

