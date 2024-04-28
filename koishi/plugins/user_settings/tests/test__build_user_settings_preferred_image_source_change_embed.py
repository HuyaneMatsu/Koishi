import vampytest
from hata import Embed, User

from ..builders import build_user_settings_preferred_image_source_change_embed
from ..constants import PREFERRED_IMAGE_SOURCE_NAME_TOUHOU, PREFERRED_IMAGE_SOURCE_NONE, PREFERRED_IMAGE_SOURCE_TOUHOU


def _iter_options():
    user = User.precreate(202404270000)
    
    expected_output = Embed(
        'Great success!',
        f'Preferred image source set to `{PREFERRED_IMAGE_SOURCE_NAME_TOUHOU!s}`.'
    ).add_thumbnail(
        user.avatar_url,
    )
    yield user, PREFERRED_IMAGE_SOURCE_TOUHOU, True, True, expected_output


    expected_output = Embed(
        'Uoh',
        'Could not match any preferred image source.'
    ).add_thumbnail(
        user.avatar_url,
    )
    yield user, PREFERRED_IMAGE_SOURCE_NONE, False, False, expected_output


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_settings_preferred_image_source_change_embed(user, option, value, changed):
    """
    Tests whether ``build_user_settings_preferred_image_source_change_embed`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who's notification settings are changed.
    option : `int`
        The preferred image source that were set.
    value : `bool`
        The new value to set.
    changed : `bool`
        Whether value was changed.
    
    Returns
    -------
    embed : ``Embed``
    """
    output = build_user_settings_preferred_image_source_change_embed(user, option, value, changed)
    vampytest.assert_instance(output, Embed)
    return output
