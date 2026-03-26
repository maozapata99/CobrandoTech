import telebot
import google.generativeai as genai
import sqlite3
import warnings

warnings.filterwarnings("ignore")

# ⚠️ RECUERDA: Usa tu nueva API Key de Google Cloud (la de los créditos)
TELEGRAM_TOKEN = "8720152086:AAER4SsO9tqoQN5WBrMXQ9__3lylpCOWS8U"
GOOGLE_API_KEY = "AIzaSyDOLO7B2ygp5b_MetJzHRLo5X9OuDaT1LE"

genai.configure(api_key=GOOGLE_API_KEY)

# 🧠 PROMPT DEL SISTEMA: Personalidad de Luciana
PROMPT_SISTEMA = """Tu nombre es Luciana, asistente senior de Mao Tech en Medellín.
Eres cordial, profesional y empática. Tu objetivo es ayudar con la gestión de cobro.

REGLAS DE ORO:
1. SÍ PUEDES RECIBIR FOTOS: Dile que las envíe con confianza para validar pagos.
2. AGENTE HUMANO: Si lo piden, responde EXACTAMENTE: ESCALAR_HUMANO.
3. ERRORES: Si los datos no coinciden, sé amable y explica que no los encontraste.
4. ACUERDOS: Si el cliente no tiene todo el dinero, ofrece 2 o 3 cuotas.
"""

bot = telebot.TeleBot(TELEGRAM_TOKEN)
model = genai.GenerativeModel('gemini-flash-latest', system_instruction=PROMPT_SISTEMA)

user_state = {}

def consultar_factura(cedula):
    try:
        conn = sqlite3.connect('cobranzas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM facturas WHERE cedula=?", (cedula,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado
    except Exception as e:
        print(f"Error DB: {e}")
        return None

# 📸 MANEJADOR DE FOTOS (Comprobantes)
@bot.message_handler(content_types=['photo'])
def manejar_fotos(message):
    chat_id = message.chat.id
    if user_state.get(chat_id, {}).get('step') == 'chat_activo':
        bot.reply_to(message, "¡Excelente! Recibí la imagen de su comprobante. Un momento mientras registro el abono en el sistema...")
    else:
        bot.reply_to(message, "Por favor, primero identifíquese con su cédula para poder asociar este pago.")

# 💬 MANEJADOR DE TEXTO (Lógica principal)
@bot.message_handler(content_types=['text'])
def manejar_mensajes(message):
    chat_id = message.chat.id
    texto = message.text.strip()

    # PASO 1: Saludo inicial
    if (chat_id not in user_state) or ("hola" in texto.lower() and user_state.get(chat_id, {}).get('step') not in ['chat_activo', 'datos_agente']):
        user_state[chat_id] = {'step': 'esperando_cedula'}
        bot.reply_to(message, "¡Cordial saludo! Soy Luciana de Mao Tech. Para ayudarle con su factura, por favor indíqueme su número de cédula.")
        return

    # PASO 2: Recibir Cédula
    if user_state[chat_id].get('step') == 'esperando_cedula':
        user_state[chat_id]['cedula'] = texto
        user_state[chat_id]['step'] = 'esperando_expedicion'
        bot.reply_to(message, "Gracias. Ahora envíeme la fecha de expedición de su documento (AAAA-MM-DD).")
        return

# Paso 3: Validación e inicio de Chat (Versión Simplificada)
    if user_state[chat_id].get('step') == 'esperando_expedicion':
        cedula = user_state[chat_id]['cedula']
        datos = consultar_factura(cedula)
        
        if datos and str(datos[2]).strip() == texto:
            chat_session = model.start_chat()
            user_state[chat_id]['step'] = 'chat_activo'
            user_state[chat_id]['chat_session'] = chat_session
            
            # Generamos el link
            link_pago = f"https://pagos.maotech.com/pagar?cedula={cedula}&factura={datos[3]}"
            
            # 🧠 Solo le pasamos los datos crudos y el link
            prompt_init = (
                f"El usuario es {datos[1]}. Su deuda es de {datos[4]} (Factura: {datos[3]}). "
                f"IMPORTANTE: Muestra este link de pago ahora: {link_pago}. "
                "Sé muy amable, dile que puede pagar ahí o enviarte fotos del recibo."
            )
            
            response = chat_session.send_message(prompt_init)
            bot.reply_to(message, response.text)
        else:
            # Tu lógica de error que ya arreglamos...
            pass
        
        
    # PASO DE AGENTE HUMANO (PROTECCIÓN CONTRA BUCLES)
    if user_state[chat_id].get('step') == 'datos_agente':
        user_state[chat_id]['step'] = 'chat_activo'
        chat_session = user_state[chat_id].get('chat_session')
        try:
            # Confirmación sin repetir la palabra secreta
            response = chat_session.send_message(f"El usuario dio su teléfono: {texto}. Confírmale que un asesor le llamará y NO uses la palabra ESCALAR_HUMANO.")
            bot.reply_to(message, response.text.replace("ESCALAR_HUMANO", ""))
        except:
            bot.reply_to(message, "Perfecto, he tomado sus datos. Un asesor le contactará pronto. ¿Algo más en qué pueda ayudarle?")
        return

    # PASO 4: Chat Activo (Memoria continua)
    if user_state[chat_id].get('step') == 'chat_activo':
        if any(p in texto.lower() for p in ["gracias", "adiós", "chao"]):
            bot.reply_to(message, "¡Con mucho gusto! Fue un placer atenderle. ¡Que tenga un excelente día!")
            user_state.pop(chat_id, None)
            return

        chat_session = user_state[chat_id].get('chat_session')
        try:
            response = chat_session.send_message(texto)
            
            if "ESCALAR_HUMANO" in response.text:
                user_state[chat_id]['step'] = 'datos_agente'
                bot.reply_to(message, "Entiendo perfectamente. Por favor, indíqueme su número de teléfono para que un asesor le contacte a la brevedad.")
            else:
                bot.reply_to(message, response.text)
        except Exception as e:
            bot.reply_to(message, "¿Cómo desea proceder con su pago?")
        return

if __name__ == '__main__':
    print("🚀 Luciana en línea con manejo de errores conversacional...")
    bot.infinity_polling()