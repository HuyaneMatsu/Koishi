__all__ = ()

from re import compile as re_compile

from ...bots import FEATURE_CLIENTS

from .constants import ICON_SOURCE_RP_GROUP, ICON_KINDS_RP_GROUP
from .embed_builders import build_user_icon_embed


@FEATURE_CLIENTS.interactions(
    custom_id = re_compile(f'user\\.info\\.(\\d+)\\.{ICON_KINDS_RP_GROUP}\\.{ICON_SOURCE_RP_GROUP}'),
)
async def show_user_icon(client, event, user_id, icon_kind, icon_source):
    """
    Shows the user's icon.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the interaction.
    event : ``InteractionEvent``
        The received interaction event.
    user_id : `str`
        The user's identifier to show its icon of. (Converted to integer.)
    icon_kind : `int`
        The icon's kind. (Converted to integer.)
    icon_source : `int`
        The icon's source. (Converted to integer.)
    """
    user_id = int(user_id)
    icon_kind = int(icon_kind)
    icon_source = int(icon_source)
    
    yield
    
    user = await client.user_get(user_id, force_update = True)
    
    embed = build_user_icon_embed(user, event.guild_id, icon_kind, icon_source)
    await client.interaction_followup_message_create(event, embed = embed, show_for_invoking_user_only = True)
