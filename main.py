# main.py
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
import json
import os

app = FastAPI()
TRANSCRIPCIONES_DIR = "./clases"

@app.get("/", tags=["health"])
async def root():
    return {"message": "Servidor MCP funcionando. Usa /stream y /tools."}

@app.get("/stream", summary="SSE stream de contexto")
async def mcp_stream(request: Request):
    async def event_generator():
        if not os.path.exists(TRANSCRIPCIONES_DIR):
            yield {"event": "error", "data": json.dumps({"error": "No se encontró carpeta clases"})}
            return

        archivos = [f for f in os.listdir(TRANSCRIPCIONES_DIR) if f.endswith(".txt")]
        if not archivos:
            yield {"event": "error", "data": json.dumps({"error": "No hay archivos .txt"})}
            return

        for nombre in archivos:
            with open(os.path.join(TRANSCRIPCIONES_DIR, nombre), encoding="utf-8") as f:
                contenido = f.read()[:3000]
            yield {
                "event": "add_context",
                "data": json.dumps({
                    "name": nombre.replace(".txt", ""),
                    "type": "text",
                    "value": contenido
                })
            }
        yield {"event": "done", "data": ""}

    return EventSourceResponse(event_generator())

@app.get("/tools", summary="Lista de herramientas MCP")
async def tools():
    return {
        "tools": [
            {
                "name": "clases_transcriptas",
                "description": "Stream de clases transcritas de IA en formato texto",
                "endpoint": "/stream",
                "input_type": "none",
                "output_type": "text"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
