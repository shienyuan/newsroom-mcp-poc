# OAuth Resource Parameter Issue - Solution

## Problem Summary

When connecting to the newsroom-mcp server from VSCode, the MCP client was sending a `resource` parameter in the OAuth authorization request:

```
resource=http://localhost:8000/mcp
```

**Azure AD v2.0 does NOT support the `resource` parameter** and returns an `AADSTS901002` error when it's present.

## Root Cause

1. **MCP Client Behavior**: The MCP client (VSCode) automatically adds the `resource` parameter according to RFC 8707 (Resource Indicators)
2. **FastMCP Forwarding**: FastMCP's `OAuthProxy` automatically forwards this parameter to upstream OAuth providers
3. **Azure Incompatibility**: Azure AD v2.0 doesn't support this parameter and fails authentication

## Solution Applied

### 1. Fixed Module Name Conflict

**Problem**: The project had a `src/mcp` directory that was shadowing the installed `mcp` package, causing import errors.

**Solution**: Renamed `src/mcp` to `src/mcp_features` and updated all imports in `src/server.py`.

### 2. Using FastMCP's AzureProvider

You've reverted to using FastMCP's built-in `AzureProvider`, which is the recommended approach. The current implementation in `src/server.py`:

```python
from fastmcp.server.auth.providers.azure import AzureProvider

auth_provider = AzureProvider(
    client_id=config.azure_oauth.client_id,
    client_secret=config.azure_oauth.client_secret,
    tenant_id=config.azure_oauth.tenant_id,
    base_url=config.azure_oauth.base_url,
    redirect_path=config.azure_oauth.redirect_path,
    required_scopes=config.azure_oauth.required_scopes,
    timeout_seconds=config.azure_oauth.timeout_seconds,
)
```

### 3. Manual Workaround (Temporary)

You successfully authenticated by **manually removing the `resource` parameter from the authorization URL** in your browser before submitting it to Azure.

## Current Status

✅ **Server is running** on `http://localhost:8000`
✅ **Module conflicts resolved** (`src/mcp` → `src/mcp_features`)
✅ **Authentication works** when resource parameter is manually removed
⚠️  **Callback handling** needs testing

## Next Steps

### Option 1: Test with Manual Resource Removal (Current Approach)

1. **Start the server** (already running):
   ```bash
   python src/server.py
   ```

2. **Connect from VSCode**:
   - Add the MCP server to VSCode's `mcp.json`
   - When the OAuth authorization URL opens, manually remove the `resource` parameter
   - Complete the authentication

3. **Check if callback works**:
   - After authentication, Azure will redirect to `http://localhost:8000/auth/callback`
   - The server should handle this and complete the OAuth flow
   - VSCode should then be able to connect to the MCP server

### Option 2: Implement Custom Resource Parameter Filtering (Future)

If manual removal becomes tedious, we can implement a custom Azure provider that automatically strips the `resource` parameter. This would require:

1. Creating a custom `AzureOIDCProxy` class that extends `OAuthProxy`
2. Overriding the authorization flow to remove the `resource` parameter
3. Finding the correct method to intercept (we tried several approaches but none worked)

**Note**: This is complex because FastMCP's `OAuthProxy` adds the resource parameter deep in the authorization flow, and we haven't found the right hook to intercept it yet.

### Option 3: Report to FastMCP (Recommended)

The ideal solution is to report this issue to the FastMCP team. Azure AD v2.0 is a major OAuth provider, and FastMCP's `AzureProvider` should handle this automatically.

**Suggested GitHub Issue**:
- **Title**: "AzureProvider forwards resource parameter causing AADSTS901002 error"
- **Description**: Azure AD v2.0 doesn't support RFC 8707 resource indicators. When MCP clients send the `resource` parameter, FastMCP forwards it to Azure, causing authentication to fail.
- **Expected Behavior**: `AzureProvider` should strip the `resource` parameter before forwarding to Azure
- **Workaround**: Manually remove the parameter from the authorization URL

## Testing the Current Setup

1. **Verify server is running**:
   ```bash
   curl http://localhost:8000/.well-known/oauth-authorization-server
   ```

2. **Try connecting from VSCode**:
   - Open VSCode
   - Add to `~/Library/Application Support/Code/User/mcp.json`:
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

3. **When the OAuth URL opens**:
   - Look for `&resource=http%3A%2F%2Flocalhost%3A8000%2Fmcp` in the URL
   - Remove that entire parameter (including the `&`)
   - Complete the authentication

4. **Check the callback**:
   - After authentication, you should be redirected to `http://localhost:8000/auth/callback?code=...`
   - The server should handle this and complete the OAuth flow
   - Check the server logs for any errors

## Files Changed

- `src/server.py` - Updated imports to use `src.mcp_features` instead of `src.mcp`
- `src/mcp/` → `src/mcp_features/` - Renamed directory to avoid module conflict

## Cleanup

The following files from our debugging attempts can be removed:
- `src/auth/azure_oidc_proxy.py` (if it exists)
- `src/auth/__init__.py` (if empty)
- `TEST_OAUTH_FLOW.md`
- `MIGRATION_TO_AZURE_PROVIDER.md` (outdated)

## Summary

The core issue is that **FastMCP forwards the `resource` parameter to Azure, but Azure AD v2.0 doesn't support it**. The current workaround is to manually remove it from the authorization URL. A proper fix would require either:

1. FastMCP updating `AzureProvider` to strip this parameter automatically
2. Implementing a custom provider that does this (we attempted but couldn't find the right hook)
3. Configuring the MCP client to not send the parameter (not possible with VSCode)

For now, **manual removal works** and allows you to authenticate successfully.

