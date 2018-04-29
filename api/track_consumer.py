import prometheus_client
import que

_, pop = que.initialize(__name__, '127.0.0.1', 6379)

def received(value):
    print(value)
    # todo: write to datastore

if __name__=='__main__':
    prometheus_client.start_http_server(port=2000)
    pop('track', received)
