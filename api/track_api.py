import datetime
import flask
import prometheus_client
import api
import que
import schema

app = api.initialize(__name__)

push, _ = que.initialize(__name__, '127.0.0.1', 6379)

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
    push('track', schema.validate(schema.queue_track_1, {
        'time': str(datetime.datetime.now(datetime.timezone.utc)),
        'provider': 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', # todo: use identity
        'state': flask.request.json['state'],
        'latitude': flask.request.json['latitude'], 
        'longitude': flask.request.json['longitude']
    }))
    return 'OK'

if __name__=='__main__':
    prometheus_client.start_http_server(port=4000)
    app.run(port=4001)
