import vampytest

from datetime import datetime as DateTime, timezone as TimeZone

from ..utils import get_quest_board_resets_at


def test__get_quest_board_resets_at():
    """
    Tests whether ``get_quest_board_resets_at`` works as intended.
    """
    now = DateTime.now(TimeZone.utc)
    output = get_quest_board_resets_at()
    vampytest.assert_instance(output, DateTime)
    
    vampytest.assert_eq(output.hour, 0)
    vampytest.assert_eq(output.minute, 0)
    vampytest.assert_eq(output.second, 0)
    vampytest.assert_eq(output.microsecond, 0)
    vampytest.assert_true(output > now)
