from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/health")
def health():
    return {"healthy": True}

@app.post("/echo")
async def echo(request: Request):
    body = await request.json()
    return {
        "echoed": body,
        "from": "agents-infra-test-backend"
    }