__all__ = ('adventure_return_notifier',)

from ...bot_utils.user_getter import get_user
from ...bot_utils.utils import send_embed_to

from ..user_settings import get_one_user_settings, get_preferred_client_for_user

from .component_builders import build_adventure_return_notification_components


async def adventure_return_notifier(adventure):
    """
    Notifier for adventure arrival.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Completed adventure.
    """
    user_settings = await get_one_user_settings(adventure.user_id)
    user = await get_user(adventure.user_id)
    await send_embed_to(
        get_preferred_client_for_user(user, user_settings.preferred_client_id, None),
        user,
        None,
        build_adventure_return_notification_components(adventure),
    )
