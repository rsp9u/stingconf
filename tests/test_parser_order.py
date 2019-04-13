import os
try:
    from unittest import mock
except ImportError:
    import mock
import stingconf
import stingconf.parser


def _config_generator(tmpdir, parser=None):
    if parser is None:
        parser = stingconf.Parser()
    parser.add('foo-config', default='foo')

    config = parser.parse()
    yield config.FOO_CONFIG

    p = tmpdir.join('config.yml')
    p.write('foo_config: file-foo')
    parser.conf_file(p.strpath)
    config = parser.parse()
    yield config.FOO_CONFIG

    with mock.patch.object(stingconf.parser.sys, 'argv', ['prog_name', '--foo-config=arg-foo']):
        config = parser.parse()
        yield config.FOO_CONFIG

        os.environ['FOO_CONFIG'] = 'env-foo'
        config = parser.parse()
        os.environ.pop('FOO_CONFIG')
        yield config.FOO_CONFIG


def test_default_order_to_default(tmpdir):
    foo_getter = _config_generator(tmpdir)
    assert next(foo_getter) == 'foo'


def test_default_order_to_file(tmpdir):
    foo_getter = _config_generator(tmpdir)
    assert next(foo_getter) == 'foo'
    assert next(foo_getter) == 'file-foo'


def test_default_order_to_arg(tmpdir):
    foo_getter = _config_generator(tmpdir)
    assert next(foo_getter) == 'foo'
    assert next(foo_getter) == 'file-foo'
    assert next(foo_getter) == 'arg-foo'


def test_default_order_to_env(tmpdir):
    foo_getter = _config_generator(tmpdir)
    assert next(foo_getter) == 'foo'
    assert next(foo_getter) == 'file-foo'
    assert next(foo_getter) == 'arg-foo'
    assert next(foo_getter) == 'env-foo'


def test_custom_order_single(tmpdir):
    parser = stingconf.Parser()
    parser.order('file')
    foo_getter = _config_generator(tmpdir, parser)
    assert next(foo_getter) == 'foo'
    assert next(foo_getter) == 'file-foo'
    assert next(foo_getter) == 'file-foo'
    assert next(foo_getter) == 'file-foo'


def test_custom_order_double(tmpdir):
    parser = stingconf.Parser()
    parser.order('arg', 'file')
    foo_getter = _config_generator(tmpdir, parser)
    assert next(foo_getter) == 'foo'
    assert next(foo_getter) == 'file-foo'
    assert next(foo_getter) == 'arg-foo'
    assert next(foo_getter) == 'arg-foo'


def test_custom_order_full(tmpdir):
    parser = stingconf.Parser()
    parser.order('arg', 'env', 'default', 'file')
    foo_getter = _config_generator(tmpdir, parser)
    assert next(foo_getter) == 'foo'
    assert next(foo_getter) == 'foo'
    assert next(foo_getter) == 'arg-foo'
    assert next(foo_getter) == 'arg-foo'
