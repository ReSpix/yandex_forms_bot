import pytest
from utils import is_weekend
from datetime import datetime


@pytest.mark.parametrize('date', [
    datetime(2024, 7, 15),
    datetime(2024, 7, 16),
    datetime(2024, 7, 17),
    datetime(2024, 7, 18),
    datetime(2024, 7, 19)
])
def test_not_weekend(date):
    assert not is_weekend(date)


@pytest.mark.parametrize('date', [
    datetime(2024, 7, 20),
    datetime(2024, 7, 21)
])
def test_is_weekend(date):
    assert is_weekend(date)
