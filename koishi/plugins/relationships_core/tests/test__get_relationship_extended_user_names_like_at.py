from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from hata import GuildProfile, User

from ..relationship import Relationship
from ..relationship_completion import get_relationship_extended_user_names_like_at
from ..relationship_extension_trace import RelationshipExtensionTrace
from ..relationship_types import (
    RELATIONSHIP_TYPE_DAUGHTER, RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_SISTER_LIL,
    RELATIONSHIP_TYPE_WAIFU
)


def _iter_options():
    guild_id = 202501110010_000000
    
    user_id_0 = 202501110011_000000
    user_id_1 = 202501110012_000000
    user_id_2 = 202501110013_000000
    user_id_3 = 202501110014_000000
    
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
        {
            user_id_1 : RelationshipExtensionTrace(
                user_id_1,
                RELATIONSHIP_TYPE_DAUGHTER,
                (relationship_0,),
            ),
            user_id_2 : RelationshipExtensionTrace(
                user_id_2,
                RELATIONSHIP_TYPE_DAUGHTER,
                (relationship_1,),
            ),
            user_id_3 : RelationshipExtensionTrace(
                user_id_3,
                RELATIONSHIP_TYPE_DAUGHTER,
                (relationship_2,),
            ),
        },
        [
            user_1,
            user_2,
            user_3,
        ],
        [
            ('Okuu', str(user_id_3)),
        ],
    )
    
    relationship_0 = Relationship(user_id_1, user_id_0, RELATIONSHIP_TYPE_MAMA, 1000, now)
    relationship_1 = Relationship(user_id_2, user_id_0, RELATIONSHIP_TYPE_MAMA, 1002, now)
    relationship_2 = Relationship(user_id_0, user_id_3, RELATIONSHIP_TYPE_MAMA, 1004, now)
    
    yield (
        user_id_0,
        'bird',
        guild_id,
        {
            user_id_1 : RelationshipExtensionTrace(
                user_id_1,
                RELATIONSHIP_TYPE_MAMA,
                (relationship_0,),
            ),
            user_id_2 : RelationshipExtensionTrace(
                user_id_2,
                RELATIONSHIP_TYPE_MAMA,
                (relationship_1,),
            ),
            user_id_3 : RelationshipExtensionTrace(
                user_id_3,
                RELATIONSHIP_TYPE_DAUGHTER,
                (relationship_2,),
            ),
        },
        [
            user_1,
            user_2,
            user_3,
        ],
        [
            ('BirdBrain', str(user_id_3)),
        ],
    )
    
    
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_WAIFU, 1000, now)
    relationship_1 = Relationship(user_id_1, user_id_2, RELATIONSHIP_TYPE_SISTER_BIG, 1000, now)
    relationship_2 = Relationship(user_id_3, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 1000, now)
    
    yield (
        user_id_0,
        'bird',
        guild_id,
        {
            user_id_1 : RelationshipExtensionTrace(
                user_id_1,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_0,),
            ),
            user_id_2 : RelationshipExtensionTrace(
                user_id_2,
                RELATIONSHIP_TYPE_SISTER_LIL, # not actually, but doesnt matter
                (relationship_0, relationship_1,),
            ),
            user_id_3 : RelationshipExtensionTrace(
                user_id_3,
                RELATIONSHIP_TYPE_SISTER_BIG, # not actually, but doesnt matter
                (relationship_0, relationship_2,),
            ),
        },
        [
            user_1,
            user_2,
            user_3,
        ],
        [
            ('BirdBrain', str(user_id_3)),
        ],
    )
    

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
        {
            user_id_1 : RelationshipExtensionTrace(
                user_id_1,
                RELATIONSHIP_TYPE_DAUGHTER,
                (relationship_0,),
            ),
            user_id_2 : RelationshipExtensionTrace(
                user_id_2,
                RELATIONSHIP_TYPE_DAUGHTER,
                (relationship_1,),
            ),
            user_id_3 : RelationshipExtensionTrace(
                user_id_3,
                RELATIONSHIP_TYPE_MAMA,
                (relationship_2,),
            ),
        },
        [
            user_1,
            user_2,
            user_3,
        ],
        None,
    )
    
    
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1000, now)
    relationship_1 = Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 1000, now)
    relationship_2 = Relationship(user_id_3, user_id_0, RELATIONSHIP_TYPE_MAMA, 1000, now)
    
    yield (
        user_id_0,
        'satori',
        guild_id,
        {
            user_id_1 : RelationshipExtensionTrace(
                user_id_1,
                RELATIONSHIP_TYPE_DAUGHTER,
                (relationship_0,),
            ),
            user_id_2 : RelationshipExtensionTrace(
                user_id_2,
                RELATIONSHIP_TYPE_DAUGHTER,
                (relationship_1,),
            ),
            user_id_3 : RelationshipExtensionTrace(
                user_id_3,
                RELATIONSHIP_TYPE_MAMA,
                (relationship_2,),
            ),
        },
        [
            user_1,
            user_2,
            user_3,
        ],
        None,
    )
    
    
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_WAIFU, 1000, now)
    relationship_1 = Relationship(user_id_1, user_id_2, RELATIONSHIP_TYPE_SISTER_BIG, 1000, now)
    relationship_2 = Relationship(user_id_3, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 1000, now)
    
    yield (
        user_id_0,
        'satori',
        guild_id,
        {
            user_id_1 : RelationshipExtensionTrace(
                user_id_1,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_0,),
            ),
            user_id_2 : RelationshipExtensionTrace(
                user_id_2,
                RELATIONSHIP_TYPE_SISTER_LIL, # not actually, but doesnt matter
                (relationship_0, relationship_1,),
            ),
            user_id_3 : RelationshipExtensionTrace(
                user_id_3,
                RELATIONSHIP_TYPE_SISTER_BIG, # not actually, but doesnt matter
                (relationship_0, relationship_2,),
            ),
        },
        [
            user_1,
            user_2,
            user_3,
        ],
        None,
    )
    
    relationship_0 = Relationship(user_id_1, user_id_0, RELATIONSHIP_TYPE_MAMA, 1000, now)
    relationship_1 = Relationship(user_id_2, user_id_0, RELATIONSHIP_TYPE_MAMA, 1002, now)
    relationship_2 = Relationship(user_id_0, user_id_3, RELATIONSHIP_TYPE_MAMA, 1004, now)
    
    yield (
        user_id_0,
        str(user_id_3),
        guild_id,
        {
            user_id_1 : RelationshipExtensionTrace(
                user_id_1,
                RELATIONSHIP_TYPE_MAMA,
                (relationship_0,),
            ),
            user_id_2 : RelationshipExtensionTrace(
                user_id_2,
                RELATIONSHIP_TYPE_MAMA,
                (relationship_1,),
            ),
            user_id_3 : RelationshipExtensionTrace(
                user_id_3,
                RELATIONSHIP_TYPE_DAUGHTER,
                (relationship_2,),
            ),
        },
        [
            user_1,
            user_2,
            user_3,
        ],
        [
            ('BirdBrain', str(user_id_3)),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_relationship_extended_user_names_like_at(
    user_id, value, guild_id, relationship_extension_traces, users
):
    """
    Tests whether ``get_relationship_extended_user_names_like_at`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier who is requesting.
    
    value : `None | str`
        The value to auto complete.
    
    guild_id : `int`
        The respective guild's identifier.
    
    relationship_extension_traces : ``None | dict<int, RelationshipExtensionTrace>``
        Relationship extension traces to return.
    
    users : `None | list<str>`
        Users to return when requested.
    
    Returns
    -------
    output : `None | list<(str, str)>`
    
    Raises
    ------
    InteractionAbortedError
    """
    async def mock_get_relationship_extension_traces(input_user_id):
        nonlocal user_id
        nonlocal relationship_extension_traces
        
        vampytest.assert_eq(input_user_id, user_id)
        
        return relationship_extension_traces
    
    
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
        get_relationship_extended_user_names_like_at,
        get_relationship_extension_traces = mock_get_relationship_extension_traces,
        get_users_unordered = mock_get_users_unordered,
    )
    
    output = await mocked(user_id, value, guild_id)
    vampytest.assert_instance(output, list, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, tuple)
            vampytest.assert_eq(len(element), 2)
            vampytest.assert_instance(element[0], str)
            vampytest.assert_instance(element[1], str)
    
    return output
