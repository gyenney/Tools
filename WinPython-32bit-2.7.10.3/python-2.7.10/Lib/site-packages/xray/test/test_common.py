from xray import Dataset

from . import TestCase


class TestDataset(TestCase):
    def test_pipe(self):
        df = Dataset({'A': ('x', [1, 2, 3])})
        f = lambda x, y: x ** y
        result = df.pipe(f, 2)
        expected = Dataset({'A': ('x', [1, 4, 9])})
        self.assertDatasetIdentical(result, expected)

        result = df.A.pipe(f, 2)
        self.assertDataArrayIdentical(result, expected.A)

    def test_pipe_tuple(self):
        df = Dataset({'A': ('x', [1, 2, 3])})
        f = lambda x, y: y
        result = df.pipe((f, 'y'), 0)
        self.assertDatasetIdentical(result, df)

        result = df.A.pipe((f, 'y'), 0)
        self.assertDataArrayIdentical(result, df.A)

    def test_pipe_tuple_error(self):
        df = Dataset({'A': ('x', [1, 2, 3])})
        f = lambda x, y: y
        with self.assertRaises(ValueError):
            df.pipe((f, 'y'), x=1, y=0)

        with self.assertRaises(ValueError):
            df.A.pipe((f, 'y'), x=1, y=0)
