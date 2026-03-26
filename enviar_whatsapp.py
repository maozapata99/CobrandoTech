import requests  # <--- ESTA ES LA LÍNEA QUE FALTA

ACCESS_TOKEN = "EAAXYqM6jjlsBQ7eIvRNPvcZClA8ZAa6fXEeLpxDUSyNgUOqWGHUODBUzgZB1ZAZA9ti4r5588s9WPj9MZBTTbqPqsa95qP75CugoUd6AfZBoyPUmoLwKKyH7d7L5OSqvfG7HtpmmReNZAQd4ggJdL1zsbkrZAq7dzgErfX9M5pkXZBSnpqfiqjEmQTM6dxIZCGS2DZAFqs2IZA6BGC4svknwncEFGmLDQUazWAPyPZCoYSnZBxYc28Q8LZAVa6mdeM092V6jikiMm9yyE6vMjyZC5XbLAPgZDZD" # Tu token
PHONE_ID = "1055330667657398"

url = f"https://graph.facebook.com/v22.0/{PHONE_ID}/messages"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

data = {
    "messaging_product": "whatsapp",
    "to": "573012038907",
    "type": "template",
    "template": {
        "name": "hello_world", # <--- Vuelve a usar este nombre exacto
        "language": { "code": "en_US" }
    }
}

response = requests.post(url, headers=headers, json=data)
print(response.json())