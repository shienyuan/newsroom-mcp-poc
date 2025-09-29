# Newsroom MCP - OAuth MCP Server

> A Model Context Protocol (MCP) server with Azure OAuth authentication, showcasing all three core MCP features: Resources, Tools, and Prompts.

[![FastMCP](https://img.shields.io/badge/FastMCP-2.9.0+-blue.svg)](https://gofastmcp.com)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Overview

This project implements an MCP server with Azure OAuth authentication using the FastMCP framework. It demonstrates all three core MCP primitives (Resources, Tools, and Prompts) with simple examples, while maintaining enterprise-grade security through Microsoft Entra ID (Azure AD).

### What is MCP?

The Model Context Protocol (MCP) is an open protocol that enables AI assistants to securely interact with external tools, data sources, and services. This server implements MCP with OAuth authentication, allowing AI assistants to access protected resources on behalf of authenticated users.

### MCP Core Features

This server demonstrates:
- **Resources** - Expose data and content for AI context
- **Tools** - Enable AI to perform actions and operations
- **Prompts** - Provide reusable prompt templates

## ✨ Features

- 🔐 **Azure OAuth Authentication** - Secure authentication via Microsoft Entra ID
- � **MCP Resources** - Authenticated data access for AI context
- 🛠️ **MCP Tools** - Authenticated actions and operations
- 💬 **MCP Prompts** - Reusable prompt templates
- 🔍 **OAuth Discovery** - Automatic authentication requirement discovery
- 🔒 **OAuth 2.1 + PKCE** - Modern security standards
- 📝 **Environment-based Config** - Secure credential management
- 🚦 **HTTP Transport** - Required for OAuth flows
- 📊 **Logging & Monitoring** - Request correlation and audit trails

## 📋 Prerequisites

- Python 3.8 or higher
- Azure account with app registration permissions
- pip (Python package manager)

## 🏗️ Project Structure

```
newsroom-mcp/
├── src/
│   ├── __init__.py                # Package initialization
│   ├── server.py                  # Main MCP server implementation
│   ├── config.py                  # Configuration management
│   └── mcp/
│       ├── __init__.py
│       ├── resources/
│       │   ├── __init__.py
│       │   └── sample.py          # Sample resource implementations
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── echo.py            # Echo tool implementation
│       │   └── info.py            # Server info tool
│       └── prompts/
│           ├── __init__.py
│           └── greeting.py        # Greeting prompt template
├── tests/
│   ├── __init__.py
│   ├── test_resources.py          # Resource tests
│   ├── test_tools.py              # Tool tests
│   └── test_prompts.py            # Prompt tests
├── docs/
│   └── OAuth-MCP-Server-MVP.md    # Detailed implementation plan
├── .env                           # Environment variables (not in git)
├── .env.example                   # Example environment file
├── .gitignore                     # Git ignore file
├── pyproject.toml                 # Modern Python project configuration
├── requirements.txt               # Python dependencies (or use pyproject.toml)
└── README.md                      # This file
```

### Structure Explanation

- **`src/`** - Main application source following src-layout pattern
  - **`mcp/`** - MCP-specific implementations
    - **`resources/`** - MCP resource implementations
    - **`tools/`** - MCP tool implementations
    - **`prompts/`** - MCP prompt template implementations
  - **`config.py`** - Centralized configuration and environment management
  - **`server.py`** - Main server entry point
- **`tests/`** - Test suite with pytest
- **`docs/`** - Documentation files
- **`pyproject.toml`** - Modern Python packaging and dependency management

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd newsroom-mcp
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Azure App Registration

#### Create Azure App Registration

1. Navigate to [Azure Portal](https://portal.azure.com)
2. Go to **Microsoft Entra ID** → **App registrations**
3. Click **"New registration"**
4. Configure:
   - **Name**: `Newsroom MCP Server`
   - **Supported account types**: Choose based on your needs
   - **Redirect URI**: 
     - Platform: `Web`
     - URI: `http://localhost:8000/auth/callback`
5. Click **"Register"**

#### Get Credentials

1. **Application (client) ID**: Copy from the Overview page
2. **Directory (tenant) ID**: Copy from the Overview page
3. **Client Secret**:
   - Go to **"Certificates & secrets"**
   - Click **"New client secret"**
   - Add description and expiration
   - **Copy the secret value immediately** (you won't see it again!)

#### Set API Permissions (Optional)

1. Go to **"API permissions"**
2. Add permissions as needed (e.g., `User.Read` for Microsoft Graph)
3. Grant admin consent if required

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Azure credentials
nano .env  # or use your preferred editor
```

Update `.env` with your Azure credentials:

```env
# Azure OAuth Configuration
FASTMCP_SERVER_AUTH_AZURE_CLIENT_ID=your-application-client-id
FASTMCP_SERVER_AUTH_AZURE_CLIENT_SECRET=your-client-secret-value
FASTMCP_SERVER_AUTH_AZURE_TENANT_ID=your-directory-tenant-id
FASTMCP_SERVER_AUTH_AZURE_BASE_URL=http://localhost:8000
FASTMCP_SERVER_AUTH_AZURE_REDIRECT_PATH=/auth/callback
FASTMCP_SERVER_AUTH_AZURE_REQUIRED_SCOPES=openid,profile,email
FASTMCP_SERVER_AUTH_AZURE_TIMEOUT_SECONDS=30
```

### 5. Install the Package (Development Mode)

```bash
# Install in editable mode with all dependencies
pip install -e .

# Or if using requirements file
pip install -r requirements.txt
```

### 6. Start the Server

```bash
# Run from the project root
python -m src.server

# Or run directly
python src/server.py
```

You should see:

```
INFO:src.server:Azure OAuth provider configured successfully
INFO:src.server:Starting Azure OAuth MCP Server...
INFO:uvicorn:Started server process
INFO:uvicorn:Waiting for application startup.
INFO:uvicorn:Application startup complete.
INFO:uvicorn:Uvicorn running on http://localhost:8000
```

## 🔧 Available MCP Features

This POC implements simple examples of all three MCP primitives:

### 📦 Resources

Resources expose data and content that can be used as context by AI assistants.

#### `sample_data`

A simple resource that returns sample JSON data.

**URI:** `sample://data`

**Returns:** Static JSON object with sample information.

**Example Response:**
```json
{
  "message": "This is sample data from an MCP resource",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "id": 1,
    "name": "Sample Resource",
    "type": "demonstration"
  }
}
```

### 🛠️ Tools

Tools enable AI assistants to perform actions and operations.

#### `echo`

A simple echo tool that returns the input message.

**Parameters:**
- `message` (string, required): The message to echo back.

**Returns:** The same message that was provided.

**Example:**
```json
{
  "name": "echo",
  "arguments": {
    "message": "Hello, MCP!"
  }
}
```

**Response:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "Echo: Hello, MCP!"
    }
  ]
}
```

#### `server_info`

Returns metadata about the MCP server and its capabilities.

**Parameters:** None

**Returns:** Server information including name, version, authentication method, and available features.

**Example:**
```json
{
  "name": "server_info",
  "arguments": {}
}
```

**Response:**
```json
{
  "name": "Newsroom MCP",
  "version": "1.0.0",
  "authentication": "Azure OAuth (Microsoft Entra ID)",
  "features": {
    "resources": ["sample_data"],
    "tools": ["echo", "server_info"],
    "prompts": ["greeting_template"]
  }
}
```

### 💬 Prompts

Prompts provide reusable prompt templates for common workflows.

#### `greeting_template`

A simple prompt template for generating personalized greetings.

**Parameters:**
- `name` (string, required): The name of the person to greet.
- `style` (string, optional): The greeting style (formal/casual). Defaults to "casual".

**Returns:** A prompt template for generating a greeting.

**Example:**
```json
{
  "name": "greeting_template",
  "arguments": {
    "name": "Alice",
    "style": "formal"
  }
}
```

**Generated Prompt:**
```
Generate a formal greeting for Alice.
The greeting should be professional and respectful.
```

## 🔌 Client Integration

### MCP Client Configuration

Configure your MCP client to connect to the server:

```json
{
  "mcpServers": {
    "newsroom-oauth": {
      "url": "http://localhost:8000/mcp",
      "transport": "http"
    }
  }
}
```

### Endpoints

- **MCP Endpoint**: `http://localhost:8000/mcp`
- **OAuth Discovery**: `http://localhost:8000/.well-known/oauth-protected-resource`
- **OAuth Callback**: `http://localhost:8000/auth/callback`
- **Health Check**: `http://localhost:8000/health` (if implemented)

### Authentication Flow

1. **Discovery**: Client fetches OAuth configuration from discovery endpoint
2. **Authorization**: Client redirects user to Azure login page
3. **Callback**: Azure redirects back to server with authorization code
4. **Token Exchange**: Server exchanges code for access token
5. **Tool Access**: Client uses token to call authenticated MCP tools

## 🔒 Security Best Practices

### Environment Variables

- ✅ Never commit `.env` file to version control
- ✅ Use strong, unique client secrets
- ✅ Rotate secrets regularly (before expiration)
- ✅ Use different credentials for dev/staging/production

### OAuth Configuration

- ✅ Use HTTPS in production (required for OAuth)
- ✅ Validate redirect URIs strictly
- ✅ Implement token expiration and refresh
- ✅ Use minimal required scopes
- ✅ Enable audit logging

### Production Deployment

- ✅ Use environment-specific configurations
- ✅ Enable HTTPS/TLS
- ✅ Implement rate limiting
- ✅ Set up monitoring and alerting
- ✅ Use secrets management service (Azure Key Vault, etc.)

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_tools.py

# Run with verbose output
pytest -v
```

### Manual Testing

```bash
# Test server health
curl http://localhost:8000/health

# Test OAuth discovery
curl http://localhost:8000/.well-known/oauth-protected-resource

# Test with MCP client (requires authentication)
# Use Claude Desktop or another MCP-compatible client
```

### Testing with Claude Desktop

1. Add server configuration to Claude Desktop settings
2. Restart Claude Desktop
3. Authenticate via Azure when prompted
4. Try the different MCP features:
   - **Resource**: "Show me the sample_data resource"
   - **Tool**: "Use the echo tool to repeat 'Hello MCP'"
   - **Prompt**: "Use the greeting_template prompt for Alice in formal style"

## 🐛 Troubleshooting

### Server won't start

- **Check Python version**: Ensure Python 3.8+
- **Verify dependencies**: Run `pip install -r requirements.txt`
- **Check environment variables**: Ensure all required vars are set in `.env`
- **Port conflict**: Ensure port 8000 is available

### Authentication fails

- **Verify Azure credentials**: Double-check client ID, secret, and tenant ID
- **Check redirect URI**: Must match exactly in Azure and `.env`
- **Inspect logs**: Look for error messages in server output
- **Token expiration**: Client secret may have expired

### Tools not accessible

- **Authentication required**: Ensure OAuth flow completed successfully
- **Check scopes**: Verify required scopes are granted
- **Token validation**: Check server logs for token validation errors

## 📚 Documentation

- [FastMCP Documentation](https://gofastmcp.com)
- [Azure OAuth Integration](https://gofastmcp.com/integrations/azure)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [OAuth 2.1 Specification](https://oauth.net/2.1/)
- [Azure App Registration Guide](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)

## 🚀 Next Steps

- [ ] Add business-specific MCP tools
- [ ] Implement real data sources for resources
- [ ] Create domain-specific prompt templates
- [ ] Set up database integration
- [ ] Configure production deployment
- [ ] Add monitoring and metrics
- [ ] Implement fine-grained permissions
- [ ] Add API key authentication option (for service-to-service)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastMCP](https://gofastmcp.com) - MCP server framework
- [Anthropic](https://anthropic.com) - MCP protocol specification
- [Microsoft Azure](https://azure.microsoft.com) - OAuth provider

## 📞 Support

For questions or issues:

- Open an issue in this repository
- Check the [FastMCP documentation](https://gofastmcp.com)
- Review the [OAuth-MCP-Server-MVP.md](OAuth-MCP-Server-MVP.md) implementation plan

---

**Built with ❤️ using FastMCP and Azure OAuth**

