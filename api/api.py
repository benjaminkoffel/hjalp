import functools
import time
import flask
import jsonschema
import prometheus_client

def initialize(name):
    app = flask.Flask(name)
    metric_latency = prometheus_client.Histogram('request_latency', 'request latency', ['endpoint', 'method', 'path', 'status'])
    metric_counter = prometheus_client.Counter('request_counter', 'request counter', ['endpoint', 'method', 'path', 'status'])
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
        metric_latency.labels(endpoint=app.name, method=flask.request.method, path=flask.request.path, status=response.status_code).observe(latency)
        metric_counter.labels(endpoint=app.name, method=flask.request.method, path=flask.request.path, status=response.status_code).inc()
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
