from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from hata import ClientUserBase, GuildProfile, User
from hata.ext.slash import InteractionAbortedError

from ..relationship import Relationship
from ..relationship_completion import get_extender_relationship_and_relationship_and_user_like_at
from ..relationship_types import RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_WAIFU


def _iter_options():
    guild_id = 202501090040
    
    user_id_0 = 202501090041
    user_id_1 = 202501090042
    user_id_2 = 202501090043
    user_id_3 = 202501090044
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_0.guild_profiles[guild_id] = GuildProfile(nick = 'Sister')
    
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    user_1.guild_profiles[guild_id] = GuildProfile(nick = 'Flower')
    
    user_2 = User.precreate(user_id_2, name = 'Orin')
    user_2.guild_profiles[guild_id] = GuildProfile(nick = 'Maid')
    
    user_3 = User.precreate(user_id_3, name = 'Okuu')
    user_3.guild_profiles[guild_id] = GuildProfile(nick = 'BirdBrain')
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1000, now)
    relationship_1 = Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 1000, now)
    relationship_2 = Relationship(user_id_0, user_id_3, RELATIONSHIP_TYPE_MAMA, 1000, now)
    
    yield (
        user_id_0,
        'okuu',
        0,
        [
            relationship_0,
            relationship_1,
            relationship_2,
        ],
        None,
        [
            user_1,
            user_2,
            user_3,
        ],
        (None, relationship_2, user_3),
    )
    
    relationship_0 = Relationship(user_id_1, user_id_0, RELATIONSHIP_TYPE_MAMA, 1000, now)
    relationship_1 = Relationship(user_id_2, user_id_0, RELATIONSHIP_TYPE_MAMA, 1002, now)
    relationship_2 = Relationship(user_id_0, user_id_3, RELATIONSHIP_TYPE_MAMA, 1004, now)
    
    yield (
        user_id_0,
        'bird',
        guild_id,
        [
            relationship_0,
            relationship_1,
            relationship_2,
        ],
        None,
        [
            user_1,
            user_2,
            user_3,
        ],
        (None, relationship_2, user_3),
    )
    
    
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_WAIFU, 1000, now)
    relationship_1 = Relationship(user_id_1, user_id_2, RELATIONSHIP_TYPE_SISTER_BIG, 1000, now)
    relationship_2 = Relationship(user_id_3, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 1000, now)
    
    yield (
        user_id_0,
        'bird',
        guild_id,
        [
            relationship_0,
        ],
        [
            (relationship_0, [relationship_1, relationship_2]),
        ],
        [
            user_1,
            user_2,
            user_3,
        ],
        (relationship_0, relationship_2, user_3),
    )


def _iter_options__aborted():
    guild_id = 202501040090
    
    user_id_0 = 202501040091
    user_id_1 = 202501040092
    user_id_2 = 202501040093
    user_id_3 = 202501040094
    
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

    
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1000, now)
    relationship_1 = Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 1000, now)
    relationship_2 = Relationship(user_id_3, user_id_0, RELATIONSHIP_TYPE_MAMA, 1000, now)
    
    yield (
        user_id_0,
        'satori',
        0,
        [
            relationship_0,
            relationship_1,
            relationship_2,
        ],
        None,
        [
            user_1,
            user_2,
            user_3,
        ],
    )
    
    
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1000, now)
    relationship_1 = Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 1000, now)
    relationship_2 = Relationship(user_id_3, user_id_0, RELATIONSHIP_TYPE_MAMA, 1000, now)
    
    yield (
        user_id_0,
        'satori',
        guild_id,
        [
            relationship_0,
            relationship_1,
            relationship_2,
        ],
        None,
        [
            user_1,
            user_2,
            user_3,
        ],
    )
    
    
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_WAIFU, 1000, now)
    relationship_1 = Relationship(user_id_1, user_id_2, RELATIONSHIP_TYPE_SISTER_BIG, 1000, now)
    relationship_2 = Relationship(user_id_3, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 1000, now)
    
    yield (
        user_id_0,
        'satori',
        guild_id,
        [
            relationship_0,
        ],
        [
            (relationship_0, [relationship_1, relationship_2]),
        ],
        [
            user_1,
            user_2,
            user_3,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__aborted()).raising(InteractionAbortedError))
async def test__get_extender_relationship_and_relationship_and_user_like_at(
    user_id, value, guild_id, relationship_listing, relationship_listing_extend, users
):
    """
    Tests whether ``get_extender_relationship_and_relationship_and_user_like_at`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier who is requesting.
    
    value : `None | str`
        The value to auto complete.
    
    guild_id : `int`
        The respective guild's identifier.
    
    relationship_listing : `None | list<Relationship>`
        Relationships to return when requested.
    
    relationship_listing_extend : `None | list<(Relationship, list<Relationship>)>`
        The relationship extend to return when requested.
    
    users : `None | list<str>`
        Users to return when requested.
    
    Returns
    -------
    output : `(None | Relationship, Relationship, ClientUserBase)`
    
    Raises
    ------
    InteractionAbortedError
    """
    async def mock_get_relationship_listing_and_extend(input_user_id):
        nonlocal user_id
        nonlocal relationship_listing
        nonlocal relationship_listing_extend
        
        vampytest.assert_eq(input_user_id, user_id)
        
        return relationship_listing, relationship_listing_extend
    
    
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
        get_extender_relationship_and_relationship_and_user_like_at,
        get_relationship_listing_and_extend = mock_get_relationship_listing_and_extend,
        get_users_unordered = mock_get_users_unordered,
    )
    
    output = await mocked(user_id, value, guild_id)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 3)
    vampytest.assert_instance(output[0], Relationship, nullable = True)
    vampytest.assert_instance(output[1], Relationship)
    vampytest.assert_instance(output[2], ClientUserBase)
    return output
