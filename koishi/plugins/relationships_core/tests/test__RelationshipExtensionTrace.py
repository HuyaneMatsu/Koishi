from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..relationship import Relationship
from ..relationship_extension_trace import RelationshipExtensionTrace
from ..relationship_types import RELATIONSHIP_TYPE_DAUGHTER, RELATIONSHIP_TYPE_GRANNY, RELATIONSHIP_TYPE_MAMA 


def _assert_fields_set(relationship_extension_trace):
    """
    Asserts whether all fields are set of the given instance.
    
    Parameters
    ----------
    relationship_extension_trace : ``RelationshipExtensionTrace``
        The instance to check.
    """
    vampytest.assert_instance(relationship_extension_trace, RelationshipExtensionTrace)
    vampytest.assert_instance(relationship_extension_trace.relationship_route, tuple)
    vampytest.assert_instance(relationship_extension_trace.relationship_type, int)
    vampytest.assert_instance(relationship_extension_trace.user_id, int)


def test__RelationshipExtensionTrace__new():
    """
    Tests whether ``RelationshipExtensionTrace.__new__`` works as intended.
    """
    user_id_0 = 202601210000
    user_id_1 = 202601210001
    user_id_2 = 202601210002
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    user_id = user_id_2
    relationship_type = RELATIONSHIP_TYPE_GRANNY
    relationship_route = (
        Relationship(
            user_id_0,
            user_id_1,
            RELATIONSHIP_TYPE_MAMA,
            1000,
            now,
        ),
        Relationship(
            user_id_2,
            user_id_1,
            RELATIONSHIP_TYPE_DAUGHTER,
            1000,
            now,
        ),
    )
    
    relationship_extension_trace = RelationshipExtensionTrace(
        user_id,
        relationship_type,
        relationship_route,
    )
    _assert_fields_set(relationship_extension_trace)
    
    vampytest.assert_eq(relationship_extension_trace.user_id, user_id)
    vampytest.assert_eq(relationship_extension_trace.relationship_type, relationship_type)
    vampytest.assert_eq(relationship_extension_trace.relationship_route, relationship_route)


def test__RelationshipExtensionTrace__repr():
    """
    Tests whether ``RelationshipExtensionTrace.__repr__`` works as intended.
    """
    user_id_0 = 202601210010
    user_id_1 = 202601210011
    user_id_2 = 202601210012
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    user_id = user_id_2
    relationship_type = RELATIONSHIP_TYPE_GRANNY
    relationship_route = (
        Relationship(
            user_id_0,
            user_id_1,
            RELATIONSHIP_TYPE_MAMA,
            1000,
            now,
        ),
        Relationship(
            user_id_2,
            user_id_1,
            RELATIONSHIP_TYPE_DAUGHTER,
            1000,
            now,
        ),
    )
    
    relationship_extension_trace = RelationshipExtensionTrace(
        user_id,
        relationship_type,
        relationship_route,
    )
    output = repr(relationship_extension_trace)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    user_id_0 = 202601210010
    user_id_1 = 202601210011
    user_id_2 = 202601210012
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(
        user_id_0,
        user_id_1,
        RELATIONSHIP_TYPE_MAMA,
        1000,
        now,
    )
    
    relationship_1 = Relationship(
        user_id_2,
        user_id_1,
        RELATIONSHIP_TYPE_DAUGHTER,
        1000,
        now,
    )
    
    user_id = user_id_2,
    relationship_type = RELATIONSHIP_TYPE_GRANNY
    relationship_route = (
        relationship_0,
        relationship_1,
    )
    
    keyword_parameters = {
        'user_id': user_id,
        'relationship_type': relationship_type,
        'relationship_route': relationship_route,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'user_id': user_id_1,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'relationship_type': RELATIONSHIP_TYPE_MAMA,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'relationship_route': (
                relationship_0,
            ),
        },
        False,
    )
    

@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__RelationshipExtensionTrace__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``RelationshipExtensionTrace.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    relationship_extension_trace_0 = RelationshipExtensionTrace(**keyword_parameters_0)
    relationship_extension_trace_1 = RelationshipExtensionTrace(**keyword_parameters_1)
    
    output = relationship_extension_trace_0 == relationship_extension_trace_1
    vampytest.assert_instance(output, bool)
    return output
