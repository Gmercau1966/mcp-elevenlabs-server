from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from sse_starlette.sse import EventSourceResponse
import os
import asyncio

app = FastAPI()

@app.get("/tools")
async def tools():
    return [{
        "name": "clases_transcriptas",
        "description": "Stream de clases transcritas de IA en formato texto",
        "endpoint": "/stream",
        "input_type": "none",
        "output_type": "text"
    }]

@app.get("/stream")
async def stream():
    async def event_generator():
        while True:
            files = [f for f in os.listdir("clases") if f.endswith(".txt")]
            if files:
                for fname in sorted(files):
                    with open(os.path.join("clases", fname), "r", encoding="utf-8") as f:
                        text = f.read()
                    yield {"event": "message", "data": text}
                    await asyncio.sleep(10)
            else:
                yield {"event": "message", "data": "Sin clases disponibles aún."}
                await asyncio.sleep(10)
    return EventSourceResponse(event_generator())

@app.get("/")
async def root():
    return PlainTextResponse("Servidor MCP activo.")
