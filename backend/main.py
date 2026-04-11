from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator

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