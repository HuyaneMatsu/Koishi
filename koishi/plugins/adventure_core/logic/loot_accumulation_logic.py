__all__ = ()

from math import floor

from .loot_accumulation import LootAccumulation


def get_option_amount(option, random):
    """
    Generates an amount of the given option with the given random number generator.
    
    Parameters
    ----------
    option : ``OptionBase``
        Option to use.
    
    random : `random.Random`
        Random number generator to use.
    
    Returns
    -------
    amount : `int`
    """
    chance_in = option.chance_in
    chance_out = option.chance_out
    if (chance_in != chance_out) and (random.random() * chance_out >= chance_in):
        amount = 0
    else:
        amount = option.amount_base + floor(random.random() * (option.amount_interval + 1))
    
    return amount


def accumulate_loot_loot(loot, accumulations, random):
    """
    Sums the durations of looting, adding the result the accumulated one.
    
    Parameters
    ----------
    loot : ``None | tuple<OptionLoot>``
        Loot options.
    
    accumulations : ``dict<int, LootAccumulation>``
        Loot accumulations by `item_id`.
    
    random : `random.Random`
        Random number generator to use.
    """
    if (loot is not None):
        for option in loot:
            amount = get_option_amount(option, random)
            if not amount:
                continue
            
            duration_cost = option.duration_cost_flat + (amount * option.duration_cost_scaling)
            energy_cost = option.energy_cost_flat + (amount * option.energy_cost_scaling)
            
            item_id = option.item_id
            try:
                accumulation = accumulations[item_id]
            except KeyError:
                accumulation = LootAccumulation(amount, duration_cost, energy_cost)
                accumulations[item_id] = accumulation
            else:
                accumulation.amount += amount
                accumulation.duration_cost += duration_cost
                accumulation.energy_cost += energy_cost
            continue


def accumulate_battle_loot(battle, accumulations, random):
    """
    Sums the durations of the battles, adding the result the accumulated one.
    
    Parameters
    ----------
    battle : ``None | tuple<OptionBattle>``
        Battle options.
    
    accumulations : ``dict<int, LootAccumulation>``
        Loot accumulations by `item_id`.
    
    random : `random.Random`
        Random number generator to use.
    """
    if (battle is not None):
        for option in battle:
            amount = get_option_amount(option, random)
            if not amount:
                continue
            
            for _ in range(amount):
                 accumulate_loot_loot(option.loot, accumulations, random)


def accumulate_action_loot(action, random):
    """
    Accumulates the loot for the given action.
    
    Parameters
    ----------
    action : ``Action``
        Action to accumulate loot for.
    
    random : `random.Random`
        Random number generator to use.
    
    
    Returns
    -------
    loot_accumulations : ``dict<int, LootAccumulation>``
        Loot accumulations by `item_id`.
    """
    loot_accumulations = {}
    accumulate_battle_loot(action.battle, loot_accumulations, random)
    accumulate_loot_loot(action.loot, loot_accumulations, random)
    return loot_accumulations
