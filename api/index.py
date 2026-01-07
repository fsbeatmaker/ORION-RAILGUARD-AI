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
    <html>
    <body>
        <h2>Chatbot IA</h2>

        <form method="get">
            <input name="message" placeholder="Digite sua mensagem..." autofocus />
            <button type="submit">Enviar</button>
        </form>

        <p><b>{resposta}</b></p>
    </body>
    </html>
    """
