import jsonschema

def validate(schema, value):
    jsonschema.validate(value, schema)
    return value

queue_track_1 = {
    'type': 'object',
    'properties': {
        'time': { 'type': 'string' },
        'provider': { 'type': 'string' },
        'state': { 'type': 'string', 'pattern': 'online|offline' },
        'latitude': { 'type': 'number' },
        'longitude': { 'type': 'number' },
    },
    'required': ['state', 'latitude', 'longitude']
}
