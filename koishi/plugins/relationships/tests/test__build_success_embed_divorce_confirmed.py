import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_success_embed_divorce_confirmed


def _iter_options():
    guild_id = 202501050004
    
    target_user = User.precreate(202501050005, name = 'Satori')
    target_user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        target_user,
        0,
        0,
        0,
        Embed(
            'Divorcing confirmed',
            (
                'You have divorced Satori.'
            ),
        )
    )
    
    yield (
        target_user,
        0,
        0,
        guild_id,
        Embed(
            'Divorcing confirmed',
            (
                'You have divorced Sato.'
            ),
        )
    )
    
    yield (
        target_user,
        1000,
        0,
        0,
        Embed(
            'Divorcing confirmed',
            (
                f'You have divorced Satori.\n'
                f'\n'
                f'You received 1000 {EMOJI__HEART_CURRENCY} after investing much into the relationship.'
            ),
        )
    )
    
    yield (
        target_user,
        0,
        2000,
        0,
        Embed(
            'Divorcing confirmed',
            (
                f'You have divorced Satori.\n'
                f'\n'
                f'They received 2000 {EMOJI__HEART_CURRENCY} after investing much into the relationship.'
            ),
        )
    )
    
    yield (
        target_user,
        1000,
        2000,
        0,
        Embed(
            'Divorcing confirmed',
            (
                f'You have divorced Satori.\n'
                f'\n'
                f'You received 1000 {EMOJI__HEART_CURRENCY} after investing much into the relationship.\n'
                f'They received 2000 {EMOJI__HEART_CURRENCY} after investing much into the relationship.'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed_divorce_confirmed(target_user, source_received, target_received, guild_id):
    """
    Tests whether ``build_success_embed_divorce_confirmed`` works as intended.
    
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
    output : ``Embed``
    """
    output = build_success_embed_divorce_confirmed(target_user, source_received, target_received, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
