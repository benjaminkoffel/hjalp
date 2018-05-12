import os
import prometheus_client
import db
import schema
import stream

consume = stream.consumer(__name__, os.environ['KAFKA_HOST'], os.environ['KAFKA_PORT'])

execute = db.initialize(__name__, os.environ['POSTGRES_HOST'], os.environ['POSTGRES_PORT'])

def init():
    execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    execute('CREATE TABLE IF NOT EXISTS track (time TIMESTAMP, provider UUID, state TEXT, latitude SMALLINT, longitude SMALLINT);')

def received(data):
    execute('INSERT INTO track (time, provider, state, latitude, longitude) VALUES (%s, %s, %s, %s, %s)', 
        (data['time'], data['provider'], data['state'], data['latitude'], data['longitude']))

if __name__=='__main__':
    prometheus_client.start_http_server(port=4020)
    init()
    consume('queue_track_1', lambda data: received(schema.validate(schema.queue_track_1, data)))
