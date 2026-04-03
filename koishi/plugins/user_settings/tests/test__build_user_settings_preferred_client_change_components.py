import vampytest
from hata import Component, User, create_text_display

from ..builders import build_user_settings_preferred_client_change_components


def _iter_options():
    client_name = 'satori'
    client = User.precreate(202402260009, name = client_name)
    
    yield (
        client,
        0,
        True,
        True,
        [
            create_text_display(f'Preferred client set to `{client_name!s}`.'),
        ],
    )
    
    yield (
        None,
        0,
        False,
        False,
        [
            create_text_display('Could not match any available clients.'),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_settings_preferred_client_change_components(client, guild_id, value, changed):
    """
    Tests whether ``build_user_settings_preferred_client_change_components`` works as intended.
    
    Parameters
    ----------
    client : ``None | ClientUserBase`
        The client who were set as prefer`red client.
    
    guild_id : `int`
        The local guild's name.
    
    value : `bool`
        The new value to set.
    
    changed : `bool`
        Whether value was changed.
    
    Returns
    -------
    components : ``list<Component>``
    """
    output = build_user_settings_preferred_client_change_components(client, guild_id, value, changed)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
