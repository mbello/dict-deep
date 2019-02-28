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
deep_set(d, "a->b->c", "Hello World", getter=lambda o, k: o.setdefault(k, dict()), sep="->")
print("{}: {}".format(i, deep_get(d, "a->b->c", sep="->")))

# Alternative 5
i += 1
d = {}
keys = 'a.b.c'
keys = keys.split()
_ = deep_get(d=d, key=keys[0:-1], default=lambda: dict(), sep=".")
_[keys[-1]] = "Hello World"
print("{}: {}".format(i, deep_get(d, keys)))

# deep_del
i += 1
d = {}
deep_set(d, "1.1.1", 'a', default=lambda: dict())
deep_set(d, "1.1.2", 'Hello World')
deep_set(d, "1.1.3", 'c')
print("{}: {}".format(i, deep_del(d, "1.1.2")[1]))
print(d)
