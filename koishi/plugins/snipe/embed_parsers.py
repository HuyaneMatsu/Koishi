__all__ = ()

from hata import EMOJIS, Emoji

from .constants import MATCH_GUILD_ID_IN_FOOTER, MATCH_ID_IN_FIELD_VALUE, MATCH_NAME_IN_FIELD_VALUE


def parse_source_message_url(message):
    """
    Parses the originally sniped message's url from the given embed.
    
    Parameters
    ----------
    message : ``Message``
        The message to check.
    
    Returns
    -------
    message_url : `None`, `str`
    """
    embed = message.embed
    if embed is None:
        return
    
    embed_author = embed.author
    if embed_author is None:
        return
    
    return embed_author.url


def get_entity_id_from_event(event):
    """
    Parses the entity's identifier from the given event's message.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    entity_id : `int`
    """
    message = event.message
    if message is None:
        return 0
    
    embed = message.embed
    if embed is None:
        return 0
    
    return get_entity_id_from_embed(embed)


def get_guild_and_entity_id_from_event(event):
    """
    Parses the guild's and the entity's identifier from the given event's message.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    guild_id : `int`
    entity_id : `int`
    """
    message = event.message
    if message is None:
        return 0, 0
    
    embed = message.embed
    if embed is None:
        return 0, 0
    
    return get_guild_id_from_embed(embed), get_entity_id_from_embed(embed)
    

def get_entity_id_from_embed(embed):
    """
    Parses the entity's identifier from the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to parse from.
    
    Returns
    -------
    entity_id : `int`
    """
    fields = embed.fields
    if (fields is None) or len(fields) < 2:
        return 0
    
    field = fields[1]
    match = MATCH_ID_IN_FIELD_VALUE.search(field.value)
    if match is None:
        return 0
    
    return int(match.group(0))


def get_guild_id_from_embed(embed):
    """
    Parses out the guild's identifier from the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to parse from.
    
    Returns
    -------
    guild_id : `int`
    """
    footer = embed.footer
    if footer is None:
        return 0
    
    footer_text = footer.text
    if footer_text is None:
        return 0
    
    match = MATCH_GUILD_ID_IN_FOOTER.fullmatch(footer_text)
    if match is None:
        return 0
    
    return int(match.group(1))


def get_emoji_name_and_animated_from_embed(embed):
    """
    Parses the emoji's name and whether it is animated from the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to parse from.
    
    Returns
    -------
    name : `str`
    animated : `bool`
    """
    url = embed.url
    if url is None:
        animated = False
    else:
        animated = url.endswith('.gif')
    
    fields = embed.fields
    if fields is None:
        name = ''
    else:
        field = fields[0]
        match = MATCH_NAME_IN_FIELD_VALUE.search(field.value)
        if match is None:
            name = ''
        else:
            name = match.group(0)
    
    return name, animated


def get_emoji_from_event(event):
    """
    Parses back the emoji of the given event.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    emoji : ``None | Emoji``
    """
    message = event.message
    if message is None:
        return None
    
    embed = message.embed
    if embed is None:
        return None
    
    emoji_id = get_entity_id_from_embed(embed)
    if not emoji_id:
        return None
    
    emoji = EMOJIS.get(emoji_id, None)
    if emoji is None:
        emoji = Emoji._create_partial(emoji_id, *get_emoji_name_and_animated_from_embed(embed))
    
    return emoji
