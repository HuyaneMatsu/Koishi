__all__ = ('loot_data_build', 'loot_data_iter')

from struct import Struct


LOOT_STRUCT = Struct('<BIQ')
LOOT_STRUCT_SIZE = LOOT_STRUCT.size


def loot_data_build(looted_items):
    """
    Packs loot into a binary string.
    
    Parameters
    ----------
    looted_items : `list<(int, int, int)>`
        A list of tuple of 3 elements: loot state, item id and given amount.
    
    Returns
    -------
    loot_data : `None | bytes`
    """
    if looted_items:
        return b''.join([LOOT_STRUCT.pack(*looted_item) for looted_item in looted_items])


def loot_data_iter(loot_data):
    """
    Iterates over the given loot data.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    loot_data : `None | bytes`
        Encoded loot data.
    
    Yields
    -------
    looted_item : `(int, int, int)`
    """
    if loot_data is None:
        return
    
    yield from LOOT_STRUCT.iter_unpack(loot_data)
