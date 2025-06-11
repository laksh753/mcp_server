#!/usr/bin/env python3
import asyncio
import json
import sys
import logging
from typing import Any, Dict, List, Optional

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from mcp.server import Server
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
    logger.info("MCP imports successful")
except ImportError as e:
    logger.error(f"Failed to import MCP: {e}")
    print("Error: MCP library not found. Install with: pip install mcp")
    sys.exit(1)

# Create server instance
server = Server("dummy-api-server")
logger.info("Server instance created")

# Dummy data store
users_db = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
]

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available tools"""
    logger.info("Listing tools")
    try:
        tools = [
            types.Tool(
                name="get_users",
                description="Get all users from the dummy database",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            types.Tool(
                name="get_user",
                description="Get a specific user by ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "integer",
                            "description": "The ID of the user to retrieve"
                        }
                    },
                    "required": ["user_id"]
                }
            ),
            types.Tool(
                name="create_user",
                description="Create a new user",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "User's name"},
                        "email": {"type": "string", "description": "User's email"}
                    },
                    "required": ["name", "email"]
                }
            )
        ]
        logger.info(f"Returning {len(tools)} tools")
        return tools
    except Exception as e:
        logger.error(f"Error in list_tools: {e}")
        raise

@server.call_tool()
async def handle_call_tool(name: str, arguments: Optional[Dict[str, Any]] = None) -> List[types.TextContent]:
    """Handle tool calls"""
    logger.info(f"Tool called: {name} with arguments: {arguments}")
    
    if arguments is None:
        arguments = {}
    
    try:
        if name == "get_users":
            result = json.dumps(users_db, indent=2)
            logger.info("Returning all users")
            return [types.TextContent(type="text", text=result)]
        
        elif name == "get_user":
            user_id = arguments.get("user_id")
            if user_id is None:
                error_msg = "Error: user_id is required"
                logger.warning(error_msg)
                return [types.TextContent(type="text", text=error_msg)]
            
            user = next((u for u in users_db if u["id"] == user_id), None)
            if user:
                result = json.dumps(user, indent=2)
                logger.info(f"Found user with ID {user_id}")
                return [types.TextContent(type="text", text=result)]
            else:
                error_msg = f"User with ID {user_id} not found"
                logger.warning(error_msg)
                return [types.TextContent(type="text", text=error_msg)]
        
        elif name == "create_user":
            user_name = arguments.get("name")
            email = arguments.get("email")
            
            if not user_name or not email:
                error_msg = "Error: Both name and email are required"
                logger.warning(error_msg)
                return [types.TextContent(type="text", text=error_msg)]
            
            # Check if email already exists
            existing_user = next((u for u in users_db if u["email"] == email), None)
            if existing_user:
                error_msg = f"Error: User with email {email} already exists"
                logger.warning(error_msg)
                return [types.TextContent(type="text", text=error_msg)]
            
            new_id = max(u["id"] for u in users_db) + 1 if users_db else 1
            new_user = {
                "id": new_id,
                "name": user_name,
                "email": email
            }
            users_db.append(new_user)
            result = f"Created user: {json.dumps(new_user, indent=2)}"
            logger.info(f"Created new user with ID {new_id}")
            return [types.TextContent(type="text", text=result)]
        
        else:
            error_msg = f"Error: Unknown tool '{name}'"
            logger.error(error_msg)
            return [types.TextContent(type="text", text=error_msg)]
            
    except Exception as e:
        error_msg = f"Error processing tool '{name}': {str(e)}"
        logger.error(error_msg)
        return [types.TextContent(type="text", text=error_msg)]

async def main():
    """Run the server"""
    logger.info("Starting MCP server...")
    
    try:
        # Test if we can create the stdio server
        logger.info("Creating stdio server...")
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            logger.info("Stdio server created successfully")
            
            # Create initialization options
            # Create a simple notification options object
            class SimpleNotificationOptions:
                def __init__(self):
                    self.tools_changed = False
                    self.prompts_changed = False  
                    self.resources_changed = False
            
            notification_options = SimpleNotificationOptions()
            
            init_options = InitializationOptions(
                server_name="dummy-api-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=notification_options,
                    experimental_capabilities={}
                )
            )
            logger.info("Initialization options created")
            
            # Run the server
            logger.info("Running server...")
            await server.run(read_stream, write_stream, init_options)
            
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

def test_server():
    """Simple test function to verify server components"""
    print("Testing server components...")
    
    # Test tool listing
    try:
        import asyncio
        tools = asyncio.run(handle_list_tools())
        print(f"✓ Tools list working: {len(tools)} tools found")
    except Exception as e:
        print(f"✗ Tools list failed: {e}")
        return False
    
    # Test tool calling
    try:
        result = asyncio.run(handle_call_tool("get_users", {}))
        print(f"✓ Tool calling working: {len(result)} results")
    except Exception as e:
        print(f"✗ Tool calling failed: {e}")
        return False
    
    print("✓ All tests passed!")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_server()
    else:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\nServer stopped.")
        except Exception as e:
            print(f"Fatal error: {e}")
            sys.exit(1)
