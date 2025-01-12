import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_notification_embed_divorced


def _iter_options():
    guild_id = 202501050008
    
    source_user = User.precreate(202501050009, name = 'Satori')
    source_user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        source_user,
        0,
        0,
        Embed(
            'You have been divorced',
            (
                'Satori divorced you.'
            ),
        )
    )
    
    yield (
        source_user,
        0,
        guild_id,
        Embed(
            'You have been divorced',
            (
                'Sato divorced you.'
            ),
        )
    )
    
    yield (
        source_user,
        1000,
        0,
        Embed(
            'You have been divorced',
            (
                f'Satori divorced you.\n'
                f'\n'
                f'You received 1000 {EMOJI__HEART_CURRENCY} after investing much into the relationship.'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_notification_embed_divorced(source_user, target_received, guild_id):
    """
    Tests whether ``build_notification_embed_divorced`` works as intended.
    
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
    output : ``Embed``
    """
    output = build_notification_embed_divorced(source_user, target_received, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
