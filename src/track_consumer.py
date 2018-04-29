import time
import redis

redis_conn = redis.Redis('127.0.0.1', 6379)

track_queue = 'track'

def main():
    while True:
        value = redis_conn.blpop(track_queue)
        try:
            print('received', value) 
            # todo: write value to datastore
        except Exception:
            redis_conn.rpush(track_queue, value)
            time.sleep(1)

if __name__=='__main__':
    main()
