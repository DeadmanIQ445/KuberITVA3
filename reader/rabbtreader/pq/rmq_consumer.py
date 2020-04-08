import psycopg2

from .base_consumer import BaseConsumer
import pika
import time
import threading


class RMQConsumer(BaseConsumer):

    def heartbeat(self):
        while True:
            time.sleep(40)
            self.connection.process_data_events()

    def __init__(self, config, post):
        self.host = config['host']
        self.queue = config['queue']
        self.login = config['login']
        self.port = config['port']
        self.password = config['password']
        # init rmq channel
        credentials = pika.PlainCredentials(self.login, self.password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.callback, queue=self.queue)
        threading.Thread(target=self.heartbeat).start()
        self.post = post


    def callback(self, ch, method, properties, body):
        conn = psycopg2.connect(dbname=self.post['dbname'], user=self.post['user'],
                                password=self.post['password'], host=self.post['host'], port=self.post['port'])
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS reader (message VARCHAR );")
        cursor.execute(f"INSERT INTO reader VALUES ('{body.decode('UTF-8')}');")
        conn.commit()
        cursor.close()
        conn.close()
        print(" [x] Received %r" % body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.start_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()
        self.connection.close()
