import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_failure_embed_you_already_have_waifu


def _iter_options():
    guild_id = 202412280000
    
    waifu = User.precreate(202412280001, name = 'Koishi')
    waifu.guild_profiles[guild_id] = GuildProfile(nick = 'Koi')
    
    user = User.precreate(202412280002, name = 'Satori')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        waifu,
        user,
        0,
        Embed(
            'You already have a waifu',
            (
                'What would Koishi say if they would know about Satori?'
            ),
        )
    )
    
    yield (
        waifu,
        user,
        guild_id,
        Embed(
            'You already have a waifu',
            (
                'What would Koi say if they would know about Sato?'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_you_already_have_waifu(waifu, user, guild_id):
    """
    Tests whether ``build_failure_embed_you_already_have_waifu`` works as intended.
    
    Parameters
    ----------
    waifu : ``ClientUserBase``
        The current waifu.
    
    user : ``ClientUserBase``
        The user on the other end.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_you_already_have_waifu(waifu, user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
