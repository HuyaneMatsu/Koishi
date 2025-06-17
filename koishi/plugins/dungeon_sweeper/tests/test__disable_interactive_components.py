import vampytest
from hata import create_button, create_container, create_row, create_section, create_text_display

from ..helpers import disable_interactive_components


def test__disable_interactive_components():
    """
    Tests whether ``disable_interactive_components`` works as intended.
    """
    components = (
        create_text_display('who'),
        create_container(
            create_section(
                create_text_display('is'),
                thumbnail = create_button(custom_id = '0', label = 'cat'),
            ),
            create_row(
                create_button(custom_id = '1', label = 'now'),
            )
        ),
    )
    
    expected_output = (
        create_text_display('who'),
        create_container(
            create_section(
                create_text_display('is'),
                thumbnail = create_button(custom_id = '0', label = 'cat', enabled = False),
            ),
            create_row(
                create_button(custom_id = '1', label = 'now', enabled = False),
            )
        ),
    )
    
    disable_interactive_components(components)
    
    vampytest.assert_eq(components, expected_output)
