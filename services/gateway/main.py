import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Pedidos Veloz - API Gateway")
PEDIDOS_URL = os.getenv("PEDIDOS_URL", "http://pedidos:8001")

class PedidoInput(BaseModel):
    cliente: str
    item: str
    quantidade: int
    valor: float

@app.get("/health")
def health():
    return {"status": "ok", "service": "gateway"}

@app.post("/api/pedidos")
async def criar_pedido(pedido: PedidoInput):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{PEDIDOS_URL}/pedidos", json=pedido.model_dump(), timeout=5.0)
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Erro ao comunicar com Pedidos: {str(e)}")

@app.get("/api/pedidos")
async def listar_pedidos():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{PEDIDOS_URL}/pedidos", timeout=5.0)
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Erro ao consultar Pedidos: {str(e)}")