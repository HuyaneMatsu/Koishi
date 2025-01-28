import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_failure_embed_you_already_have_mistress


def _iter_options():
    guild_id = 202501010000
    
    mistress = User.precreate(202501010001, name = 'Koishi')
    mistress.guild_profiles[guild_id] = GuildProfile(nick = 'Koi')
    
    user = User.precreate(202501010002, name = 'Satori')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        mistress,
        user,
        0,
        Embed(
            'You already have a mistress',
            (
                f'Koishi would surely not be pleased if they would know about '
                f'Satori.'
            ),
        )
    )
    
    yield (
        mistress,
        user,
        guild_id,
        Embed(
            'You already have a mistress',
            (
                f'Koi would surely not be pleased if they would know about '
                f'Sato.'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_you_already_have_mistress(mistress, user, guild_id):
    """
    Tests whether ``build_failure_embed_you_already_have_mistress`` works as intended.
    
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
    output = build_failure_embed_you_already_have_mistress(mistress, user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
