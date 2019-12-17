

def deep_get(o, k, accessor: callable = None, getter: callable = None, sep: str = '.',
             empty_list_as_none: bool = False, list_of_len_one_as_value: bool = False):
    getter = __getter(getter, accessor)
    keys = __keys(k, sep)
    
    for k in keys:
        o = getter(o, k)

    if (empty_list_as_none or list_of_len_one_as_value) and isinstance(o, list) and len(o) <= 1:
        if empty_list_as_none and len(o) == 0:
            o = None
        elif list_of_len_one_as_value and len(o) == 1:
            o = o[0]
    
    return o


def deep_set(o, k, v, accessor: callable = None, getter: callable = None, setter: callable = None, sep: str = '.'):
    keys = __keys(k, sep)
    getter = __getter(getter, accessor)
    setter = __setter(setter)
    
    for i in range(len(keys) - 1):
        o = getter(o, keys[i])
    
    setter(o, keys[-1], v)


def deep_del(o: dict, k, accessor: callable = None, deleter: callable = None, sep: str = '.'):
    keys = __keys(k, sep)
    accessor = accessor if accessor is not None else lambda o, k: o.get(k)
    
    for i in range(len(keys) - 1):
        if o is None:
            return False, None
        o = accessor(o, keys[i])
    
    if o is not None and isinstance(o, dict) and keys[-1] in o:
        retval = accessor(o, keys[-1])
        if deleter is None:
            del o[keys[-1]]
        else:
            deleter(o, keys[-1])
        return True, retval
    else:
        return False, None


def __keys(key, sep: str):
    if isinstance(key, str):
        return key.split(sep=sep)
    else:
        return list(key)


def __getter(getter: callable, accessor: callable):
    if getter is not None:
        return getter
    if accessor is None:
        accessor = lambda o, k: o.get(k)
    
    def __default_getter(o, k):
        if isinstance(o, list) and isinstance(k, str):
            r = []
            for i in o:
                r.append(accessor(i, k))
            return r
        return accessor(o, k)
    
    return __default_getter


def __setter(setter: callable):
    def __default_setter(o, k, v):
        o[k] = v
    return setter if setter is not None else __default_setter
