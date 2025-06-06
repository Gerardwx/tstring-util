#!/usr/bin/env python3
from tstring import render

def double(value):
    print(f"twice {value} is {2*value}")

def test_lazy():
    number = 1
    flavor = 'spicy'
    embedx = t'Call function {double:!fn} {number} {flavor}'
    number = 2


    r = render(embedx)
    assert r ==  "Call function twice 2 is 4 spicy"
    print(r)
