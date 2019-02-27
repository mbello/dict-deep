from dict_deep import deep_get, deep_set


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
