__all__ = (
    'build_failure_embed_no_item_discarded', 'build_failure_embed_no_item_like', 'build_success_embed_item_discarded',
)

from hata import Embed


def build_failure_embed_no_item_like(value):
    """
    Builds a failure embed for the case when there is no item like the given value in the inventory
    
    Parameters
    ----------
    value : `str`
        The item's name to select.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Oh no',
        f'Could not discard {value!s}, you do not have such an item.',
    )


def build_failure_embed_no_item_discarded(item, new_amount):
    """
    Builds a failure embed for the case when the no items where discarded.
    
    Parameters
    ----------
    item : ``Item``
        The selected item.
    
    new_amount : `int`
        Items left.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Oh no',
        f'You did not discard any of your {new_amount} {item.name}.',
    )


def build_success_embed_item_discarded(item, discarded_amount, new_amount):
    """
    Builds a success embed when the selected item was equipped and there was no previously equipped item.
    
    Parameters
    ----------
    item : ``Item``
        The selected item.
    
    discarded_amount : `int`
        The amount of cards discarded.
    
    new_amount : `int`
        Items left.
    
    Returns
    -------
    embed : ``Embed``
    """
    description_parts = []
    
    description_parts.append('You discarded ')
    description_parts.append(str(discarded_amount))
    description_parts.append(' ')
    description_parts.append(item.name)
    
    if new_amount:
        description_parts.append(', keeping ')
        description_parts.append(str(new_amount))
    
    description_parts.append('.')
    
    return Embed(
        'Great success!',
        ''.join(description_parts),
    )
