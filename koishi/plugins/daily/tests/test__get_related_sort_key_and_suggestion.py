from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import User

from ..related_completion import get_related_sort_key_and_suggestion


def _iter_options():
    user_id = 202412110030_000000
    user = User.precreate(user_id, name = 'remilia')
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        user,
        0,
        now,
        DateTime(2016, 5, 13, tzinfo = TimeZone.utc),
        (
            now,
            ('remilia', str(user_id)),
        ),
    )
    
    yield (
        user,
        0,
        now,
        DateTime(2017, 5, 14, tzinfo = TimeZone.utc),
        (
            DateTime(2017, 5, 14, tzinfo = TimeZone.utc),
            ('remilia (1 year)', str(user_id))
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_related_sort_key_and_suggestion(related_user, guild_id, now, daily_can_claim_at):
    """
    Tests whether ``get_related_sort_key_and_suggestion`` works as intended.
    
    Parameters
    ----------
    related_user : ``ClientUserBase``
        The related user.
    
    guild_id : `int`
        Respective guild's identifier to extend naming for.
    
    now : ``DateTime`
        Current time.
    
    daily_can_claim_at : `DateTime`
        When the user can claim their daily.
    
    Returns
    -------
    output : `(DateTime, (str, str))`
    """
    output = get_related_sort_key_and_suggestion(related_user, guild_id, now, daily_can_claim_at)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_instance(output[0], DateTime)
    vampytest.assert_instance(output[1], tuple)
    vampytest.assert_eq(len(output[1]), 2)
    vampytest.assert_instance(output[1][0], str)
    vampytest.assert_instance(output[1][1], str)
    return output
