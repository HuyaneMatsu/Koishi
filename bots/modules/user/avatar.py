__all__ = ()

from hata import Embed, User

from .constants import ICON_SOURCES, ICON_SOURCES_REVERSED
from .icon_helpers import get_avatar_of


async def user_avatar_command(
    event,
    user : (User, 'Choose a user!') = None,
    icon_source : (ICON_SOURCES, 'Which avatar of the user?', 'type') = ICON_SOURCES,
):
    """Shows your or the chosen user's avatar."""
    if user is None:
        user = event.user
    
    icon_url = get_avatar_of(user, event.guild_id, icon_source)
    if icon_url is None:
        icon_url = user.default_avatar_url
    
    return Embed(
        f'{user:f}\'s {ICON_SOURCES_REVERSED[icon_source]} avatar',
        color = (event.id >> 22) & 0xffffff,
        url = icon_url,
    ).add_image(
        icon_url,
    )
