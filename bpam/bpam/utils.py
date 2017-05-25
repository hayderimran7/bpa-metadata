import json


def json_encoder(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        return json.JSONEncoder().default(obj)


def common_values(dicts):
    """
    given a list of dicts, return a dict with only the values shared
    in common between those dicts
    """
    all_keys = set()
    for d in dicts:
        all_keys = all_keys.union(set(d.keys()))
    r = {}
    for k in all_keys:
        vals = set([repr(d.get(k)) for d in dicts])
        if len(vals) == 1:
            r[k] = dicts[0][k]
    return r
