import vampytest
from hata import Embed, GuildProfile, User

from ..embed_builders import build_failure_embed_already_related
from ..relationship_types import RELATIONSHIP_TYPE_MAMA


def _iter_options():
    guild_id = 202412280004
    
    user = User.precreate(202412280005, name = 'Satori')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        True,
        True,
        user,
        0,
        Embed(
            'You are already related',
            (
                f'You are already the mama of Satori.\n'
                f'Divorce them before reissuing a new proposal.'
            ),
        )
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        False,
        True,
        user,
        0,
        Embed(
            'You are already related',
            (
                f'You are already the daughter of Satori.\n'
                f'Divorce them before reissuing a new proposal.'
            ),
        )
    )
    yield (
        RELATIONSHIP_TYPE_MAMA,
        True,
        False,
        user,
        0,
        Embed(
            'You are already related',
            (
                f'You are already the daughter of Satori.\n'
                f'Divorce them before accepting their proposal.'
            ),
        )
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        False,
        False,
        user,
        0,
        Embed(
            'You are already related',
            (
                f'You are already the mama of Satori.\n'
                f'Divorce them before accepting their proposal.'
            ),
        )
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        True,
        True,
        user,
        guild_id,
        Embed(
            'You are already related',
            (
                f'You are already the mama of Sato.\n'
                f'Divorce them before reissuing a new proposal.'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_already_related(relationship_type, outgoing, checked_at_creation, user, guild_id):
    """
    Tests whether ``build_failure_embed_already_related`` works as intended.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    outgoing : `bool`
        Whether the relationship is outgoing.
    
    checked_at_creation : `bool`
        Whether we are building a failure embed for creation (or accetage).
    
    user : ``ClientUserBase``
        The related user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_already_related(relationship_type, outgoing, checked_at_creation, user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
