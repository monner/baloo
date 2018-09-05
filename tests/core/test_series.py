import numpy as np
import pytest

from baloo import Series, RangeIndex, Index
from baloo.weld import create_placeholder_weld_object
from .indexes.utils import assert_indexes_equal


def assert_series_equal(actual, expected):
    actual = actual.evaluate()
    expected = expected.evaluate()

    np.testing.assert_array_equal(actual.values, expected.values)
    assert actual.dtype == expected.dtype
    # might seem redundant but testing the __len__ function
    assert len(actual) == len(expected)
    assert actual.name == expected.name
    assert_indexes_equal(actual.index, expected.index)


class TestSeries(object):
    def test_evaluate(self):
        data = np.array([1, 2, 3], dtype=np.int64)
        actual = Series(data)
        expected = Series(data, RangeIndex(3))

        assert_series_equal(actual, expected)

    def test_len_raw(self):
        data = np.array([1, 2, 3], dtype=np.int64)
        ind = Series(data)

        actual = len(ind)
        expected = 3

        assert actual == expected

    def test_len_lazy(self):
        data = np.array([1, 2, 3], dtype=np.int64)
        weld_obj = create_placeholder_weld_object(data)
        ind = Series(weld_obj, dtype=np.dtype(np.int64))

        actual = len(ind)
        expected = 3

        assert actual == expected

    @pytest.mark.parametrize('comparison, expected', [
        ('<', Series(np.array([True, False, False]), Index(np.array([0, 1, 2])), np.dtype(np.bool))),
        ('<=', Series(np.array([True, True, False]), Index(np.array([0, 1, 2])), np.dtype(np.bool))),
        ('==', Series(np.array([False, True, False]), Index(np.array([0, 1, 2])), np.dtype(np.bool))),
        ('!=', Series(np.array([True, False, True]), Index(np.array([0, 1, 2])), np.dtype(np.bool))),
        ('>=', Series(np.array([False, True, True]), Index(np.array([0, 1, 2])), np.dtype(np.bool))),
        ('>', Series(np.array([False, False, True]), Index(np.array([0, 1, 2])), np.dtype(np.bool))),
    ])
    def test_comparison(self, comparison, expected):
        sr = Series(np.array([1, 2, 3]))

        actual = eval('sr {} 2'.format(comparison))

        assert_series_equal(actual, expected)

    def test_filter(self):
        sr = Series(np.array([1, 2, 3]))

        actual = sr[sr != 2]
        expected = Series(np.array([1, 3]), Index(np.array([0, 2])), np.dtype(np.int64))

        assert_series_equal(actual, expected)

    def test_filter_combined(self):
        sr = Series(np.arange(4))

        actual = sr[(sr != 0) & (sr != 3)]
        expected = Series(np.array([1, 2]), Index(np.array([1, 2])), np.dtype(np.int64))

        assert_series_equal(actual, expected)

    def test_slice(self):
        sr = Series(np.array([1, 2, 3, 4, 5], dtype=np.float32))

        actual = sr[1:3]
        expected = Series(np.array([2, 3]), Index(np.array([1, 2])), np.dtype(np.float32))

        assert_series_equal(actual, expected)

    @pytest.mark.parametrize('operation, expected', [
        ('&', Series(np.array([True, False, False, False]), Index(np.arange(4)), np.dtype(np.bool))),
        ('|', Series(np.array([True, True, True, False]), Index(np.arange(4)), np.dtype(np.bool)))
    ])
    def test_bool_operations(self, operation, expected):
        sr1 = Series(np.array([True, True, False, False]))
        sr2 = Series(np.array([True, False, True, False]))

        actual = eval('sr1 {} sr2'.format(operation))

        assert_series_equal(actual, expected)

    def test_invert(self):
        sr = Series(np.array([True, False, True, False]))

        actual = ~sr
        expected = Series(np.array([False, True, False, True]), Index(np.arange(4)), np.dtype(np.bool))

        assert_series_equal(actual, expected)

    def test_head(self):
        sr = Series(np.array([1, 2, 3, 4, 5], dtype=np.float32))

        actual = sr.head(2)
        expected = Series(np.array([1, 2]), RangeIndex(2), np.dtype(np.float32))

        assert_series_equal(actual, expected)

    def test_tail(self):
        sr = Series(np.array([1, 2, 3, 4, 5], dtype=np.float32))

        actual = sr.tail(2)
        expected = Series(np.array([4, 5]), Index(np.array([3, 4])), np.dtype(np.float32))

        assert_series_equal(actual, expected)

    def test_iloc_int(self):
        sr = Series(np.array([1, 2, 3, 4, 5], dtype=np.float32))

        actual = sr.iloc[2].evaluate()
        expected = 3

        assert actual == expected

    def test_iloc_slice(self):
        sr = Series(np.array([1, 2, 3, 4, 5], dtype=np.float32))

        actual = sr.iloc[1:3]
        expected = Series(np.array([2, 3]), Index(np.array([1, 2])), np.dtype(np.float32))

        assert_series_equal(actual, expected)
