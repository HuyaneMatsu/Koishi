import vampytest
from hata import User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..content_building import produce_break_up_notification_description


def _iter_options():
    source_user = User.precreate(202501050009, name = 'Satori')
    
    yield (
        source_user,
        0,
        0,
        (
            'Satori broke up with you.'
        ),
    )
    
    yield (
        source_user,
        1000,
        0,
        (
            f'Satori broke up with you.\n'
            f'\n'
            f'You received 1000 {EMOJI__HEART_CURRENCY} after investing much into the relationship.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_break_up_notification_description(source_user, target_received, guild_id):
    """
    Tests whether ``produce_break_up_notification_description`` works as intended.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who divorced.
    
    target_received : `int`
        The amount of balance the target user received.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_break_up_notification_description(source_user, target_received, guild_id)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
