import os
import json
import time
import psycopg2
import pika
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Serviço de Pedidos")

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "pedidos_db")
DB_USER = os.getenv("DB_USER", "veloz")
DB_PASS = os.getenv("DB_PASS", "veloz123")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

def get_db():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

@app.on_event("startup")
def startup():
    for _ in range(10):
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS pedidos (
                    id SERIAL PRIMARY KEY,
                    cliente VARCHAR(100),
                    item VARCHAR(100),
                    quantidade INT,
                    valor NUMERIC(10,2),
                    status VARCHAR(50)
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            break
        except Exception:
            time.sleep(2)

class Pedido(BaseModel):
    cliente: str
    item: str
    quantidade: int
    valor: float

def publicar_evento(evento: dict):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.exchange_declare(exchange="pedidos_events", exchange_type="fanout")
        channel.basic_publish(exchange="pedidos_events", routing_key="", body=json.dumps(evento))
        connection.close()
    except Exception as e:
        print(f"[WARN] Falha ao publicar no RabbitMQ: {e}", flush=True)

@app.get("/health")
def health():
    return {"status": "ok", "service": "pedidos"}

@app.post("/pedidos")
def criar_pedido(pedido: Pedido):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO pedidos (cliente, item, quantidade, valor, status) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
        (pedido.cliente, pedido.item, pedido.quantidade, pedido.valor, "CRIADO")
    )
    pedido_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    evento = {"evento": "PedidoCriado", "pedido_id": pedido_id, **pedido.model_dump()}
    publicar_evento(evento)
    return {"mensagem": "Pedido criado com sucesso", "pedido": evento}

@app.get("/pedidos")
def listar_pedidos():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, cliente, item, quantidade, valor, status FROM pedidos;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "cliente": r[1], "item": r[2], "quantidade": r[3], "valor": float(r[4]), "status": r[5]} for r in rows]