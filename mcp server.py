#!/usr/bin/env python3
import asyncio
import json
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Create server instance
server = Server("dummy-api-server")

# Dummy data store
users_db = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
]

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """List available tools"""
    return [
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

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls"""
    
    if name == "get_users":
        return [types.TextContent(
            type="text",
            text=json.dumps(users_db, indent=2)
        )]
    
    elif name == "get_user":
        user_id = arguments.get("user_id")
        user = next((u for u in users_db if u["id"] == user_id), None)
        if user:
            return [types.TextContent(type="text", text=json.dumps(user, indent=2))]
        else:
            return [types.TextContent(type="text", text=f"User with ID {user_id} not found")]
    
    elif name == "create_user":
        new_id = max(u["id"] for u in users_db) + 1 if users_db else 1
        new_user = {
            "id": new_id,
            "name": arguments["name"],
            "email": arguments["email"]
        }
        users_db.append(new_user)
        return [types.TextContent(
            type="text", 
            text=f"Created user: {json.dumps(new_user, indent=2)}"
        )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")

async def main():
    """Run the server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="dummy-api-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())