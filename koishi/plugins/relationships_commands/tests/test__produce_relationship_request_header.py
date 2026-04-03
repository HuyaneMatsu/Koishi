import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ...relationships_core import RELATIONSHIP_TYPE_WAIFU

from ..content_building import produce_relationship_request_header


def _iter_options():
    yield (
        RELATIONSHIP_TYPE_WAIFU,
        True,
        'Orin',
        1000,
        f'Marriage proposal towards Orin (1000 {EMOJI__HEART_CURRENCY})',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_relationship_request_header(relationship_type, outgoing, user_name, investment):
    """
    Tests whether ``produce_relationship_request_header`` works as intended.
    
    Parameters
    ----------
    relationship_type : `int`
        The relationship's type.
    
    outgoing : `bool`
        Whether the request is outgoing.
    
    user_name : `str`
        The displayed user's name.
    
    investment : `int`
        The source user's investment.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_relationship_request_header(relationship_type, outgoing, user_name, investment)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
