__all__ = ()

from .constants import DECIMAL_RP


def get_selected_entity_id(event):
    """
    Gets the selected entity's identifier. Used on component select interaction events.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        Received interaction event.
    
    Returns
    -------
    entity_id : `int`
        Returns `-1` on failure.
    """
    values = event.values
    if values is None:
        return -1
    
    value = values[0]
    try:
        entity_id = int(value)
    except ValueError:
        entity_id = - 1
    
    return entity_id


def is_event_user_same(event):
    """
    Checks whether the event's user is the same as who called it originally.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        Received interaction event.
    
    Returns
    -------
    user_same : `bool`
    """
    message = event.message
    if message is None:
        return False
    
    interaction = message.interaction
    if interaction is None:
        return False
    
    return event.user_id == interaction.user_id


def get_name_and_page(event):
    """
    Gets the selected page's query and index. Used when moving either left or right between pages.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        Received interaction event.
    
    Returns
    -------
    name_and_page : `None | (str, int)`
    """
    message = event.message
    if message is None:
        return
    
    embed = message.embed
    if embed is None:
        return
    
    embed_title = embed.title
    if embed_title is None:
        return
    
    embed_footer = embed.footer
    if embed_footer is None:
        return
    
    embed_footer_text = embed_footer.text
    if embed_footer_text is None:
        return
    
    matched = DECIMAL_RP.match(embed_footer_text, len('Page: '))
    if matched is None:
        return
    
    page_identifier = int(matched.group(0))
    name = embed_title[len('Search result for: '):]
    
    return name, page_identifier
