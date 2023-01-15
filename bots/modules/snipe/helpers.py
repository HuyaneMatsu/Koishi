__all__ = ()

from hata import ComponentType
from hata.ext.slash import Row

from .constants import EMBED_AUTHOR_ID_PATTERN


def is_event_user_same(event, message):
    """
    Returns whether the event's user is same as the source event's user.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The event to match it's original command's invoker to the new invoker.
    message : ``Message``
        The message to check against.
    
    Returns
    -------
    is_event_user_same : `bool`
    """
    interaction = message.interaction
    if (interaction is not None):
        return (event.user is interaction.user)
    
    embed = message.embed
    if embed is None:
        return True
    
    author = embed.author
    if author is None:
        return True
    
    name = author.name
    if (name is None):
        return True
    
    match = EMBED_AUTHOR_ID_PATTERN.fullmatch(name)
    if match is None:
        return True
    
    return (int(match.group(1)) == event.user.id)


def translate_component(component, table):
    """
    Translate the component or it's sub components using the given table.
    
    Parameters
    ----------
    component : ``Component``
        The component to translate.
    table : `dict` of `str`, ``Component``
        Custom-id - component relations.
    
    Returns
    -------
    component : ``Component``
    """
    if component.type is ComponentType.row:
        return Row(*(table.get(sub_component.custom_id, sub_component) for sub_component in component))
    
    return table.get(component.custom_id, component)


def translate_components(components, table):
    """
    Translates the given components.
    
    Parameters
    ----------
    components : `GeneratorType`
        Component generator.
    table : `dict` of `str`, ``Component``
        Custom-id - component relations.
    
    Returns
    -------
    components : `list` of ``Component``
    """
    return [translate_component(component, table) for component in components]


async def propagate_check_error_message(client, event, error_message):
    """
    Propagates the given check error message to the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        the client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    error_message : `str`
        The error message to propagate.
    """
    if not event.is_acknowledged():
        await client.interaction_component_acknowledge(event)
    
    await client.interaction_followup_message_create(event, error_message, show_for_invoking_user_only = True)


async def check_has_manage_emojis_and_stickers_permission(client, event):
    """
    Checks whether the user has manage emojis and sticker permission.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        the client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    has_permissions : `bool`
    """
    if not event.user_permissions.can_manage_emojis_and_stickers:
        await propagate_check_error_message(
            client,
            event,
            '**You** are required to have `manage emojis and stickers` permission to **invoke** any action.',
        )
        return False
    
    guild = event.guild
    if (guild is None) or (not guild.cached_permissions_for(client).can_manage_emojis_and_stickers):
        await propagate_check_error_message(
            client,
            event,
            '**I** require to have `manage emojis and stickers` permission to **execute** any action.',
        )
        return False
    
    return True
