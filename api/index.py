from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
import requests

app = FastAPI()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.get("/", response_class=HTMLResponse)
def chatbot(message: str = ""):
    resposta = ""

    if message:
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://vercel.com",
                "X-Title": "Chatbot IA OpenRouter",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "system", "content": "Você é um chatbot amigável, educado e inteligente."},
                    {"role": "user", "content": message}
                ]
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=20
            )

            data = response.json()
            resposta = data["choices"][0]["message"]["content"]

        except Exception as e:
            resposta = f"Erro ao gerar resposta da IA: {str(e)}"

    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Orion Railguard AI</title>
        <style>
            body {{
                font-family: Arial;
                background: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .chat {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                width: 420px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            input {{
                width: 100%;
                padding: 10px;
                margin-top: 10px;
            }}
            button {{
                width: 100%;
                padding: 10px;
                margin-top: 10px;
                background: #0070f3;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            .msg-user {{
                background: #d1e7dd;
                padding: 8px;
                border-radius: 5px;
                margin-top: 10px;
            }}
            .msg-bot {{
                background: #e0e0e0;
                padding: 8px;
                border-radius: 5px;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="chat">
            <div class="msg-bot">
                Olá! 👋 Sou o Orion, atendente IA da Presoft. Como posso ajudar?
            </div>

            {f'<div class="msg-user">{message}</div>' if message else ''}
            {f'<div class="msg-bot">{resposta}</div>' if resposta else ''}

            <form method="get">
                <input name="message" placeholder="Digite sua mensagem..." autofocus />
                <button type="submit">Enviar</button>
            </form>
        </div>
    </body>
    </html>
    """
