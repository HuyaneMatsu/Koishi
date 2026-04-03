import vampytest

from ..content_building import get_relationship_request_type_concept
from ..relationship_types import RELATIONSHIP_TYPE_WAIFU


def _iter_options():
    yield (
        RELATIONSHIP_TYPE_WAIFU,
        True,
        'Marriage proposal',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_relationship_request_type_concept(relationship_type, capitalised):
    """
    Tests whether ``get_relationship_request_type_concept`` works as intended.
    
    Parameters
    ----------
    relationship_type : `int`
        The relationship's type.
    
    capitalised : `bool`
        Whether to return a capitalised version,
    
    Returns
    -------
    output : `str`
    """
    output = get_relationship_request_type_concept(relationship_type, capitalised)
    vampytest.assert_instance(output, str)
    return output
