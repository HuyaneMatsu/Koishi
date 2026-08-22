__all__ = ()

from hata.ext.slash import P

from ...bots import FEATURE_CLIENTS

from .component_building import build_roll_response_components
from .constants import (
    DICE_COUNT_THRESHOLD_LOWER, DICE_COUNT_THRESHOLD_UPPER, DICE_FIX_AMOUNT_THRESHOLD_LOWER,
    DICE_FIX_AMOUNT_THRESHOLD_UPPER, DICE_SIZE_THRESHOLD_LOWER, DICE_SIZE_THRESHOLD_UPPER, LUCK_AMOUNT_THRESHOLD_LOWER,
    LUCK_AMOUNT_THRESHOLD_UPPER
)
from .custom_ids import CUSTOM_ID_ROLL_PATTERN
from .helpers import iter_roll_dices, parse_dice_string


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def roll(
    client,
    interaction_event,
    dice_string : (str, 'Dices to roll.', 'dice-format') = None,
    luck : P(int, min_value = LUCK_AMOUNT_THRESHOLD_LOWER,  max_value = LUCK_AMOUNT_THRESHOLD_UPPER) = 0,
):
    """
    Rolls with dices.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    dice_string : `None | str` = `None`, Optional
        Dice string to roll.
    
    luck : `int` = `0`, Optional
        Luck amount.
    """
    while True:
        parse_result = parse_dice_string(dice_string)
        if parse_result is None:
            error_message = (
                'Invalid dice format, please use any of the following:\n'
                '\*no input\* -> rolls a single dice with 6 sides\n'
                '2 -> rolls 2 dices with 6 sides\n'
                'd7 -> tolls a single dice with 7 sides\n'
                '2d7 -> rolls 2 dices with 7 sides\n'
                '+6 -> adds 6\n'
                '2d+7 -> rolls 2 dices with 7 sides and then adds 6'
            )
            break
        
        dice_count, dice_sides, fix_amount = parse_result
        
        if dice_count < DICE_COUNT_THRESHOLD_LOWER:
            error_message = f'Dice count less than the lower threshold {dice_count} < {DICE_COUNT_THRESHOLD_LOWER}.'
            break
        
        if not dice_count:
            dice_sides = 0
        else:
            if dice_count > DICE_COUNT_THRESHOLD_UPPER:
                error_message = f'Dice count greater than the upper threshold {dice_count} > {DICE_COUNT_THRESHOLD_UPPER}.'
                break
            
            if dice_sides < DICE_SIZE_THRESHOLD_LOWER:
                error_message = f'Dice sides less than the lower threshold {dice_sides} < {DICE_SIZE_THRESHOLD_LOWER}.'
                break
        
        if dice_sides > DICE_SIZE_THRESHOLD_UPPER:
            error_message = f'Dice sides greater than the upper threshold {dice_sides} > {DICE_SIZE_THRESHOLD_UPPER}.'
            break
        
        if fix_amount < DICE_FIX_AMOUNT_THRESHOLD_LOWER:
            error_message = f'Fix amount less than the lower threshold {fix_amount} < {DICE_FIX_AMOUNT_THRESHOLD_LOWER}.'
            break
        
        if fix_amount > DICE_FIX_AMOUNT_THRESHOLD_UPPER:
            error_message = f'Fix amount greater than the upper threshold {fix_amount} > {DICE_FIX_AMOUNT_THRESHOLD_UPPER}.'
            break
        
        if luck < LUCK_AMOUNT_THRESHOLD_LOWER:
            error_message = f'Luck less than the lower threshold {luck} < {LUCK_AMOUNT_THRESHOLD_LOWER}.'
            break
        
        if luck > LUCK_AMOUNT_THRESHOLD_UPPER:
            error_message = f'Luck greater than the upper threshold {luck} > {LUCK_AMOUNT_THRESHOLD_UPPER}.'
            break
        
        rolls = [*iter_roll_dices(dice_count, dice_sides, luck)]
        result = fix_amount + sum(rolls)
        
        await client.interaction_response_message_create(
            interaction_event,
            components = build_roll_response_components(dice_count, dice_sides, fix_amount, luck, rolls, result),
        )
        return
        
    await client.interaction_response_message_create(
        interaction_event,
        content = error_message,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ROLL_PATTERN)
async def handle_additional_dice_roll(
    client,
    interaction_event,
    dice_count,
    dice_sides,
    fix_amount_positive,
    fix_amount,
    luck_positive,
    luck,
):
    """
    Handles an additional dice roll interaction.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    dice_count : `str`
        Amount of dices to roll as a string representing a hexadecimal integer.
    
    dice_sides : `str`
        How much sides each side have as a string representing a hexadecimal integer.
    
    fix_amount_positive : `str`
        Whether fix amount is positive as a string representing a hexadecimal integer.
    
    fix_amount : `str`
        Added or subtracted amount as a string representing a hexadecimal integer.
    
    luck_positive : `str`
        Whether luck is positive as a string representing a hexadecimal integer.
    
    luck : `str`
        How lucky the user is as a string representing a hexadecimal integer.
    """
    try:
        dice_count = int(dice_count, 16)
        dice_sides = int(dice_sides, 16)
        fix_amount_positive = int(fix_amount_positive, 16)
        fix_amount = int(fix_amount, 16)
        luck_positive = int(luck_positive, 16)
        luck = int(luck, 16)
    except ValueError:
        return
    
    if not fix_amount_positive:
        fix_amount = -fix_amount
    
    if not luck_positive:
        luck = -luck
    
    rolls = [*iter_roll_dices(dice_count, dice_sides, luck)]
    result = fix_amount + sum(rolls)
    
    await client.interaction_component_acknowledge(interaction_event)
    await client.interaction_followup_message_create(
        interaction_event,
        components = build_roll_response_components(dice_count, dice_sides, fix_amount, luck, rolls, result),
    )
    return
