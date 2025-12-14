import vampytest

from ....bot_utils.constants import ROLE__SUPPORT__ELEVATED

from ..content_building import produce_gift_requirements_unsatisfied_error_message


def _iter_options():
    yield (
        (
            f'You must be either related the targeted user, '
            f'or have {ROLE__SUPPORT__ELEVATED.name} role in my support guild to target anyone.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_gift_requirements_unsatisfied_error_message():
    """
    Tests whether ``produce_gift_requirements_unsatisfied_error_message`` works as intended.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_gift_requirements_unsatisfied_error_message()]
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
