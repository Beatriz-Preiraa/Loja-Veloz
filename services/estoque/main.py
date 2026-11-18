import os
import json
import time
import threading
import pika
from fastapi import FastAPI

app = FastAPI(title="Serviço de Estoque")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")

def consumir_eventos():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            channel = connection.channel()
            channel.exchange_declare(exchange="pedidos_events", exchange_type="fanout")
            result = channel.queue_declare(queue="fila_estoque", durable=True)
            channel.queue_bind(exchange="pedidos_events", queue=result.method.queue)

            def callback(ch, method, properties, body):
                dados = json.loads(body)
                print(f"[ESTOQUE] Baixa de {dados.get('quantidade')}x '{dados.get('item')}' concluída para Pedido #{dados.get('pedido_id')}", flush=True)
                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(queue="fila_estoque", on_message_callback=callback)
            channel.start_consuming()
        except Exception:
            time.sleep(3)

@app.on_event("startup")
def start_consumer():
    threading.Thread(target=consumir_eventos, daemon=True).start()

@app.get("/health")
def health():
    return {"status": "ok", "service": "estoque"}