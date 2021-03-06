import functools
import time
import flask
import jsonschema
import prometheus_client
import redis

def initialize(name):
    app = flask.Flask(name)
    request_latency = prometheus_client.Histogram('request_latency', 'request latency', ['app', 'method', 'path', 'status'])
    request_counter = prometheus_client.Counter('request_counter', 'request counter', ['app', 'method', 'path', 'status'])
    @app.route('/health')
    def health():
        return 'OK'
    @app.route('/version')
    def version():
        return '0.1.0'
    @app.before_request
    def before_request():
        flask.request.start_time = time.time()
    @app.after_request
    def after_request(response):
        latency = time.time() - flask.request.start_time
        request_latency.labels(app=name, method=flask.request.method, path=flask.request.path, status=response.status_code).observe(latency)
        request_counter.labels(app=name, method=flask.request.method, path=flask.request.path, status=response.status_code).inc()
        return response
    return app

def validate(schema):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                jsonschema.validate(flask.request.json, schema)
            except Exception as e:
                return 'BAD REQUEST', 400
            return func(*args, **kw)
        return wrapper
    return decorator
