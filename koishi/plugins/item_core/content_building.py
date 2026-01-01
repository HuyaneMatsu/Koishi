__all__ = ('produce_flags_section', 'produce_weight')

from .flags import (
    ITEM_FLAG_COSTUME, ITEM_FLAG_EDIBLE, ITEM_FLAG_HEAD, ITEM_FLAG_NPC, ITEM_FLAG_SPECIES, ITEM_FLAG_WEAPON
)


ITEM_FLAGS_AND_NAMES = (
    (ITEM_FLAG_EDIBLE, 'Edible'),
    (ITEM_FLAG_COSTUME, 'Costume'),
    (ITEM_FLAG_HEAD, 'Head accessory'),
    (ITEM_FLAG_SPECIES, 'Species'),
    (ITEM_FLAG_WEAPON, 'Weapon'),
    (ITEM_FLAG_NPC, 'NPC'),
)


def produce_flags_section(flags):
    """
    Produces item flags section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    flags : `int`
        Item flags to produce.
    
    Yields
    ------
    part : `int`
    """
    first = True
    
    for flag, name in ITEM_FLAGS_AND_NAMES:
        if not flags & flag:
            continue
        
        if first:
            first = False
        else:
            yield '\n'
        
        yield '- '
        yield name


def produce_weight(weight):
    """
    Produces the given weight.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    weight : `int`
        Weight in grams.
    
    Yields
    ------
    part : `str`
    """
    kilo_grams, grams = divmod(weight, 1000)
    yield str(kilo_grams)
    yield '.'
    grams_string = str(grams)
    yield '0' * (3 - len(grams_string))
    yield grams_string
