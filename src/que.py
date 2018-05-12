import json
import time
import prometheus_client
import redis

def initialize(name, host, port):
    queue_latency = prometheus_client.Histogram('queue_latency', 'queue latency', ['app', 'queue'])
    queue_counter = prometheus_client.Counter('queue_counter', 'queue counter', ['app', 'queue'])
    dequeue_latency = prometheus_client.Histogram('dequeue_latency', 'queue latency', ['app', 'queue'])
    dequeue_counter = prometheus_client.Counter('dequeue_counter', 'queue counter', ['app', 'queue'])
    for _ in range(10):
        try:
            redis_conn = redis.Redis(host, port, decode_responses=True)
            break
        except Exception as e:
            print('ERROR', e)
            time.sleep(1)
    def push(queue, data):
        value = json.dumps(data)
        with queue_latency.labels(app=name, queue=queue).time():
            redis_conn.rpush(queue, value)
        queue_counter.labels(app=name, queue=queue).inc()
    def pop(queue, function):
        while True:
            try:
                _, value = redis_conn.blpop(queue)
                dequeue_counter.labels(app=name, queue=queue).inc()
                try:
                    with dequeue_latency.labels(app=name, queue=queue).time():
                        function(json.loads(value))
                except Exception as e:
                    print('ERROR:', e)
                    push(queue + '.dead', value)
            except Exception as e:
                print('ERROR:', e)
    return push, pop
