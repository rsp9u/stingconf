from stingconf import config


def test_config():
    c = config.Config()
    c.add('FOO', 'foo', {'type': str})

    assert c.FOO == 'foo'
    assert c.meta.FOO['type'] == str


def test_config_multi():
    c = config.Config()
    c.add('FOO', 'foo', {})
    c.add('BAR', 'bar', {})

    keys = [k for k in c.keys()]
    keys.sort()
    assert keys == ['BAR', 'FOO']

    values = [v for v in c.values()]
    values.sort()
    assert values == ['bar', 'foo']

    items = [(k, v) for k, v in c.items()]
    items.sort()
    assert items == [('BAR', 'bar'), ('FOO', 'foo')]
