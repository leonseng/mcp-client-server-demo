from datetime import datetime
import os

from mcp.server.fastmcp import FastMCP

HOST = os.getenv("MCP_SERVER_HOST", "127.0.0.1")
PORT = os.getenv("MCP_SERVER_PORT", 8000)

mcp = FastMCP("My mcp", stateless_http=True, host=HOST, port=PORT)

@mcp.tool()
def to_upper_case(input_str: str) -> str:
    return input_str.upper()

@mcp.resource("users://{user_name}/id")
def get_user_id(user_name: str) -> str:
    return user_name.encode("utf-8").hex()

@mcp.resource("time://now")
def get_time() -> str:
    return datetime.now().isoformat()


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
