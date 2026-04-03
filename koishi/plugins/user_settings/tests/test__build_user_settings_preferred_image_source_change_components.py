import vampytest
from hata import Component, create_text_display

from ..builders import build_user_settings_preferred_image_source_change_components
from ..constants import PREFERRED_IMAGE_SOURCE_NAME_TOUHOU, PREFERRED_IMAGE_SOURCE_NONE, PREFERRED_IMAGE_SOURCE_TOUHOU


def _iter_options():
    yield (
        PREFERRED_IMAGE_SOURCE_TOUHOU,
        True,
        True,
        [
            create_text_display(f'Preferred image source set to `{PREFERRED_IMAGE_SOURCE_NAME_TOUHOU!s}`.')
        ],
    )
    
    yield (
        PREFERRED_IMAGE_SOURCE_NONE,
        False,
        False,
        [
            create_text_display('Could not match any preferred image source.'),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_settings_preferred_image_source_change_components(option, value, changed):
    """
    Tests whether ``build_user_settings_preferred_image_source_change_components`` works as intended.
    
    Parameters
    ----------
    option : `int`
        The preferred image source that were set.
    
    value : `bool`
        The new value to set.
    
    changed : `bool`
        Whether value was changed.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_user_settings_preferred_image_source_change_components(option, value, changed)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
