import datetime
import os
import flask
import prometheus_client
import api
import kaf
import schema
import svc

config = {
    'prometheus_port': 4010,
    'flask_port': 4011
}

name, instance, log, discover = svc.initialize('track_api_1', config, os.environ['ZOOKEEPER_HOST'], os.environ['ZOOKEEPER_PORT'])

produce = kaf.producer(name, instance, os.environ['KAFKA_HOST'], os.environ['KAFKA_PORT'])

app = api.initialize(name)

# todo: authenticate provider
@app.route('/track', methods=['POST'])
@api.validate(schema.request_track_1)
def track():
    provider = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11' # todo: use identity
    produce('queue_track_1', provider, schema.validate(schema.queue_track_1, {
        'provider': provider,
        'time': datetime.datetime.utcnow().timestamp(),
        'state': flask.request.json['state'],
        'latitude': flask.request.json['latitude'], 
        'longitude': flask.request.json['longitude']
    }))
    return 'OK'

if __name__=='__main__':
    prometheus_client.start_http_server(port=config['prometheus_port'])
    app.run(host='0.0.0.0', port=config['flask_port'])
