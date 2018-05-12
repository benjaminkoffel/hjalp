import datetime
import os
import flask
import prometheus_client
import api
import schema
import stream

app = api.initialize(__name__)

produce = stream.producer(__name__, os.environ['KAFKA_HOST'], os.environ['KAFKA_PORT'])

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
    provider = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11' # todo: use identity
    produce('queue_track_1', provider, schema.validate(schema.queue_track_1, {
        'time': str(datetime.datetime.now(datetime.timezone.utc)),
        'provider': provider,
        'state': flask.request.json['state'],
        'latitude': flask.request.json['latitude'], 
        'longitude': flask.request.json['longitude']
    }))
    return 'OK'

if __name__=='__main__':
    prometheus_client.start_http_server(port=4010)
    app.run(host='0.0.0.0', port=4011)
