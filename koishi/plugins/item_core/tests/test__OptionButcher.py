import vampytest

from ..option_butcher import OptionButcher


def _assert_fields_set(option_butcher):
    """
    Asserts whether all fields are set of the given option butcher.
    
    Parameters
    ----------
    option_butcher : ``OptionButcher``
        The option to check.
    """
    vampytest.assert_instance(option_butcher, OptionButcher)
    vampytest.assert_instance(option_butcher.amount, int)
    vampytest.assert_instance(option_butcher.chance_in, int)
    vampytest.assert_instance(option_butcher.chance_out, int)
    vampytest.assert_instance(option_butcher.chance_scaling_enabled, int)
    vampytest.assert_instance(option_butcher.energy_cost_flat, int)
    vampytest.assert_instance(option_butcher.energy_cost_scaling_failure, int)
    vampytest.assert_instance(option_butcher.energy_cost_scaling_success, int)
    vampytest.assert_instance(option_butcher.item_id, int)


def test__OptionButcher__new():
    """
    Tests whether ``OptionButcher.__new__`` works as intended.
    """
    chance_scaling_enabled = True
    chance_in = 2
    chance_out = 3
    amount = 12
    item_id = 20
    energy_cost_flat = 10
    energy_cost_scaling_success = 30
    energy_cost_scaling_failure = 20
    
    option_butcher = OptionButcher(
        chance_scaling_enabled,
        chance_in,
        chance_out,
        amount,
        item_id,
        energy_cost_flat,
        energy_cost_scaling_success,
        energy_cost_scaling_failure,
    )
    
    _assert_fields_set(option_butcher)
    
    vampytest.assert_eq(option_butcher.amount, amount)
    vampytest.assert_eq(option_butcher.chance_in, chance_in)
    vampytest.assert_eq(option_butcher.chance_out, chance_out)
    vampytest.assert_eq(option_butcher.chance_scaling_enabled, chance_scaling_enabled)
    vampytest.assert_eq(option_butcher.energy_cost_flat, energy_cost_flat)
    vampytest.assert_eq(option_butcher.energy_cost_scaling_failure, energy_cost_scaling_failure)
    vampytest.assert_eq(option_butcher.energy_cost_scaling_success, energy_cost_scaling_success)
    vampytest.assert_eq(option_butcher.item_id, item_id)


def test__OptionButcher__repr():
    """
    Tests whether ``OptionButcher.__repr__`` works as intended.
    """
    chance_scaling_enabled = True
    chance_in = 2
    chance_out = 3
    amount = 12
    item_id = 20
    energy_cost_flat = 10
    energy_cost_scaling_success = 30
    energy_cost_scaling_failure = 20
    
    option_butcher = OptionButcher(
        chance_scaling_enabled,
        chance_in,
        chance_out,
        amount,
        item_id,
        energy_cost_flat,
        energy_cost_scaling_success,
        energy_cost_scaling_failure,
    )
    
    output = repr(option_butcher)
    vampytest.assert_instance(output, str)


def test__OptionButcher__hash():
    """
    Tests whether ``OptionButcher.__hash__`` works as intended.
    """
    chance_scaling_enabled = True
    chance_in = 2
    chance_out = 3
    amount = 12
    item_id = 20
    energy_cost_flat = 10
    energy_cost_scaling_success = 30
    energy_cost_scaling_failure = 20
    
    option_butcher = OptionButcher(
        chance_scaling_enabled,
        chance_in,
        chance_out,
        amount,
        item_id,
        energy_cost_flat,
        energy_cost_scaling_success,
        energy_cost_scaling_failure,
    )
    
    output = hash(option_butcher)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    chance_scaling_enabled = True
    chance_in = 2
    chance_out = 3
    amount = 12
    item_id = 20
    energy_cost_flat = 10
    energy_cost_scaling_success = 30
    energy_cost_scaling_failure = 20
    
    keyword_parameters = {
        'amount': amount,
        'chance_scaling_enabled': chance_scaling_enabled,
        'chance_in': chance_in,
        'chance_out': chance_out,
        'energy_cost_flat': energy_cost_flat,
        'energy_cost_scaling_failure': energy_cost_scaling_failure,
        'energy_cost_scaling_success': energy_cost_scaling_success,
        'item_id': item_id,
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
            'amount': 15,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'chance_scaling_enabled': False,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'chance_in': 1,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'chance_out': 2,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'energy_cost_flat': 16,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'energy_cost_scaling_failure': 17,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'energy_cost_scaling_success': 35,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'item_id': 18,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__OptionButcher__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``OptionButcher.__eq__`` works as intended.
    
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
    OptionButcher_0 = OptionButcher(**keyword_parameters_0)
    OptionButcher_1 = OptionButcher(**keyword_parameters_1)
    
    output = OptionButcher_0 == OptionButcher_1
    vampytest.assert_instance(output, bool)
    return output
