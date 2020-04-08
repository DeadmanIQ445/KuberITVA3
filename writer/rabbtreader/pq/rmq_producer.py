from .base_producer import BaseProducer
import pika
import psycopg2


class RMQProducer(BaseProducer):
    def __init__(self, config, post):
        self.host = config['host']
        self.queue = config['queue']
        self.login = config['login']
        self.password = config['password']
        self.post = post

    def publish(self, message):
        credentials = pika.PlainCredentials(self.login, self.password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, credentials=credentials))
        conn = psycopg2.connect(dbname=self.post['dbname'], user=self.post['user'],
                                password=self.post['password'], host=self.post['host'], port=self.post['port'])
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS writer (message VARCHAR );")
        cursor.execute(f"INSERT INTO writer VALUES ('{message}');")
        conn.commit()
        cursor.close()
        conn.close()
        print('SHould\'ve created a table')
        channel = connection.channel()
        channel.queue_declare(queue=self.queue, durable=True)
        channel.basic_publish(exchange='',
                              routing_key=self.queue,
                              body=message,
                              properties=pika.BasicProperties(
                                  delivery_mode=2,
                              ))
        connection.close()
