from itertools import count
import traceback
from unittest import TestCase
import more

class TakeTest(TestCase):
    def test_simple_take(self):
        t = more.take(range(10),5)
        self.assertEqual(t, [0,1,2,3,4])

    def test_null_take(self):
        t = more.take(range(10),0)
        self.assertEqual(t,[])

    def test_negative_take(self):
        self.assertRaises(ValueError, lambda: more.take(-3, range(10)))

    def test_take_too_much(self):
        t = more.take(range(5), 10)
        self.assertEqual(t, [0,1,2,3,4])


class ChunkedTest(TestCase):
    def test_even(self):
        self.assertEqual(
            list(more.chunked('ABCDEF',3)), [['A','B','C'], ['D','E','F']]
        )

    def test_odd(self):
        self.assertEqual(
            list(more.chunked('ABCDE',3)), [['A','B','C'],['D','E']]
        )

    def test_none(self):
        self.assertEqual(
            list(more.chunked('ABCDE', None)),[['A','B','C','D','E']]
        )

    def test_strict_false(self):
        self.assertEqual(
            list(more.chunked('ABCDE', 3, strict=False)),
            [['A','B','C'], ['D', 'E']]
        )

    def test_strict_true(self):
        def f():
            return list(more.chunked('ABCDE',3, strict=True))
        self.assertRaisesRegex(ValueError, 'iterator is not divisible by n', f)
        self.assertEqual(
            list(more.chunked('ABCDEF', 3, strict=True)),
            [['A','B','C'],['D','E','F']]
        )

    def test_strict_true_size_none(self):
        def f():
            return list(more.chunked('ABCDE', None, strict=True))
        self.assertRaisesRegex(
            ValueError, 'n cant be None when strict is True', f
        )


class FirstTest(TestCase):
    def test_many(self):
        self.assertEqual(more.first(x for x in range(4)), 0)

    def test_one(self):
        self.assertEqual(more.first([3]), 3)
    
    def test_default(self):
        self.assertEqual(more.first([], 'boo'), 'boo')

    def test_empty_stop_iteration(self):
        try:
            more.first([])
        except ValueError:
            formatted_exec = traceback.format_exc()
            self.assertIn('StopIteration', formatted_exec)
            self.assertIn('The above exception was the direct cause', formatted_exec)
        else:
            self.fail()

class LastTest(TestCase):
    def test_basic(self):
        cases = [
            (range(4), 3),
            (iter(range(4)), 3),
            (range(1), 0),
            (iter(range(1)), 0),
            ({n: str(n) for n in range(5)}, 4)
        ]
        for iterable, expected in cases:
            with self.subTest(iterable=iterable):
                self.assertEqual(more.last(iterable), expected)

    def test_default(self):
        for iterable, default, expected in [
            (range(1), None, 0),
            ([], None, None),
            ({}, None, None),
            (iter([]), None, None)
        ]:
            with self.subTest(args=(iterable, default)):
                self.assertEqual(more.last(iterable, default=default), expected)
    
    def test_empty(self):
        for iterable in ([], iter(range(0))):
            with self.subTest(iterable=iterable):
                with self.assertRaises(ValueError):
                    more.last(iterable)

class NthOrLastTests(TestCase):
    def test_basic(self):
        self.assertEqual(more.nth_or_last(range(3), 1), 1)
        self.assertEqual(more.nth_or_last(range(3), 3), 2) # [0, 1, 2]

    def test_default_value(self):
        default = 42
        self.assertEqual(more.nth_or_last(range(0), 2, default), default)

    def test_empty_iterable_no_default(self):
        self.assertRaises(ValueError, lambda:more.nth_or_last(range(0), 0))

class OneTest(TestCase):
    def test_basic(self):
        it = ['item']
        self.assertEqual(more.one(it), 'item')

    def test_too_short(self):
        it = []
        for too_short, exc_type in [
            (None, ValueError),
            (IndexError, IndexError)
        ]:
            with self.subTest(too_short=too_short):
                try:
                    more.one(it, too_short=too_short)
                except exc_type:
                    formatted_exc = traceback.format_exc()
                    self.assertIn('StopIteration', formatted_exc)
                    self.assertIn('The above exception was the direct cause', formatted_exc)
                else:
                    self.fail()

                def test_too_long(self):
                    it = count()
                    self.assertRaises(ValueError, lambda: more.one(it))
                    self.assertEqual(next(it), 2)
                    self.assertRaises(
                        OverflowError, lambda: more.one(it, too_long=OverflowError)
                    )

                def test_too_long_default_message(self):
                    it = count()
                    self.assertRaisesRegex(
                        ValueError,
                        'Expected exactly one item in iterable, but got 1, 1, and perhaps more.',
                        lambda:more.one(it)
                    )

class TestInterleave(TestCase):
    def test_even(self):
        actual = list(more.interleave([1,4,7], [2,5,8], [3,6,9]))
        expected = [1,2,3,4,5,6,7,8,9]
        self.assertEqual(actual, expected)

    def test_short(self):
        actual = list(more.interleave([1,4], [2,5,7], [3,6,8]))
        expected = [1,2,3,4,5,6]
        self.assertEqual(actual, expected)

    def test_mixed_types(self):
        it_list = ['a', 'b', 'c', 'd']
        it_str = '123456'
        it_inf = count()
        actual = list(more.interleave(it_list, it_str, it_inf))
        expected = ['a', '1', 0, 'b', '2', 1, 'c', '3', 2, 'd', '4', 3]
        self.assertEqual(actual, expected)