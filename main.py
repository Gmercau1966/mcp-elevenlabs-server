from flask import Flask, Response, jsonify
import time

app = Flask(__name__)

# Endpoint que expone los tools para ElevenLabs
@app.route('/tools', methods=['GET'])
def get_tools():
    tools = [
        {
            "name": "clases_transcriptas",
            "description": "Stream de clases transcriptas de IA en formato texto",
            "endpoint": "/stream",
            "input_type": "none",
            "output_type": "text",
            "type": "text"  # ← Este campo es clave para que ElevenLabs lo lea correctamente
        }
    ]
    return jsonify({"tools": tools})

# Endpoint de tipo stream para ElevenLabs
@app.route('/stream', methods=['GET'])
def stream_text():
    def generate():
        yield 'event: add_context\n'
        yield 'data: {"name": "clase_2", "type": "text", "value": "(250) 💥 CURSO DE IA GRATIS - Día 2: Crea GPTs Personalizados como un PRO..."}\n\n'
        time.sleep(1)
        yield 'event: add_context\n'
        yield 'data: {"name": "clase_3", "type": "text", "value": "(250) 💥 CURSO DE IA GRATIS - Día 3: Automatiza con Make y Descubre la 3° jornada..."}\n\n'
    return Response(generate(), mimetype='text/event-stream')

# Root para ver que el server está vivo
@app.route('/')
def home():
    return 'MCP Server for ElevenLabs running'

if __name__ == '__main__':
    app.run(debug=True, port=10000)
