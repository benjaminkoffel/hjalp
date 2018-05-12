import os
import flask
import prometheus_client
import api
import stream

app = api.initialize(__name__)

produce = stream.producer(__name__, os.environ['KAFKA_HOST'], os.environ['KAFKA_PORT'])

# todo: authenticate consumer
@app.route('/dispatch', methods=['POST'])
@api.validate({
    'type': 'object',
    'properties': {
        'latitude': { 'type': 'number' },
        'longitude': { 'type': 'number' },
    },
    'required': ['latitude', 'longitude']
})
def dispatch():
    consumer = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11' # todo: use identity
    produce('queue_dispatch_1', consumer, {
        'time': str(datetime.datetime.now(datetime.timezone.utc)),
        'consumer': consumer,
        'latitude': flask.request.json['latitude'], 
        'longitude': flask.request.json['longitude']
    })
    return 'OK'

if __name__=='__main__':
    prometheus_client.start_http_server(port=4030)
    app.run(host='0.0.0.0', port=4031)
