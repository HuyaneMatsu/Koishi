import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_notification_embed_other


def _iter_options():
    user_id = 202502150020
    guild_id = 202502150021
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver')
    
    yield (
        3,
        user,
        0,
        Embed(
            'Love is in the air',
            (
                f'Keine sent out their hired ninjas to locate and burn your 3rd divorce papers.\n'
                f'The task was completed splendid; now you cannot hide and seek with them.'
            ),
        ),
    )
    
    yield (
        3,
        user,
        guild_id,
        Embed(
            'Love is in the air',
            (
                f'Caver sent out their hired ninjas to locate and burn your 3rd divorce papers.\n'
                f'The task was completed splendid; now you cannot hide and seek with them.'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_notification_embed_other(relationship_divorce_count, source_user, guild_id):
    """
    Tests whether ``build_notification_embed_other`` works as intended.
    
    Parameters
    ----------
    relationship_divorce_count : `int`
        The current relationship divorce count.
    
    source_user : `ClientUserBase``
        The source user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_notification_embed_other(relationship_divorce_count, source_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
