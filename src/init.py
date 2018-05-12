import cassandra.cluster
import cassandra.policies

session = cassandra.cluster.Cluster(['localhost'], load_balancing_policy=cassandra.policies.RoundRobinPolicy(), port=9042).connect()
session.execute("CREATE KEYSPACE IF NOT EXISTS hjalp WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }")
session.set_keyspace('hjalp')
