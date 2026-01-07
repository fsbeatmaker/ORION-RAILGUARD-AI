from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def test_env():
    key = os.getenv("OPENAI_API_KEY")
    return f"""
    <h2>Teste ENV</h2>
    <p>API KEY carregada? {'SIM' if key else 'NÃO'}</p>
    """
