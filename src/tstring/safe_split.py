# noinspection PyUnresolvedReferences
from string.templatelib import Interpolation, Template
from tstring import iformat

def safe_split(tmpl: Template,sep:str|None=None) -> list[str] :
    """split tmpl by splitting strings while keeping interpolations intact"""
    parts: list[str] = []
    for item in tmpl: 
        if isinstance(item,str):
            s_split = item.split(sep)
            parts.extend(s_split)
        elif isinstance(item,Interpolation):
            parts.append(iformat(item))
    return parts
