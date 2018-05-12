import os
import flask
import prometheus_client
import api
import que

app = api.initialize(__name__)

push, _ = que.initialize(__name__, os.environ['REDIS_HOST'], os.environ['REDIS_PORT'])

# todo: authenticate consumer
@app.route('/accept', methods=['POST'])
@api.validate({
    'type': 'object',
    'properties': {
        'dispatch': { 'type': 'string' },
    },
    'required': ['dispatch']
})
def accept():
    push('queue_accept_1', {
        'time': str(datetime.datetime.now(datetime.timezone.utc)),
        'provider': 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', # todo: use identity
        'dispatch': flask.request.json['dispatch']
    })
    return 'OK'

if __name__=='__main__':
    prometheus_client.start_http_server(port=4050)
    app.run(host='0.0.0.0', port=4051)
