import vampytest
from hata import Component, create_label, create_text_input

from ..component_building import build_duration_input_component
from ..constants import DURATION_ALLOWED_LENGTH_MAX_THRESHOLD


def _iter_options():
    yield (
        0,
        create_label(
            'Duration',
            'w for week, d for day, h for hour, m for minute, s for second.',
            create_text_input(
                custom_id = 'duration',
                max_length = DURATION_ALLOWED_LENGTH_MAX_THRESHOLD,
                value = None,
            ),
        ),
    )
    
    yield (
        3600,
        create_label(
            'Duration',
            'w for week, d for day, h for hour, m for minute, s for second.',
            create_text_input(
                custom_id = 'duration',
                max_length = DURATION_ALLOWED_LENGTH_MAX_THRESHOLD,
                value = '1h',
            ),
        ),
    )

 
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_duration_input_component(default):
    """
    Tests whether ``build_duration_input_component`` works as intended.
    
    Parameters
    ----------
    default : `int`
        Default duration to use.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_duration_input_component(default)
    vampytest.assert_instance(output, Component)
    return output
