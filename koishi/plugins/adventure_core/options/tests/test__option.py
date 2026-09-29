import vampytest

from ..option import OptionBase, OptionBattle, OptionLoot, option_base_create, option_battle_create, option_loot_create


def test__option_base_create():
    chance_scaling_enabled = False
    chance_in = 2
    chance_out = 100
    amount_scaling_enabled = True
    amount_min = 31
    amount_max = 6
    
    option = option_base_create(
        chance_scaling_enabled,
        chance_in,
        chance_out,
        amount_scaling_enabled,
        amount_min,
        amount_max,
    )
    
    vampytest.assert_instance(option, OptionBase)
    vampytest.assert_instance(option.amount_base, int)
    vampytest.assert_instance(option.amount_interval, int)
    vampytest.assert_instance(option.amount_scaling_enabled, bool)
    vampytest.assert_instance(option.chance_in, int)
    vampytest.assert_instance(option.chance_out, int)
    vampytest.assert_instance(option.chance_scaling_enabled, bool)
    
    vampytest.assert_eq(option.amount_base, amount_min)
    vampytest.assert_eq(option.amount_interval, amount_max - amount_min)
    vampytest.assert_eq(option.amount_scaling_enabled, amount_scaling_enabled)
    vampytest.assert_eq(option.chance_in, chance_in)
    vampytest.assert_eq(option.chance_out, chance_out)
    vampytest.assert_eq(option.chance_scaling_enabled, chance_scaling_enabled)


def test__option_battle_create():
    chance_scaling_enabled = False
    chance_in = 2
    chance_out = 100
    amount_scaling_enabled = True
    amount_min = 31
    amount_max = 6
    enemy_id = 5333
    loot = (
        option_loot_create(False, 1, 1, False, 1, 1, 130, 22, 2, 20, 1),
        option_loot_create(False, 1, 2, False, 2, 4, 132, 22, 2, 20, 1),
    )
    
    option = option_battle_create(
        chance_scaling_enabled,
        chance_in,
        chance_out,
        amount_scaling_enabled,
        amount_min,
        amount_max,
        enemy_id,
        loot,
    )
    
    vampytest.assert_instance(option, OptionBattle)
    vampytest.assert_instance(option.amount_base, int)
    vampytest.assert_instance(option.amount_interval, int)
    vampytest.assert_instance(option.amount_scaling_enabled, bool)
    vampytest.assert_instance(option.chance_in, int)
    vampytest.assert_instance(option.chance_out, int)
    vampytest.assert_instance(option.chance_scaling_enabled, bool)
    vampytest.assert_instance(option.enemy_id, int)
    vampytest.assert_instance(option.loot, tuple, nullable = True)
    
    vampytest.assert_eq(option.amount_base, amount_min)
    vampytest.assert_eq(option.amount_interval, amount_max - amount_min)
    vampytest.assert_eq(option.amount_scaling_enabled, amount_scaling_enabled)
    vampytest.assert_eq(option.chance_in, chance_in)
    vampytest.assert_eq(option.chance_out, chance_out)
    vampytest.assert_eq(option.chance_scaling_enabled, chance_scaling_enabled)
    vampytest.assert_eq(option.enemy_id, enemy_id)
    vampytest.assert_eq(option.loot, loot)


def test__option_loot_create():
    chance_scaling_enabled = False
    chance_in = 2
    chance_out = 100
    amount_scaling_enabled = True
    amount_min = 31
    amount_max = 6
    item_id = 5333
    duration_cost_flat = 22
    duration_cost_scaling = 2
    energy_cost_flat = 20
    energy_cost_scaling = 1
    
    option_loot = option_loot_create(
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
    )
    
    vampytest.assert_instance(option_loot, OptionLoot)
    vampytest.assert_instance(option_loot.amount_base, int)
    vampytest.assert_instance(option_loot.amount_interval, int)
    vampytest.assert_instance(option_loot.amount_scaling_enabled, bool)
    vampytest.assert_instance(option_loot.chance_in, int)
    vampytest.assert_instance(option_loot.chance_out, int)
    vampytest.assert_instance(option_loot.chance_scaling_enabled, bool)
    vampytest.assert_instance(option_loot.duration_cost_flat, int)
    vampytest.assert_instance(option_loot.duration_cost_scaling, int)
    vampytest.assert_instance(option_loot.energy_cost_flat, int)
    vampytest.assert_instance(option_loot.energy_cost_scaling, int)
    vampytest.assert_instance(option_loot.item_id, int)
    
    vampytest.assert_eq(option_loot.amount_base, amount_min)
    vampytest.assert_eq(option_loot.amount_interval, amount_max - amount_min)
    vampytest.assert_eq(option_loot.amount_scaling_enabled, amount_scaling_enabled)
    vampytest.assert_eq(option_loot.chance_in, chance_in)
    vampytest.assert_eq(option_loot.chance_out, chance_out)
    vampytest.assert_eq(option_loot.chance_scaling_enabled, chance_scaling_enabled)
    vampytest.assert_eq(option_loot.item_id, item_id)
    vampytest.assert_eq(option_loot.duration_cost_flat, duration_cost_flat)
    vampytest.assert_eq(option_loot.duration_cost_scaling, duration_cost_scaling)
    vampytest.assert_eq(option_loot.energy_cost_flat, energy_cost_flat)
    vampytest.assert_eq(option_loot.energy_cost_scaling, energy_cost_scaling)
