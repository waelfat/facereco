from fastapi import Request
import json
from typing import Any

def extract_properties(data: Any) -> dict[str, Any]:
    if isinstance(data, dict):
        return {k: extract_properties(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [extract_properties(v) for v in data]
    else:
        return str(data)

    # properties = {
    #     "method": request.method,
    #     "url": str(request.url),
    #     "headers": dict(request.headers),
    #     "cookies": request.cookies,
    #     "query_params": request.query_params,
    #     "path_params": request.path_params,
    #     "client": {
    #         "host": request.client.host,
    #         "port": request.client.port,
    #         "ip": request.client.ip,
    #     },
    #     "body": {
    #         "content": request.body(),
    #         "encoding": request.headers.get("content-encoding", "utf-8"),
    #         "media_type": request.headers.get("content-type", "application/octet-stream")
    #     },
    # }
    # return properties

async def mw_log_request(request: Request,call_next):
    try:
        body = await request.json()
        properties = extract_properties(body)
    except json.JSONDecodeError:
        properties = "Binary or file"

    log_entry={
        "url": request.url.path,
        "method": request.method,
        "headers": dict(request.headers),
        "properties": properties
    }
    with open("log.txt", "a") as f:
        f.write(json.dumps(log_entry, indent=4) + "\n")
    response = await call_next(request)
    return response