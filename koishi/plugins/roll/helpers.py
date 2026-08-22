__all__ = ()

from random import random
from math import floor

from .constants import DICE_PATTERN


def parse_dice_string(dice_string):
    """
    Parses dice string.
    
    Parameters
    ----------
    dice_string : `None | str`
        Dice string to parse.
    
    Returns
    -------
    output : `None | (int, int, int)`
    """
    while True:
        if dice_string is None:
            dice_count = 1
            dice_sides = 6
            fix_amount = 0
            break
        
        dice_format = ''.join(dice_string.split())
        if (not dice_format):
            dice_count = 1
            dice_sides = 6
            fix_amount = 0
            break
        
        if dice_format.isdigit():
            dice_count = int(dice_format)
            dice_sides = 6
            fix_amount = 0
            break
        
        match = DICE_PATTERN.fullmatch(dice_format)
        if (match is not None):
            dice_count_string, dice, dice_sides_string, fix_added_string, fix_amount_string = match.groups()
            if (dice is None):
                dice_count = 0
                dice_sides = 0
            else:
                if dice_count_string is None:
                    dice_count = 1
                else:
                    dice_count = int(dice_count_string)
                
                if dice_sides_string is None:
                    dice_sides = 6
                else:
                    dice_sides = int(dice_sides_string)
            
            if fix_added_string is None:
                fix_amount = 0
            else:
                fix_amount = int(fix_amount_string)
                if fix_added_string != '+':
                    fix_amount = - fix_amount
            break
        
        return None
    
    return dice_count, dice_sides, fix_amount


def iter_roll_dices(dice_count, dice_sides, luck):
    """
    Rolls dices dice count times.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    dice_count : `int`
        Amount of dices to roll.
    
    dice_sides : `int`
        How much sides each side have.
    
    luck : `int`
        How lucky the user is.
    
    Returns
    -------
    roll : `int`
    """
    if not luck:
        for _ in range(dice_count):
            yield 1 + floor(random() * dice_sides)
        return
    
    if luck > 0:
        luck_positive = True
    else:
        luck_positive = False
        luck = -luck
    
    for _ in range(dice_count):
        luck_local = luck
        factor = random()
        
        while True:
            if luck_local >= 100:
                luck_local -= 100
            
            elif luck_local > random() * 100.0:
                luck_local = 0
                
            else:
                break
            
            local_factor = random()
            if (local_factor > factor) if luck_positive else (local_factor < factor):
                factor = local_factor
            
            if not luck_local:
                break
        
        yield 1 + floor(factor * dice_sides)
