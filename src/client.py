import asyncio
import os
import time

from pydantic import FileUrl
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import ListRootsResult, Root
from mcp.shared.context import RequestContext

SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000/mcp/")

async def list_roots_callback(context: RequestContext[ClientSession, None]) -> ListRootsResult:
    print("List roots callback triggered")
    return ListRootsResult(
        roots=[
            Root(
                uri=FileUrl("file:///tmp/"),
                name="search_directory_1",
            ),
            Root(
                uri=FileUrl("file://."),
                name="search_directory_2",
            )
        ]
    )

async def main():
    print(f"Connecting to server at {SERVER_URL}...")

    async with streamablehttp_client(SERVER_URL) as (read, write, _):
        async with ClientSession(read, write, list_roots_callback=list_roots_callback) as session:
            await session.initialize()
            print()

            print("# List resources")
            res = await session.list_resources()
            print(f"Found {len(res.resources)} resource(s): {[r.name for r in res.resources]}")
            res = await session.read_resource("time://now")
            print(f"Current time: {res.contents[0].text}\n")
            time.sleep(1)

            print("# Get resource template")
            res = await session.list_resource_templates()
            print(f"Found {len(res.resourceTemplates)} resource template(s): {[rt.name for rt in res.resourceTemplates]}")
            user = "John"
            res = await session.read_resource(f"users://{user}/id")
            print(f"{user}'s ID: {res.contents[0].text}\n")
            time.sleep(1)

            # Call tool to check file exists on server, within directories defined by client via Roots
            print("# Call tool")
            res = await session.call_tool("file_exists", {"filename": "pyproject.toml"})
            print(f"Response: {res.content[0].text}\n")
            time.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())