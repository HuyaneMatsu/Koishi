import vampytest

from ..base import OptionBase


def _assert_fields_set(option_base):
    """
    Asserts whether the loot option has all of its fields set.
    
    Parameters
    ----------
    option_base : ``OptionBase``
    """
    vampytest.assert_instance(option_base, OptionBase)
    vampytest.assert_instance(option_base.amount_base, int)
    vampytest.assert_instance(option_base.amount_interval, int)
    vampytest.assert_instance(option_base.chance_in, int)
    vampytest.assert_instance(option_base.chance_out, int)


def test__OptionBase__new():
    """
    Tests whether ``OptionBase.__new__`` works as intended.
    """
    chance_in = 2
    chance_out = 100
    amount_min = 31
    amount_max = 6
    
    option_base = OptionBase(
        chance_in,
        chance_out,
        amount_min,
        amount_max,
    )
    
    _assert_fields_set(option_base)
    
    vampytest.assert_eq(option_base.amount_base, amount_min)
    vampytest.assert_eq(option_base.amount_interval, amount_max - amount_min)
    vampytest.assert_eq(option_base.chance_in, chance_in)
    vampytest.assert_eq(option_base.chance_out, chance_out)


def test__OptionBase__repr():
    """
    Tests whether ``OptionBase.__repr__`` works as intended.
    """
    chance_in = 2
    chance_out = 100
    amount_min = 31
    amount_max = 6
    
    option_base = OptionBase(
        chance_in,
        chance_out,
        amount_min,
        amount_max,
    )
    
    output = repr(option_base)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    chance_in = 2
    chance_out = 100
    amount_min = 31
    amount_max = 6
    
    keyword_parameters = {
        'chance_in': chance_in,
        'chance_out': chance_out,
        'amount_min': amount_min,
        'amount_max': amount_max,
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
            'chance_in': 5,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'chance_out': 5,
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


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__OptionBase__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``OptionBase.__eq__`` works as intended.
    
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
    option_base_0 = OptionBase(**keyword_parameters_0)
    option_base_1 = OptionBase(**keyword_parameters_1)
    
    output = option_base_0 == option_base_1
    vampytest.assert_instance(output, bool)
    return output


def test__OptionBase__hash():
    """
    Tests whether ``OptionBase.__hash__`` works as intended.
    """
    chance_in = 2
    chance_out = 100
    amount_min = 31
    amount_max = 6
    
    option_base = OptionBase(
        chance_in,
        chance_out,
        amount_min,
        amount_max,
    )
    
    output = hash(option_base)
    vampytest.assert_instance(output, int)
