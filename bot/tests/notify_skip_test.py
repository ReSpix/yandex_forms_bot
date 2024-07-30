from unittest.mock import patch

from utils import is_notify_skip


def test_no_skip():
    with patch("utils.CONFIG", {"notify": True, "skip_weekends": False}), patch(
        "utils.is_weekend", return_value=False
    ):
        assert not is_notify_skip()


def test_no_skip_no_weekends():
    with patch("utils.CONFIG", {"notify": True, "skip_weekends": True}), patch(
        "utils.is_weekend", return_value=False
    ):
        assert not is_notify_skip()


def test_no_skip_weekends():
    with patch("utils.CONFIG", {"notify": True, "skip_weekends": False}), patch(
        "utils.is_weekend", return_value=True
    ):
        assert not is_notify_skip()


def test_global_skip():
    with patch("utils.CONFIG", {"notify": False, "skip_weekends": False}), patch(
        "utils.is_weekend", return_value=False
    ):
        assert is_notify_skip()


def test_weekend_skip():
    with patch("utils.CONFIG", {"notify": True, "skip_weekends": True}), patch(
        "utils.is_weekend", return_value=True
    ):
        assert is_notify_skip()


def test_both_skip():
    with patch("utils.CONFIG", {"notify": False, "skip_weekends": True}), patch(
        "utils.is_weekend", return_value=True
    ):
        assert is_notify_skip()
