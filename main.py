from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
import json
import os

app = FastAPI()
TRANSCRIPCIONES_DIR = "./clases"

@app.get("/")
async def root():
    return {"message": "Servidor MCP funcionando. Usa /stream para obtener las clases."}

@app.get("/stream")
async def mcp_stream(request: Request):
    async def event_generator():
        if not os.path.exists(TRANSCRIPCIONES_DIR):
            yield {
                "event": "error",
                "data": json.dumps({"error": "No se encontró la carpeta de clases"})
            }
            return

        archivos_txt = [f for f in os.listdir(TRANSCRIPCIONES_DIR) if f.endswith(".txt")]

        if not archivos_txt:
            yield {
                "event": "error",
                "data": json.dumps({"error": "No hay archivos .txt disponibles"})
            }
            return

        for filename in archivos_txt:
            filepath = os.path.join(TRANSCRIPCIONES_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                contenido = file.read()

            contenido = contenido[:3000]  # Límite para evitar sobrecarga

            yield {
                "event": "add_context",
                "data": json.dumps({
                    "name": filename.replace(".txt", ""),
                    "type": "text",
                    "value": contenido
                })
            }

        yield {"event": "done", "data": ""}

    return EventSourceResponse(event_generator())

@app.get("/tools")
async def tools():
    tools_data = {
        "tools": [
            {
                "name": "clases_transcriptas",
                "description": "Stream de clases transcriptas de IA en formato texto",
                "endpoint": "/stream",
                "input_type": "none",
                "output_type": "text"
            }
        ]
    }
    return JSONResponse(content=tools_data)  # Asegura cabecera Content-Type: application/json

# Para desarrollo local (no se usa en Render, pero lo dejo por si lo corrés localmente)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
