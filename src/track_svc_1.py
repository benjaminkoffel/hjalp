import datetime
import os
import uuid
import prometheus_client
import cas
import kaf
import schema
import svc

config = {
    'prometheus_port': 5010
}

name, instance, log, discover = svc.initialize('track_svc_1', config, os.environ['ZOOKEEPER_HOST'], os.environ['ZOOKEEPER_PORT'])

consume = kaf.consumer(name, instance, os.environ['KAFKA_HOST'], os.environ['KAFKA_PORT'])

execute = cas.initialize(name, os.environ['CASSANDRA_HOST'], os.environ['CASSANDRA_PORT'])

def received(data):
    values = (uuid.UUID(data['provider']), datetime.datetime.fromtimestamp(data['time']), data['state'], data['latitude'], data['longitude'])
    execute('INSERT INTO track_event (provider, time, state, latitude, longitude) VALUES (?, ?, ?, ?, ?)', values)
    execute('INSERT INTO track_current (provider, time, state, latitude, longitude) VALUES (?, ?, ?, ?, ?)', values)

if __name__=='__main__':
    execute('CREATE TABLE IF NOT EXISTS track_event (provider UUID, time TIMESTAMP, state TEXT, latitude INT, longitude INT, PRIMARY KEY (time, provider));')
    execute('CREATE TABLE IF NOT EXISTS track_current (provider UUID, time TIMESTAMP, state TEXT, latitude INT, longitude INT, PRIMARY KEY (provider));')
    prometheus_client.start_http_server(port=config['prometheus_port'])
    consume('queue_track_1', lambda data: received(schema.validate(schema.queue_track_1, data)))
