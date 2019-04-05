import pytest
from stingconf import utils


@pytest.mark.parametrize('type_str,test_input,expected', [
    ('str', 0, '0'),
    ('int', '0', 0),
    ('float', '0.1', 0.1),
    ('bool', 'True', True),
])
def test_str_to_type(type_str, test_input, expected):
    cast_func = utils.str_to_type(type_str)
    assert expected == cast_func(test_input)


@pytest.mark.parametrize('test_input,expected', [
    ('spi-nal-case', 'SPI_NAL_CASE'),
    ('mixed-CASE', 'MIXED_CASE'),
    ('-prefix', '_PREFIX'),
    ('postfix-', 'POSTFIX_'),
])
def test_to_upper_snake(test_input, expected):
    assert expected == utils.to_upper_snake(test_input)
