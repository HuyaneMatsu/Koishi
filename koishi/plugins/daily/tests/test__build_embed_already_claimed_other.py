from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import Embed, User

from ....bot_utils.constants import COLOR__GAMBLING

from ..embed_builders import build_embed_already_claimed_other


def _iter_options():
    yield (
        DateTime.now(TimeZone.utc) + RelativeDelta(years = 1, months = 1, days = 1, seconds = 10),
        User.precreate(202412110000, name = 'Remilia'),
        0,
        Embed(
            'Remilia already claimed their daily hearts for today~',
            'Come back in 1 year, 1 month, 1 day.',
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_embed_already_claimed_other(daily_can_claim_at, target_user, guild_id):
    """
    Tests whether ``build_embed_already_claimed_other`` works as intended.
    
    Parameters
    ----------
    daily_can_claim_at : `DateTime`
        When the user can claim their daily.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        Respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_embed_already_claimed_other(daily_can_claim_at, target_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
