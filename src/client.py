import asyncio
import os
import time

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000/mcp/")

async def main():
    print(f"Connecting to server at {SERVER_URL}...")

    async with streamablehttp_client(SERVER_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
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

            print("# Call tool")
            res = await session.list_tools()
            print(f"Found {len(res.tools)} tool(s): {[t.name for t in res.tools]}")
            text = "hello"
            res = await session.call_tool("to_upper_case", {"input_str": text})
            print(f"Converting '{text}' to upper case: {res.content[0].text}\n")
            time.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())