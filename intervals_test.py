from intervals import Interval, union, intersection, difference

import unittest


class TestIntervalOperations(unittest.TestCase):
    def test_union(self):
        self.assertEqual(union([Interval(1, 3), Interval(2, 4)]), [Interval(1, 4)])
        self.assertEqual(union([Interval(1, 2), Interval(3, 4)]), [Interval(1, 2), Interval(3, 4)])
        self.assertEqual(union([Interval(1, 4), Interval(2, 3)]), [Interval(1, 4)])
        self.assertEqual(union([]), [])

    def test_intersection(self):
        self.assertEqual(intersection([Interval(1, 3)], [Interval(2, 4)]), [Interval(2, 3)])
        self.assertEqual(intersection([Interval(1, 2)], [Interval(3, 4)]), [])
        self.assertEqual(intersection([], [Interval(1, 2)]), [])

    def test_difference(self):
        self.assertEqual(difference(Interval(1, 5), [Interval(2, 3)]), [Interval(1, 2), Interval(3, 5)])
        self.assertEqual(difference(Interval(1, 5), [Interval(6, 7)]), [Interval(1, 5)])
        self.assertEqual(difference(Interval(1, 5), [Interval(1, 5)]), [])


if __name__ == '__main__':
    unittest.main()