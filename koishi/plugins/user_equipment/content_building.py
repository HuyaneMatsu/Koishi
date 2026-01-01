__all__ = ()

from ..item_modifier_core import produce_modifiers_section


def produce_equipped_item_description(title, item, item_emoji_default, item_name_default):
    """
    Produces equipped item description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    title : `str`
        Title to show.
    
    item : ``None | Item``
        Item to render.
    
    item_emoji_default : ``None | Emoji``
        Emoji to use if item is `None`.
    
    item_name_default : ``None | Emoji``
        Name to use if item is `None`.
    
    Yields
    ------
    part : `str`
    """
    if item is None:
        item_emoji = item_emoji_default
        item_name = item_name_default
        item_modifiers = None
        
    else:
        item_emoji = item.emoji
        item_name = item.name
        item_modifiers = item.modifiers
    
    yield '### '
    yield title
    yield ': '
    if (item_emoji is not None):
        yield item_emoji.as_emoji
        yield ' '
    
    yield item_name
    
    if (item_modifiers is not None):
        yield '\n'
        yield from produce_modifiers_section(item_modifiers)
