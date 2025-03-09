import vampytest

from ..love_option import LoveOption
from ..love_options import LOVE_OPTIONS


def test__LOVE_OPTIONS():
    """
    Tests `LOVE_OPTIONS`.
    """
    vampytest.assert_eq(len(LOVE_OPTIONS), 101)
    for value in LOVE_OPTIONS:
        vampytest.assert_instance(value, LoveOption)
