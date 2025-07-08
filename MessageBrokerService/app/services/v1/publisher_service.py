import pika
import json
from app.core.config import settings

class PublisherService:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=settings.BROKER_HOST)
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=settings.BROKER_EXCHANGE,
            exchange_type='fanout',
            durable=True
        )

    def publish(self, message: dict):
        self.channel.basic_publish(
            exchange=settings.BROKER_EXCHANGE,
            routing_key='',
            body=json.dumps(message).encode('utf-8'),  # ✅ convert to bytes
            properties=pika.BasicProperties(delivery_mode=2)
        )
