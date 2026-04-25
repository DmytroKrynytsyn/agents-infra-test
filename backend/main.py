import logging
from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator

class FilterHealthMetrics(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        return "/health" not in msg and "/metrics" not in msg

logging.getLogger("uvicorn.access").addFilter(FilterHealthMetrics())

app = FastAPI()
Instrumentator().instrument(app).expose(app)


@app.get("/health")
def health():
    return {"healthy": True}


@app.post("/echo")
async def echo(request: Request):
    body = await request.json()
    return {
        "echoed": body,
        "from": "agents-infra-test-backend, 2"
    }