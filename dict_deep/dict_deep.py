METHOD_DEFAULT = 0
METHOD_ATTR = 1
METHOD_GET = 2
METHOD_SETDEFAULT = 3


def deep_get(d: dict, key, access_method: int = METHOD_DEFAULT, default: callable = None, sep: str = '.', ):
    if access_method == METHOD_DEFAULT:
        access_method = METHOD_ATTR if default is None else METHOD_SETDEFAULT

    if isinstance(key, str):
        keys = key.split(sep=sep)
    else:
        keys = list(key)
    
    if access_method == METHOD_ATTR:
        for k in keys:
            d = d[k]
    elif access_method == METHOD_GET:
        for k in keys:
            d = d.get(k, default())
    elif access_method == METHOD_SETDEFAULT:
        for k in keys:
            d = d.setdefault(k, default())
    else:
        raise ValueError('deep_get: invalid access method, use one of METHOD_ATTR, METHOD_GET or METHOD_SETDEFAULT')
    
    return d


def deep_set(d: dict, key, value, default: callable = None, sep: str = '.'):
    if isinstance(key, str):
        keys = key.split(sep=sep)
    else:
        keys = list(key)
    
    _d = d
    for i in range(len(keys) - 1):
        d = d[keys[i]] if default is None else d.setdefault(keys[i], default())
    
    d[keys[-1]] = value
