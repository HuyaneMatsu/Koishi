__all__ = ()


def produce_roll_description(dice_count, dice_sides, fix_amount, luck, rolls, result):
    """
    Produces roll description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    dice_count : `int`
        Amount of dices to roll.
    
    dice_sides : `int`
        How much sides each side have.
    
    fix_amount : `int`
        Added or subtracted amount.
    
    luck : `int`
        How lucky the user is.
    
    rolls : `list<int>`
        Rolls.
    
    result : `int`
        The sum of all rolls and the fix amount.
    
    Yields
    ------
    part : `str`
    """
    if (dice_count and dice_sides) or fix_amount:
        yield 'Rolling '
        
        if (dice_count and dice_sides):
            yield str(dice_count)
            yield 'd'
            yield str(dice_sides)
        
        if fix_amount:
            yield ('+' if fix_amount > 0 else '-')
            yield str(abs(fix_amount))
        
        if luck:
            yield ' with '
            yield str(luck)
            yield ' luck'
        
        yield '\n'
    
    if dice_count > 1:
        yield 'Rolls: '
        for index in range(len(rolls)):
            if index:
                yield ', '
            yield str(rolls[index])
        yield '\n'
    
    yield 'Result: **'
    yield str(result)
    yield '**'
