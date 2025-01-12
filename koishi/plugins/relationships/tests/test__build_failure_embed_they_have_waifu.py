import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_failure_embed_they_already_have_waifu


def _iter_options():
    guild_id = 202412280010
    
    waifu = User.precreate(202412280011, name = 'Koishi')
    waifu.guild_profiles[guild_id] = GuildProfile(nick = 'Koi')
    
    user = User.precreate(202412280012, name = 'Satori')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        waifu,
        user,
        0,
        Embed(
            'They already have a waifu',
            (
                f'Satori is already married to Koishi!!'
            ),
        )
    )
    
    yield (
        waifu,
        user,
        guild_id,
        Embed(
            'They already have a waifu',
            (
                f'Sato is already married to Koi!!'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_they_already_have_waifu(waifu, user, guild_id):
    """
    Tests whether ``build_failure_embed_they_already_have_waifu`` works as intended.
    
    Parameters
    ----------
    waifu : ``ClientUserBase``
        The current waifu.
    
    user : ``ClientUserBase``
        The user with waifu.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_they_already_have_waifu(waifu, user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
