__all__ = ()

from hata import InteractionType
from hata.ext.slash import Button, Row, abort

from ...move_message_core import get_webhook

from .constants import CHANNEL_MOVER_ACTIVE_FROM, CHANNEL_MOVER_ACTIVE_TO


def add_embed_field(embed, name, value, inline = False):
    """
    Adds a field to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to add the field to.
    name : `str`
        Field name.
    value : `str`
        Field value.
    inline : `bool` = `False`, Optional
        Whether the field should be inlined.
    
    Returns
    -------
    embed : ``Embed``
    """
    return embed.add_field(
        name,
        (
            f'```\n'
            f'{value}\n'
            f'```'
        ),
        inline = inline,
    )


def add_embed_thumbnail(embed, guild):
    """
    Adds the guild icon as the embed's thumbnail if applicable.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to add the thumbnail to.
    guild : ``None | Guild``
        Respective guild.
    
    Returns
    -------
    embed : ``Embed``
    """
    if (guild is not None):
        icon_url = guild.icon_url
        if (icon_url is not None):
            embed.add_thumbnail(icon_url)

    return embed


def build_components_continue(source_channel, target_channel, last_message_id):
    """
    Helper function to create continue components to continue a message move operation.
    
    Parameters
    ----------
    source_channel : ``Channel``
        Source channel to move messages from.
    target_channel : ``Channel``
        The target channel to move messages to.
    last_message_id : `int`
        The last moved message's identifier.
    """
    return Row(
        Button(
            'Try to resume',
            custom_id = f'channel_mover.resume.{source_channel.id}.{target_channel.id}.{last_message_id}',
        ),
    )


def check_movable(source_channel, target_channel):
    """
    Checks whether the given source - target channel relation can be moved right now.
    
    Parameters
    ----------
    source_channel : ``Channel``
        The channel to move from.
    target_channel : ``Channel``
        The channel to move to.
    """
    if source_channel is target_channel:
        abort(
            f'The source and the target channel cannot be the same ({source_channel.mention}).'
        )
        
    if source_channel.id in CHANNEL_MOVER_ACTIVE_TO:
        abort(
            f'The source channel ({source_channel.mention}) is targeted by an other move.\n'
            f'Cannot move from it for the while.'
        )
    
    if target_channel.id in CHANNEL_MOVER_ACTIVE_FROM:
        abort(
            f'The target channel ({source_channel.mention}) is being moved.\n'
            f'Cannot move into it for the while.'
        )


async def try_initialize_channel_move(client, event, source_channel, target_channel):
    """
    Tries to initialize the channel move by creating the required webhook.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client in context.
    event : ``InteractionEvent``
        The received interaction event.
    source_channel : ``Channel``
        The channel to move from.
    target_channel : ``Channel``
        The channel to move to.
    
    Returns
    -------
    webhook : ``Webhook``
    """
    CHANNEL_MOVER_ACTIVE_FROM.add(source_channel.id)
    CHANNEL_MOVER_ACTIVE_TO.add(target_channel.id)
    try:
        if target_channel.is_in_group_thread():
            channel_id = target_channel.parent_id
        else:
            channel_id = target_channel.id
        
        
        if event.type is InteractionType.message_component:
            await client.interaction_component_acknowledge(event)
            
        await (
            type(client).interaction_response_message_create
                if event.type is InteractionType.application_command else
            type(client).interaction_followup_message_create
        )(
            client,
            event,
            'Initializing channel move.',
            show_for_invoking_user_only = True,
        )
        
        webhook = await get_webhook(client, channel_id)
    except:
        CHANNEL_MOVER_ACTIVE_FROM.discard(source_channel.id)
        CHANNEL_MOVER_ACTIVE_TO.discard(target_channel.id)
        raise
    
    return webhook
