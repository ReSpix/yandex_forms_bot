from utils import is_weekend
from datetime import datetime


def test_weekend1():
    date = datetime(2024, 7, 15)
    assert not is_weekend(date)


def test_weekend2():
    date = datetime(2024, 7, 16)
    assert not is_weekend(date)


def test_weekend3():
    date = datetime(2024, 7, 17)
    assert not is_weekend(date)


def test_weekend4():
    date = datetime(2024, 7, 18)
    assert not is_weekend(date)


def test_weekend5():
    date = datetime(2024, 7, 19)
    assert not is_weekend(date)


def test_weekend6():
    date = datetime(2024, 7, 20)
    assert is_weekend(date)


def test_weekend7():
    date = datetime(2024, 7, 21)
    assert is_weekend(date)
