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

## How to use

    from dict_deep import __version__, deep_get, deep_set
    
    
    # Alternative 1
    d = {'a': {'b': {}}}
    deep_set(d, "a.b.c", "Hello World")
    print(deep_get(d, "a.b.c"))
    
    # Alternative 2
    d = {}
    deep_set(d, ['a', 'b', 'c'], "Hello World", default=lambda: dict())
    print(deep_get(d, "a.b.c"))
    
    # Alternative 3
    d = {}
    deep_set(d, "a->b->c", "Hello World", default=lambda: dict(), sep="->")
    print(deep_get(d, "a->b->c", sep="->"))
    
    # Alternative 4
    d = {}
    _ = deep_get(d=d, key=['a', 'b'], default=lambda: dict(), sep=".")
    _['c'] = "Hello World"
    print(deep_get(d, "a.b.c"))
