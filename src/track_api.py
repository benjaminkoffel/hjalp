import json
import flask
import prometheus_client
import redis
import api

app = api.initialize(__name__)

queue_latency = prometheus_client.Histogram('queue_latency', 'queue latency', ['endpoint', 'method', 'path', 'queue'])

redis_conn = redis.Redis('127.0.0.1', 6379)

track_queue = 'track'

# todo: authenticate provider
@app.route('/track', methods=['POST'])
@api.validate({
    'type': 'object',
    'properties': {
        'state': { 'type': 'string', 'pattern': 'online|offline' },
        'latitude': { 'type': 'number' },
        'longitude': { 'type': 'number' },
    },
    'required': ['state', 'latitude', 'longitude']
})
def track():
    with queue_latency.labels(endpoint=app.name, method=flask.request.method, path=flask.request.path, queue=track_queue).time():
        redis_conn.rpush(track_queue, json.dumps(flask.request.json))
    return 'OK'

if __name__=='__main__':
    prometheus_client.start_http_server(port=5001)
    app.run(port=5000)
