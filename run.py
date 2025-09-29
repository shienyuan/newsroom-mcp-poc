#!/usr/bin/env python3
"""Convenience script to run the Newsroom MCP server.

This script provides a simple way to start the server with proper error handling
and helpful messages.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    try:
        from src.server import mcp
        from src.config import get_config
        
        config = get_config()
        
        print("=" * 60)
        print(f"Starting {config.server.name} v{config.server.version}")
        print("=" * 60)
        print()
        
        # Run the server
        mcp.run(
            transport="http",
            host=config.server.host,
            port=config.server.port
        )
        
    except ImportError as e:
        print("❌ Error: Missing dependencies")
        print()
        print("Please install the required dependencies:")
        print("  pip install -r requirements.txt")
        print()
        print(f"Details: {e}")
        sys.exit(1)
        
    except ValueError as e:
        print("❌ Error: Configuration problem")
        print()
        print("Please check your .env file and ensure all required")
        print("environment variables are set correctly.")
        print()
        print("Required variables:")
        print("  - FASTMCP_SERVER_AUTH_AZURE_CLIENT_ID")
        print("  - FASTMCP_SERVER_AUTH_AZURE_CLIENT_SECRET")
        print("  - FASTMCP_SERVER_AUTH_AZURE_TENANT_ID")
        print()
        print(f"Details: {e}")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print()
        print("Server stopped by user")
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

