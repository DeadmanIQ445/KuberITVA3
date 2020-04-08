from .base_producer import BaseProducer
import pika
import logging

log = logging.getLogger(__name__)


class RMQProducer(BaseProducer):
    def __init__(self, config):
        log.info("Start initialization")
        log.debug("Init config %s", config)
        self.host = config['host']
        self.queue = config['queue']
        self.login = config['login']
        self.password = config['password']
        log.info("Finish initialization")

    def publish(self, message):
        log.info("Start publish")
        credentials = pika.PlainCredentials(self.login, self.password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, credentials=credentials))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue, durable=True)
        channel.basic_publish(exchange='',
                              routing_key=self.queue,
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,
                              ))
        connection.close()
        log.info("Finish publish")
