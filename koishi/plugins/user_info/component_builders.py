__all__ = ('build_user_info_components',)

from hata.ext.slash import Button, Row

from .constants import ICON_KIND_AVATAR, ICON_KIND_BANNER, ICON_SOURCE_GLOBAL, ICON_SOURCE_GUILD


def build_user_info_components(user, guild_id):
    """
    Builds user info components.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user to generate the components for.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    components : ``Component``
    """
    user_id = user.id
    
    if user.get_guild_profile_for(guild_id) is None:
        components = Row(
            Button('Show avatar', custom_id = f'user.info.{user_id}.{ICON_KIND_AVATAR}.{ICON_SOURCE_GLOBAL}'),
            Button('Show banner', custom_id = f'user.info.{user_id}.{ICON_KIND_BANNER}.{ICON_SOURCE_GLOBAL}'),
        )
    else:
        components = Row(
            Button('Show global avatar', custom_id = f'user.info.{user_id}.{ICON_KIND_AVATAR}.{ICON_SOURCE_GLOBAL}'),
            Button('Show guild avatar', custom_id = f'user.info.{user_id}.{ICON_KIND_AVATAR}.{ICON_SOURCE_GUILD}'),
            Button('Show global banner', custom_id = f'user.info.{user_id}.{ICON_KIND_BANNER}.{ICON_SOURCE_GLOBAL}'),
            Button('Show guild banner', custom_id = f'user.info.{user_id}.{ICON_KIND_BANNER}.{ICON_SOURCE_GUILD}'),
        )
    
    return components
