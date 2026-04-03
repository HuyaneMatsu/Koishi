import vampytest
from hata import GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..content_building import produce_break_up_success_description


def _iter_options():
    guild_id = 202501050004
    
    target_user = User.precreate(202501050005, name = 'Satori')
    target_user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        target_user,
        0,
        0,
        0,
        (
            'You have broke up with Satori.'
        ),
    )
    
    yield (
        target_user,
        -1000,
        -1000,
        0,
        (
            'You have broke up with Satori.'
        ),
    )
    
    yield (
        target_user,
        0,
        0,
        guild_id,
        (
            'You have broke up with Sato.'
        ),
    )
    
    yield (
        target_user,
        1000,
        0,
        0,
        (
            f'You have broke up with Satori.\n'
            f'\n'
            f'You received 1000 {EMOJI__HEART_CURRENCY} after investing much into the relationship.'
        ),
    )
    
    yield (
        target_user,
        0,
        2000,
        0,
        (
            f'You have broke up with Satori.\n'
            f'\n'
            f'They received 2000 {EMOJI__HEART_CURRENCY} after investing much into the relationship.'
        ),
    )
    
    yield (
        target_user,
        1000,
        2000,
        0,
        (
            f'You have broke up with Satori.\n'
            f'\n'
            f'You received 1000 {EMOJI__HEART_CURRENCY} after investing much into the relationship.\n'
            f'They received 2000 {EMOJI__HEART_CURRENCY} after investing much into the relationship.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_break_up_success_description(target_user, source_received, target_received, guild_id):
    """
    Tests whether ``produce_break_up_success_description`` works as intended.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The user who is the target of the proposal.
    
    source_received : `int`
        The amount of balance the source user received.
    
    target_received : `int`
        The amount of balance the target user received.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_break_up_success_description(target_user, source_received, target_received, guild_id)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
