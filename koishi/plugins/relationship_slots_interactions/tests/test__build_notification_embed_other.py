import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_notification_embed_other


def _iter_options():
    user_id = 202502150010
    guild_id = 202502150011
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver')
    
    yield (
        3,
        user,
        0,
        Embed(
            'Love is in the air',
            f'You have been gifted your 3rd relationship slot by Keine.'
        ),
    )
    
    yield (
        3,
        user,
        guild_id,
        Embed(
            'Love is in the air',
            f'You have been gifted your 3rd relationship slot by Caver.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_notification_embed_other(new_relationship_slot_count, source_user, guild_id):
    """
    Tests whether ``build_notification_embed_other`` works as intended.
    
    Parameters
    ----------
    new_relationship_slot_count : `int`
        The new relationship slot count.
    
    source_user : `ClientUserBase``
        The source user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_notification_embed_other(new_relationship_slot_count, source_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
