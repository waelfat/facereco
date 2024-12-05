from fastapi import Request
import json
from typing import Any
import os

LOG_FILE_PATH = "request_logs.json"

def extract_properties(data: Any) -> Any:
    if isinstance(data, dict):
        return {key: extract_properties(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [extract_properties(item) for item in data]
    else:
        return str(type(data).__name__)

async def mw_log_request(request: Request, call_next):
    
    properties = {}

    if request.method in ("POST", "PUT", "PATCH"):
        try:
            content_type = request.headers.get("content-type")
            if content_type and "application/json" in content_type:
                body = await request.json()
                properties = extract_properties(body)
            elif content_type and "multipart/form-data" in content_type:
                form = await request.form()
                for key, value in form.items():
                    if hasattr(value, "filename"):
                        properties[key] = "file"
                    else:
                        properties[key] = str(type(value).__name__)
            else:
                properties = "Unsupported Content Type"
        except Exception as e:
            properties = f"Error extracting properties: {e}"

    log_entry = {
        "url": str(request.url),
        "method": request.method,
        "properties": properties
    }
    
    # Write the log entry to a file
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")

    response = await call_next(request)
    return response
