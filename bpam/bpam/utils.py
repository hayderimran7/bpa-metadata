import json


def json_encoder(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        return json.JSONEncoder().default(obj)
