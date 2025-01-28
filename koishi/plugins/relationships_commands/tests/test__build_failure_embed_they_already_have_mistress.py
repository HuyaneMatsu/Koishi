import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_failure_embed_they_already_have_mistress


def _iter_options():
    guild_id = 202412290000
    
    mistress = User.precreate(202412290001, name = 'Koishi')
    mistress.guild_profiles[guild_id] = GuildProfile(nick = 'Koi')
    
    user = User.precreate(202412290002, name = 'Satori')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        mistress,
        user,
        0,
        Embed(
            'They already have a mistress',
            (
                f'Satori\'s mistress is Koishi, '
                f'therefore they cannot serve you.'
            ),
        )
    )
    
    yield (
        mistress,
        user,
        guild_id,
        Embed(
            'They already have a mistress',
            (
                f'Sato\'s mistress is Koi, '
                f'therefore they cannot serve you.'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_they_already_have_mistress(mistress, user, guild_id):
    """
    Tests whether ``build_failure_embed_they_already_have_mistress`` works as intended.
    
    Parameters
    ----------
    mistress : ``ClientUserBase``
        The current mistress.
    
    user : ``ClientUserBase``
        The user who has mistress.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_they_already_have_mistress(mistress, user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
