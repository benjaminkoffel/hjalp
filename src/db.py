import time
import prometheus_client
import psycopg2

def initialize(name, host, port):
    db_latency = prometheus_client.Histogram('db_latency', 'db latency', ['app', 'query'])
    db_counter = prometheus_client.Counter('db_counter', 'db counter', ['app', 'query'])
    for _ in range(10):
        try:
            postgres = psycopg2.connect(host=host, port=port, dbname='postgres', user='postgres', password='password')
            break
        except Exception as e:
            print('ERROR', e)
            time.sleep(1)
    def execute(query, values=None):
        with db_latency.labels(app=name, query=query).time():
            cursor = postgres.cursor()
            cursor.execute(query, values)
            data = cursor.fetchall() if cursor.description else []
            postgres.commit()
            cursor.close()
        db_counter.labels(app=name, query=query).inc()
        return data
    execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
    execute('CREATE TABLE IF NOT EXISTS accept (time TIMESTAMP, dispatch UUID, provider UUID);')
    execute('CREATE TABLE IF NOT EXISTS dispatch (time TIMESTAMP, dispatch UUID, consumer UUID, latitude SMALLINT, longitude SMALLINT, state SMALLINT);')
    execute('CREATE TABLE IF NOT EXISTS track (time TIMESTAMP, provider UUID, state TEXT, latitude SMALLINT, longitude SMALLINT);')
    return execute
