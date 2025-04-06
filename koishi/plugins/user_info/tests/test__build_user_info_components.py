import vampytest
from hata import Component, GuildProfile, User
from hata.ext.slash import Button, Row

from ..component_builders import build_user_info_components


def _iter_options():
    user_id = 202503300000
    guild_id = 202503300001
    
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile()
    
    yield (
        user,
        0,
        Row(
            Button('Show avatar', custom_id = f'user.info.{user_id}.1.2'),
            Button('Show banner', custom_id = f'user.info.{user_id}.2.2'),
        ),
    )
    
    yield (
        user,
        guild_id,
        Row(
            Button('Show global avatar', custom_id = f'user.info.{user_id}.1.2'),
            Button('Show guild avatar', custom_id = f'user.info.{user_id}.1.3'),
            Button('Show global banner', custom_id = f'user.info.{user_id}.2.2'),
            Button('Show guild banner', custom_id = f'user.info.{user_id}.2.3'),
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_info_components(user, guild_id):
    """
    Tests whether ``build_user_info_components`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user to generate the components for.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``Component``
    """
    output = build_user_info_components(user, guild_id)
    vampytest.assert_instance(output, Component)
    return output
