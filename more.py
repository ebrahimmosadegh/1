from collections import deque
from functools import partial
from itertools import islice, chain, repeat
from typing import Sequence

l = [1,2,3,4,5,6] # [[1,2,3],[4,5,6],[7]]
s = ['a', 'b', 'c', 'd']
e = []
_marker = object()

def take(iterable, n):
    return list(islice(iterable, n))

def raise_(exception, *args):
    raise exception(*args)

def chunked(iterable, n, strict=False):
    iterator = iter(partial(take, iter(iterable), n), [])
    if strict:
        if n is None:
            raise ValueError('n cant be None when strict is True')
        def ret():
            for chunk in iterator:
                if len(chunk) != n:
                    raise ValueError('iterator is not divisible by n')
                yield chunk
        return iter(ret())
    else:
        return iterator

# print(list(chunked(l, 3, strict=True)))

def first(iterable, default=_marker):
    try:
        return next(iter(iterable))
    except StopIteration as e:
        if default is _marker:
            raise ValueError('first() was called on an empty iterable, and no '
            'default value was provided.') from e
        return default
    
# print(first(e))

def last(iterable, default=_marker):
    try:
        if isinstance(iterable,Sequence):
            return iterable[-1]
        elif hasattr(iterable, '__reversed__'):
            return next(reversed(iterable))
        else:
            return deque(iterable, maxlen=1)[-1]
    except (IndexError, TypeError, StopIteration):
        if default is _marker:
            raise ValueError(
                'last() was called on an empty iterable, and no default was provided.'
            )
        return default

# print(last(l))

def nth_or_last(iterable, n, default=_marker):
    return last(islice(iterable, n+1), default=default)

# print(nth_or_last(l, 4))


def one(iterable, too_short=None, too_long=None):
    it = iter(iterable)
    try:
        first_value = next(it)
    except StopIteration as e:
        raise(
            too_short or ValueError('too few items in iterable (expected 1')
        ) from e
    
    try:
        second_value = next(it)
    except StopIteration:
        pass
    else:
        msg =(
            'Expected exactly one item in iterable, but got {!r}, {!r},'
            'and perhaps more.'.format(first_value, second_value)
        )
        raise too_long or ValueError(msg)
    return first_value


def interleave(*iterable):
    return chain.from_iterable(zip(*iterable))

# print(list(interleave(l, s))) # [1, 'a', 2, 'b', 3, 'c', 4, 'd']

def repeat_each(iterable, n=2):
    return chain.from_iterable(map(repeat, iterable, repeat(n)))

# print(list(repeat_each(s))) # ['a', 'a', 'b', 'b', 'c', 'c', 'd', 'd']

def strictly_n(iterable, n, too_short=None, too_long=None):
    if too_short is None:
        too_short = lambda item_count: raise_(
            ValueError,
            f'Too few items in iterable (got {item_count})'
        )
    if too_long is None:
        too_long = lambda item_count: raise_(
            ValueError,
            f'Too many items in iterable (got at least {item_count})'
        )
    
    it = iter(iterable)
    for i in range(n):
        try:
            item = next(it)
        except StopIteration:
            too_short(i)
            return
        else:
            yield item
    
    try:
        next(it)
    except StopIteration:
        pass
    else:
        too_long(n+1)

# print(list(strictly_n(s, 4))) # ['a', 'b', 'c', 'd']

def only(iterable, default=None, too_long=None):
    it = iter(iterable)
    first_value = next(it, default)

    try:
        second_value = next(it)
    except StopIteration:
        pass
    else:
        msg = (
            'Expected exactly one item in iterable, but got {}, {}, '
            'and perhaps more.'.format(first_value, second_value)
        )
        raise too_long or ValueError(msg)
    return first_value
