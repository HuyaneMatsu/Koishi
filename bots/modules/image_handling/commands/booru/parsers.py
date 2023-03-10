__all__ = ()


def parse_image_url(event):
    """
    Gets the current image's url from the given event's message.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    image_url : `None`, `str`
    """
    message = event.message
    if message is None:
        return None
    
    embed = message.embed
    if embed is None:
        return None
    
    image = embed.image
    if image is None:
        return None
    
    return image.url


def event_user_matches(event):
    """
    Returns whether the event's user matches the original invoker.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    matching : `bool`
    """
    if not event.guild_id:
        # Direct message
        return True
    
    message = event.message
    if message is None:
        return False
    
    interaction = message.interaction
    if interaction is None:
        return False
    
    return event.user is interaction.user
