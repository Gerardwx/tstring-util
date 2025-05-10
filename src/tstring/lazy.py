import sys
import io
import inspect
from string.templatelib import Template

def render(template: Template, ctx: dict[str, object] | None = None) -> str:
    """
    Render a PEP 750 t-string, only treating interpolations whose
    format_spec == "!fn" as calls.  Any callable marked !fn will
    consume as many following interpolations as its positional args,
    be invoked, and its stdout captured inline.  All other
    interpolations (including those consumed as args) and static text
    are rendered in order.
    """
    ctx = ctx or globals()
    strings = template.strings
    interps = template.interpolations

    out: list[str] = []
    i = 0
    while i < len(interps):
        # 1) static text before this interpolation
        out.append(strings[i])

        interp = interps[i]
        expr = interp.expression
        spec = interp.format_spec

        if spec == "!fn":
            # deferred-eval the callable
            fn = eval(expr, ctx)
            if not callable(fn):
                raise ValueError(f"{expr!r} is not callable")

            # inspect how many fixed args, and if *args is present
            sig = inspect.signature(fn)
            params = sig.parameters.values()
            pos_count = sum(
                1 for p in params
                if p.kind in (inspect.Parameter.POSITIONAL_ONLY,
                              inspect.Parameter.POSITIONAL_OR_KEYWORD)
            )
            has_varargs = any(
                p.kind is inspect.Parameter.VAR_POSITIONAL
                for p in params
            )

            # decide how many following interps to consume
            available = len(interps) - (i + 1)
            take = available if has_varargs else min(pos_count, available)

            # eval each of the next `take` expressions
            args = [
                eval(interps[i + j].expression, ctx)
                for j in range(1, take + 1)
            ]

            # capture stdout of the call
            buf = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = buf
            try:
                fn(*args)
            finally:
                sys.stdout = old_stdout

            out.append(buf.getvalue().rstrip("\n"))
            i += 1 + take
        else:
            # normal interpolation: deferred eval and str()
            val = eval(expr, ctx)
            out.append(str(val))
            i += 1

    # trailing static text
    out.append(strings[-1])

    result = "".join(out)
    return result

def hello(name):
    print(f"hello {name}")

who = 'bob'
flavor = 'spicy'
embedx = t'Call function {hello:!fn} {who} {flavor}'
who = 'jane'

r = render(embedx)
print(r)
# → Call function hello jane spicy
embedn = t'Call function {hello} {who} {flavor}'
r = render(embedn)
print(r)

