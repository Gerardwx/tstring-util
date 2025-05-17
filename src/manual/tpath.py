#!/usr/bin/env python3
from tstring import path

if __name__ == "__main__":
    p = path(t'/etc')
    print(p.as_posix())
