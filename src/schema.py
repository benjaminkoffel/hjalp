import jsonschema

def validate(schema, value):
    jsonschema.validate(value, schema)
    return value

request_track_1 = {
    'type': 'object',
    'properties': {
        'state': { 'type': 'string', 'pattern': 'online|offline' },
        'latitude': { 'type': 'number' },
        'longitude': { 'type': 'number' },
    },
    'required': ['state', 'latitude', 'longitude']
}

queue_track_1 = {
    'type': 'object',
    'properties': {
        'time': { 'type': 'number' },
        'provider': { 'type': 'string' },
        'state': { 'type': 'string', 'pattern': 'online|offline' },
        'latitude': { 'type': 'number' },
        'longitude': { 'type': 'number' },
    },
    'required': ['time', 'provider', 'state', 'latitude', 'longitude']
}

queue_dispatch_1 = {
    'type': 'object',
    'properties': {
        'time': { 'type': 'string' },
        'consumer': { 'type': 'string' },
        'latitude': { 'type': 'number' },
        'longitude': { 'type': 'number' },
    },
    'required': ['time', 'consumer', 'latitude', 'longitude']
}

queue_accept_1 = {
    'type': 'object',
    'properties': {
        'time': { 'type': 'string' },
        'provider': { 'type': 'string' },
        'dispatch': { 'type': 'string' },
    },
    'required': ['time', 'provider', 'dispatch']
}
