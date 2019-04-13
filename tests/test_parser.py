import os
import pytest
try:
    from unittest import mock
except ImportError:
    import mock
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

    config = parser.parse()
    assert config.FOO_CONFIG == default


def test_without_default():
    parser = stingconf.Parser()
    parser.add('foo-config')

    config = parser.parse()
    assert hasattr(config, 'FOO_CONFIG') is False


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
    config = parser.parse()
    os.environ.pop('FOO_CONFIG')
    assert config.FOO_CONFIG == env_value


@pytest.mark.parametrize('type_func,env_values,delimiter', [
    (str, ['foo', 'bar'], ','),
    (str, ['foo', 'bar'], '|'),
    (int, [100, 200], ':'),
    (float, [10.0, 5.5], '&'),
    (bool, [True, False], '::'),
])
def test_repeatable_env(type_func, env_values, delimiter):
    parser = stingconf.Parser()
    parser.add('foo-config', type=type_func, repeatable=True, delimiter=delimiter)

    os.environ['FOO_CONFIG'] = delimiter.join([str(v) for v in env_values])
    config = parser.parse()
    os.environ.pop('FOO_CONFIG')
    assert config.FOO_CONFIG == env_values


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
        config = parser.parse()
        assert config.FOO_CONFIG == arg_value


@pytest.mark.parametrize('type_func,arg_values', [
    (str, ['foo', 'bar']),
    (int, [100, 200]),
    (float, [10.0, 5.5]),
    (bool, [True, False]),
])
def test_repeatable_arg(type_func, arg_values):
    parser = stingconf.Parser()
    parser.add('foo-config', type=type_func, repeatable=True)

    with mock.patch.object(stingconf.parser.sys, 'argv', ['prog_name', '--foo-config'] + [str(v) for v in arg_values]):
        config = parser.parse()
        assert config.FOO_CONFIG == arg_values


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
    config = parser.parse()
    assert config.FOO_CONFIG == file_value


@pytest.mark.parametrize('type_func,file_values', [
    (str, ['foo', 'bar']),
    (int, [100, 200]),
    (float, [10.0, 5.5]),
    (bool, [True, False]),
])
def test_repeatable_file(tmpdir, type_func, file_values):
    parser = stingconf.Parser()
    parser.add('foo-config', type=type_func, repeatable=True)

    p = tmpdir.join('config.yml')
    p.write('foo_config: [' + ','.join([str(v) for v in file_values]) + ']')
    parser.conf_file(p.strpath)
    config = parser.parse()
    assert config.FOO_CONFIG == file_values


def test_env_prefix():
    parser = stingconf.Parser()
    parser.env_prefix('TEST')
    parser.add('foo-config')

    os.environ['FOO_CONFIG'] = 'foo'
    os.environ['TEST_FOO_CONFIG'] = 'test-foo'
    config = parser.parse()
    os.environ.pop('FOO_CONFIG')
    os.environ.pop('TEST_FOO_CONFIG')
    assert config.FOO_CONFIG == 'test-foo'


def test_env_no_prefix():
    parser = stingconf.Parser()
    parser.env_prefix('TEST')
    parser.add('foo-config', env={'no_prefix': True})

    os.environ['FOO_CONFIG'] = 'foo'
    os.environ['TEST_FOO_CONFIG'] = 'test-foo'
    config = parser.parse()
    os.environ.pop('FOO_CONFIG')
    os.environ.pop('TEST_FOO_CONFIG')
    assert config.FOO_CONFIG == 'foo'


def test_env_ignorecase():
    parser = stingconf.Parser()
    parser.env_prefix('TEST')
    parser.add('foo-config', env={'ignorecase': True})

    os.environ['test_foo_config'] = 'foo'
    config = parser.parse()
    os.environ.pop('test_foo_config')
    assert config.FOO_CONFIG == 'foo'


def test_env_ignorecase_mixed_case():
    parser = stingconf.Parser()
    parser.env_prefix('TEST')
    parser.add('foo-config', env={'ignorecase': True})

    os.environ['test_FOO_config'] = 'foo'
    config = parser.parse()
    os.environ.pop('test_FOO_config')
    assert config.FOO_CONFIG == 'foo'


def test_arg_short():
    parser = stingconf.Parser()
    parser.add('foo-config', short='f')

    with mock.patch.object(stingconf.parser.sys, 'argv', ['prog_name', '-f', 'foo']):
        config = parser.parse()
        assert config.FOO_CONFIG == 'foo'


def test_arg_long_prefix():
    parser = stingconf.Parser()
    parser.add('foo-config', long_prefix='-')

    with mock.patch.object(stingconf.parser.sys, 'argv', ['prog_name', '-foo-config', 'foo']):
        config = parser.parse()
        assert config.FOO_CONFIG == 'foo'


def test_arg_short_prefix():
    parser = stingconf.Parser()
    parser.add('foo-config', short='f', short_prefix='--')

    with mock.patch.object(stingconf.parser.sys, 'argv', ['prog_name', '--f', 'foo']):
        config = parser.parse()
        assert config.FOO_CONFIG == 'foo'


def test_file_json(tmpdir):
    parser = stingconf.Parser()
    parser.add('foo-config')

    p = tmpdir.join('config.json')
    p.write('{"foo_config": "foo"}')
    parser.conf_file(p.strpath, type='json')
    config = parser.parse()
    assert config.FOO_CONFIG == 'foo'


def test_pass_args():
    parser = stingconf.Parser()
    parser.add('foo-config')

    config = parser.parse(['--foo-config', 'foo'])
    assert config.FOO_CONFIG == 'foo'
