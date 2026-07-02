__all__ = (
    'butcher_calculate_step', 'butcher_calculate_done', 'butcher_done_append', 'butcher_estimate_energy_cost',
    'butcher_estimate_loot_chance_and_amounts'
)

from math import ceil
from random import Random

from ..seeding import step_seed, step_seed_initial

from .flags import ITEM_FLAG_BUTCHERABLE
from .utils import get_item_nullable


def butcher_get_part_count(item):
    """
    Gets how much further butcherable parts the given item has.
    
    Parameters
    ----------
    item : ``Item``
        Item to get count of.
    
    Returns
    -------
    count : `int`
    """
    count = 0
    
    options_butcher = item.options_butcher
    if (options_butcher is not None):
        for option in options_butcher:
            item = get_item_nullable(option.item_id)
            if (item is None) or not (item.flags & ITEM_FLAG_BUTCHERABLE):
                continue
            
            count += (1 + butcher_get_part_count(item)) * option.amount
            continue
    
    return count


def butcher_estimate_loot_chance_and_amounts(options, multiplier):
    """
    Estimates the loot for the given options.
    
    Parameters
    ----------
    options : ``tuple<OptionButcher>``
        Options for butchering.
    
    multiplier : `float`
        Chance multiplier of the user.
    
    Returns
    -------
    accumulated_amounts_normalised : `list<(int, float, int)>`
    """
    accumulated_amounts = []
    
    for option in reversed(options):
        chance_in = option.chance_in
        chance_out = option.chance_out
        if chance_in == chance_out:
            chance = 1.0
        else:
            chance = (chance_in << 1) / chance_out
            if option.chance_scaling_enabled:
                chance *= multiplier
            
            if chance >= 1.0:
                fraction = 1.0 / chance
                chance = (1.0 - fraction) + (0.5 * fraction)
            else:
                chance = (0.5 * chance) * (2.0 - chance)
        accumulated_amounts.append((option.item_id, chance, option.amount))
    
    accumulated_amounts_normalised = []
    
    while accumulated_amounts:
        item_id, chance, amount_accumulated = accumulated_amounts.pop()
        chance_accumulated = chance * amount_accumulated
        
        for index in reversed(range(len(accumulated_amounts))):
            item_id_iterated, chance_iterated, amount_iterated = accumulated_amounts[index]
            if item_id_iterated != item_id:
                continue
            
            del accumulated_amounts[index]
            
            amount_accumulated += amount_iterated
            chance_accumulated += chance_iterated * amount_iterated
            continue
        
        accumulated_amounts_normalised.append((item_id, chance_accumulated / amount_accumulated, amount_accumulated))
        continue
    
    return accumulated_amounts_normalised


def butcher_estimate_energy_cost(options, multiplier):
    """
    Estimates the energy cost the given options.
    
    Parameters
    ----------
    options : ``tuple<OptionButcher>``
        Options for butchering.
    
    multiplier : `float`
        Chance multiplier of the user.
    
    Returns
    -------
    energy_cost : `int`
    """
    energy_cost_accumulated = 0.0
    for option in options:
        energy_cost_accumulated += (
            option.energy_cost_flat +
            option.amount * max(option.energy_cost_scaling_success, option.energy_cost_scaling_failure)
        )
    
    return ceil(energy_cost_accumulated / multiplier)


def get_option_amount(option, random, multiplier):
    """
    Gets amount for the given option.
    
    Parameters
    ----------
    option : ``tuple<OptionButcher>``
        Option  for butchering.
    
    random : `random.Random`
        Random number generator to use.
    
    multiplier : `float`
        Chance multiplier of the user.
    
    Returns
    -------
    amount : `int`
    """
    chance_in = option.chance_in
    chance_out = option.chance_out
    if chance_in == chance_out:
        amount_multiplier = 1.0
    else:
        amount_multiplier = (chance_in << 1) / chance_out
        if option.chance_scaling_enabled:
            amount_multiplier *= multiplier
        
        position = random.random() * 2.0 - 1.0
        negative = position < 0
        
        position *= position
        
        if negative:
            position = -position
        
        position = (position + 1.0) * 0.5
        
        if amount_multiplier >= 1.0:
            amount_multiplier *= position
            if amount_multiplier >= 1.0:
                amount_multiplier = 1.0
        elif random.random() > amount_multiplier:
            amount_multiplier *= position
        else:
            amount_multiplier = position
    
    return round(option.amount * amount_multiplier)


