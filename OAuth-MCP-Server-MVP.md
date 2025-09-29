# OAuth MCP Server MVP

## 🚀 Overview

This document outlines a comprehensive MVP (Minimum Viable Product) for building a simple OAuth MCP server with Azure authentication and a hello world route. The implementation uses FastMCP framework with Azure OAuth integration through the OAuth Proxy pattern.

## 📋 Research Summary

### Key Findings

- **FastMCP Framework**: The standard Python framework for building MCP servers with decorators like `@mcp.tool`, `@mcp.resource`, and `@mcp.prompt`
- **Azure OAuth Integration**: Uses OAuth Proxy pattern since Azure doesn't support Dynamic Client Registration (DCR)
- **Authentication Pattern**: OAuth Proxy bridges traditional OAuth with MCP's DCR expectations
- **Transport**: HTTP transport required for OAuth flows
- **Environment Configuration**: Production-ready with environment variable management

### Architecture Components

1. **FastMCP Server**: Core MCP server implementation
2. **Azure OAuth Provider**: Authentication using Microsoft Entra ID
3. **OAuth Proxy**: Handles DCR translation and callback forwarding
4. **Environment Management**: Secure credential handling
5. **HTTP Transport**: Required for OAuth authentication flows

## 🏗️ Implementation Plan

### Project Structure

```
oauth-mcp-server-mvp/
├── server.py              # Main MCP server implementation
├── .env                   # Environment variables (not in git)
├── .env.example          # Example environment file
├── requirements.txt       # Python dependencies
├── README.md             # Setup and usage instructions
└── .gitignore            # Git ignore file
```

### Core Files

#### 1. Main Server (`server.py`)

```python
import os
import logging
from fastmcp import FastMCP
from fastmcp.server.auth.providers.azure import AzureProvider
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server with Azure OAuth
mcp = FastMCP(
    name="Azure OAuth MCP Server MVP",
    instructions="A simple MCP server with Azure OAuth authentication and a hello world tool."
)

# Configure Azure OAuth (auto-configures from environment variables)
try:
    azure_auth = AzureProvider()
    mcp.auth = azure_auth
    logger.info("Azure OAuth provider configured successfully")
except Exception as e:
    logger.error(f"Failed to configure Azure OAuth: {e}")
    raise

@mcp.tool
async def hello_world(name: str = "World") -> str:
    """A simple hello world tool that demonstrates authenticated MCP functionality."""
    return f"Hello, {name}! You've successfully authenticated with Azure and accessed this MCP tool."

@mcp.tool
async def server_info() -> dict:
    """Get information about this MCP server."""
    return {
        "name": "Azure OAuth MCP Server MVP",
        "version": "1.0.0",
        "authentication": "Azure OAuth (Microsoft Entra ID)",
        "tools": ["hello_world", "server_info"]
    }

if __name__ == "__main__":
    logger.info("Starting Azure OAuth MCP Server...")
    mcp.run(transport="http", host="localhost", port=8000)
```

#### 2. Environment Configuration (`.env`)

```env
# Azure OAuth Configuration
FASTMCP_SERVER_AUTH_AZURE_CLIENT_ID=your-azure-client-id-here
FASTMCP_SERVER_AUTH_AZURE_CLIENT_SECRET=your-azure-client-secret-here
FASTMCP_SERVER_AUTH_AZURE_TENANT_ID=your-azure-tenant-id-here
FASTMCP_SERVER_AUTH_AZURE_BASE_URL=http://localhost:8000
FASTMCP_SERVER_AUTH_AZURE_REDIRECT_PATH=/auth/callback
FASTMCP_SERVER_AUTH_AZURE_REQUIRED_SCOPES=openid,profile,email
FASTMCP_SERVER_AUTH_AZURE_TIMEOUT_SECONDS=30
```

#### 3. Dependencies (`requirements.txt`)

```txt
fastmcp[auth]>=2.9.0
python-dotenv>=1.0.0
```

## ⚙️ Azure Setup Requirements

### 1. Azure App Registration

1. Go to **Azure Portal** → **Microsoft Entra ID** → **App registrations**
2. Click **"New registration"**
3. Set application name: `"MCP OAuth Server MVP"`
4. Set redirect URI: `http://localhost:8000/auth/callback`
5. Click **"Register"**

### 2. Configure Credentials

1. Note the **Application (client) ID** from the Overview page
2. Go to **"Certificates & secrets"** → **"New client secret"**
3. Create and note the **client secret value**
4. Note the **Directory (tenant) ID** from the Overview page

### 3. Set Permissions (Optional)

- Add Microsoft Graph permissions if needed (e.g., `User.Read`)

## 🔧 Key Features

### 🔐 OAuth Proxy Pattern

- Bridges Azure's traditional OAuth with MCP's Dynamic Client Registration expectations
- Handles callback forwarding and token exchange automatically
- Maintains full OAuth 2.1 and PKCE security

### 🛠️ MCP Tools

- **`hello_world`**: Simple greeting tool requiring authentication
- **`server_info`**: Returns server metadata and capabilities

### 🔍 OAuth Discovery

- Automatic OAuth discovery endpoints at `/.well-known/oauth-protected-resource`
- MCP clients can automatically discover authentication requirements

## 🚦 Usage Flow

1. **Start Server**: `python server.py`
2. **Client Discovery**: MCP clients discover OAuth requirements
3. **Authentication**: Client redirects user to Azure login
4. **Token Exchange**: Server handles OAuth callback and token validation
5. **Tool Access**: Authenticated clients can call `hello_world` and `server_info` tools

## 🧪 Testing the MVP

### Manual Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables in .env file
cp .env.example .env
# Edit .env with your Azure credentials

# Start the server
python server.py
```

### Client Integration

- **Server URL**: `http://localhost:8000`
- **MCP Endpoint**: `http://localhost:8000/mcp`
- **OAuth Discovery**: `http://localhost:8000/.well-known/oauth-protected-resource`

## 🔒 Security Considerations

- ✅ Uses OAuth 2.1 with PKCE
- ✅ Environment-based credential management
- ✅ Automatic token validation via Microsoft Graph
- ✅ Secure callback handling
- ✅ Request correlation logging

## 🚀 Next Steps for Enhancement

1. **Add More Tools**: Expand functionality beyond hello world
2. **Database Integration**: Add persistent storage for user data
3. **Advanced Scopes**: Implement fine-grained permissions
4. **Deployment**: Configure for production environments
5. **Monitoring**: Add metrics and health checks
6. **Resource Management**: Add MCP resources for data access
7. **Prompt Templates**: Implement reusable prompt templates

## 📚 Technical References

### FastMCP Documentation
- [FastMCP Getting Started](https://gofastmcp.com/getting-started/welcome)
- [Azure OAuth Integration](https://gofastmcp.com/integrations/azure)
- [OAuth Proxy Pattern](https://gofastmcp.com/servers/auth/oauth-proxy)

### Azure Documentation
- [Azure App Registration](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [OAuth 2.0 and OpenID Connect](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-protocols)

## 🎯 Success Criteria

This MVP successfully demonstrates:

- ✅ **OAuth Authentication**: Working Azure OAuth integration
- ✅ **MCP Protocol**: Compliant MCP server implementation
- ✅ **Tool Protection**: Authenticated access to server tools
- ✅ **Discovery**: Automatic OAuth requirement discovery
- ✅ **Security**: Production-ready security practices
- ✅ **Extensibility**: Foundation for additional features

---

*This MVP provides a solid foundation for building more complex OAuth-protected MCP servers while demonstrating the core concepts and patterns needed for Azure authentication integration.*
