from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route('/', methods=['GET'])
def inicio():
    return "¡Hola! El servidor de mi agente de cobros está funcionando perfectamente 🚀", 200
# Este es el token que tú inventas para configurar en Meta
TOKEN_VERIFICACION = "MAO_TECH_2026" 

@app.route('/webhook', methods=['GET'])
def verificar_webhook():
    # Meta envía un "challenge" para verificar que tu servidor funciona
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == TOKEN_VERIFICACION:
        return challenge, 200
    return "Error de verificación", 403

@app.route('/webhook', methods=['POST'])
def recibir_mensajes():
    data = request.get_json()
    try:
        # Extraemos el mensaje del JSON que envía WhatsApp
        mensaje = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        numero = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
        
        print(f"Mensaje recibido de {numero}: {mensaje}")

        # AQUÍ es donde luego conectaremos tu IA (Llama 3 o Cobranza)
        # Por ahora, solo imprimimos en consola.
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)