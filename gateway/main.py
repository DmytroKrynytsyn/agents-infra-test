import os
import logging
import httpx
from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

class FilterHealthMetrics(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        return "/health" not in msg and "/metrics" not in msg

logging.getLogger("uvicorn.access").addFilter(FilterHealthMetrics())

app = FastAPI()

Instrumentator(
    should_ignore_handler_paths=["/health", "/metrics"]
).instrument(app).expose(app)

BACKEND_URL = os.getenv("BACKEND_URL", "http://agents-infra-test-backend.agents-infra-test.svc.cluster.local")

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"healthy": True}

@app.post("/call-backend")
async def call_backend(payload: dict):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{BACKEND_URL}/echo", json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=str(e))