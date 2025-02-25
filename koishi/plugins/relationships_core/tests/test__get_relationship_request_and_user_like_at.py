import vampytest

from hata import ClientUserBase, GuildProfile, User
from hata.ext.slash import InteractionAbortedError

from ..relationship_request import RelationshipRequest
from ..relationship_request_completion import get_relationship_request_and_user_like_at
from ..relationship_types import RELATIONSHIP_TYPE_MAMA


def _iter_options():
    guild_id = 202501020060_000000
    
    user_id_0 = 202501020061_000000
    user_id_1 = 202501020062_000000
    user_id_2 = 202501020063_000000
    user_id_3 = 202501020064_000000
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_0.guild_profiles[guild_id] = GuildProfile(nick = 'Sister')
    
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    user_1.guild_profiles[guild_id] = GuildProfile(nick = 'Flower')
    
    user_2 = User.precreate(user_id_2, name = 'Orin')
    user_2.guild_profiles[guild_id] = GuildProfile(nick = 'Maid')
    
    user_3 = User.precreate(user_id_3, name = 'Okuu')
    user_3.guild_profiles[guild_id] = GuildProfile(nick = 'BirdBrain')
    
    relationship_request_0 = RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_1 = RelationshipRequest(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_2 = RelationshipRequest(user_id_0, user_id_3, RELATIONSHIP_TYPE_MAMA, 1000)
    
    yield (
        user_id_0,
        True,
        'okuu',
        0,
        [
            relationship_request_0,
            relationship_request_1,
            relationship_request_2,
        ],
        [
            user_1,
            user_2,
            user_3,
        ],
        (relationship_request_2, user_3),
    )
    
    relationship_request_0 = RelationshipRequest(user_id_1, user_id_0, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_1 = RelationshipRequest(user_id_2, user_id_0, RELATIONSHIP_TYPE_MAMA, 1002)
    relationship_request_2 = RelationshipRequest(user_id_3, user_id_0, RELATIONSHIP_TYPE_MAMA, 1004)
    
    yield (
        user_id_0,
        False,
        'okuu',
        0,
        [
            relationship_request_0,
            relationship_request_1,
            relationship_request_2,
        ],
        [
            user_1,
            user_2,
            user_3,
        ],
        (relationship_request_2, user_3),
    )
    
    relationship_request_0 = RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_1 = RelationshipRequest(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_2 = RelationshipRequest(user_id_0, user_id_3, RELATIONSHIP_TYPE_MAMA, 1000)
    
    yield (
        user_id_0,
        True,
        'bird',
        guild_id,
        [
            relationship_request_0,
            relationship_request_1,
            relationship_request_2,
        ],
        [
            user_1,
            user_2,
            user_3,
        ],
        (relationship_request_2, user_3),
    )
    
    relationship_request_0 = RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_1 = RelationshipRequest(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_2 = RelationshipRequest(user_id_0, user_id_3, RELATIONSHIP_TYPE_MAMA, 1000)
    
    yield (
        user_id_0,
        True,
        str(user_id_3),
        guild_id,
        [
            relationship_request_0,
            relationship_request_1,
            relationship_request_2,
        ],
        [
            user_1,
            user_2,
            user_3,
        ],
        (relationship_request_2, user_3),
    )


def _iter_options__aborted():
    guild_id = 202501020070_000000
    
    user_id_0 = 202501020071_000000
    user_id_1 = 202501020072_000000
    user_id_2 = 202501020073_000000
    user_id_3 = 202501020074_000000
    user_id_4 = 202502220000_000000
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_0.guild_profiles[guild_id] = GuildProfile(nick = 'Sister')
    
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    user_1.guild_profiles[guild_id] = GuildProfile(nick = 'Flower')
    
    user_2 = User.precreate(user_id_2, name = 'Orin')
    user_2.guild_profiles[guild_id] = GuildProfile(nick = 'Maid')
    
    user_3 = User.precreate(user_id_3, name = 'Okuu')
    user_3.guild_profiles[guild_id] = GuildProfile(nick = 'BirdBrain')
    
    yield (
        user_id_0,
        True,
        None,
        0,
        None,
        None,
    )
    
    
    relationship_request_0 = RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_1 = RelationshipRequest(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_2 = RelationshipRequest(user_id_0, user_id_3, RELATIONSHIP_TYPE_MAMA, 1000)
    
    yield (
        user_id_0,
        True,
        'satori',
        0,
        [
            relationship_request_0,
            relationship_request_1,
            relationship_request_2,
        ],
        [
            user_1,
            user_2,
            user_3,
        ],
    )
    
    
    relationship_request_0 = RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_1 = RelationshipRequest(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_2 = RelationshipRequest(user_id_0, user_id_3, RELATIONSHIP_TYPE_MAMA, 1000)
    
    yield (
        user_id_0,
        True,
        'satori',
        guild_id,
        [
            relationship_request_0,
            relationship_request_1,
            relationship_request_2,
        ],
        [
            user_1,
            user_2,
            user_3,
        ],
    )
    
    
    relationship_request_0 = RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_1 = RelationshipRequest(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_2 = RelationshipRequest(user_id_0, user_id_3, RELATIONSHIP_TYPE_MAMA, 1000)
    
    yield (
        user_id_0,
        True,
        str(user_id_4),
        guild_id,
        [
            relationship_request_0,
            relationship_request_1,
            relationship_request_2,
        ],
        [
            user_1,
            user_2,
            user_3,
        ],
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__aborted()).raising(InteractionAbortedError))
async def test__get_relationship_request_and_user_like_at(
    user_id, outgoing, value, guild_id, relationship_requests, users
):
    """
    Tests whether ``get_relationship_request_and_user_like_at`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier who is requesting.
    
    outgoing : `bool`
        Whether to render the outgoing embed.
    
    value : `None | str`
        The value to auto complete.
    
    guild_id : `int`
        The respective guild's identifier.
    
    relationship_requests : `None | list<RelationshipRequest>`
        Relationship requests to return when requested.
    
    users : `None | list<str>`
        Users to return when requested.
    
    Returns
    -------
    output : `(RelationshipRequest, ClientUserBase)`
    
    Raises
    ------
    InteractionAbortedError
    """
    async def mock_get_relationship_request_listing(input_user_id, input_outgoing):
        nonlocal user_id
        nonlocal outgoing
        nonlocal relationship_requests
        
        vampytest.assert_eq(input_user_id, user_id)
        vampytest.assert_eq(input_outgoing, outgoing)
        
        return relationship_requests
    
    async def mock_get_users_unordered(input_user_ids):
        nonlocal users
        if users is None:
            raise RuntimeError
        
        vampytest.assert_eq(
            {*input_user_ids},
            {user.id for user in users},
        )
        
        return users
    
    
    mocked = vampytest.mock_globals(
        get_relationship_request_and_user_like_at,
        get_relationship_request_listing = mock_get_relationship_request_listing,
        get_users_unordered = mock_get_users_unordered,
    )
    
    output = await mocked(user_id, outgoing, value, guild_id)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_instance(output[0], RelationshipRequest)
    vampytest.assert_instance(output[1], ClientUserBase)
    return output
