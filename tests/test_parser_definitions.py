import os
import stingconf


def _definitions():
    return {
        'items': {
            'foo-config': {
                'default': 5,
                'type': 'int',
            },
            'bar-config': {
                'default': 0,
                'type': 'int',
            },
        }
    }


def test_parse_with_definitions():
    os.environ['BAR_CONFIG'] = '10'

    parser = stingconf.Parser('Test module', _definitions())
    config = parser.parse()
    assert config.FOO_CONFIG == 5
    assert config.BAR_CONFIG == 10

    os.environ.pop('BAR_CONFIG')


def test_parse_with_definitions_twice():
    os.environ['BAR_CONFIG'] = '10'
    d = _definitions()

    parser = stingconf.Parser('Test module', d)
    config = parser.parse()
    assert config.FOO_CONFIG == 5
    assert config.BAR_CONFIG == 10

    parser = stingconf.Parser('Test module', d)
    config = parser.parse()
    assert config.FOO_CONFIG == 5
    assert config.BAR_CONFIG == 10

    os.environ.pop('BAR_CONFIG')
