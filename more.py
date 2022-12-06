from functools import partial
from itertools import islice

l = [1,2,3,4,5,6] # [[1,2,3],[4,5,6],[7]]

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

print(list(chunked(l, 3, strict=True)))