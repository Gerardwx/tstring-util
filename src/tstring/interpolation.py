from string.templatelib import Interpolation
from typing import Literal


# dervied from https://raw.githubusercontent.com/davepeck/pep750-examples/refs/heads/main/pep/fstring.py
def iformat(interp: Interpolation) -> str:
    """Format an interpolation like an f-string: apply conversion then format specifier."""
    value = interp.value
    conv = interp.conversion

    # apply conversion (ascii, repr, str) if specified
    if conv == "a":
        value = ascii(value)
    elif conv == "r":
        value = repr(value)
    elif conv == "s":
        value = str(value)
    # None or other means leave value as is

    # apply the format specifier
    return format(value, interp.format_spec)

