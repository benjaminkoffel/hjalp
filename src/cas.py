import time
import prometheus_client
import cassandra.cluster
import cassandra.policies

def initialize(name, host, port):
    db_latency = prometheus_client.Histogram('db_latency', 'db latency', ['app', 'query'])
    db_counter = prometheus_client.Counter('db_counter', 'db counter', ['app', 'query'])
    for _ in range(100):
        try:
            session = cassandra.cluster.Cluster([host], load_balancing_policy=cassandra.policies.RoundRobinPolicy(), port=port).connect()
            break
        except Exception as e:
            print('ERROR', e)
            time.sleep(1)
    session.execute("CREATE KEYSPACE IF NOT EXISTS hjalp WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }")
    session.set_keyspace('hjalp')        
    def execute(query, values=tuple()):
        with db_latency.labels(app=name, query=query).time():
            rows = session.execute(session.prepare(query).bind(values))
            data = [r._asdict() for r in rows]
        db_counter.labels(app=name, query=query).inc()
        return data
    return execute
