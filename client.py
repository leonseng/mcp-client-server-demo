import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main():
    server_url = "http://127.0.0.1:8000/mcp/"

    async with streamablehttp_client(server_url) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print()
            print("# List resources")
            res = await session.list_resources()
            print(f"Found {len(res.resources)} resource(s): {[r.name for r in res.resources]}")
            res = await session.read_resource("users://names")
            print(f"Users: {json.loads(res.contents[0].text)}\n")

            print("# Get resource template")
            res = await session.list_resource_templates()
            print(f"Found {len(res.resourceTemplates)} resource template(s): {[rt.name for rt in res.resourceTemplates]}")
            user = "John"
            res = await session.read_resource(f"users://{user}/id")
            print(f"{user}'s ID: {res.contents[0].text}\n")

            print("# Call tool")
            res = await session.list_tools()
            print(f"Found {len(res.tools)} tool(s): {[t.name for t in res.tools]}")
            text = "hello"
            res = await session.call_tool("to_upper_case", {"input_str": text})
            print(f"Converting '{text}' to upper case: {res.content[0].text}\n")


if __name__ == "__main__":
    asyncio.run(main())