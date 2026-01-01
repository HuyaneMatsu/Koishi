__all__ = ()

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from ..item_core import produce_flags_section, produce_weight
from ..item_modifier_core import produce_modifiers_section


def produce_item_inspect_description(item):
    """
    Produces item inspect description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item : ``Item``
        The selected item.
    
    Yields
    ------
    part : `str`
    """
    yield '## '
    
    emoji = item.emoji
    if (emoji is not None):
        yield emoji.as_emoji
        yield ' '
    
    yield item.name
    
    description = item.description
    if (description is not None):
        yield '\n\n'
        yield description
    
    yield '\n\n### Trading information\nWeight: '
    yield from produce_weight(item.weight)
    yield ' kg\nValue: '
    yield str(item.value)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    
    flags = item.flags
    if flags:
        yield '\n### Categories\n'
        yield from produce_flags_section(flags)
    
    modifiers = item.modifiers
    if (modifiers is not None):
        yield '\n### Modifiers\n'
        yield from produce_modifiers_section(modifiers)
