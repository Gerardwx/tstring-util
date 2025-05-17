#!/usr/bin/env python3
from pathlib import Path
from tstring import render

def hello(name):
    print(f"hello {name}")

def test_lazy():
    who = 'bob'
    flavor = 'spicy'
    embedx = t'Call function {hello:!fn} {who} {flavor}'
    who = 'jane'


    r = render(embedx)
    assert r ==  "Call function hello jane spicy"
    print(r)




if __name__ == "__main__":
    test_lazy()
