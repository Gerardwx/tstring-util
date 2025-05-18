import pytest
from string.templatelib import Template
from tstring import safe_split

# Test splitting only static text with space separator
def test_static_split_space():
    tmpl = t"one two three"
    assert safe_split(tmpl, sep=" ") == ["one", "two", "three"]

# Test that interpolations are substituted before splitting
def test_interpolation_intact():
    name = 'Bob'
    tmpl = t"Hello {name} world"
    split_up = safe_split(tmpl, sep=" ")
    assert split_up == ["Hello", "", "Bob", "","world"]

# Test custom separator (comma) with interpolation
def test_custom_separator():
    fruit = 'mango'
    tmpl = t"apple,banana,{fruit},cherry"
    split_up = safe_split(tmpl, sep=",") 
    assert safe_split(tmpl, sep=",") == ["apple", "banana", "","mango", "","cherry"]

# Test that separators inside interpolated values are preserved
def test_preserve_sep_in_interpolation():
    no_good = 'a/b'
    tmpl = t"{no_good}"
    assert safe_split(tmpl, sep="/") == ["a/b"]

# Test consecutive separators produce empty parts
def test_consecutive_seps():
    tmpl = t"one,,two"
    assert safe_split(tmpl, sep=",") == ["one", "", "two"]


def test_default_sep_none():
    tmpl = t"  foo   bar baz  "
    # default sep=None splits on whitespace and strips empties
    assert safe_split(tmpl) == ["foo", "bar", "baz"]


def test_empty_template():
    tmpl = t""
    # empty template yields empty list
    assert safe_split(tmpl) == []


def test_empty_sep_string_raises():
    tmpl = t"abc"
    # splitting with empty string is invalid
    with pytest.raises(ValueError):
        safe_split(tmpl, sep="")


def test_multi_char_separator():
    tmpl = t"abXXcdXXef"
    assert safe_split(tmpl, sep="XX") == ["ab", "cd", "ef"]

