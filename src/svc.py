import atexit
import json
import logging
import random
import uuid
import kazoo
import kazoo.client

def initialize(name, config, host, port):
    instance = str(uuid.uuid4())
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger(name)
    zk = kazoo.client.KazooClient(hosts='{}:{}'.format(host, port))
    def unregister():
        zk.stop()
    atexit.register(unregister)
    zk.start()
    zk.create('/services/{}/{}'.format(name, instance), value=json.dumps(config).encode('utf-8'), ephemeral=True, makepath=True)
    def discover(path):
        try:
            items = zk.get_children(path)
            random.shuffle(items)
            for i in items:
                return discover('{}/{}'.format(path, i))
            value, _ = zk.get(path)
            return value
        except kazoo.exceptions.NoNodeError:
            return None
    return name, instance, log, discover
