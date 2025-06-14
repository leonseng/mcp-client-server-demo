import asyncio
import os
import time

from pydantic import FileUrl
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import ListRootsResult, Root, CreateMessageRequestParams, CreateMessageResult, TextContent
from mcp.shared.context import RequestContext


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

async def sampling_callback(
    context: RequestContext[ClientSession, None],
    params: CreateMessageRequestParams,
) -> CreateMessageResult:
    print("Sampling callback triggered")
    return CreateMessageResult(
        role="assistant",
        content=TextContent(
            type="text", text=f"You are asking about `{params.messages[0].content.text}`"
        ),
        model="test-model",
        stopReason="endTurn",
    )

async def logging_callback(
    context: RequestContext[ClientSession, None]
) -> None:
    print(f"Logging callback triggered: {context.logger}:{context.level} - {context.data}")


async def main():
    SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000/mcp/")
    print(f"Connecting to server at {SERVER_URL}...")

    async with streamablehttp_client(SERVER_URL) as (read, write, _):
        async with ClientSession(read, write, logging_callback=logging_callback, list_roots_callback=list_roots_callback, sampling_callback=sampling_callback) as session:
            await session.initialize()

            print("\n# List resources")
            res = await session.list_resources()
            print(f"Found {len(res.resources)} resource(s): {[r.name for r in res.resources]}")

            print("\n# Get resource")
            res = await session.read_resource("time://now")
            print(f"Current time: {res.contents[0].text}")
            time.sleep(1)

            print("\n# Get resource template")
            res = await session.list_resource_templates()
            print(f"Found {len(res.resourceTemplates)} resource template(s): {[rt.name for rt in res.resourceTemplates]}")
            user = "John"
            res = await session.read_resource(f"users://{user}/id")
            print(f"{user}'s ID: {res.contents[0].text}")
            time.sleep(1)

            print("\n# Call basic tool: base64_encode")
            input_string = "hello"
            res = await session.call_tool("base64_encode", {"input_string": input_string})
            print(f"Response: base64 encoding of {input_string} is {res.content[0].text}")
            time.sleep(1)

            # Call tool to check file exists on server, within directories defined by client via Roots
            print("\n# Call tool to test client capability: list_roots ")
            res = await session.call_tool("file_exists", {"filename": "pyproject.toml"})
            print(f"Response: {res.content[0].text}")
            time.sleep(1)

            # Call tool to test sampling, i.e. server calling LLM via client
            print("\n# Call tool to test client capability: sampling")
            res = await session.call_tool("sampling_test", {"message": "some input"})
            print(f"Response: {res.content[0].text}")
            time.sleep(1)

            print ("\n# Send notification to server")
            # Observe behaviour in packet capture
            await session.send_roots_list_changed()
            time.sleep(1)

            print ("\n# Trigger server to send notification to client")
            await session.call_tool("trigger_server_notifications")
            time.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
