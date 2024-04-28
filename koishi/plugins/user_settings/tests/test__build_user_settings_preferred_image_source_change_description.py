import vampytest

from ..builders import build_user_settings_preferred_image_source_change_description
from ..constants import (
    PREFERRED_IMAGE_SOURCE_NAME_NONE, PREFERRED_IMAGE_SOURCE_NAME_TOUHOU, PREFERRED_IMAGE_SOURCE_NONE,
    PREFERRED_IMAGE_SOURCE_TOUHOU
)


def _iter_options():
    yield (
        PREFERRED_IMAGE_SOURCE_NONE,
        False,
        False,
        'Could not match any preferred image source.',
    )
    yield (
        PREFERRED_IMAGE_SOURCE_NONE,
        True,
        False,
        f'Preferred image source was already `{PREFERRED_IMAGE_SOURCE_NAME_NONE!s}`.',
    )
    yield (
        PREFERRED_IMAGE_SOURCE_NONE,
        True,
        True,
        f'Preferred image source set to `{PREFERRED_IMAGE_SOURCE_NAME_NONE!s}`.',
    )
    yield (
        PREFERRED_IMAGE_SOURCE_TOUHOU,
        True,
        False,
        f'Preferred image source was already `{PREFERRED_IMAGE_SOURCE_NAME_TOUHOU!s}`.',
    )
    yield (
        PREFERRED_IMAGE_SOURCE_TOUHOU,
        True,
        True,
        f'Preferred image source set to `{PREFERRED_IMAGE_SOURCE_NAME_TOUHOU!s}`.',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_settings_preferred_image_source_change_description(option, value, changed):
    """
    Tests whether ``build_user_settings_preferred_image_source_change_description`` works as intended.
    
    Parameters
    ----------
    option : `int`
        The preferred image source that were set.
    hit : `bool`
        Whether a client option was hit by the user's input.
    changed : `bool`
        Whether value was changed.
    
    Returns
    -------
    output : `str`
    """
    return build_user_settings_preferred_image_source_change_description(option, value, changed)
