import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My mcp", stateless_http=True, host="127.0.0.1", port=8000)


@mcp.tool()
def to_upper_case(input_str: str) -> str:
    return input_str.upper()

@mcp.resource("users://{user_name}/id")
def get_user_id(user_name: str) -> str:
    return user_name.encode("utf-8").hex()

@mcp.resource("users://names")
def list_users()-> list[str]:
    user_names = ["alice", "bob", "charlie", "dave", "eve"]
    return user_names


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
