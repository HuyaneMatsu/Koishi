__all__ = ('adventure_action_notifier', 'adventure_return_notifier',)

from config import MARISA_MODE

from ...bot_utils.user_getter import get_user
from ...bot_utils.utils import send_embed_to

from .component_building import (
    build_adventure_action_notification_components, build_adventure_return_notification_components
)

try:
    from ..user_settings import (
        USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_ADVENTURE_ACTION, get_one_user_settings, get_preferred_client_for_user
    )
except ImportError:
    if not MARISA_MODE:
        raise
    
    from scarletio import copy_docs
    
    from ...bots import MAIN_CLIENT
    
    USER_SETTINGS_AVAILABLE = False
    USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_ADVENTURE_ACTION = 0

else:
    USER_SETTINGS_AVAILABLE = True


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


# Overwrite the function if user settings are not available.
if not USER_SETTINGS_AVAILABLE:
    @copy_docs(adventure_return_notifier)
    async def adventure_return_notifier(adventure):
        user = await get_user(adventure.user_id)
        await send_embed_to(
            MAIN_CLIENT,
            user,
            None,
            build_adventure_return_notification_components(adventure),
        )


async def adventure_action_notifier(adventure, adventure_action):
    """
    Notifier for adventure arrival.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Completed adventure.
    
    adventure_action : ``AdventureAction``
        The performed action.
    """
    user_settings = await get_one_user_settings(adventure.user_id)
    # adventure action is toggleable, so check whether the user has it turned on.
    if (user_settings.notification_flags >> USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_ADVENTURE_ACTION) & 1:
        user = await get_user(adventure.user_id)
        await send_embed_to(
            get_preferred_client_for_user(user, user_settings.preferred_client_id, None),
            user,
            None,
            build_adventure_action_notification_components(adventure, adventure_action),
        )


# Overwrite the function if user settings are not available.
if not USER_SETTINGS_AVAILABLE:
    @copy_docs(adventure_action_notifier)
    async def adventure_action_notifier(adventure, adventure_action):
        return
