import vampytest
from hata import Component, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..checks import check_insufficient_available_balance


def _iter_options():
    yield (
        200,
        199,
        None,
    )
    
    yield (
        200,
        200,
        None,
    )
    
    yield (
        200,
        201,
        [
            create_text_display(
                f'You have {200} available {EMOJI__HEART_CURRENCY} '
                f'which is lower than {201} {EMOJI__HEART_CURRENCY}.'
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__check_insufficient_available_balance(available_balance, investment):
    """
    Tests whether ``check_insufficient_available_balance`` works as intended.
    
    Parameters
    ----------
    available_balance : `int`
        The user' available balance.
    
    investment : `int`
        Investment to propose with.
    
    Returns
    -------
    output : ``None | list<Component>``
    """
    output = check_insufficient_available_balance(available_balance, investment)
    vampytest.assert_instance(output, list, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Component)
    
    return output
