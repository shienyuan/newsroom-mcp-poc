# Newsroom MCP - Quick Start Guide

## 🚀 Quick Setup for Claude Desktop

### 1. Start the Server

```bash
cd /path/to/newsroom-mcp
source venv/bin/activate
python run_server.py
```

### 2. Add to Claude Desktop

**Config file location:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Add this configuration:**

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

### 3. Restart Claude Desktop

Completely quit and restart Claude Desktop (Cmd+Q on macOS, or quit from system tray).

### 4. Authenticate

When Claude Desktop connects, your browser will open for Azure login. Sign in with your Microsoft account.

### 5. Test It!

Ask Claude:
- "What MCP servers are available?"
- "Use the echo tool to say 'Hello!'"
- "Show me the sample_data resource"

---

## 🔧 Quick Setup for Augment Code

### 1. Start the Server

```bash
cd /path/to/newsroom-mcp
source venv/bin/activate
python run_server.py
```

### 2. Add to Augment Code

Add to your Augment Code MCP configuration:

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

### 3. Authenticate

Augment Code will open your browser for Azure OAuth authentication.

---

## 📦 Available Features

### Resources
- **sample_data** (`sample://data`) - Returns sample JSON data

### Tools
- **echo** - Echoes back your message
- **server_info** - Returns server metadata

### Prompts
- **greeting_template** - Generates personalized greetings

---

## 🔍 Troubleshooting

### Server won't start?
```bash
# Check if .env file exists
ls -la .env

# Verify dependencies
source venv/bin/activate
pip list | grep fastmcp
```

### Can't connect from Claude Desktop?
1. Verify server is running: `curl http://localhost:8000/.well-known/oauth-protected-resource`
2. Check JSON syntax in config file
3. Completely restart Claude Desktop

### Authentication fails?
1. Check Azure credentials in `.env`
2. Verify redirect URI in Azure App Registration: `http://localhost:8000/auth/callback`
3. Try re-authenticating by restarting the client

---

## 📚 Full Documentation

- **Claude Desktop Setup**: See `docs/CLAUDE_DESKTOP_SETUP.md`
- **Augment Code Setup**: See `docs/AUGMENT_CODE_SETUP.md`
- **Project README**: See `README.md`

---

## 🆘 Quick Commands

```bash
# Start server
python run_server.py

# Test OAuth discovery
curl http://localhost:8000/.well-known/oauth-protected-resource

# Test OAuth metadata
curl http://localhost:8000/.well-known/oauth-authorization-server

# Check server is protecting MCP endpoint
curl http://localhost:8000/mcp
# Should return: {"error": "invalid_token", ...}

# View server logs
# Just watch the terminal where run_server.py is running
```

---

## ✅ Checklist

- [ ] Server running on http://localhost:8000
- [ ] Configuration added to Claude Desktop/Augment Code
- [ ] Client restarted
- [ ] Browser opened for OAuth
- [ ] Logged in with Microsoft account
- [ ] Can see MCP server in client
- [ ] Can call tools/resources

---

**Need help?** Check the full documentation in the `docs/` folder!

