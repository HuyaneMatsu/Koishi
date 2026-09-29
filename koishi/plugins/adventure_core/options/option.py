__all__ = (
    'OptionBase', 'OptionBattle', 'OptionLoot', 'option_base_create', 'option_battle_create', 'option_loot_create'
)

from scarletio import RichType


class OptionBase(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Base type for randomization based options.
    
    Attributes
    ----------
    amount_base : `int`
        The base amount that is always given.
    
    amount_interval : `int`
        The interval between the base amount and the maximal amount that can be given.
    
    amount_scaling_enabled : `int`
        Whether the amount should be scaled by the multiplier.
    
    chance_in : `int`
        The chance to be chosen in.
    
    chance_out : `int`
        The chance to be chosen out of.
    
    chance_scaling_enabled : `bool`
        Whether the chance should be scaled by the multiplier.
    """
    __slots__ = (
        'amount_base', 'amount_interval', 'amount_scaling_enabled', 'chance_in', 'chance_out', 'chance_scaling_enabled'
    )


class OptionBattle(OptionBase):
    """
    Represents battled enemies for completing an action.
    
    Attributes
    ----------
    amount_base : `int`
        The base amount that is always given.
    
    amount_interval : `int`
        The interval between the base amount and the maximal amount that can be given.
    
    amount_scaling_enabled : `int`
        Whether the amount should be scaled by the multiplier.
    
    chance_in : `int`
        The chance to be chosen in.
    
    chance_out : `int`
        The chance to be chosen out of.
    
    chance_scaling_enabled : `bool`
        Whether the chance should be scaled by the multiplier.
    
    enemy_id : `int`
        The given enemy's identifier.
    
    loot : ``None | tuple<LootOption>``
        Additional role options for battled enemies.
    """
    __slots__ = ('enemy_id', 'loot')


class OptionLoot(OptionBase):
    """
    Represents awarded items by completing an action.
    
    Attributes
    ----------
    amount_base : `int`
        The base amount that is always given.
    
    amount_interval : `int`
        The interval between the base amount and the maximal amount that can be given.
    
    amount_scaling_enabled : `int`
        Whether the amount should be scaled by the multiplier.
    
    chance_in : `int`
        The chance to be chosen in.
    
    chance_out : `int`
        The chance to be chosen out of.
    
    chance_scaling_enabled : `bool`
        Whether the chance should be scaled by the multiplier.
    
    duration_cost_flat : `int`
        The required  duration to execute this action.
    
    duration_cost_scaling : `int`
        The required duration by item given to complete this action.
    
    energy_cost_flat : `int`
        The required energy to successfully execute this action.
    
    energy_cost_scaling : `int`
        The required energy for each item given.
    
    item_id : `int`
        The given item's identifier.
    """
    __slots__ = (
        'duration_cost_flat', 'duration_cost_scaling', 'energy_cost_flat', 'energy_cost_scaling', 'item_id',
    )


def option_base_create(
    chance_scaling_enabled,
    chance_in,
    chance_out,
    amount_scaling_enabled,
    amount_min,
    amount_max,
):
    """
    Creates a new base option. Used only for testing.
    
    Parameters
    ----------
    chance_scaling_enabled : `bool`
        Whether the chance should be scaled by the multiplier.
    
    chance_in : `int`
        The chance to be chosen in.
    
    chance_out : `int`
        The chance to be chosen out of.
    
    amount_scaling_enabled : `int`
        Whether the amount should be scaled by the multiplier.
    
    amount_min : `int`
        The minimal amount to battle.
    
    amount_max : `int`
        The maximal amount to battle.
    
    Returns
    -------
    option : ``OptionBase``
    """
    option = object.__new__(OptionBase)
    
    option.chance_scaling_enabled = chance_scaling_enabled
    option.chance_in = chance_in
    option.chance_out = chance_out
    option.amount_scaling_enabled = amount_scaling_enabled
    option.amount_base = amount_min
    option.amount_interval = amount_max - amount_min
    
    return option


def option_battle_create(
    chance_scaling_enabled,
    chance_in,
    chance_out,
    amount_scaling_enabled,
    amount_min,
    amount_max,
    enemy_id,
    loot,
):
    """
    Creates a new battle option.
    
    Parameters
    ----------
    chance_scaling_enabled : `bool`
        Whether the chance should be scaled by the multiplier.
    
    chance_in : `int`
        The chance to be chosen in.
    
    chance_out : `int`
        The chance to be chosen out of.
    
    amount_scaling_enabled : `int`
        Whether the amount should be scaled by the multiplier.
    
    amount_min : `int`
        The minimal amount to battle.
    
    amount_max : `int`
        The maximal amount to battle.
    
    enemy_id : `int`
        The given enemy's identifier.
    
    loot : ``None | tuple<LootOption>``
        Additional role options for battled enemies.
    
    Returns
    -------
    option : ``OptionBattle``
    """
    option = object.__new__(OptionBattle)
    
    option.chance_scaling_enabled = chance_scaling_enabled
    option.chance_in = chance_in
    option.chance_out = chance_out
    option.amount_scaling_enabled = amount_scaling_enabled
    option.amount_base = amount_min
    option.amount_interval = amount_max - amount_min
    
    option.enemy_id = enemy_id
    option.loot = loot
    
    return option



def option_loot_create(
    chance_scaling_enabled,
    chance_in,
    chance_out,
    amount_scaling_enabled,
    amount_min,
    amount_max,
    item_id,
    duration_cost_flat,
    duration_cost_scaling,
    energy_cost_flat,
    energy_cost_scaling,
):
    """
    Creates a new loot option.
    
    Parameters
    ----------
    chance_scaling_enabled : `bool`
        Whether the chance should be scaled by the multiplier.
    
    chance_in : `int`
        The chance to be chosen in.
    
    chance_out : `int`
        The chance to be chosen out of.
    
    amount_scaling_enabled : `int`
        Whether the amount should be scaled by the multiplier.
    
    amount_min : `int`
        The minimal amount.
    
    amount_max : `int`
        The maximal amount.
    
    item_id : `int`
        The given item's identifier.
    
    duration_cost_flat : `int`
        The required  duration to execute this action.
    
    duration_cost_scaling : `int`
        The required duration by item given to complete this action.
    
    energy_cost_flat : `int`
        The required energy to successfully execute this action.
    
    energy_cost_scaling : `int`
        The required energy for each item given.
    
    Returns
    -------
    option : ``OptionLoot``
    """
    option = object.__new__(OptionLoot)
    
    option.chance_scaling_enabled = chance_scaling_enabled
    option.chance_in = chance_in
    option.chance_out = chance_out
    option.amount_scaling_enabled = amount_scaling_enabled
    option.amount_base = amount_min
    option.amount_interval = amount_max - amount_min
    
    option.duration_cost_flat = duration_cost_flat
    option.duration_cost_scaling = duration_cost_scaling
    option.energy_cost_flat = energy_cost_flat
    option.energy_cost_scaling = energy_cost_scaling
    option.item_id = item_id
    
    return option
