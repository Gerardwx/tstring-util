# tstring-util
Utlities for Python 3.14 t-string.

Python 3.14 supports creating objects of type *string.templatelib.Template* by prefixing with a "t". 


## lazy rendering
**render(string.templatelib.Template)->str**

Provides ability to write t-string with function calls with deferred evaluation.
Any callable marked !fn will consume as many following interpolations as its positional args,
be invoked, and its stdout captured inline. Everything else is rendered in order. 

### Example
```
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
```

