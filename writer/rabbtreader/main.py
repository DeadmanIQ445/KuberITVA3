from pq import RMQProducer
import sys


def make_config(host, port, queue, login, password):
    config = dict()
    config['host'] = host
    config['port'] = port
    config['queue'] = queue
    config['login'] = login
    config['password'] = password
    return config


def post_conf(host="localhost", port=32432, queue="MYQ", login="postgresadmin", password="admin123",dbname="postgresdb"):
    config = dict()
    config['host'] = host
    config['dbname'] = dbname
    config['port'] = port
    config['queue'] = queue
    config['user'] = login
    config['password'] = password
    return config



consumer_config = make_config(sys.argv[1],sys.argv[2], "MYQ", sys.argv[3], sys.argv[4])
post_conf = post_conf(host=sys.argv[5], port=sys.argv[6])
consumer = RMQProducer(consumer_config, post_conf)
consumer.publish("CHange da world")
consumer.publish("My final message")
consumer.publish("goodb ye")