def butcher_calculate_step(item, index, seed, multiplier):
    """
    Calculate a single butcher step.
    
    Parameters
    ----------
    item : ``Item``
        The item to butcher.
    
    index : `int`
        The item's index in the butcher queue. `-1` if initial.
    
    seed : `int`
        Seed to use.
    
    multiplier : `float`
        Chance multiplier of the user.
    
    Returns
    -------
    accumulated_amounts_normalised_and_accumulated_energy_cost : ``(None | list<(int, int)>, int)``
    """
    options_butcher = item.options_butcher
    if (options_butcher is None):
        return None, 0
    
    seed = step_seed_initial(seed, index + 2)
    
    return butcher_calculate_amounts_and_energy_cost(
        options_butcher, Random(seed), multiplier,
    )


def butcher_calculate_amounts_and_energy_cost(options_butcher, random, multiplier):
    """
    Calculates butcher loot amount and energy cost.
    
    Parameters
    ----------
    options_butcher : ``tuple<OptionButcher>``
        Options for butchering.
    
    random : `random.Random`
        Random number generator to use.
    
    multiplier : `float`
        Chance multiplier of the user.
    
    Returns
    -------
    accumulated_amounts_normalised_and_accumulated_energy_cost : ``(None | list<(int, int)>, int)``
    """
    accumulated_energy_cost = 0
    accumulated_amounts = []
    
    for option in reversed(options_butcher):
        amount = get_option_amount(option, random, multiplier)
        accumulated_energy_cost += (
            option.energy_cost_flat +
            amount * option.energy_cost_scaling_success +
            (option.amount - amount) * option.energy_cost_scaling_failure
        )
        if amount:
            accumulated_amounts.append((option.item_id, amount))
    
    energy_cost = ceil(accumulated_energy_cost / multiplier)
    
    if not accumulated_amounts:
        return None, energy_cost
    
    accumulated_amounts_normalised = []
    
    while accumulated_amounts:
        item_id, amount_accumulated = accumulated_amounts.pop()
        
        for index in reversed(range(len(accumulated_amounts))):
            item_id_iterated, amount_iterated = accumulated_amounts[index]
            if item_id_iterated != item_id:
                continue
            
            del accumulated_amounts[index]
            
            amount_accumulated += amount_iterated
            continue
        
        accumulated_amounts_normalised.append((item_id, amount_accumulated))
        continue
    
    return accumulated_amounts_normalised, energy_cost


def butcher_add_to_amounts_accumulation(butcher_amounts_accumulated, item_id, amount):
    """
    Adds a single amounts into an accumulation.
    
    Parameters
    ----------
    butcher_amounts_accumulated : `None | list<(int, int)>`
        Already accumulated butchered items.
    
    item_id : `int`
        Item identifier to add.
    
    amount : `int`
        Amount to add.
    
    Returns
    -------
    butcher_amounts_accumulated : `list<(int, int)>`
    """
    if butcher_amounts_accumulated is None:
        butcher_amounts_accumulated = [(item_id, amount)]
    
    else:
        for index in range(len(butcher_amounts_accumulated)):
            item_id_iterated, amount_iterated = butcher_amounts_accumulated[index]
            if item_id_iterated == item_id:
                butcher_amounts_accumulated[index] = (item_id, amount_iterated + amount)
                break
        else:
            butcher_amounts_accumulated.append((item_id, amount))
    
    return butcher_amounts_accumulated


