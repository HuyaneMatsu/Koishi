__all__ = ()

from hata.ext.slash import Option


def _create_emoji_option_value(prefix, emoji):
    """
    Creates an emoji option value.
    
    Parameters
    ----------
    prefix : `str`
        Prefix to use.
    emoji : ``Emoji``
        The emoji to create value for.
    
    Returns
    -------
    value : `str`
    """
    if emoji.is_unicode_emoji():
        emoji_id = 0
        name = emoji.unicode
        animated = ''
    else:
        emoji_id = emoji.id
        name = emoji.name
        animated = format(emoji.animated, 'd')
    
    return _create_option_value(prefix, emoji_id, name, animated)


def _create_option_value(prefix, entity_id, name, animated):
    """
    Creates an option value.
    
    Parameters
    ----------
    prefix : `str`
        Prefix to use to identify the entity type.
    entity_id : `int`
        The entity's identifier.
    name : `str`
        The entity's name.
    animated : `str`
        Whether the entity is animated (emoji only).
    """
    return f'{prefix}:{entity_id}:{name}:{animated}'


def select_option_builder_emoji(emoji):
    """
    Builds a select option for the given emoji.
    
    Parameters
    ----------
    emoji : ``Emoji``
        The emoji to create option for.
    
    Returns
    -------
    option : ``StringSelectOption``
    """
    return Option(_create_emoji_option_value('e', emoji), emoji.name, emoji)


def select_option_builder_reaction(reaction):
    """
    Builds a select option for the given reaction.
    
    Parameters
    ----------
    reaction : ``Emoji``
        The reaction to create option for.
    
    Returns
    -------
    option : ``StringSelectOption``
    """
    return Option(_create_emoji_option_value('r', reaction), reaction.name, reaction)


def select_option_builder_sticker(sticker):
    """
    Builds a select option for the given sticker.
    
    Parameters
    ----------
    sticker : ``Sticker``
        The sticker to create option for.
    
    Returns
    -------
    option : ``StringSelectOption``
    """
    return Option(_create_option_value('s', sticker.id, '', ''), sticker.name)
