from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
import os
import json

app = FastAPI()
TRANSCRIPCIONES_DIR = "./clases"

@app.get("/")
async def root():
    return {"message": "Servidor MCP funcionando. Usa /stream para obtener las clases."}

@app.get("/stream")
async def stream_clases(request: Request):
    async def event_generator():
        # Verifica si existe la carpeta de transcripciones
        if not os.path.exists(TRANSCRIPCIONES_DIR):
            yield {
                "event": "error",
                "data": json.dumps({"error": "No se encontró la carpeta de clases"})
            }
            return

        # Lista los archivos .txt
        archivos = [
            f for f in os.listdir(TRANSCRIPCIONES_DIR)
            if f.endswith(".txt")
        ]

        # Si no hay archivos .txt, lanza error
        if not archivos:
            yield {
                "event": "error",
                "data": json.dumps({"error": "No hay archivos .txt disponibles"})
            }
            return

        # Streamea cada archivo como contexto
        for archivo in archivos:
            with open(os.path.join(TRANSCRIPCIONES_DIR, archivo), "r", encoding="utf-8") as f:
                contenido = f.read()

            yield {
                "event": "add_context",
                "data": json.dumps({
                    "name": archivo.replace(".txt", ""),
                    "type": "text",
                    "value": contenido[:3000]  # Trunca a 3000 caracteres si es largo
                })
            }

        # Señal de fin del stream
        yield {"event": "done", "data": ""}

    return EventSourceResponse(event_generator())

@app.get("/tools")
async def tools():
    return [
        {
            "name": "clases_transcriptas",
            "description": "Stream de clases transcritas de IA en formato texto",
            "endpoint": "/stream",
            "input_type": "none",
            "output_type": "text"
        }
    ]
