from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..relationship import Relationship
from ..relationship_completion import get_relationship_to_deepen
from ..relationship_extension_trace import RelationshipExtensionTrace
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_SISTER_LIL, RELATIONSHIP_TYPE_WAIFU


def _iter_options():
    user_id_0 = 202502150000
    user_id_1 = 202502150001
    user_id_2 = 202502150002
    user_id_3 = 202502150003
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    # none
    yield (
        user_id_0,
        user_id_1,
        None,
        None,
    )
    
    # miss
    relationship_0 = Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_WAIFU, 1000, now)
    relationship_1 = Relationship(user_id_0, user_id_3, RELATIONSHIP_TYPE_SISTER_BIG, 1000, now)
    
    yield (
        user_id_0,
        user_id_1,
        {
            user_id_2 : RelationshipExtensionTrace(
                user_id_2,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_0,),
            ),
            user_id_3 : RelationshipExtensionTrace(
                user_id_3,
                RELATIONSHIP_TYPE_SISTER_LIL,
                (relationship_1,),
            )
        },
        None,
    )
    
    # direct normal
    relationship_0 = Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_WAIFU, 1000, now)
    relationship_1 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 1000, now)
    
    yield (
        user_id_0,
        user_id_1,
        {
            user_id_2 : RelationshipExtensionTrace(
                user_id_2,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_0,),
            ),
            user_id_1 : RelationshipExtensionTrace(
                user_id_1,
                RELATIONSHIP_TYPE_SISTER_LIL,
                (relationship_1,),
            )
        },
        relationship_1,
    )
    
    # direct reverse
    relationship_0 = Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_WAIFU, 1000, now)
    relationship_1 = Relationship(user_id_1, user_id_0, RELATIONSHIP_TYPE_SISTER_BIG, 1000, now)
    
    yield (
        user_id_0,
        user_id_1,
        {
            user_id_2 : RelationshipExtensionTrace(
                user_id_2,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_0,),
            ),
            user_id_1 : RelationshipExtensionTrace(
                user_id_1,
                RELATIONSHIP_TYPE_SISTER_BIG,
                (relationship_1,),
            )
        },
        relationship_1,
    )
    
    # extended normal
    relationship_0 = Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_WAIFU, 1000, now)
    relationship_1 = Relationship(user_id_2, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 1000, now)
    
    yield (
        user_id_0,
        user_id_1,
        {
            user_id_2 : RelationshipExtensionTrace(
                user_id_2,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_0,),
            ),
            user_id_1 : RelationshipExtensionTrace(
                user_id_1,
                RELATIONSHIP_TYPE_SISTER_BIG, # not actually this one, but it is okay
                (relationship_0, relationship_1),
            )
        },
        relationship_0,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_relationship_to_deepen(source_user_id, target_user_id, relationship_extension_traces):
    """
    Tests whether ``get_relationship_to_deepen`` works as intended.
    
    Parameters
    ----------
    source_user_id : `int`
        The source user's identifier.
    
    target_user_id : `int`
        The target user's identifier.
    
    relationship_extension_traces : ```None | dict<int, RelationshipExtensionTrace>``
        The relationship extensions traces to return.
    
    Returns
    -------
    relationship : `None | Relationship`
    """
    async def mock_get_relationship_extension_traces(input_user_id):
        nonlocal source_user_id
        nonlocal relationship_extension_traces
        
        vampytest.assert_eq(input_user_id, source_user_id)
        
        return relationship_extension_traces
    
    
    mocked = vampytest.mock_globals(
        get_relationship_to_deepen,
        get_relationship_extension_traces = mock_get_relationship_extension_traces,
    )
    
    
    output = await mocked(source_user_id, target_user_id)
    vampytest.assert_instance(output, Relationship, nullable = True)
    return output
