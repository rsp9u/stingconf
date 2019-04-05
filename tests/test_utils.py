from stingconf import utils


def test_str_to_type():
    type_map = {
        'str': (0, '0'),
        'int': ('0', 0),
        'float': ('0.1', 0.1),
        'bool': ('True', True),
    }

    for type_str, (input, expected) in type_map.items():
        cast_func = utils.str_to_type(type_str)
        assert expected == cast_func(input)


def test_to_upper_snake():
    strings = [
        ('spi-nal-case', 'SPI_NAL_CASE'),
        ('mixed-CASE', 'MIXED_CASE'),
        ('-prefix', '_PREFIX'),
        ('postfix-', 'POSTFIX_'),
    ]

    for (input, expected) in strings:
        assert expected == utils.to_upper_snake(input)
