from math import floor

import vampytest

from ..loot import OptionLoot


def _assert_fields_set(option_loot):
    """
    Asserts whether the loot option has all of its fields set.
    
    Parameters
    ----------
    option_loot : ``OptionLoot``
    """
    vampytest.assert_instance(option_loot, OptionLoot)
    vampytest.assert_instance(option_loot.amount_base, int)
    vampytest.assert_instance(option_loot.amount_interval, int)
    vampytest.assert_instance(option_loot.chance_byte_size, int)
    vampytest.assert_instance(option_loot.duration_cost_flat, int)
    vampytest.assert_instance(option_loot.duration_cost_scaling, int)
    vampytest.assert_instance(option_loot.energy_cost_flat, int)
    vampytest.assert_instance(option_loot.energy_cost_scaling, int)
    vampytest.assert_instance(option_loot.item_id, int)


def test__OptionLoot__new():
    """
    Tests whether ``OptionLoot.__new__`` works as intended.
    """
    chance = 0.4
    amount_min = 31
    amount_max = 6
    item_id = 5333
    duration_cost_flat = 22
    duration_cost_scaling = 2
    energy_cost_flat = 20
    energy_cost_scaling = 1
    
    option_loot = OptionLoot(
        chance,
        amount_min,
        amount_max,
        item_id,
        duration_cost_flat,
        duration_cost_scaling,
        energy_cost_flat,
        energy_cost_scaling,
    )
    
    _assert_fields_set(option_loot)
    
    vampytest.assert_eq(option_loot.amount_base, amount_min)
    vampytest.assert_eq(option_loot.amount_interval, amount_max - amount_min)
    vampytest.assert_eq(option_loot.chance_byte_size, floor(chance * 255))
    vampytest.assert_eq(option_loot.item_id, item_id)
    vampytest.assert_eq(option_loot.duration_cost_flat, duration_cost_flat)
    vampytest.assert_eq(option_loot.duration_cost_scaling, duration_cost_scaling)
    vampytest.assert_eq(option_loot.energy_cost_flat, energy_cost_flat)
    vampytest.assert_eq(option_loot.energy_cost_scaling, energy_cost_scaling)


def test__OptionLoot__repr():
    """
    Tests whether ``OptionLoot.__repr__`` works as intended.
    """
    chance = 0.4
    amount_min = 31
    amount_max = 6
    item_id = 5333
    duration_cost_flat = 22
    duration_cost_scaling = 2
    energy_cost_flat = 20
    energy_cost_scaling = 1
    
    option_loot = OptionLoot(
        chance,
        amount_min,
        amount_max,
        item_id,
        duration_cost_flat,
        duration_cost_scaling,
        energy_cost_flat,
        energy_cost_scaling,
    )
    
    output = repr(option_loot)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    chance = 0.4
    amount_min = 31
    amount_max = 6
    item_id = 5333
    duration_cost_flat = 22
    duration_cost_scaling = 2
    energy_cost_flat = 20
    energy_cost_scaling = 1
    
    keyword_parameters = {
        'chance': chance,
        'amount_min': amount_min,
        'amount_max': amount_max,
        'item_id': item_id,
        'duration_cost_flat': duration_cost_flat,
        'duration_cost_scaling': duration_cost_scaling,
        'energy_cost_flat': energy_cost_flat,
        'energy_cost_scaling': energy_cost_scaling,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'chance': 0.6,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'amount_min': 3,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'amount_max': 5,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'item_id': 4555,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'duration_cost_flat': 10,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'duration_cost_scaling': 12,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'duration_cost_flat': 7,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'duration_cost_scaling': 8,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'energy_cost_flat': 7,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'energy_cost_scaling': 8,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__OptionLoot__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``OptionLoot.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    option_loot_0 = OptionLoot(**keyword_parameters_0)
    option_loot_1 = OptionLoot(**keyword_parameters_1)
    
    output = option_loot_0 == option_loot_1
    vampytest.assert_instance(output, bool)
    return output


def test__OptionLoot__hash():
    """
    Tests whether ``OptionLoot.__hash__`` works as intended.
    """
    chance = 0.4
    amount_min = 31
    amount_max = 6
    item_id = 5333
    duration_cost_flat = 20
    duration_cost_scaling = 1
    energy_cost_flat = 20
    energy_cost_scaling = 1
    
    option_loot = OptionLoot(
        chance,
        amount_min,
        amount_max,
        item_id,
        duration_cost_flat,
        duration_cost_scaling,
        energy_cost_flat,
        energy_cost_scaling,
    )
    
    output = hash(option_loot)
    vampytest.assert_instance(output, int)
