import json
import os

import pika
from django.conf import settings

BROKER_URL = settings.BROKER_URL


from apps.notifications.consumer_methods import NotificationConsumer
from apps.notifications.routing_keys import ROUTING_KEYS


class BaseConsumer(object):
    exchange = "test_exchange"
    exchange_type = "direct"
    queue = "test_queue"
    consumer_name = None


    def __init__(self):
        self.BROKER_URL = BROKER_URL

    
    def init_consumer(self):
        self.__make_connection()
        self.__queue_declare()
        self.__exchange_declare()
        self.__bind_queue()


    def base_consume(self):
        self.channel.basic_consume(self.queue, self.__callback, auto_ack=True)
        self.channel.start_consuming()

    
    def __make_connection(self):
        params = pika.URLParameters(BROKER_URL)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def __queue_declare(self):
        self.channel.queue_declare(queue=self.queue)


    def __exchange_declare(self):
        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type=self.exchange_type
        )
    
    def __callback(self, ch, method, properties, body):
        for consumer_method in ROUTING_KEYS[self.consumer_name][method.routing_key]:
            NotificationConsumer.body = body
            getattr(NotificationConsumer, consumer_method)()


    def __bind_queue(self):
        for key in ROUTING_KEYS:
            self.channel.queue_bind(
                queue=self.queue,
                exchange=self.exchange,
                routing_key=key
            )