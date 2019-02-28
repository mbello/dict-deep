## Description

Simple functions to set or get values from a nested dict structure or in fact a deep structure of any object, because
since version 2 we no longer assume we are dealing with dicts.

Although we make your life easier if working with dicts (see the default argument that was left for this purpose),
we now let you use custom getter, setter, deleter callables so that you can traverse a nested structure of any kind of 
object.

This module DOES NOT implement dotted notation as an alternative access method for dicts.
I generally do not like changing python dicts to enable dot notation, hence no available
package fitted my needs for a simple deep accessor.


## Functions

*deep_get* accepts:
- d: required. Any object, usually a dictionary.
- key: required. A string or anything accepted by the list() constructor.
- default: optional, callable: a callable to be used as default for the dict .setdefault function. If d is not a dict, use a custom getter instead.
- getter: optional, callable. If getter is set, default is ignored. Must be a callable that accepts an object and a key as arguments. (ex. lambda o, k: o[k])
- sep: optional, string: by default it is a dot '.', you can use anything the string function split will accept

Returns the value corresponding to 'key' on 'd'


*deep_set* accepts:
- d: same as above
- key: same as above
- value: required, self explanatory
- default: optional, callable: If set, will use setdefault to traverse the nested dict structure. See comments from deep_get.
- getter: same as above.
- setter: optional, callable. A callable that takes 3 parameters: o, k, v - where o = any object, k = key, v = value  
- sep: same as above

No return value


*deep_del* accepts:
- d: same as above
- key: same as above
- sep: same as above
- getter: same as above. However, make your getter return None if you want to avoid exceptions being raised.
- deleter: optional callable: A callable that takes 2 parameters: o, k (object and key). By default we call 'del o[k]'

Returns a tuple:
(True, <value of the entry that was deleted>) or
(False, None)


## Usage

    from dict_deep import deep_get, deep_set, deep_del
    
    
    i = 1
    
    
    # Alternative 1
    d = {'a': {'b': {}}}
    deep_set(d, "a.b.c", "Hello World")
    print("{}: {}".format(i, deep_get(d, "a.b.c")))
    i += 1


    # Alternative 2
    d = {}
    deep_set(d, ['a', 'b', 'c'], "Hello World", default=lambda: dict())
    print("{}: {}".format(i, deep_get(d, "a.b.c")))    
    i += 1
    
    
    # Alternative 3
    d = {}
    deep_set(d, "a->b->c", "Hello World", default=lambda: dict(), sep="->")
    print("{}: {}".format(i, deep_get(d, "a->b->c", sep="->")))
    i += 1
    
    
    # Alternative 4
    d = {}
    deep_set(d, "a->b->c", "Hello World", getter=lambda o, k: o.setdefault(k, dict()), sep="->")
    print("{}: {}".format(i, deep_get(d, "a->b->c", sep="->")))
    i += 1
    
    
    # Alternative 5
    d = {}
    keys = 'a.b.c'
    keys = keys.split()
    _ = deep_get(d=d, key=keys[0:-1], default=lambda: dict(), sep=".")
    _[keys[-1]] = "Hello World"
    print("{}: {}".format(i, deep_get(d, keys)))
    i += 1
    
    
    # deep_del
    d = {}
    deep_set(d, "1.1.1", 'a', default=lambda: dict())
    deep_set(d, "1.1.2", 'Hello World')
    deep_set(d, "1.1.3", 'c')
    print("{}: {}".format(i, deep_del(d, "1.1.2")[1]))
    print(d)