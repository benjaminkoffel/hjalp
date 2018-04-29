import json
import flask
import prometheus_client
import api
import que

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
    push('track', json.dumps({
        'state': flask.request.json['state'],
        'latitude': flask.request.json['latitude'], 
        'longitude': flask.request.json['longitude']
    }))
    return 'OK'

if __name__=='__main__':
    prometheus_client.start_http_server(port=1000)
    app.run(port=1001)
