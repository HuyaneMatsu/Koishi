import vampytest
from hata import Component, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..checks import check_insufficient_investment


def _iter_options():
    yield (
        199,
        200,
        None,
    )
    
    yield (
        200,
        200,
        None,
    )
    
    yield (
        201,
        200,
        [
            create_text_display(
                f'Your investment {200} {EMOJI__HEART_CURRENCY} is lower than the required '
                f'{201} {EMOJI__HEART_CURRENCY}.'
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__check_insufficient_investment(relationship_value, investment):
    """
    Tests whether ``check_insufficient_investment`` works as intended.
    
    Parameters
    ----------
    relationship_value : `int`
        The minimal value the user needs to propose with to start the relationship.
    
    investment : `int`
        Investment to propose with.
    
    Returns
    -------
    output : ``None | list<Component>``
    """
    output = check_insufficient_investment(relationship_value, investment)
    vampytest.assert_instance(output, list, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Component)
    
    return output
