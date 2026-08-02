import vampytest
from hata import Component, create_label, create_user_select

from ..component_building import build_users_input_component


def _iter_options():
    return create_label(
        'Select users',
        None,
        create_user_select(
            custom_id = 'users',
            min_values = 1,
            required = True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_users_input_component():
    """
    Tests whether ``build_users_input_component`` works as intended.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_users_input_component()
    vampytest.assert_instance(output, Component)
    return output
