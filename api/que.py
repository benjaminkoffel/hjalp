import time
import prometheus_client
import redis

def initialize(name, server, port):
    redis_conn = redis.Redis(server, port)
    queue_latency = prometheus_client.Histogram('queue_latency', 'queue latency', ['app', 'queue'])
    queue_counter = prometheus_client.Counter('queue_counter', 'queue counter', ['app', 'queue'])
    dequeue_latency = prometheus_client.Histogram('dequeue_latency', 'queue latency', ['app', 'queue'])
    dequeue_counter = prometheus_client.Counter('dequeue_counter', 'queue counter', ['app', 'queue'])
    def push(queue, value):
        with queue_latency.labels(app=name, queue=queue).time():
            redis_conn.rpush(queue, value)
        queue_counter.labels(app=name, queue=queue).inc()
    def pop(queue, function):
        while True:
            try:
                with dequeue_latency.labels(app=name, queue=queue).time():
                    value = redis_conn.blpop(queue)
                try:
                    function(value)
                except Exception as e:
                    print('ERROR:', e)
                    redis_conn.rpush(queue, value)
                    time.sleep(1)
                dequeue_counter.labels(app=name, queue=queue).inc()
            except Exception as e:
                print('ERROR:', e)
    return push, pop
