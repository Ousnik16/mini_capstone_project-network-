import time
from collections import defaultdict

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.config import settings


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.storage = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_host = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - settings.rate_limit_window_seconds
        calls = [ts for ts in self.storage[client_host] if ts >= window_start]
        self.storage[client_host] = calls

        if len(calls) >= settings.rate_limit_requests:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

        self.storage[client_host].append(now)
        return await call_next(request)
