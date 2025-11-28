__all__ = ()

def produce_successful_item_discard_description(item, discarded_amount, new_amount):
    """
    Produces a successful item discard message.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item : ``Item``
        The selected item.
    
    discarded_amount : `int`
        The amount of cards discarded.
    
    new_amount : `int`
        Items left.
    
    Yields
    ------
    part : `str`
    """
    yield 'You discarded '
    yield str(discarded_amount)
    yield ' '
    
    emoji = item.emoji
    if (emoji is not None):
        yield emoji.as_emoji
        yield ' '
    
    yield item.name
    
    if new_amount:
        yield ', keeping '
        yield str(new_amount)
    
    yield '.'
