import re
from enum import Enum


class Casing(Enum):
    NONE = 0
    CAMEL_CASE = 1
    PASCAL_CASE = 2
    SNAKE_CASE = 3


def simple_naming_convention_tester(s: str, prefix=None, suffix=None, casing=Casing.NONE) -> (bool, str):
    if not isinstance(s, str):
        raise AttributeError(f'simple_naming_convention_tester input must be string, got {type(s)}')
    if prefix is not None and isinstance(prefix, str):
        if s.startswith(prefix):
            s = s.lstrip(prefix)
        else:
            return False, f'{s} does not start with prefix "{prefix}"'

    if suffix is not None and isinstance(suffix, str):
        if s.endswith(suffix):
            s = s.rstrip(suffix)
        else:
            return False, f'{s} does not start with suffix "{suffix}"'

    match casing:
        case Casing.NONE:
            return True, 'OK'
        case Casing.CAMEL_CASE:
            return is_camel_case(s)
        case Casing.PASCAL_CASE:
            return is_pascal_case(s)
        case Casing.SNAKE_CASE:
            return is_snake_case(s)
        case _:
            raise KeyError('Unsupported Casing test')


def is_camel_case(s: str) -> (bool, str):
    """Check if a string is in camelCase format."""
    if not isinstance(s, str):
        raise AttributeError(f'is_camel_case input must be string, got {type(s)}')
    pattern = "^([a-z][A-Za-z0-9]+)*$"
    if re.match(pattern, s):
        if s != s.lower() and s != s.upper() and "_" not in s:
            return True, 'OK'
        else:
            return False, f'{s} is not formatted in camel case'
    else:
        return False, f'{s} is not formatted in camel case'


def is_pascal_case(s: str) -> (bool, str):
    """Check if a string is in PascalCase format."""
    if not isinstance(s, str):
        raise AttributeError(f'is_pascal_case input must be string, got {type(s)}')
    pattern = "^([A-Z][A-Za-z0-9]+)*$"
    if re.match(pattern, s):
        if s != s.lower() and s != s.upper() and "_" not in s:
            return True, 'OK'
        else:
            return False, f'{s} is not formatted in pascal case'
    else:
        return False, f'{s} is not formatted in pascal case'


def is_snake_case(s: str) -> (bool, str):
    """Check if a string is in snake_case format."""
    if not isinstance(s, str):
        raise AttributeError(f'is_snake_case input must be string, got {type(s)}')
    pattern = "^([a-z][a-z0-9_]+)*$"
    if re.match(pattern, s):
        return True, 'OK'
    else:
        return False, f'{s} is not formatted in snake case'
