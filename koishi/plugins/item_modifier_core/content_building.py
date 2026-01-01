__all__ = ('produce_modifiers_section',)

from .helpers import get_modifier_name_and_amount_postfix


def produce_modifiers_section(modifiers):
    """
    Produces a modifiers section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    modifier. : ``tuple<Modifier>``
        The modifiers to produce.
    
    Yields
    ------
    part : `str`
    """
    first = True
    
    for modifier in modifiers:
        if first:
            first = False
        else:
            yield '\n'
        
        yield '- '
        name, postfix = get_modifier_name_and_amount_postfix(modifier.type)
        amount = modifier.amount
        yield ('+' if amount >= 0 else '-')
        yield str(abs(amount))
        if (postfix is not None):
            yield postfix
        
        yield ' '
        yield name
        continue
