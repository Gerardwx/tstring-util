import pytest
from string.templatelib import Interpolation, Template
from tstring import iformat

# helper to extract the first interpolation formatting result

def _parse_first(ts: Template) -> str:
    for item in ts:
        if isinstance(item, Interpolation):
            return iformat(item)


def test_inter_basic():
    name = 'Dolly'
    assert _parse_first(t'hello {name}') == 'Dolly'
    frac = 1 / 3
    assert _parse_first(t'round it {frac:.2f}') == '0.33'


def test_repr_conversion():
    data = [1, 2, 3]
    assert _parse_first(t'list: {data!r}') == "[1, 2, 3]"


def test_ascii_conversion():
    s = 'café'
    # ascii() escapes non-ASCII via \x sequences
    assert _parse_first(t'ascii: {s!a}') == "'caf\\xe9'"


def test_str_conversion():
    class Dummy:
        def __str__(self):
            return "dummy"
        def __repr__(self):
            return "repr_dummy"
    d = Dummy()
    assert _parse_first(t'str: {d!s}') == "dummy"


def test_default_conversion():
    class Dummy2:
        def __str__(self):
            return "default"
        def __repr__(self):
            return "repr2"
    d2 = Dummy2()
    assert _parse_first(t'default: {d2}') == "default"


def test_integer_zero_padding():
    num = 7
    assert _parse_first(t'pad: {num:04d}') == "0007"


def test_float_default_format():
    x = 3.14159
    # default float formatting uses str(x)
    assert _parse_first(t'value: {x}') == str(x)


def test_error_on_bad_spec():
    # invalid format spec should raise ValueError
    with pytest.raises(ValueError):
        _parse_first(t'bad: {10:.2x}')

