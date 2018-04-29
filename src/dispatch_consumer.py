import time
import redis

redis_conn = redis.Redis('127.0.0.1', 6379)

dispatch_queue = 'dispatch'

def main():
    while True:
        value = redis_conn.blpop(dispatch_queue)
        try:
            print('received', value) 
            # todo: notify nearby providers
        except Exception:
            redis_conn.rpush(dispatch_queue, value)
            time.sleep(1)

if __name__=='__main__':
    main()
