from dict_deep import deep_get, deep_set, deep_del


def test1():
    v = "Hello World"
    o = {'a': {'b': {}}}
    deep_set(o, "a.b.c", v)
    assert deep_get(o, "a.b.c") == v


def test2():
    v = "Hello World"
    o = {}
    deep_set(o, ['a', 'b', 'c'], v)
    assert deep_get(o, "a.b.c") == v


def test3():
    v = "Hello World"
    o = {}
    deep_set(o, "a->b->c", v, sep="->")
    assert deep_get(o, "a->b->c", sep="->") == v


def test4():
    v = "Hello World"
    o = {}
    deep_set(o, "a->b->c", v, getter=lambda o, k: o.setdefault(k, dict()), sep="->")
    assert deep_get(o, "a->b->c", sep="->") == v

    
def test5():
    v = "Hello World"
    o = {}
    keys = 'a.b.c'
    keys = keys.split('.')
    _ = deep_get(o=o, k=keys[0:-1], accessor=lambda o, k: o.setdefault(k, dict()), sep=".")
    _[keys[-1]] = "Hello World"
    assert deep_get(o, keys) == v


def test6():
    o: dict = {}
    deep_set(o, "1.1.1", 'a', accessor=lambda o, k: o.setdefault(k, dict()))
    deep_set(o, "1.1.2", 'Hello World')
    deep_set(o, "1.1.3", 'c')
    deep_del(o, "1.1.2")
    assert deep_get(o, "1.1.1") == 'a'
    assert deep_get(o, "1.1.2") is None
    assert deep_get(o, "1.1.3") == 'c'

    assert o['1']['1']['1'] == 'a'
    assert o['1']['1']['3'] == 'c'
    assert o['1']['1'].get('2') is None


def test7():
    o = {'students': [{'name': 'Joe', 'age': 10, 'gender': 'male'}, {'name': 'Maria', 'age': 12, 'gender': 'female'}]}
    keys = ['students', 'name']
    l = deep_get(o, keys)
    assert isinstance(l, list)
    assert len(l) == 2
    assert l[0] == 'Joe'
    assert l[1] == 'Maria'

    keys = ['students', ['name', 'age']]
    l = deep_get(o, keys)
    assert isinstance(l, list)
    assert len(l) == 2
    assert isinstance(l[0], dict)
    assert l[0]['name'] == 'Joe'
    assert l[0]['age'] == 10
    assert isinstance(l[1], dict)
    assert l[1]['name'] == 'Maria'
    assert l[1]['age'] == 12

    keys = ['students', 'gender']
    deep_set(o, keys, 'Nowadays better not ask')
    l = deep_get(o, keys)
    assert isinstance(l, list)
    assert len(l) == 2
    assert l[0] == l[1] == 'Nowadays better not ask'

    deep_del(o, keys)
    l = deep_get(o, keys)
    assert isinstance(l, list)
    assert len(l) == 2
    assert l[0] is None and l[1] is None

    keys = ['director', 'name']
    l = deep_get(o, keys)
    assert l is None


# https://github.com/mbello/dict-deep/issues/2
def test_issue2():
    assert deep_get({"a": "b"}, "a") == 'b'
    assert deep_get({"a": "b"}, "c") is None
    assert deep_get({"a": "b"}, "c.d") is None
    assert deep_get({"a": "b"}, "c.d.e") is None
    assert deep_get({}, "a") is None
    assert deep_get({}, "c") is None
    assert deep_get({}, "c.d") is None
    assert deep_get({}, "c.d.e") is None
