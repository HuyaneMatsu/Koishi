import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_failure_embed_you_already_have_master


def _iter_options():
    guild_id = 202501010000
    
    master = User.precreate(202501010001, name = 'Koishi')
    master.guild_profiles[guild_id] = GuildProfile(nick = 'Koi')
    
    user = User.precreate(202501010002, name = 'Satori')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        master,
        user,
        0,
        Embed(
            'You already have a master',
            (
                f'Koishi would surely not be pleased if they would know about '
                f'Satori.'
            ),
        )
    )
    
    yield (
        master,
        user,
        guild_id,
        Embed(
            'You already have a master',
            (
                f'Koi would surely not be pleased if they would know about '
                f'Sato.'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_you_already_have_master(master, user, guild_id):
    """
    Tests whether ``build_failure_embed_you_already_have_master`` works as intended.
    
    Parameters
    ----------
    master : ``ClientUserBase``
        The current master.
    
    user : ``ClientUserBase``
        The user who has master.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_you_already_have_master(master, user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
