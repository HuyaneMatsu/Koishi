import vampytest

from ..loot_accumulation import LootAccumulation


def _assert_fields_set(loot_accumulation):
    """
    Tests whether the given instance has all of its fields set.
    
    Parameters
    ----------
    loot_accumulation : ``LootAccumulation``
        The instance to check.
    """
    vampytest.assert_instance(loot_accumulation, LootAccumulation)
    vampytest.assert_instance(loot_accumulation.amount, int)
    vampytest.assert_instance(loot_accumulation.duration_cost, int)
    vampytest.assert_instance(loot_accumulation.energy_cost, int)


def test__LootAccumulation__new():
    """
    Tests whether ``LootAccumulation.__new__`` works as intended.
    """
    amount = 5
    duration_cost = 720
    energy_cost = 60
    
    loot_accumulation = LootAccumulation(
        amount,
        duration_cost,
        energy_cost,
    )
    
    _assert_fields_set(loot_accumulation)
    
    vampytest.assert_eq(loot_accumulation.amount, amount)
    vampytest.assert_eq(loot_accumulation.duration_cost, duration_cost)
    vampytest.assert_eq(loot_accumulation.energy_cost, energy_cost)



def test__LootAccumulation__repr():
    """
    Tests whether ``LootAccumulation.__repr__`` works as intended.
    """
    amount = 5
    duration_cost = 720
    energy_cost = 60
    
    loot_accumulation = LootAccumulation(
        amount,
        duration_cost,
        energy_cost,
    )
    
    output = repr(loot_accumulation)
    vampytest.assert_instance(output, str)



def _iter_options__eq():
    amount = 5
    duration_cost = 720
    energy_cost = 60
    
    keyword_parameters = {
        'amount': amount,
        'duration_cost': duration_cost,
        'energy_cost': energy_cost,
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
            'amount': 6,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'duration_cost': 466,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'energy_cost': 56,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__LootAccumulation__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``LootAccumulation.__eq__`` works as intended.
    
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
    loot_accumulation_0 = LootAccumulation(**keyword_parameters_0)
    loot_accumulation_1 = LootAccumulation(**keyword_parameters_1)
    
    output = loot_accumulation_0 == loot_accumulation_1
    vampytest.assert_instance(output, bool)
    return output


def test__LootAccumulation__hash():
    """
    Tests whether ``LootAccumulation.__hash__`` works as intended.
    """
    amount = 5
    duration_cost = 720
    energy_cost = 60
    
    loot_accumulation = LootAccumulation(
        amount,
        duration_cost,
        energy_cost,
    )
    
    output = hash(loot_accumulation)
    vampytest.assert_instance(output, int)


def test__LootAccumulation__copy():
    """
    Tests whether ``LootAccumulation.copy`` works as intended.
    """
    amount = 5
    duration_cost = 720
    energy_cost = 60
    
    loot_accumulation = LootAccumulation(
        amount,
        duration_cost,
        energy_cost,
    )
    
    copy = loot_accumulation.copy()
    
    _assert_fields_set(copy)
    
    vampytest.assert_eq(copy, loot_accumulation)
