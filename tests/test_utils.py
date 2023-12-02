import pytest
from src.utils import is_camel_case, is_pascal_case, is_snake_case, simple_naming_convention_tester, Casing


def test_is_camel_case():
    assert (True, 'OK') == is_camel_case('testString')
    assert (True, 'OK') == is_camel_case('aTS')
    assert (True, 'OK') == is_camel_case('testStringWithNumbers89')
    assert (True, 'OK') == is_camel_case('testString45WithNumbers')
    err_msg = ' is not formatted in camel case'
    false_test_strings = ['test_string', 'TestString', 'TS', '_', '_TS', 'TS_', 'testString withSpace', '8', '_8', '8_',
                          '8TS', 'TS8']
    for s in false_test_strings:
        assert is_camel_case(s) == (False, f'{s}{err_msg}')


def test_is_pascal_case():
    assert (True, 'OK') == is_pascal_case('TestString')
    assert (True, 'OK') == is_pascal_case('TSs')
    assert (True, 'OK') == is_pascal_case('TestStringWithNumbers89')
    assert (True, 'OK') == is_pascal_case('TestString45WithNumbers')

    err_msg = ' is not formatted in pascal case'
    false_test_strings = ['teststring', 'test_string', 'TS', '_', '_TS', 'TS_', '_a', '_TaS', 'TaS_',
                          'testString withSpace', '8', '_8', '8_', '8TS', 'TS8']
    for s in false_test_strings:
        assert is_pascal_case(s) == (False, f'{s}{err_msg}')


def test_is_snake_case():
    assert (True, 'OK') == is_snake_case('test_string')
    assert (True, 'OK') == is_snake_case('test_str78ing')
    assert (True, 'OK') == is_snake_case('test_89')
    assert (True, 'OK') == is_snake_case('s_')
    err_msg = ' is not formatted in snake case'
    false_test_strings = ['8', '_8', '8_', '_8_', '_s', '_s_', '_', '_S', 'S_', '_S_']
    for s in false_test_strings:
        assert is_snake_case(s) == (False, f'{s}{err_msg}')


def test_is_camel_case_no_string_type_exception():
    with pytest.raises(AttributeError, match=f'is_camel_case input must be string, got {type(None)}'):
        is_camel_case(None)

    bool_var = bool(True)
    with pytest.raises(AttributeError, match=f'is_camel_case input must be string, got {type(bool_var)}'):
        is_camel_case(bool_var)

    int_var = int(True)
    with pytest.raises(AttributeError, match=f'is_camel_case input must be string, got {type(int_var)}'):
        is_camel_case(int_var)


def test_is_pascal_case_no_string_type_exception():
    with pytest.raises(AttributeError, match=f'is_pascal_case input must be string, got {type(None)}'):
        is_pascal_case(None)

    bool_var = bool(True)
    with pytest.raises(AttributeError, match=f'is_pascal_case input must be string, got {type(bool_var)}'):
        is_pascal_case(bool_var)

    int_var = int(True)
    with pytest.raises(AttributeError, match=f'is_pascal_case input must be string, got {type(int_var)}'):
        is_pascal_case(int_var)


def test_is_snake_case_no_string_type_exception():
    with pytest.raises(AttributeError, match=f'is_snake_case input must be string, got {type(None)}'):
        is_snake_case(None)

    bool_var = bool(True)
    with pytest.raises(AttributeError, match=f'is_snake_case input must be string, got {type(bool_var)}'):
        is_snake_case(bool_var)

    int_var = int(True)
    with pytest.raises(AttributeError, match=f'is_snake_case input must be string, got {type(int_var)}'):
        is_snake_case(int_var)


def test_simple_naming_convention_tester():
    assert (True, 'OK') == simple_naming_convention_tester('testString', casing=Casing.CAMEL_CASE)
    assert (True, 'OK') == simple_naming_convention_tester('I_testString', prefix='I_', casing=Casing.CAMEL_CASE)
    assert (True, 'OK') == simple_naming_convention_tester('testString', casing=Casing.CAMEL_CASE)
    assert (True, 'OK') == simple_naming_convention_tester('testString', casing=Casing.CAMEL_CASE)

    assert (True, 'OK') == simple_naming_convention_tester('I_FieldbusParameter', prefix='I_', casing=Casing.PASCAL_CASE)

    #

    in_string = 'I_tesI_tString'
    assert (False, f'{in_string} is not formatted in camel case') == simple_naming_convention_tester(in_string, casing=Casing.CAMEL_CASE)






