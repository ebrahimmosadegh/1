import unittest
import two

class TwoTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(two.add(3, 5), 8)
        self.assertEqual(two.add(-1, 3), 2)

    def test_substract(self):
        self.assertEqual(two.substract(2, 4), -2)
        self.assertEqual(two.substract(-2, -4), 2)

    def test_multiply(self):
        self.assertEqual(two.multiply(0, 2), 0)
        self.assertEqual(two.multiply(-2, -3), 6)
        self.assertEqual(two.multiply(-2, 4), -8)

    def test_division(self):
        self.assertEqual(two.division(0, 2), 0)
        self.assertEqual(two.multiply(3, 0), 0)
        self.assertEqual(two.division(9, 3), 3)
        self.assertRaises(ZeroDivisionError, two.division, 4, 0)


if __name__ == '__main__':
    unittest.main()