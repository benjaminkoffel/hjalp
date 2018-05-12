import os
import prometheus_client
import schema
import stream

consume = stream.consumer(__name__, os.environ['KAFKA_HOST'], os.environ['KAFKA_PORT'])

execute = db.initialize(__name__, os.environ['POSTGRES_HOST'], os.environ['POSTGRES_PORT'])

def init():
    execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    execute('CREATE TABLE IF NOT EXISTS dispatch (time TIMESTAMP, dispatch UUID, consumer UUID, latitude SMALLINT, longitude SMALLINT, state SMALLINT);')

def received(value):
    execute('IF NOT EXISTS (SELECT 1 FROM dispatch WHERE consumer = %s AND state = 0)' +
        ' INSERT INTO dispatch (time, dispatch, consumer, latitude, longitude, state) VALUES (%s, uuid_generate_v4(), %s, %s, %s, 0)' +
        ' END IF', 
        (data['consumer'], data['time'], data['consumer'], data['latitude'], data['longitude']))

if __name__=='__main__':
    prometheus_client.start_http_server(port=4040)
    init()
    consume('queue_dispatch_1', lambda data: received(schema.validate(schema.queue_dispatch_1, data)))
