import vampytest

from ..relationship_connection_types import (
    RELATIONSHIP_CONNECTION_TYPE_IN_LAW, RELATIONSHIP_CONNECTION_TYPE_NONE, RELATIONSHIP_CONNECTION_TYPE_NAME_DEFAULT,
    get_relationship_connection_type_name
)


def _iter_options():
    yield RELATIONSHIP_CONNECTION_TYPE_NONE, None
    yield RELATIONSHIP_CONNECTION_TYPE_IN_LAW, 'in law'
    yield 1000, RELATIONSHIP_CONNECTION_TYPE_NAME_DEFAULT


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_relationship_connection_type_name(input_value):
    """
    Tests whether ``get_relationship_connection_type_name`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to test with.
    
    Returns
    -------
    output : `None | str`
    """
    output = get_relationship_connection_type_name(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
