from functools import partial
from itertools import islice

l = [1,2,3,4,5,6] # [[1,2,3],[4,5,6],[7]]
e = []
_marker = object()

def take(iterable, n):
    return list(islice(iterable, n))

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