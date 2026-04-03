from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING

from ..embed_builders import build_embed_already_claimed_self


def _iter_options():
    yield (
        DateTime.now(TimeZone.utc) + RelativeDelta(years = 1, months = 1, days = 1, seconds = 10),
        Embed(
            'You already claimed your daily hearts for today~',
            'Come back in 1 year, 1 month, 1 day.',
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_embed_already_claimed_self(daily_can_claim_at):
    """
    Tests whether ``build_embed_already_claimed_self`` works as intended.
    
    Parameters
    ----------
    daily_can_claim_at : `DateTime`
        When the user can claim their daily.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_embed_already_claimed_self(daily_can_claim_at)
    vampytest.assert_instance(output, Embed)
    return output
