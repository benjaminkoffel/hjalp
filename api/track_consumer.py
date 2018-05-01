import json
import prometheus_client
import que
import db
import schema

_, pop = que.initialize(__name__, '127.0.0.1', 6379)

execute = db.initialize()

def received(data):
    print(data)
    execute('INSERT INTO track (time, provider, state, latitude, longitude) VALUES (%s, %s, %s, %s, %s)', 
        (data['time'], data['provider'], data['state'], data['latitude'], data['longitude']))

if __name__=='__main__':
    prometheus_client.start_http_server(port=5000)
    pop('track', lambda data: received(schema.validate(schema.queue_track_1, data)))
