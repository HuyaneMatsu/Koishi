import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_failure_embed_they_already_have_mama


def _iter_options():
    guild_id = 202501030030
    
    mama = User.precreate(202501030031, name = 'Koishi')
    mama.guild_profiles[guild_id] = GuildProfile(nick = 'Koi')
    
    user = User.precreate(202501030032, name = 'Satori')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        mama,
        user,
        0,
        Embed(
            'They already have a mama',
            (
                f'Satori\'s mama is Koishi, '
                f'therefore you cannot adopt them.'
            ),
        )
    )
    
    yield (
        mama,
        user,
        guild_id,
        Embed(
            'They already have a mama',
            (
                f'Sato\'s mama is Koi, '
                f'therefore you cannot adopt them.'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_they_already_have_mama(mama, user, guild_id):
    """
    Tests whether ``build_failure_embed_they_already_have_mama`` works as intended.
    
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
    output = build_failure_embed_they_already_have_mama(mama, user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
