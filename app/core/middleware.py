from fastapi import Request
from loguru import logger
import time

async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    client_ip = request.client.host if request.client else "unknown"

    logger.bind(
        ip=client_ip,
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        duration=f"{duration:.2f}s"
    ).info("request")

    return response
