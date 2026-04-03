__all__ = ('produce_modifiers_section',)

from .helpers import get_modifier_name_and_value_producer_and_amount_postfix


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
        
        (
            modifier_name,
            value_producer,
            modifier_amount_postfix,
        ) = get_modifier_name_and_value_producer_and_amount_postfix(modifier.type)
        
        amount = modifier.amount
        yield ('+' if amount >= 0 else '-')
        amount = abs(amount)
        
        if value_producer is None:
            yield str(amount)
        else:
            yield from value_producer(amount)
            
        if (modifier_amount_postfix is not None):
            yield modifier_amount_postfix
        
        yield ' '
        yield modifier_name
        continue
