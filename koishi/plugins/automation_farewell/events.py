__all__ = ()

from hata import Embed, now_as_id

from ...bot_utils.multi_client_utils import get_first_client_with_message_create_permissions_from
from ...bots import FEATURE_CLIENTS

from ..automation_core import get_farewell_fields
from ..embed_image_refresh import schedule_image_refresh

from .farewell_styles import get_farewell_style


async def farewell_user(client, guild, user, farewell_style, farewell_channel):
    """
    Farewells the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The guild the farewell the user at.
    user : ``ClientUserBase``
        The user to farewell.
    farewell_style : ``FarewellStyle``
        The farewell style to use.
    farewell_channel : ``Channel``
        The channel to farewell the user at.
    """
    seed = guild.id ^ user.id
    
    items = farewell_style.items
    item = items[seed % len(items)]
    
    message_content = item.message_content_builder(user.full_name)
    
    color = (now_as_id() >> 22) & 0xffffff
    
    message = await client.message_create(
        farewell_channel,
        content = f'> {message_content}',
        embed = Embed(color = color).add_image(item.image).add_footer(f'By {item.image_creator}.'),
        silent = True,
    )
    schedule_image_refresh(client, message)


@FEATURE_CLIENTS.events
async def guild_user_delete(client, guild, user, guild_profile):
    """
    Handles a guild user delete event.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    guild : ``Guild``
        The guild the user has been deleted from.
    user : ``ClientUserBase``
        The deleted user.
    guild_profile : `None`, ``GuildProfile``
        The user's guild profile.
    """
    farewell_fields = get_farewell_fields(guild.id)
    if (farewell_fields is None):
        return
    
    farewell_channel, farewell_style_name = farewell_fields
    
    if client is not get_first_client_with_message_create_permissions_from(farewell_channel, FEATURE_CLIENTS):
        return
    
    farewell_style = get_farewell_style(farewell_style_name, client.id)
    
    # Send message
    await farewell_user(client, guild, user, farewell_style, farewell_channel)
