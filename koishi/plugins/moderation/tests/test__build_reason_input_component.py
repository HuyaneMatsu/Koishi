import vampytest
from hata import Component, TextInputStyle, create_label, create_text_input

from ..component_building import build_reason_input_component
from ..constants import REASON_ALLOWED_LENGTH_THRESHOLD


def _iter_options():
    reason = 'frog'
    
    yield (
        None,
        create_label(
            'Reason',
            None,
            create_text_input(
                custom_id = 'reason',
                max_length = REASON_ALLOWED_LENGTH_THRESHOLD,
                value = None,
                style = TextInputStyle.paragraph,
            ),
        ),
    )
    
    yield (
        reason,
        create_label(
            'Reason',
            None,
            create_text_input(
                custom_id = 'reason',
                max_length = REASON_ALLOWED_LENGTH_THRESHOLD,
                value = reason,
                style = TextInputStyle.paragraph,
            ),
        ),
    )
    
    
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_reason_input_component(reason):
    """
    Tests whether ``build_reason_input_component`` works as intended.
    
    Parameters
    ----------
    reason : `None | str`
        Current ban reason.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_reason_input_component(reason)
    vampytest.assert_instance(output, Component)
    return output
