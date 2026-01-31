import vampytest

from ..relationship_types import RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_NAME_DEFAULT, produce_relationship_type_name_advanced


def _iter_options():
    yield RELATIONSHIP_TYPE_MAMA, 'mama'
    yield 1000, 'little sister & mama & daughter & mistress & maid & sister'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_relationship_type_name_advanced(input_value):
    """
    Tests whether ``produce_relationship_type_name_advanced`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to test with.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_relationship_type_name_advanced(input_value)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
