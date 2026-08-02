import vampytest
from hata import Component, StringSelectOption, create_label, create_string_select

from ..component_building import build_notify_user_input_component


def _iter_options():
    return create_label(
        'Notify user',
        None,
        create_string_select(
            [
                StringSelectOption('0', 'Nah', default = True),
                StringSelectOption('1', 'Yes'),
            ],
            custom_id = 'notify_user',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_notify_user_input_component():
    """
    Tests whether ``build_notify_user_input_component`` works as intended.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_notify_user_input_component()
    vampytest.assert_instance(output, Component)
    return output
