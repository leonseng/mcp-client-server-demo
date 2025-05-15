# MCP Client-Server Demo

Basic demo of MCP client-server model using the MCP Python SDK

## Prerequisite

- [uv](https://github.com/astral-sh/uv)

Setup the Python execution environment
```
uv sync
source .venv/bin/activate
```

## Demo Instructions

Start the MCP server
```
uv run server.py
```

In a separate terminal, run the MCP client
```
uv run client.py
```

You should see
```
# List resources
Found 1 resource(s): ['users://names']
Users: ['alice', 'bob', 'charlie', 'dave', 'eve']

# Get resource template
Found 1 resource template(s): ['get_user_id']
John's ID: 4a6f686e

# Call tool
Found 1 tool(s): ['to_upper_case']
Converting 'hello' to upper case: HELLO
```


## Project bootstrap

> This section can be safely ignored, and is only here for project bootstrap documentation purposes

```
uv venv
source .venv/bin/activate
uv init
uv add "mcp[cli]"
```
