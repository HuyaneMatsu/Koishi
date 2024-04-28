import vampytest
from hata import Embed, User

from ..builders import build_user_settings_preferred_client_change_embed


def _iter_options():
    client_name = 'satori'
    client = User.precreate(202402260009, name = client_name)
    user = User.precreate(202402260010)
    
    expected_output = Embed(
        'Great success!',
        f'Preferred client set to `{client_name!s}`.'
    ).add_thumbnail(
        user.avatar_url,
    )
    yield user, client, True, True, expected_output


    expected_output = Embed(
        'Uoh',
        'Could not match any available clients.'
    ).add_thumbnail(
        user.avatar_url,
    )
    yield user, None, False, False, expected_output


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_settings_preferred_client_change_embed(user, option, value, changed):
    """
    Tests whether ``build_user_settings_preferred_client_change_embed`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who's notification settings are changed.
    option : `None | ClientUserBase`
        The preferred client.
    value : `bool`
        The new value to set.
    changed : `bool`
        Whether value was changed.
    
    Returns
    -------
    embed : ``Embed``
    """
    output = build_user_settings_preferred_client_change_embed(user, option, value, changed)
    vampytest.assert_instance(output, Embed)
    return output
