import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_success_embed_relationship_updated
from ..relationship_types import RELATIONSHIP_TYPE_MAMA


def _iter_options():
    guild_id = 202501090000
    
    target_user = User.precreate(202501090001, name = 'Satori')
    target_user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        target_user,
        0,
        Embed(
            'Relationship updated',
            f'You have become the mama of Satori.',
        ),
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        target_user,
        guild_id,
        Embed(
            'Relationship updated',
            f'You have become the mama of Sato.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed_relationship_updated(relationship_type, target_user, guild_id):
    """
    Tests whether ``build_success_embed_relationship_updated`` works as intended.
    
    Parameters
    ----------
    relationship_type : `int`
        The relationship's type.
    
    target_user : ``ClientUserBase``
        The targeted user. May be actually the source user if the relationship is reversed.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_success_embed_relationship_updated(relationship_type, target_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
