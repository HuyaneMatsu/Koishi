from datetime import datetime as DateTime

import vampytest
from hata import DATETIME_FORMAT_CODE, TIMESTAMP_STYLES, Embed, datetime_to_unix_time, format_unix_time

from .mocks import DateTimeMock, is_instance_mock

from ..constants import EMBED_COLOR
from ..helpers import build_format_time_embed


def _iter_options():
    date_time = DateTime(2016, 5, 14)
    unix_time = datetime_to_unix_time(date_time)
    
    format_0 = format_unix_time(unix_time, TIMESTAMP_STYLES.short_time)
    format_1 = format_unix_time(unix_time, TIMESTAMP_STYLES.long_time)
    format_2 = format_unix_time(unix_time, TIMESTAMP_STYLES.short_date)
    format_3 = format_unix_time(unix_time, TIMESTAMP_STYLES.long_date)
    format_4 = format_unix_time(unix_time, TIMESTAMP_STYLES.short_date_time)
    format_5 = format_unix_time(unix_time, TIMESTAMP_STYLES.long_date_time)
    format_6 = format_unix_time(unix_time, TIMESTAMP_STYLES.relative_time)
    
    yield (
        date_time,
        DateTime(2016, 5, 15),
        Embed(
            'Formatting time',
            f'UTC: {date_time:{DATETIME_FORMAT_CODE}} | 1 day ago',
            color = EMBED_COLOR,
        ).add_field(
            'Output',
            (
                f'`{format_0}` {format_0}\n'
                f'`{format_1}` {format_1}\n'
                f'`{format_2}` {format_2}\n'
                f'`{format_3}` {format_3}\n'
                f'`{format_4}` {format_4}\n'
                f'`{format_5}` {format_5}\n'
                f'`{format_6}` {format_6}'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_format_time_embed(input_date_time, current_date_time):
    """
    Tests whether ``build_format_time_embed`` works as intended.
    
    Parameters
    ----------
    input_date_time : `DateTime`
        Date time to test with.
    
    current_date_time : `DateTime`
        Current date time to test with.
    
    Returns
    -------
    output : ``Embed``
    """
    DateTimeMock.set_current(current_date_time)

    mocked = vampytest.mock_globals(
        build_format_time_embed, 4, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    output = mocked(input_date_time)
    vampytest.assert_instance(output, Embed)
    return output
