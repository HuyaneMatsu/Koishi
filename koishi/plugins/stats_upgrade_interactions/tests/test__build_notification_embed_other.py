import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_notification_embed_other


def _iter_options():
    user = User.precreate(202503150006, name = 'Sariel')
    guild_id = 202503150007
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Angel')
    
    yield (
        2,
        13,
        user,
        0,
        Embed(
            'Love is in the air',
            f'Sariel upgraded your bedroom skills to 13.',
        ),
    )
    
    yield (
        2,
        13,
        user,
        guild_id,
        Embed(
            'Love is in the air',
            f'Angel upgraded your bedroom skills to 13.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_notification_embed_other(
    stat_index, stat_value_after, source_user, guild_id
):
    """
    Tests whether ``build_notification_embed_other`` works as intended.
    
    Parameters
    ----------
    stat_index : `int`
        The index of the stat.
    
    stat_value_after : `int`
        The stats value after upgrade.
    
    source_user : `ClientUserBase``
        The user who bought the role.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_notification_embed_other(
        stat_index, stat_value_after, source_user, guild_id
    )
    vampytest.assert_instance(output, Embed)
    return output
