import vampytest

from ..relationship_types import get_relationship_type_name, RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_NAME_DEFAULT


def _iter_options():
    yield RELATIONSHIP_TYPE_MAMA, 'mama'
    yield 1000, RELATIONSHIP_TYPE_NAME_DEFAULT


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_relationship_type_name(input_value):
    """
    Tests whether ``get_relationship_type_name`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to test with.
    
    Returns
    -------
    output : `str`
    """
    output = get_relationship_type_name(input_value)
    vampytest.assert_instance(output, str)
    return output
