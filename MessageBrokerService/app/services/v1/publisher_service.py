import pika
import json
import time
from app.core.config import settings

class PublisherService:
    def __init__(self):
        self.connection = None
        self.channel = None

    def _connect(self, retries=5, delay=3):
        if self.connection and not self.connection.is_closed:
            return

        for attempt in range(retries):
            try:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=settings.BROKER_HOST)
                )
                self.channel = self.connection.channel()
                self.channel.exchange_declare(
                    exchange=settings.BROKER_EXCHANGE,
                    exchange_type='fanout',
                    durable=True
                )
                break  # ✅ Connection successful
            except pika.exceptions.AMQPConnectionError as e:
                print(f"[RabbitMQ] Connection failed: {e}. Retrying in {delay} sec...")
                time.sleep(delay)
        else:
            raise Exception("[RabbitMQ] Could not connect after several retries.")

    def publish(self, message: dict):
        self._connect()
        self.channel.basic_publish(
            exchange=settings.BROKER_EXCHANGE,
            routing_key='',
            body=json.dumps(message).encode('utf-8'),
            properties=pika.BasicProperties(delivery_mode=2)
        )
