## Description

Simple functions to set or get values from a nested dict structure

This module DOES NOT implement dotted notation as an alternative access method for dicts.
I generally do not like changing python dicts to enable dot notation, hence no available
package fitted my needs for a simple deep accessor.


## Arguments

*deep_get* accepts:
- d: the dictionary
- key: a string OR anything accepted by the list() constructor
- access_method: one of METHOD_ATTR (assumed if default is None), METHOD_GET,
                 METHOD_SETDEFAULT (assumed if default is not None). This determines the method
                 to be used to access the nested dict structure. 
- default: a callable to be used as default for the dict .get or .setdefault functions
- sep: by default it is a dot '.', you can use anything the string function split will accept


*deep_set* accepts:
- d: same as above
- key: same as above
- value
- default: if set (not None which is the default), will use setdefault to traverse the nested dict structure
- sep: same as above


*deep_del* accepts:
- d: same as above
- key: same as above
- sep: same as above

It returns a tuple:
(True, <value of the entry that was deleted>) or
(False, None)

## How to use

    from dict_deep import deep_get, deep_set, deep_del
    
    
    i = 0
    
    # Alternative 1
    i += 1
    d = {'a': {'b': {}}}
    deep_set(d, "a.b.c", "Hello World")
    print("{}: {}".format(i, deep_get(d, "a.b.c")))
    
    # Alternative 2
    i += 1
    d = {}
    deep_set(d, ['a', 'b', 'c'], "Hello World", default=lambda: dict())
    print("{}: {}".format(i, deep_get(d, "a.b.c")))
    
    # Alternative 3
    i += 1
    d = {}
    deep_set(d, "a->b->c", "Hello World", default=lambda: dict(), sep="->")
    print("{}: {}".format(i, deep_get(d, "a->b->c", sep="->")))
    
    # Alternative 4
    i += 1
    d = {}
    _ = deep_get(d=d, key=['a', 'b'], default=lambda: dict(), sep=".")
    _['c'] = "Hello World"
    print("{}: {}".format(i, deep_get(d, "a.b.c")))
    
    # deep_del
    i += 1
    d = {}
    deep_set(d, "1.1.1", 'a', default=lambda: dict())
    deep_set(d, "1.1.2", 'Hello World')
    deep_set(d, "1.1.3", 'c')
    print("{}: {}".format(i, deep_del(d, "1.1.2")[1]))
