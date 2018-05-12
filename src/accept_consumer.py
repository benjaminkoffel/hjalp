import os
import prometheus_client
import que
import schema

_, pop = que.initialize(__name__, os.environ['REDIS_HOST'], os.environ['REDIS_PORT'])

execute = db.initialize(__name__, os.environ['POSTGRES_HOST'], os.environ['POSTGRES_PORT'])

def received(value):
    execute('IF EXISTS (SELECT 1 FROM dispatch WHERE dispatch = %s AND state = 0)' +
        ' INSERT INTO accept (time, dispatch, provider) VALUES (%s, %s, %s)' +
        ' UPDATE dispatch SET state = 1 WHERE dispatch = %s'
        ' END IF', 
        (data['dispatch'], data['time'], data['dispatch'], data['provider'], data['dispatch']))

if __name__=='__main__':
    prometheus_client.start_http_server(port=4040)
    pop('queue_accept_1', lambda data: received(schema.validate(schema.queue_accept_1, data)))
