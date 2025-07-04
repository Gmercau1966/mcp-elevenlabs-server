    from fastapi import FastAPI, Request
    from sse_starlette.sse import EventSourceResponse
    import json
    import os

    app = FastAPI()
    TRANSCRIPCIONES_DIR = "clases"

    @app.get("/stream")
    async def mcp_stream(request: Request):
        async def event_generator():
            for filename in os.listdir(TRANSCRIPCIONES_DIR):
                if filename.endswith(".txt"):
                    filepath = os.path.join(TRANSCRIPCIONES_DIR, filename)
                    with open(filepath, "r", encoding="utf-8") as file:
                        contenido = file.read()

                    contenido = contenido[:3000]  # Límite opcional

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
