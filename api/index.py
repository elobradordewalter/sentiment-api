from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import anthropic
import os

app = FastAPI(title="API de Sentimiento", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

cliente = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

class TextoEntrada(BaseModel):
    texto: str

@app.get("/")
def raiz():
    return {"estado": "funcionando", "servicio": "API de Análisis de Sentimiento"}

@app.post("/sentimiento")
def analizar_sentimiento(entrada: TextoEntrada):
    mensaje = cliente.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=10,
        messages=[
            {
                "role": "user",
                "content": f"Analizá el sentimiento de este texto. Respondé SOLO con una palabra: POSITIVO, NEGATIVO o NEUTRO.\n\nTexto: {entrada.texto}"
            }
        ]
    )
    resultado = mensaje.content[0].text.strip().upper()
    if resultado not in ["POSITIVO", "NEGATIVO", "NEUTRO"]:
        resultado = "NEUTRO"
    return {
        "sentimiento": resultado,
        "texto": entrada.texto
    }
