import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...relationships_core import RELATIONSHIP_TYPE_MAMA

from ..embed_builders import build_success_embed_request_created


def _iter_options():
    guild_id = 202412290004
    
    target_user = User.precreate(202412290005, name = 'Satori')
    target_user.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        1000,
        target_user,
        0,
        Embed(
            'Relationship request created',
            (
                f'You sent an adoption agreement to Satori '
                f'with 1000 {EMOJI__HEART_CURRENCY}'
            ),
        )
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        1000,
        target_user,
        guild_id,
        Embed(
            'Relationship request created',
            (
                f'You sent an adoption agreement to Sato '
                f'with 1000 {EMOJI__HEART_CURRENCY}'
            ),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed_request_created(relationship_type, investment, target_user, guild_id):
    """
    Tests whether ``build_success_embed_request_created`` works as intended.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relation type.
    
    investment : `int`
        The amount of balance to propose with.
    
    target_user : ``ClientUserBase``
        The user who is the target of the proposal.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_success_embed_request_created(relationship_type, investment, target_user, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
