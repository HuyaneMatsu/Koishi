import vampytest

from datetime import datetime as DateTime, timezone as TimeZone

from ....bot_utils.time import unix_time_seconds_get

from ..utils import get_quest_board_resets_at


def test__get_quest_board_resets_at():
    now = unix_time_seconds_get()
    output = get_quest_board_resets_at()
    
    vampytest.assert_instance(output, int)
    vampytest.assert_true(output > now)
    
    output_date_time = DateTime.fromtimestamp(output, TimeZone.utc)
    vampytest.assert_eq(output_date_time.hour, 0)
    vampytest.assert_eq(output_date_time.minute, 0)
    vampytest.assert_eq(output_date_time.second, 0)
    vampytest.assert_eq(output_date_time.microsecond, 0)
