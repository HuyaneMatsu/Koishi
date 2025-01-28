import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_failure_embed_you_already_have_mama


def _iter_options():
    guild_id = 202501030020
    
    mama = User.precreate(202501030021, name = 'Koishi')
    mama.guild_profiles[guild_id] = GuildProfile(nick = 'Koi')
    
    user = User.precreate(202501030022, name = 'Satori')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        mama,
        user,
        0,
        Embed(
            'You already have a mama',
            (
                f'Koishi would send you to your dark room, so you don\'t ever think about '
                f'Satori.'
            ),
        )
    )
    
    yield (
        mama,
        user,
        guild_id,
        Embed(
            'You already have a mama',
            (
                f'Koi would send you to your dark room, so you don\'t ever think about '
                f'Sato.'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_you_already_have_mama(mama, user, guild_id):
    """
    Tests whether ``build_failure_embed_you_already_have_mama`` works as intended.
    
    Parameters
    ----------
    mama : ``ClientUserBase``
        The current mama.
    
    user : ``ClientUserBase``
        The user who has mama.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_you_already_have_mama(mama, user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
