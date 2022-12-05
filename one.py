# module
"""
>>> add(5, 6)
11
>>> substract(7, 6)
1
>>> multiply(4, 5)
20
"""

def add(x, y):
    """
    >>> add(7,6)
    13
    >>> add(4, -1)
    3
    >>> add(0, 5)
    5
    """
    return x + y

def substract(x, y):
    """
    >>> substract(5 , 4)
    1
    >>> substract(6, 9)
    -3
    """
    return x - y

def multiply(x, y):
    """
    >>> multiply(5, 6)
    30
    >>> multiply(5, 'b')
    'bbbbb'
    """
    return x * y