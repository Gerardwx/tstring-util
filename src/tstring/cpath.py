import os
from pathlib import Path
from typing import Tuple

# noinspection PyUnresolvedReferences
from string.templatelib import Interpolation, Template
from tstring import iformat
# define invalid characters (path separator(s) and NUL)
SEPARATORS = {os.sep}
if os.altsep:
    SEPARATORS.add(os.altsep)
STRIP = ''.join(SEPARATORS)
NUL = "\x00"

def _check(value:str)->Tuple[bool, None | str]:
    """check for NUL and separators in value"""
    if NUL in value:
        return True,False
    for sep in SEPARATORS:
        if sep in value:
            return False, sep
    return False, None


def path(tmpl: Template) -> Path:
    """
    Build a Path from a PEP 750 t-string Template by substituting each
    interpolation. Raises ValueError if any interpolation contains
    invalid filename characters (path separators or NUL).
    """
    parts: list[str] = []


    for p, item in enumerate(tmpl):
        match item:
            case str() as s:
                clean = s.strip(STRIP)
                parts.append(clean)

            case Interpolation(arg, name, conversion, format_spec) as inter:
                value = iformat(inter)

                # noinspection PyUnboundLocalVariable
                is_null, sep = _check(value)
                if is_null:
                    raise ValueError(f"Invalid character {NUL!r} in interpolation {name!r}")
                if sep is not None:
                    if p  == 0 and len(value) > 1:  # allow separator at beginning to make absolute
                        _, sep = _check(value[1:])
                if sep is not None:
                    raise ValueError(f"Invalid character {sep!r} in interpolation {name!r}")


                parts.append(value)

    # assemble the final path
    return Path().joinpath(*parts)
