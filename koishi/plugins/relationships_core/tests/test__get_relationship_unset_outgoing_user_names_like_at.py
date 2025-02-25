from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from hata import GuildProfile, User

from ..relationship import Relationship
from ..relationship_completion import get_relationship_unset_outgoing_user_names_like_at
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_UNSET


def _iter_options():
    guild_id = 202501080010_000000
    
    user_id_0 = 202501080011_000000
    user_id_1 = 202501080012_000000
    user_id_2 = 202501080013_000000
    user_id_3 = 202501080014_000000
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_0.guild_profiles[guild_id] = GuildProfile(nick = 'Sister')
    
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    user_1.guild_profiles[guild_id] = GuildProfile(nick = 'Flower')
    
    user_2 = User.precreate(user_id_2, name = 'Orin')
    user_2.guild_profiles[guild_id] = GuildProfile(nick = 'Maid')
    
    user_3 = User.precreate(user_id_3, name = 'Okuu')
    user_3.guild_profiles[guild_id] = GuildProfile(nick = 'BirdBrain')
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        user_id_0,
        None,
        0,
        None,
        None,
        None,
    )
    
    yield (
        user_id_0,
        None,
        0,
        [
            Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_UNSET, 1000, now),
            Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_UNSET, 1002, now),
            Relationship(user_id_3, user_id_0, RELATIONSHIP_TYPE_SISTER_BIG, 1004, now),
        ],
        [
            user_1,
            user_2,
        ],
        [
            ('Koishi', str(user_id_1)),
            ('Orin', str(user_id_2)),
        ],
    )
    
    yield (
        user_id_0,
        None,
        guild_id,
        [
            Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_UNSET, 1000, now),
            Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_UNSET, 1002, now),
            Relationship(user_id_3, user_id_0, RELATIONSHIP_TYPE_SISTER_BIG, 1004, now),
        ],
        [
            user_1,
            user_2,
        ],
        [
            ('Flower', str(user_id_1)),
            ('Maid', str(user_id_2)),
        ],
    )
    
    yield (
        user_id_0,
        'koi',
        0,
        [
            Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_UNSET, 1000, now),
            Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_UNSET, 1002, now),
            Relationship(user_id_3, user_id_0, RELATIONSHIP_TYPE_SISTER_BIG, 1004, now),
        ],
        [
            user_1,
            user_2,
        ],
        [
            ('Koishi', str(user_id_1)),
        ],
    )
    
    yield (
        user_id_0,
        'koi',
        guild_id,
        [
            Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_UNSET, 1000, now),
            Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_UNSET, 1002, now),
            Relationship(user_id_3, user_id_0, RELATIONSHIP_TYPE_SISTER_BIG, 1004, now),
        ],
        [
            user_1,
            user_2,
        ],
        [
            ('Flower', str(user_id_1)),
        ],
    )
    
    yield (
        user_id_0,
        'satori',
        0,
        [
            Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_UNSET, 1000, now),
            Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_UNSET, 1002, now),
            Relationship(user_id_3, user_id_0, RELATIONSHIP_TYPE_SISTER_BIG, 1004, now),
        ],
        [
            user_1,
            user_2,
        ],
        None,
    )
    
    yield (
        user_id_0,
        str(user_id_1),
        0,
        [
            Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_UNSET, 1000, now),
            Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_UNSET, 1002, now),
            Relationship(user_id_3, user_id_0, RELATIONSHIP_TYPE_SISTER_BIG, 1004, now),
        ],
        [
            user_1,
            user_2,
        ],
        [
            ('Koishi', str(user_id_1)),
        ],
    )
    
    yield (
        user_id_0,
        str(user_id_3),
        0,
        [
            Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_UNSET, 1000, now),
            Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_UNSET, 1002, now),
            Relationship(user_id_3, user_id_0, RELATIONSHIP_TYPE_SISTER_BIG, 1004, now),
        ],
        [
            user_1,
            user_2,
        ],
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_relationship_unset_outgoing_user_names_like_at(user_id, value, guild_id, relationships, users):
    """
    Tests whether ``get_relationship_unset_outgoing_user_names_like_at`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier who is requesting.
    
    value : `None | str`
        The value to auto complete.
    
    guild_id : `int`
        The respective guild's identifier.
    
    relationships : `None | list<Relationship>`
        Relationships to return when requested.
    
    users : `None | list<str>`
        Users to return when requested.
    
    Returns
    -------
    output : `None | list<(str, str)>`
    """
    async def mock_get_relationship_listing(input_user_id):
        nonlocal user_id
        nonlocal relationships
        
        vampytest.assert_eq(input_user_id, user_id)
        
        return relationships
    
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
        get_relationship_unset_outgoing_user_names_like_at,
        get_relationship_listing = mock_get_relationship_listing,
        get_users_unordered = mock_get_users_unordered,
    )
    
    output = await mocked(user_id, value, guild_id)
    vampytest.assert_instance(output, list, nullable = True)
    return output
