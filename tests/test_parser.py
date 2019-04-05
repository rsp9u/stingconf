import os
import pytest
from unittest import mock
import stingconf
import stingconf.parser


@pytest.mark.parametrize('type_func,default', [
    (str, 'foo'),
    (int, 100),
    (float, 10.0),
    (bool, True),
])
def test_default(type_func, default):
    parser = stingconf.Parser()
    parser.add('foo-config', type=type_func, default=default)

    parser.parse()
    assert parser.FOO_CONFIG == default


@pytest.mark.parametrize('type_func,env_value', [
    (str, 'foo'),
    (int, 100),
    (float, 10.0),
    (bool, True),
])
def test_env(type_func, env_value):
    parser = stingconf.Parser()
    parser.add('foo-config', type=type_func)

    os.environ['FOO_CONFIG'] = str(env_value)
    parser.parse()
    os.environ.pop('FOO_CONFIG')
    assert parser.FOO_CONFIG == env_value


@pytest.mark.parametrize('type_func,arg_value', [
    (str, 'foo'),
    (int, 100),
    (float, 10.0),
    (bool, True),
])
def test_arg(type_func, arg_value):
    parser = stingconf.Parser()
    parser.add('foo-config', type=type_func)

    with mock.patch.object(stingconf.parser.sys, 'argv', ['prog_name', '--foo-config=' + str(arg_value)]):
        parser.parse()
        assert parser.FOO_CONFIG == arg_value


@pytest.mark.parametrize('type_func,file_value', [
    (str, 'foo'),
    (int, 100),
    (float, 10.0),
    (bool, True),
])
def test_file(tmpdir, type_func, file_value):
    parser = stingconf.Parser()
    parser.add('foo-config', type=type_func)

    p = tmpdir.join('config.yml')
    p.write('foo_config: ' + str(file_value))
    parser.conf_file(p.strpath)
    parser.parse()
    assert parser.FOO_CONFIG == file_value


def _config_generator(tmpdir, parser=None):
    if parser is None:
        parser = stingconf.Parser()
    parser.add('foo-config', default='foo')

    parser.parse()
    yield parser.FOO_CONFIG

    p = tmpdir.join('config.yml')
    p.write('foo_config: file-foo')
    parser.conf_file(p.strpath)
    parser.parse()
    yield parser.FOO_CONFIG

    with mock.patch.object(stingconf.parser.sys, 'argv', ['prog_name', '--foo-config=arg-foo']):
        parser.parse()
        yield parser.FOO_CONFIG

        os.environ['FOO_CONFIG'] = 'env-foo'
        parser.parse()
        os.environ.pop('FOO_CONFIG')
        yield parser.FOO_CONFIG


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


def test_env_prefix():
    parser = stingconf.Parser()
    parser.env_prefix('TEST')
    parser.add('foo-config')

    os.environ['FOO_CONFIG'] = 'foo'
    os.environ['TEST_FOO_CONFIG'] = 'test-foo'
    parser.parse()
    os.environ.pop('FOO_CONFIG')
    os.environ.pop('TEST_FOO_CONFIG')
    assert parser.FOO_CONFIG == 'test-foo'


def test_env_no_prefix():
    parser = stingconf.Parser()
    parser.env_prefix('TEST')
    parser.add('foo-config', env={'no_prefix': True})

    os.environ['FOO_CONFIG'] = 'foo'
    os.environ['TEST_FOO_CONFIG'] = 'test-foo'
    parser.parse()
    os.environ.pop('FOO_CONFIG')
    os.environ.pop('TEST_FOO_CONFIG')
    assert parser.FOO_CONFIG == 'foo'


def test_env_ignorecase():
    parser = stingconf.Parser()
    parser.env_prefix('TEST')
    parser.add('foo-config', env={'ignorecase': True})

    os.environ['test_foo_config'] = 'foo'
    parser.parse()
    os.environ.pop('test_foo_config')
    assert parser.FOO_CONFIG == 'foo'


def test_arg_short():
    parser = stingconf.Parser()
    parser.add('foo-config', short='f')

    with mock.patch.object(stingconf.parser.sys, 'argv', ['prog_name', '-f', 'foo']):
        parser.parse()
        assert parser.FOO_CONFIG == 'foo'


def test_file_json(tmpdir):
    parser = stingconf.Parser()
    parser.add('foo-config')

    p = tmpdir.join('config.json')
    p.write('{"foo_config": "foo"}')
    parser.conf_file(p.strpath, type='json')
    parser.parse()
    assert parser.FOO_CONFIG == 'foo'
