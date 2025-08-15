__all__ = ()

from .loot_accumulation import LootAccumulation
from .seed_stepping import step_seed


def get_option_amount(option, seed):
    """
    Generates an amount of the given option with the given seed.
    
    Parameters
    ----------
    option : ``OptionBase``
        Option to use.
    
    seed : `int`
        Seed used for randomization.
    
    Returns
    -------
    amount : `int`
    """
    chance_byte_size = option.chance_byte_size
    if (seed & 255) > chance_byte_size:
        amount = 0
    else:
        amount = option.amount_base + (seed % (option.amount_interval + 1))
    
    return amount


def accumulate_loot_loot(loot, accumulations, seed):
    """
    Sums the durations of looting, adding the result the accumulated one.
    
    Parameters
    ----------
    loot : ``None | tuple<OptionLoot>``
        Loot options.
    
    accumulations : ``dict<int, LootAccumulation>``
        Loot accumulations by `item_id`.
    
    seed : `int`
        Seed used for randomization.
    
    Returns
    -------
    seed : `int`
    """
    if (loot is not None):
        for option in loot:
            amount = get_option_amount(option, seed)
            seed = step_seed(seed)
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
    
    return seed


def accumulate_battle_loot(battle, accumulations, seed):
    """
    Sums the durations of the battles, adding the result the accumulated one.
    
    Parameters
    ----------
    battle : ``None | tuple<OptionBattle>``
        Battle options.
    
    accumulations : ``dict<int, LootAccumulation>``
        Loot accumulations by `item_id`.
    
    seed : `int`
        Seed used for randomization.
    
    Returns
    -------
    seed : `int`
    """
    if (battle is not None):
        for option in battle:
            amount = get_option_amount(option, seed)
            seed = step_seed(seed)
            if not amount:
                continue
            
            for _ in range(amount):
                seed = accumulate_loot_loot(option.loot, accumulations, seed)
    
    return seed


def accumulate_action_loot(action, seed):
    loot_accumulations = {}
    seed = accumulate_battle_loot(action.battle, loot_accumulations, seed)
    seed = accumulate_loot_loot(action.loot, loot_accumulations, seed)
    return loot_accumulations, seed
