

def add(a, b):
    return a + b


def test_add():
    assert add(5, 10) == 15, 'Something wrong with add'
    assert add(10, 5) == 15, 'Something wrong with add'
    assert add('a', 'b') == 'ab', 'Something wrong with add'


test_add()
