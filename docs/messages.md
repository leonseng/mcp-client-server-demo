# Message flows

## Initialization

<details>
<summary>Initialization request</summary>

```
POST /mcp/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: python-httpx/0.28.1
Accept: application/json, text/event-stream
content-type: application/json
Content-Length: 194
{"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{"sampling":{},"roots":{"listChanged":true}},"clientInfo":{"name":"mcp","version":"0.1.0"}},"jsonrpc":"2.0","id":0}

HTTP/1.1 200 OK
date: Fri, 16 May 2025 06:20:20 GMT
server: uvicorn
cache-control: no-cache, no-transform
connection: keep-alive
content-type: text/event-stream
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
x-accel-buffering: no
Transfer-Encoding: chunked
event: message
data: {"jsonrpc":"2.0","id":0,"result":{"protocolVersion":"2024-11-05","capabilities":{"experimental":{},"prompts":{"listChanged":false},"resources":{"subscribe":false,"listChanged":false},"tools":{"listChanged":false}},"serverInfo":{"name":"My mcp","version":"1.8.1"}}}
```
</details>

<details>
<summary>Initialized notification</summary>

```
POST /mcp/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: python-httpx/0.28.1
Accept: application/json, text/event-stream
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
Content-Length: 54

{"method":"notifications/initialized","jsonrpc":"2.0"}

HTTP/1.1 202 Accepted
date: Fri, 16 May 2025 06:20:20 GMT
server: uvicorn
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
content-length: 0
```
</details>

## Secondary SSE Stream

<details>
<summary>Initialization and server-to-client messages</summary>

```
GET /mcp/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: python-httpx/0.28.1
Accept: text/event-stream
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
Cache-Control: no-store


HTTP/1.1 200 OK
date: Fri, 16 May 2025 06:20:20 GMT
server: uvicorn
cache-control: no-cache, no-transform
connection: keep-alive
content-type: text/event-stream
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
x-accel-buffering: no
Transfer-Encoding: chunked

event: message
data: {"method":"roots/list","jsonrpc":"2.0","id":0}

event: message
data: {"method":"sampling/createMessage","params":{"messages":[{"role":"user","content":{"type":"text","text":"some input"}}],"maxTokens":100},"jsonrpc":"2.0","id":1}

event: message
data: {"method":"ping","jsonrpc":"2.0","id":2}

event: message
data: {"method":"notifications/tools/list_changed","jsonrpc":"2.0"}

event: message
data: {"method":"notifications/message","params":{"level":"info","logger":"log_stream","data":"This is sent via secondary SSE stream"},"jsonrpc":"2.0"}
```
</details>

## Client-To-Server Messages

<details>
<summary>List resources</summary>

```
POST /mcp/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: python-httpx/0.28.1
Accept: application/json, text/event-stream
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
Content-Length: 50

{"method":"resources/list","jsonrpc":"2.0","id":1}

HTTP/1.1 200 OK
date: Fri, 16 May 2025 06:20:20 GMT
server: uvicorn
cache-control: no-cache, no-transform
connection: keep-alive
content-type: text/event-stream
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
x-accel-buffering: no
Transfer-Encoding: chunked

event: message
data: {"jsonrpc":"2.0","id":1,"result":{"resources":[{"uri":"time://now","name":"time://now","mimeType":"text/plain"}]}}
```
</details>

<details>
<summary>Read a resource</summary>

```
POST /mcp/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: python-httpx/0.28.1
Accept: application/json, text/event-stream
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
Content-Length: 80

{"method":"resources/read","params":{"uri":"time://now"},"jsonrpc":"2.0","id":2}

HTTP/1.1 200 OK
date: Fri, 16 May 2025 06:20:20 GMT
server: uvicorn
cache-control: no-cache, no-transform
connection: keep-alive
content-type: text/event-stream
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
x-accel-buffering: no
Transfer-Encoding: chunked

event: message
data: {"jsonrpc":"2.0","id":2,"result":{"contents":[{"uri":"time://now","mimeType":"text/plain","text":"2025-05-16T16:20:20.873217"}]}}
```
</details>

<details>
<summary>List resource templates</summary>

```
POST /mcp/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: python-httpx/0.28.1
Accept: application/json, text/event-stream
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
Content-Length: 60

{"method":"resources/templates/list","jsonrpc":"2.0","id":3}

HTTP/1.1 200 OK
date: Fri, 16 May 2025 06:20:21 GMT
server: uvicorn
cache-control: no-cache, no-transform
connection: keep-alive
content-type: text/event-stream
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
x-accel-buffering: no
Transfer-Encoding: chunked

event: message
data: {"jsonrpc":"2.0","id":3,"result":{"resourceTemplates":[{"uriTemplate":"users://{user_name}/id","name":"get_user_id","description":""}]}}
```
</details>

