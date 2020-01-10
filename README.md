## Description

Simple functions to set or get values from a nested dict structure or in fact a deep structure of any object, because
since version 2 we no longer assume we are dealing with dicts.

You may use a custom accessor or pass your own getter, setter, deleter callables so that you can traverse a nested
structure of any kind of object.

This module DOES NOT implement dotted notation as an alternative access method for dicts.
I generally do not like changing python dicts to enable dot notation, hence no available
package fitted my needs for a simple deep accessor.

NEW IN VERSION 4:
Since version 3 we make no assumption that we are dealing with dicts, so you can have your nested
structure of any type. However, in version 4 we reintroduce better defaults so that for those that
are indeed working with nested dicts the default values shall be enough without having to define an
accessor or a getter.

Notes:
With deep_get, you could use 'lambda o, k: o[k]' or 'lambda o, k: o.get(k)' as either the getter or the accessor.
The only 'special' thing about the 'getter' function is that when it is invoked with 'o' being a list, it will instead
iterate over the list and call the accessor for each item in the list.

In a simplified way, this is how deep_get works:

1. The key is broken down into a list of keys: "customer.address.city" -> ['customer', 'address', 'city'] 

2. The list of keys is iterated over, calling the getter for each key and the last value retrieved is returned.
```
for k in keys[:-1]:
    if o is None:
        return o
    o = getter(o, k)

o = getter_last_step(o, keys[-1])

return o
```

You see that getter could be as simple as 'lambda o, k: o.get(k)'. However, by default the code uses a smarter getter as
defined below, which tries to deal properly with nested lists.

```
def __default_getter(o, k):
    if isinstance(o, list):
        return [accessor(i, k) for i in o]
    else:
        return accessor(o, k)
```

If you do not want this checks for nested lists, just pass your own getter which could just as well
be 'lambda o, k: o.get(k)'.

The default setter also knows how to deal with nested lists:
```
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
```
You could just as well replace if with your own 'setter=lambda o, k, v: o[k]=v' if you know that
you have no nested lists in your structures and want to avoid the overhead, but in that case you should
also change the getter 'getter=lambda o, k: o.get(k)'.

However, if you like the list handling skills of the code but just needs to change the way the value is retrieved,
in this case you pass an accessor only to deep_get or deep_set which could be, say, 'lambda o, k: o.getValueById(k)'


## Functions

*deep_get* accepts:
- o: required. Any object, usually a dictionary
- k: required. The key or keys, must be a string or anything accepted by the list() constructor
- accessor: optional, callable: Takes o, k (object and key) and returns the value. Default accessor is
  'lambda o, k: o.get(k) if hasattr(o, "get") else o[k]'
- getter: optional, callable. If getter is set, accessor is ignored. Takes an object and a key as arguments and returns
  a value
- getter_last_step: optional, callable. The getter to be used on the last step (with the last key). By default,
  if the last key is a list of keys, it returns a dict {k[0]: o[k[0]], k[1]: o[k[1]]}. If the last object is a list, it returns a list
  of dicts [{k[0]: o[0][k[0]]], k[1]: o[0][k[1]]}, {k[0]: o[1][k[0]]], k[1]: o[1][k[1]]}, ...]
- sep: optional, string: by default it is a dot '.', you can use anything the string function split will accept
- empty_list_as_none: bool = False. If true and the return value would be an empty list, returns None instead.
- list_of_len_one_as_value: bool = False. If true and the return value would be a list with a single item, returns the item instead

Returns o[k]. If o[k] does not exist, should return None (but depends on the callables used).


*deep_set* accepts:
- o: see 'deep_get'
- k: see 'deep_get'
- v: required, the value that will be set
- accessor: optional, callable: see 'deep_get'. For the deep_set function, the default accessor is:
  'lambda o, k: o.setdefault(k, dict()) if hasattr(o, "setdefault") else o[k]'
- getter: optional, callable: see 'deep_get'
- setter: optional, callable. A callable that takes 3 parameters: o, k, v - where o = any object, k = key, v = value
- sep: optional, string: see 'deep_get'

No return value


*deep_del* accepts:
- o: required: see 'deep_get'
- k: required: see 'deep_get'
- accessor: optional, callable: see 'deep_get'
- getter: optional, callable: see 'deep_get'
- deleter: optional, callable: Takes 2 parameters: o, k (object and key).
- sep: optional, string: see 'deep_get'

Returns an integer with the number of entries that were deleted.


## Example / Usage

```
from dict_deep import deep_get, deep_set, deep_del


i = 0

# 1
i += 1
o = {'a': {'b': {}}}
deep_set(o, "a.b.c", "Hello World")
print("{}: {}".format(i, deep_get(o, "a.b.c")))

# 2
i += 1
o = {}
deep_set(o, ['a', 'b', 'c'], "Hello World")
print("{}: {}".format(i, deep_get(o, "a.b.c")))

# 3
i += 1
o = {}
deep_set(o, "a->b->c", "Hello World", sep="->")
print("{}: {}".format(i, deep_get(o, "a->b->c", sep="->")))

# 4
i += 1
o = {}
deep_set(o, "a->b->c", "Hello World", getter=lambda o, k: o.setdefault(k, dict()), sep="->")
print("{}: {}".format(i, deep_get(o, "a->b->c", sep="->")))

# 5
i += 1
o = {}
keys = 'a.b.c'
keys = keys.split('.')
_ = deep_get(o=o, k=keys[0:-1], accessor=lambda o, k: o.setdefault(k, dict()), sep=".")
_[keys[-1]] = "Hello World"
print("{}: {}".format(i, deep_get(o, keys)))

# 6
i += 1
o = {}
deep_set(o, "1.1.1", 'a', accessor=lambda o, k: o.setdefault(k, dict()))
deep_set(o, "1.1.2", 'Hello World')
deep_set(o, "1.1.3", 'c')
deep_del(o, "1.1.2")
print("{}: {}".format(i, o))

# 7
i += 1
o = {'students': [{'name': 'Joe', 'age': 10, 'gender': 'male'}, {'name': 'Maria', 'age': 12, 'gender': 'female'}]}
keys = ['students', 'name']
print("{}: {}".format(i, deep_get(o, keys)))

# 8
i += 1
keys = ['students', ['name', 'age']]
print("{}: {}".format(i, deep_get(o, keys)))

# 9
i += 1
keys = ['students', 'gender']
deep_set(o, keys, 'Nowadays better not ask')
print("{}: {}".format(i, o))

# 10
i += 1
keys = ['students', 'gender']
deep_del(o, keys)
print("{}: {}".format(i, o))

# 11
i += 1
keys = ['director', 'name']
print("{}: {}".format(i, deep_get(o, keys)))
```
