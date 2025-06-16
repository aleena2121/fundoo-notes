import json
import os
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.concurrency import run_in_threadpool
from jose import jwt
from jose.exceptions import JWTError

LOG_FILE_PATH = "logs/request_logs.json"


class RequestCountMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        username = "anonymous"
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                unverified = jwt.decode(
                    token, key="", options={"verify_signature": False}
                )
                username = unverified.get("sub", "anonymous")
            except JWTError:
                pass

        method = request.method.lower()
        await run_in_threadpool(self.update_log_file, username, method)

        response = await call_next(request)
        return response

    def update_log_file(self, username: str, method: str):
        data = {}

        if os.path.exists(LOG_FILE_PATH):
            try:
                with open(LOG_FILE_PATH, "r") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        if username not in data:
            data[username] = {}
        data[username][method] = data[username].get(method, 0) + 1

        with open(LOG_FILE_PATH, "w") as f:
            json.dump(data, f, indent=4)
