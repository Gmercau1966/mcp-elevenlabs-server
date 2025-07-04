from fastapi import FastAPI
import json
import os

app = FastAPI()

# Carpeta local donde están guardadas las transcripciones
TRANSCRIPCIONES_DIR = "./clases"

# Ruta raíz
@app.get("/")
async def root():
    return {"message": "Servidor MCP funcionando. Usa /clases para obtener el contenido."}

# Nueva ruta compatible con ElevenLabs (responde en formato JSON plano)
@app.get("/clases")
async def get_clases():
    if not os.path.exists(TRANSCRIPCIONES_DIR):
        return {"error": "No se encontró la carpeta de clases"}

    archivos_txt = [
        f for f in os.listdir(TRANSCRIPCIONES_DIR)
        if f.endswith(".txt")
    ]

    if not archivos_txt:
        return {"error": "No hay archivos .txt disponibles"}

    textos = []
    for filename in archivos_txt:
        filepath = os.path.join(TRANSCRIPCIONES_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            contenido = file.read()
        contenido = contenido[:3000]  # Cortamos para no exceder límite
        textos.append(contenido)

    return {"clases": textos}

# Definición del endpoint de herramientas para que ElevenLabs lo escanee
@app.get("/tools")
async def tools():
    return [
        {
            "name": "clases_transcriptas",
            "description": "Stream de clases transcritas de IA en formato texto",
            "endpoint": "/clases",
            "input_type": "none",
            "output_type": "text"
        }
    ]

# Permite correr localmente si hace falta
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
