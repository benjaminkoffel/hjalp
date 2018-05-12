import json
import time
import prometheus_client
import kafka

def producer(name, instance, host, port):
    producer_latency = prometheus_client.Histogram('producer_latency', 'producer latency', ['app', 'instance', 'topic'])
    producer_counter = prometheus_client.Counter('producer_counter', 'producer counter', ['app', 'instance', 'topic'])
    for _ in range(100):
        try:
            producer = kafka.KafkaProducer(
                bootstrap_servers='{}:{}'.format(host, port))
            break
        except Exception as e:
            print('ERROR', e)
            time.sleep(1)
    def produce(topic, key, data):
        with producer_latency.labels(app=name, instance=instance, topic=topic).time():
            producer.send(topic, key=key.encode('utf-8'), value=json.dumps(data).encode('utf-8'))
        producer_counter.labels(app=name, instance=instance, topic=topic).inc()
    return produce

def consumer(name, instance, host, port):
    consumer_latency = prometheus_client.Histogram('consumer_latency', 'consumer latency', ['app', 'instance', 'topic'])
    consumer_counter = prometheus_client.Counter('consumer_counter', 'consumer counter', ['app', 'instance', 'topic'])
    for _ in range(100):
        try:
            consumer = kafka.KafkaConsumer(
                bootstrap_servers='{}:{}'.format(host, port),
                group_id=name,
                auto_offset_reset='earliest',
                enable_auto_commit=False)
            break
        except Exception as e:
            print('ERROR', e)
            time.sleep(1)
    def consume(topic, function):
        consumer.subscribe([topic])
        for message in consumer:
            consumer_counter.labels(app=name, instance=instance, topic=topic).inc()
            with consumer_latency.labels(app=name, instance=instance, topic=topic).time():
                function(json.loads(message.value.decode('utf-8')))
            consumer.commit()
    return consume
