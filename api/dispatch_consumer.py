import prometheus_client
import que

_, pop = que.initialize(__name__, '127.0.0.1', 6379)

def received(value):
    print(value)
    # todo: notify nearby providers

if __name__=='__main__':
    prometheus_client.start_http_server(port=4000)
    pop('dispatch', received)
