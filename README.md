## Description

Simple functions to set or get values from a nested dict structure or in fact a deep structure of any object, because
since version 2 we no longer assume we are dealing with dicts.

You may use a custom accessor or pass your own getter, setter, deleter callables so that you can traverse a nested structure of any kind of 
object.

This module DOES NOT implement dotted notation as an alternative access method for dicts.
I generally do not like changing python dicts to enable dot notation, hence no available
package fitted my needs for a simple deep accessor.

Notes:
Often, you could use 'lambda o, k: o[k]' as either the getter or the accessor. The only 'special' thing about the 'getter' function is that when it is
invoked with 'o' being a list and 'k' being a string, it will instead iterate over the list and call the accessor for each item in the list.

In a simplified way, this is how it works:

1. The key is broken down into a list of keys: "customer.address.city" -> ['customer', 'address', 'city'] 

2. The list of keys is iterated over calling the getter for each key and the last value retrieved is returned.
```
for k in keys:
   o = getter(o, k)

return o
```

You see that getter could be as simple as 'lambda o, k: o[k]'. However, by default the code uses a smarter getter as defined below,
which tries to deal properly with lists.

```
def default_getter(o, k):
    if isinstance(o, list):
        if isinstance(k, str) and not k.isdigit():
            r = []
            for i in o:
                r.append(accessor(i, k))
            return r
        elif isinstance(k, str) and k.isdigit():
            k = int(k)
    
    return accessor(o, k)
```

## Functions

*deep_get* accepts:
- o: required. Any object, usually a dictionary
- k: required. The key or keys, must be a string or anything accepted by the list() constructor
- accessor: optional, callable: Takes o, k (object and key) and returns the value. Default accessor is 'lambda: o, k: o[k]'
- getter: optional, callable. If getter is set, default is ignored. Takes an object and a key as arguments and returns a value
- sep: optional, string: by default it is a dot '.', you can use anything the string function split will accept

Returns o[k]


*deep_set* accepts:
- o: see 'deep_get'
- k: see 'deep_get'
- v: required, the value that will be set
- accessor: optional, callable: see 'deep_get'
- getter: optional, callable: see 'deep_get'
- setter: optional, callable. A callable that takes 3 parameters: o, k, v - where o = any object, k = key, v = value
- sep: optional, string: see 'deep_get'

No return value


*deep_del* accepts:
- o: required: see 'deep_get'
- k: required: see 'deep_get'
- sep: optional, string: see 'deep_get'
- accessor: optional, callable: see 'deep_get'
- deleter: optional, callable: Takes 2 parameters: o, k (object and key). By default 'del o[k]' is used.

Returns a tuple:
(True, <value of the entry that was deleted>) or
(False, None)


## Usage

```
i = 0

# Alternative 1
i += 1
o = {'a': {'b': {}}}
deep_set(o, "a.b.c", "Hello World")
print("{}: {}".format(i, deep_get(o, "a.b.c")))

# Alternative 2
i += 1
o = {}
deep_set(o, ['a', 'b', 'c'], "Hello World", accessor=lambda o, k: o.setdefault(k, dict()))
print("{}: {}".format(i, deep_get(o, "a.b.c")))

# Alternative 3
i += 1
o = {}
deep_set(o, "a->b->c", "Hello World", accessor=lambda o, k: o.setdefault(k, dict()), sep="->")
print("{}: {}".format(i, deep_get(o, "a->b->c", sep="->")))

# Alternative 4
i += 1
o = {}
deep_set(o, "a->b->c", "Hello World", getter=lambda o, k: o.setdefault(k, dict()), sep="->")
print("{}: {}".format(i, deep_get(o, "a->b->c", sep="->")))

# Alternative 5
i += 1
o = {}
keys = 'a.b.c'
keys = keys.split()
_ = deep_get(o=o, k=keys[0:-1], accessor=lambda o, k: o.setdefault(k, dict()), sep=".")
_[keys[-1]] = "Hello World"
print("{}: {}".format(i, deep_get(o, keys)))

# deep_del
i += 1
o = {}
deep_set(o, "1.1.1", 'a', accessor=lambda o, k: o.setdefault(k, dict()))
deep_set(o, "1.1.2", 'Hello World')
deep_set(o, "1.1.3", 'c')
print("{}: {}".format(i, deep_del(o, "1.1.2")[1]))
print(o)
```