def butcher_calculate_done(item, seed, butcher_flags, multiplier):
    """
    Calculates the done amounts, the energy cost and what else can be further butchered-
    
    Parameters
    ----------
    item : ``Item``
        Item to butcher.
    
    seed : `int`
        Seed to use for generation.
    
    butcher_flags : `int`
        Flags described which body parts were already butchered.
    
    multiplier : `float`
        Multiplier of the user for this given action.
    
    Returns
    -------
    butcher_amounts_and_energy_cost_and_butcherables : ``(None | list<(int, int), int, None | list<(Item, int)>)``
    """
    butcher_queue = [(item, -1, seed)]
    butcher_amounts_accumulated = None
    butcherables = None
    energy_cost_accumulated = 0
    
    while butcher_queue:
        item, index, seed = butcher_queue.pop(0)
        
        options_butcher = item.options_butcher
        if options_butcher is None:
            continue
        
        butcher_amounts, energy_cost = butcher_calculate_amounts_and_energy_cost(
            options_butcher, Random(seed), multiplier
        )
        energy_cost_accumulated += energy_cost
        if (butcher_amounts is None):
            continue
        
        for item_id, amount in butcher_amounts:
            item = get_item_nullable(item_id)
            if (item is None) or not (item.flags & ITEM_FLAG_BUTCHERABLE):
                butcher_amounts_accumulated = butcher_add_to_amounts_accumulation(
                    butcher_amounts_accumulated, item_id, amount
                )
                continue
            
            not_butchered_count = 0
            for _ in range(amount):
                index += 1
                seed = step_seed(seed)
                butchered = (butcher_flags >> index) & 1
                
                if butchered:
                    butcher_queue.append((item, index, seed))
                
                else:
                    not_butchered_count += 1
                    
                    if butcherables is None:
                        butcherables = []
                    
                    butcherables.append((item, index))
                
                part_count = butcher_get_part_count(item)
                index += part_count
                for _ in range(part_count):
                    seed = step_seed(seed)
                
                continue
            
            if not_butchered_count:
                butcher_amounts_accumulated = butcher_add_to_amounts_accumulation(
                    butcher_amounts_accumulated, item_id, not_butchered_count
                )
            continue
        continue
    
    return butcher_amounts_accumulated, energy_cost_accumulated, butcherables


def butcher_done_append(
    butcher_amounts_accumulated,
    energy_cost_accumulated,
    butcherables,
    butchered_item,
    butchered_index,
    butcher_amounts,
    energy_cost,
):
    """
    Appends butcher step result into a butcher done result.
    
    Parameters
    ----------
    butcher_amounts_accumulated : `None | list<(int, int)>`
        Butchered amounts accumulated.
    
    energy_cost_accumulated : `int`
        Energy used accumulated.
    
    butcherables : ``None | list<(Item, int)>``
        Items which can be further butchered.
    
    butchered_item : ``Item``
        The just butchered item.
    
    butchered_index : `int`
        The just butchered item's index in the butcher queue.
        
    butcher_amounts : ``None | list<(int, int)>``
        Butchered amounts from the item.
    
    energy_cost : `int`
        Energy used by butchering.
    
    Returns
    -------
    butcher_amounts_and_energy_cost_and_butcherables : ``(None | list<(int, int), int, None | list<(Item, int)>, int)``
    """
    # Remove butchered item from butcher amounts.
    if (butcher_amounts_accumulated is not None):
        butchered_item_id = butchered_item.id
        for index in range(len(butcher_amounts_accumulated)):
            item_id, amount = butcher_amounts_accumulated[index]
            if item_id != butchered_item_id:
                continue
            
            amount -= 1
            if amount:
                butcher_amounts_accumulated[index] = (item_id, amount)
            else:
                del butcher_amounts_accumulated[index]
                if not butcher_amounts_accumulated:
                    butcher_amounts_accumulated = None
            break
    
    # Remove butchered item from butcherables.
    if (butcherables is not None):
        try:
            butcherables.remove((butchered_item, butchered_index))
        except ValueError:
            pass
        else:
            if not butcherables:
                butcherables = None
    
    # Append the butchered amounts to the accumulated.
    if (butcher_amounts is not None):
        for item_id, amount in butcher_amounts:
            item = get_item_nullable(item_id)
            butcher_amounts_accumulated = butcher_add_to_amounts_accumulation(
                butcher_amounts_accumulated, item_id, amount
            )
            
            if (item is None) or not (item.flags & ITEM_FLAG_BUTCHERABLE):
                continue
            
            for _ in range(amount):
                butchered_index += 1
                if butcherables is None:
                    butcherables = []
                
                butcherables.append((item, butchered_index))
                butchered_index += butcher_get_part_count(item)
                continue
            
            continue
        
    # Add to energy usage.
    energy_cost_accumulated += energy_cost
    
    return butcher_amounts_accumulated, energy_cost_accumulated, butcherables
