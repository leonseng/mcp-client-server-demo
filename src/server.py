from datetime import datetime
import os

from mcp.server.fastmcp import FastMCP
from mcp.types import SamplingMessage, TextContent

HOST = os.getenv("MCP_SERVER_HOST", "127.0.0.1")
PORT = os.getenv("MCP_SERVER_PORT", 8000)

mcp = FastMCP("My mcp", host=HOST, port=PORT)  # optional parameter: json_response=True

@mcp.resource("users://{user_name}/id")
def get_user_id(user_name: str) -> str:
    return user_name.encode("utf-8").hex()

@mcp.resource("time://now")
def get_time() -> str:
    return datetime.now().isoformat()

@mcp.tool()
async def file_exists(filename: str) -> str:
    roots = await mcp.get_context().session.list_roots()  # list roots defined by client to define search boundary on server

    for r in roots.roots:
        if r.name.startswith("search_directory"):
            file_dir = r.uri.host + r.uri.path if r.uri.host else r.uri.path
            # convert to absolute path
            if not os.path.isabs(file_dir):
                file_dir = os.path.abspath(file_dir)

            if os.path.exists(os.path.join(file_dir, filename)):
                return f"Found {filename} in {file_dir}"

    return f"File {filename} does not exist."

@mcp.tool()
async def sampling_test(message: str) -> str:
    value = await mcp.get_context().session.create_message(
            messages=[
                SamplingMessage(
                    role="user", content=TextContent(type="text", text=message)
                )
            ],
            max_tokens=100,
        )

    return value.content.text

@mcp.tool()
async def trigger_server_notifications() -> None:

    await mcp.get_context().session.send_ping()

    # client SDK does not seem to have a callback to handle this currently
    await mcp.get_context().session.send_tool_list_changed()

    await mcp.get_context().session.send_log_message("info", "This is sent via secondary SSE stream", logger="log_stream")

    # doesn't work if server is configured to respond in JSON (log entry not observed in response)
    await mcp.get_context().log("error", "This is sent via response to client request", logger_name="log_stream")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
