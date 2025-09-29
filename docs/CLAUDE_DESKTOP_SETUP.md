# Adding Newsroom MCP to Claude Desktop

This guide shows you how to add the Newsroom MCP server to Claude Desktop with Azure OAuth authentication.

## Prerequisites

- Claude Desktop installed on your machine
- Newsroom MCP server running on `http://localhost:8000`
- Azure OAuth credentials configured in `.env`

## Step-by-Step Setup

### 1. Locate Your Claude Desktop Configuration File

The configuration file location depends on your operating system:

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

### 2. Edit the Configuration File

Open the configuration file in your text editor. If the file doesn't exist, create it.

#### If you have NO existing MCP servers:

Create the file with this content:

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

#### If you ALREADY have MCP servers configured:

Add the `newsroom-mcp` entry to your existing `mcpServers` object:

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "python",
      "args": ["server.py"]
    },
    "newsroom-mcp": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "auth": "oauth"
    }
  }
}
```

### 3. Start the Newsroom MCP Server

Before restarting Claude Desktop, make sure the server is running:

```bash
cd /path/to/newsroom-mcp
source venv/bin/activate
python run_server.py
```

You should see:
```
============================================================
Starting Newsroom MCP v1.0.0
============================================================

🚀 Newsroom MCP v1.0.0 ready!
   Authentication: Azure OAuth (Microsoft Entra ID)
   Server will run on: localhost:8000
   OAuth Redirect URI: http://localhost:8000/auth/callback
```

### 4. Restart Claude Desktop

**Important:** You must completely quit and restart Claude Desktop for the configuration changes to take effect.

**macOS:**
- Press `Cmd + Q` to quit Claude Desktop
- Reopen Claude Desktop from Applications

**Windows:**
- Right-click the Claude Desktop icon in the system tray
- Select "Quit"
- Reopen Claude Desktop from the Start menu

**Linux:**
- Close all Claude Desktop windows
- Reopen Claude Desktop from your application launcher

### 5. First Connection - OAuth Authentication

When Claude Desktop first connects to the Newsroom MCP server:

1. **Browser Opens Automatically**: Claude Desktop will open your default browser
2. **Azure Login Page**: You'll be redirected to Microsoft's login page
3. **Sign In**: Log in with your Microsoft account (the one associated with your Azure tenant)
4. **Grant Permissions**: You may be asked to grant permissions for the requested scopes (openid, profile, email)
5. **Redirect Back**: After successful login, you'll be redirected back and the browser window can be closed
6. **Token Cached**: Claude Desktop will cache the OAuth token for future use

### 6. Verify the Connection

In Claude Desktop, you should see the Newsroom MCP server listed in the MCP servers panel (usually indicated by a 🔌 icon or similar).

Try asking Claude:
- "What MCP servers are available?"
- "Show me the sample_data resource from newsroom-mcp"
- "Use the echo tool from newsroom-mcp to say 'Hello!'"

## Using the MCP Server

Once connected, you can interact with the Newsroom MCP features:

### Resources

**Sample Data Resource:**
```
"Show me the sample_data resource"
"Read the sample://data resource"
```

### Tools

**Echo Tool:**
```
"Use the echo tool to repeat 'Hello from Claude Desktop!'"
"Call the echo tool with message 'Testing MCP'"
```

**Server Info Tool:**
```
"Get the server info"
"What features does the newsroom-mcp server have?"
```

### Prompts

**Greeting Template:**
```
"Use the greeting_template prompt for Alice in formal style"
"Generate a casual greeting for Bob using the greeting template"
```

## Troubleshooting

### Server Not Showing Up

**Check the configuration file:**
```bash
# macOS/Linux
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Or use your text editor to verify the JSON is valid
```

**Common issues:**
- Missing comma between server entries
- Invalid JSON syntax (use a JSON validator)
- Wrong file path or location

### Authentication Fails

**Verify the server is running:**
```bash
curl http://localhost:8000/.well-known/oauth-protected-resource
```

Should return:
```json
{
    "resource": "http://localhost:8000/mcp",
    "authorization_servers": ["http://localhost:8000/"],
    "scopes_supported": ["openid", "profile", "email"],
    "bearer_methods_supported": ["header"]
}
```

**Check Azure credentials:**
- Verify `.env` file has correct Azure credentials
- Ensure redirect URI in Azure App Registration includes `http://localhost:8000/auth/callback`
- Check that the Azure app is not disabled

### Browser Doesn't Open

If the browser doesn't open automatically:

1. Check Claude Desktop logs (if available)
2. Try manually opening: `http://localhost:8000/authorize`
3. Restart Claude Desktop
4. Verify your default browser is set correctly

### "Connection Refused" Error

**Server not running:**
```bash
# Check if server is running
curl http://localhost:8000/mcp
# Should return: {"error": "invalid_token", ...}
```

**Start the server:**
```bash
cd /path/to/newsroom-mcp
source venv/bin/activate
python run_server.py
```

### Token Expired

OAuth tokens expire after a period of time. If you get authentication errors:

1. Claude Desktop should automatically refresh the token
2. If not, you may need to re-authenticate:
   - Restart Claude Desktop
   - The OAuth flow will run again
   - Log in through the browser

### View Server Logs

To see what's happening on the server side:

```bash
# The server logs will show all requests
# Look for lines like:
INFO:     127.0.0.1:xxxxx - "POST /mcp HTTP/1.1" 200 OK
```

## Configuration Options

### Custom Port

If you need to run the server on a different port:

1. Update `.env`:
   ```bash
   MCP_SERVER_PORT=8080
   FASTMCP_SERVER_AUTH_AZURE_BASE_URL=http://localhost:8080
   ```

2. Update Claude Desktop config:
   ```json
   {
     "mcpServers": {
       "newsroom-mcp": {
         "url": "http://localhost:8080/mcp",
         "transport": "http",
         "auth": "oauth"
       }
     }
   }
   ```

3. Update Azure App Registration redirect URI to match

### Additional Scopes

To request additional Azure/Microsoft Graph scopes:

1. Update `.env`:
   ```bash
   FASTMCP_SERVER_AUTH_AZURE_REQUIRED_SCOPES=openid,profile,email,User.Read
   ```

2. Update Azure App Registration to grant these permissions

## Security Best Practices

1. **Keep the server local**: Only run on `localhost` for development
2. **Use HTTPS in production**: Never use HTTP in production environments
3. **Protect your .env**: Never commit `.env` file with real credentials
4. **Limit scopes**: Only request the minimum required OAuth scopes
5. **Regular updates**: Keep FastMCP and dependencies updated

## Example Configuration File

Here's a complete example with multiple MCP servers:

```json
{
  "mcpServers": {
    "newsroom-mcp": {
      "url": "http://localhost:8000/mcp",
      "transport": "http",
      "auth": "oauth"
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/username/Documents"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your-token-here"
      }
    }
  }
}
```

## Uninstalling

To remove the Newsroom MCP server from Claude Desktop:

1. Open the configuration file
2. Remove the `newsroom-mcp` entry from `mcpServers`
3. Save the file
4. Restart Claude Desktop

## Getting Help

If you encounter issues:

1. **Check server logs**: Look for error messages in the terminal running the server
2. **Verify configuration**: Ensure JSON is valid and paths are correct
3. **Test manually**: Use curl to test OAuth endpoints
4. **Check Azure**: Verify Azure App Registration settings

## References

- [Claude Desktop MCP Documentation](https://modelcontextprotocol.io/docs/tools/claude-desktop)
- [FastMCP Documentation](https://gofastmcp.com)
- [Azure OAuth Setup](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)