<details>
<summary>Read resource with parameter</summary>

```
POST /mcp/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: python-httpx/0.28.1
Accept: application/json, text/event-stream
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
Content-Length: 85

{"method":"resources/read","params":{"uri":"users://John/id"},"jsonrpc":"2.0","id":4}

HTTP/1.1 200 OK
date: Fri, 16 May 2025 06:20:21 GMT
server: uvicorn
cache-control: no-cache, no-transform
connection: keep-alive
content-type: text/event-stream
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
x-accel-buffering: no
Transfer-Encoding: chunked

event: message
data: {"jsonrpc":"2.0","id":4,"result":{"contents":[{"uri":"users://John/id","mimeType":"text/plain","text":"4a6f686e"}]}}
```
</details>

<details>
<summary>Tool calling with inline notification from the server (only work for responses in SSE, not JSON)</summary>

```
POST /mcp/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: python-httpx/0.28.1
Accept: application/json, text/event-stream
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
Content-Length: 95

{"method":"tools/call","params":{"name":"trigger_server_notifications"},"jsonrpc":"2.0","id":7}

HTTP/1.1 200 OK
date: Fri, 16 May 2025 06:20:25 GMT
server: uvicorn
cache-control: no-cache, no-transform
connection: keep-alive
content-type: text/event-stream
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
x-accel-buffering: no
Transfer-Encoding: chunked

event: message
data: {"method":"notifications/message","params":{"level":"error","logger":"log_stream","data":"This is sent via response to client request"},"jsonrpc":"2.0"}

event: message
data: {"jsonrpc":"2.0","id":7,"result":{"content":[],"isError":false}}
```
</details>

<details>
<summary>Close connection</summary>

```
DELETE /mcp/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: python-httpx/0.28.1
Accept: application/json, text/event-stream
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa


HTTP/1.1 200 OK
date: Fri, 16 May 2025 06:20:26 GMT
server: uvicorn
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
content-length: 0
```
</details>

## Client-To-Server Response Messages

<details>
<summary>List roots</summary>

```
POST /mcp/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: python-httpx/0.28.1
Accept: application/json, text/event-stream
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
Content-Length: 144

{"jsonrpc":"2.0","id":0,"result":{"roots":[{"uri":"file:///tmp/","name":"search_directory_1"},{"uri":"file://./","name":"search_directory_2"}]}}

HTTP/1.1 202 Accepted
date: Fri, 16 May 2025 06:20:22 GMT
server: uvicorn
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
content-length: 0
```
</details>

<details>
<summary>LLM Sampling</summary>

```
POST /mcp/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: python-httpx/0.28.1
Accept: application/json, text/event-stream
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
Content-Length: 167

{"jsonrpc":"2.0","id":1,"result":{"role":"assistant","content":{"type":"text","text":"You are asking about `some input`"},"model":"test-model","stopReason":"endTurn"}}

HTTP/1.1 202 Accepted
date: Fri, 16 May 2025 06:20:23 GMT
server: uvicorn
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
content-length: 0
```
</details>

<details>
<summary>Notification of changes to list of roots</summary>

```
POST /mcp/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: python-httpx/0.28.1
Accept: application/json, text/event-stream
content-type: application/json
mcp-session-id: d2bac459c4d64f89ba1904ba79ed6add
Content-Length: 61

{"method":"notifications/roots/list_changed","jsonrpc":"2.0"}

HTTP/1.1 202 Accepted
date: Fri, 16 May 2025 06:50:19 GMT
server: uvicorn
content-type: application/json
mcp-session-id: d2bac459c4d64f89ba1904ba79ed6add
content-length: 0
```
</details>

<details>
<summary>Ping response</summary>

```
POST /mcp/ HTTP/1.1
Host: 127.0.0.1:8000
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: python-httpx/0.28.1
Accept: application/json, text/event-stream
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
Content-Length: 36

{"jsonrpc":"2.0","id":2,"result":{}}

HTTP/1.1 202 Accepted
date: Fri, 16 May 2025 06:20:25 GMT
server: uvicorn
content-type: application/json
mcp-session-id: a9392932da2f4e6b966d3e22cae980aa
content-length: 0
```
</details>