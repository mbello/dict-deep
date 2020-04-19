

def deep_get(o, k, accessor: callable = lambda o, k: o.get(k) if hasattr(o, "get") else o[k],
             getter: callable = None, getter_last_step: callable = None, sep: str = '.',
             empty_list_as_none: bool = False, list_of_len_one_as_value: bool = False):
    keys = __keys(k, sep)
    getter = __getter(getter, accessor)
    getter_last_step = __getter_last_step(getter_last_step, getter)
    
    for i in range(len(keys) - 1):
        if o is not None:
            o = getter(o, keys[i])

    if o is not None:
        o = getter_last_step(o, keys[-1])
        
        if (empty_list_as_none or list_of_len_one_as_value) and isinstance(o, list) and len(o) <= 1:
            if empty_list_as_none and len(o) == 0:
                o = None
            elif list_of_len_one_as_value and len(o) == 1:
                o = o[0]
    
    return o


def deep_set(o, k, v, accessor: callable = lambda o, k: o.setdefault(k, dict()) if hasattr(o, "setdefault") else o[k],
             getter: callable = None, setter: callable = None, sep: str = '.'):
    keys = __keys(k, sep)
    getter = __getter(getter, accessor)
    setter = __setter(setter)
    
    for i in range(len(keys) - 1):
        if o is None:
            return 0
        o = getter(o, keys[i])
    
    return setter(o, keys[-1], v)


def deep_del(o: dict, k, accessor: callable = lambda o, k: o.get(k) if hasattr(o, "get") else o[k],
             getter: callable = None, deleter: callable = None, sep: str = '.'):
    keys = __keys(k, sep)
    getter = __getter(getter, accessor)
    deleter = __deleter(deleter)
    
    for i in range(len(keys) - 1):
        if o is None:
            return 0
        o = getter(o, keys[i])
    
    return deleter(o, keys[-1])


def __keys(key, sep: str):
    if isinstance(key, str):
        return key.split(sep=sep)
    else:
        return list(key)


def __getter(getter: callable, accessor: callable):
    def __default_getter(o, k):
        if isinstance(o, list):
            return [accessor(i, k) for i in o]
        else:
            return accessor(o, k)
    
    return __default_getter if getter is None else getter


def __getter_last_step(getter_last_step: callable, getter: callable):
    def __default_getter_last_step(o, k):
        if isinstance(o, list) and isinstance(k, list):
            return [{item_k: getter(item_o, item_k) for item_k in k} for item_o in o if item_o is not None]
        elif isinstance(k, list):
            return {item_k: getter(o, item_k) for item_k in k}
        else:
            return getter(o, k)
    
    return __default_getter_last_step if getter_last_step is None else getter_last_step


def __setter(setter: callable):
    def __default_setter(o, k, v):
        n_set = 0
        if isinstance(o, list):
            for i in o:
                i[k] = v
                n_set += 1
            return n_set
        else:
            o[k] = v
            return 1

    return setter if setter is not None else __default_setter


def __deleter(deleter: callable):
    def __default_deleter(o, k):
        n_del = 0
        if isinstance(o, list):
            for i in o:
                try:
                    del i[k]
                except:
                    pass
                else:
                    n_del += 1
        else:
            try:
                del o[k]
            except:
                pass
            else:
                n_del += 1
        return n_del

    return deleter if deleter is not None else __default_deleter
