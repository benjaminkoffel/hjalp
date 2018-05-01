import flask
import prometheus_client
import api
import que

app = api.initialize(__name__)

push, _ = que.initialize(__name__, '127.0.0.1', 6379)

# todo: authenticate consumer
@app.route('/dispatch', methods=['POST'])
@api.validate({
    'type': 'object',
    'properties': {
        'latitude': { 'type': 'number' },
        'longitude': { 'type': 'number' },
    },
    'required': ['state', 'latitude', 'longitude']
})
def status():
    push('dispatch', {
        'latitude': flask.request.json['latitude'], 
        'longitude': flask.request.json['longitude']
    })
    return 'OK'

if __name__=='__main__':
    prometheus_client.start_http_server(port=6000)
    app.run(port=6001)
