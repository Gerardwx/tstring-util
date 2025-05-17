import pytest
from tstring.cpath import path


def test_path():
    config = '/etc'
    p = path(t'{config}/systemd')
    q = path(t'{config}systemd')
    assert p == q # separators in strings ignored
    assert p.as_posix() ==  '/etc/systemd'

def test_badpath():
    with pytest.raises(ValueError) as exc:
        no_good = 'bob/carol'
        path(t'{no_good}')
    print(str(exc.value))
