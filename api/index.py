from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
from openai import OpenAI

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_resposta(mensagem: str) -> str:
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um chatbot educado, inteligente e amigável."},
            {"role": "user", "content": mensagem}
        ]
    )
    return resposta.choices[0].message.content

@app.get("/", response_class=HTMLResponse)
def chatbot(message: str = ""):
    resposta = ""

    if message:
        try:
            resposta = gerar_resposta(message)
        except Exception as e:
            resposta = "Erro ao gerar resposta da IA 😕"

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
                width: 400px;
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
            input[type=text] {{
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
                Olá! 👋 Eu sou uma IA generativa. Pergunte qualquer coisa.
            </div>

            {f'<div class="user">{message}</div>' if message else ''}
            {f'<div class="bot">{resposta}</div>' if resposta else ''}

            <form method="get">
                <input type="text" name="message" placeholder="Digite sua mensagem..." autofocus />
                <button type="submit">Enviar</button>
            </form>
        </div>
    </body>
    </html>
    """
