import vampytest
from hata import Embed, GuildProfile, User

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..embed_builders import build_relationship_request_listing_embed
from ..relationship_request import RelationshipRequest
from ..relationship_types import (
    RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MASTER, RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_WAIFU
)


def _iter_options():
    guild_id = 202412310020
    
    user_id_0 = 202412310021
    user_id_1 = 202412310022
    user_id_2 = 202412310023
    user_id_3 = 202412310024
    user_id_4 = 202412310025
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_0.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    user_1 = User.precreate(user_id_1, name = 'Utsuho')
    user_1.guild_profiles[guild_id] = GuildProfile(nick = 'Okuu')
    
    user_2 = User.precreate(user_id_2, name = 'Rin')
    user_2.guild_profiles[guild_id] = GuildProfile(nick = 'Orin')
    
    user_3 = User.precreate(user_id_3, name = 'Koishi')
    user_3.guild_profiles[guild_id] = GuildProfile(nick = 'Koi')
    
    user_4 = User.precreate(user_id_4, name = 'Kokoro')
    user_4.guild_profiles[guild_id] = GuildProfile(nick = 'Koko')
    
    yield (
        True,
        None,
        None,
        0,
        Embed(
            'Outgoing requests',
            '*none*',
        ),
    )
    
    yield (
        True,
        [
            RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1000),
            RelationshipRequest(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 2000),
        ],
        [
            user_1,
            user_2,
        ],
        0,
        Embed(
            'Outgoing requests',
        ).add_field(
            'Adoption agreements:',
            (
                f'Rin (2000 {EMOJI__HEART_CURRENCY})\n'
                f'Utsuho (1000 {EMOJI__HEART_CURRENCY})'
            ),
        ),
    )
    
    yield (
        False,
        [
            RelationshipRequest(user_id_1, user_id_0, RELATIONSHIP_TYPE_MAMA, 1000),
            RelationshipRequest(user_id_2, user_id_0, RELATIONSHIP_TYPE_MAMA, 2000),
        ],
        [
            user_1,
            user_2,
        ],
        guild_id,
        Embed(
            'Incoming requests',
        ).add_field(
            'Adoption agreements:',
            (
                f'Okuu (1000 {EMOJI__HEART_CURRENCY})\n'
                f'Orin (2000 {EMOJI__HEART_CURRENCY})'
            ),
        ),
    )
    
    yield (
        True,
        [
            RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_WAIFU, 1000),
            RelationshipRequest(user_id_0, user_id_2, RELATIONSHIP_TYPE_SISTER_BIG, 2000),
            RelationshipRequest(user_id_0, user_id_3, RELATIONSHIP_TYPE_MAMA, 3000),
            RelationshipRequest(user_id_0, user_id_4, RELATIONSHIP_TYPE_MASTER, 4000),
        ],
        [
            user_1,
            user_2,
            user_3,
            user_4,
        ],
        0,
        Embed(
            'Outgoing requests',
        ).add_field(
            'Marriage proposals:',
            (
                f'Utsuho (1000 {EMOJI__HEART_CURRENCY})'
            ),
        ).add_field(
            'Blood-pact requests:',
            (
                f'Rin (2000 {EMOJI__HEART_CURRENCY})'
            ),
        ).add_field(
            'Adoption agreements:',
            (
                f'Koishi (3000 {EMOJI__HEART_CURRENCY})'
            ),
        ).add_field(
            'Employment contract:',
            (
                f'Kokoro (4000 {EMOJI__HEART_CURRENCY})'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_relationship_request_listing_embed(outgoing, relationship_request_listing, users, guild_id):
    """
    Tests whether ``build_relationship_request_listing_embed`` works as intended.
    
    Parameters
    ----------
    outgoing : `bool`
        Whether to render the outgoing embed.
    
    relationship_request_listing : `None | list<RelationshipRequest>`
        Incoming relationship requests.
    
    users : `None | list<ClientUserBase>`
        The requested user for each relationship.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_relationship_request_listing_embed(outgoing, relationship_request_listing, users, guild_id)
    vampytest.assert_instance(output, Embed)
    return output
