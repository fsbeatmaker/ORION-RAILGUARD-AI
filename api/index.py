from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from openai import OpenAI

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def chatbot(message: str = ""):
    resposta = ""

    if message:
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client.responses.create(
                model="gpt-4o-mini",
                input=message
            )

            resposta = response.output_text

        except Exception as e:
            resposta = f"Erro ao gerar resposta da IA: {str(e)}"

    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Chatbot IA</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
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
            .bot {{
                background: #e0e0e0;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
            }}
            .user {{
                background: #d1e7dd;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
                text-align: right;
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
        </style>
    </head>
    <body>
        <div class="chat">
            <div class="bot">
                Olá! 👋 Eu sou uma IA generativa estilo ChatGPT.
            </div>

            {f'<div class="user">{message}</div>' if message else ''}
            {f'<div class="bot">{resposta}</div>' if resposta else ''}

            <form method="get">
                <input name="message" placeholder="Digite sua mensagem..." autofocus />
                <button type="submit">Enviar</button>
            </form>
        </div>
    </body>
    </html>
    """
