from math import floor

import vampytest

from ..battle import OptionBattle
from ..loot import OptionLoot


def _assert_fields_set(option_battle):
    """
    Asserts whether the enemy option has all of its fields set.
    
    Parameters
    ----------
    option_battle : ``OptionBattle``
    """
    vampytest.assert_instance(option_battle, OptionBattle)
    vampytest.assert_instance(option_battle.amount_base, int)
    vampytest.assert_instance(option_battle.amount_interval, int)
    vampytest.assert_instance(option_battle.chance_byte_size, int)
    vampytest.assert_instance(option_battle.enemy_id, int)
    vampytest.assert_instance(option_battle.loot, tuple, nullable = True)


def test__OptionBattle__new():
    """
    Tests whether ``OptionBattle.__new__`` works as intended.
    """
    chance = 0.4
    amount_min = 31
    amount_max = 6
    enemy_id = 5333
    loot = (
        OptionLoot(1.0, 1, 1, 130, 22, 2, 20, 1),
        OptionLoot(0.5, 2, 4, 132, 22, 2, 20, 1),
    )
    
    option_battle = OptionBattle(
        chance,
        amount_min,
        amount_max,
        enemy_id,
        loot,
    )
    
    _assert_fields_set(option_battle)
    
    vampytest.assert_eq(option_battle.amount_base, amount_min)
    vampytest.assert_eq(option_battle.amount_interval, amount_max - amount_min)
    vampytest.assert_eq(option_battle.chance_byte_size, floor(chance * 255))
    vampytest.assert_eq(option_battle.enemy_id, enemy_id)
    vampytest.assert_eq(option_battle.loot, loot)


def test__OptionBattle__repr():
    """
    Tests whether ``OptionBattle.__repr__`` works as intended.
    """
    chance = 0.4
    amount_min = 31
    amount_max = 6
    enemy_id = 5333
    loot = (
        OptionLoot(1.0, 1, 1, 130, 22, 2, 20, 1),
        OptionLoot(0.5, 2, 4, 132, 22, 2, 20, 1),
    )
    
    option_battle = OptionBattle(
        chance,
        amount_min,
        amount_max,
        enemy_id,
        loot,
    )
    
    output = repr(option_battle)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    chance = 0.4
    amount_min = 31
    amount_max = 6
    enemy_id = 5333
    loot = (
        OptionLoot(1.0, 1, 1, 130, 22, 2, 20, 1),
        OptionLoot(0.5, 2, 4, 132, 22, 2, 20, 1),
    )
    
    keyword_parameters = {
        'chance': chance,
        'amount_min': amount_min,
        'amount_max': amount_max,
        'enemy_id': enemy_id,
        'loot': loot,
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
            'enemy_id': 4555,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'loot': None,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__OptionBattle__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``OptionBattle.__eq__`` works as intended.
    
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
    option_battle_0 = OptionBattle(**keyword_parameters_0)
    option_battle_1 = OptionBattle(**keyword_parameters_1)
    
    output = option_battle_0 == option_battle_1
    vampytest.assert_instance(output, bool)
    return output


def test__OptionBattle__hash():
    """
    Tests whether ``OptionBattle.__hash__`` works as intended.
    """
    chance = 0.4
    amount_min = 31
    amount_max = 6
    enemy_id = 5333
    loot = (
        OptionLoot(1.0, 1, 1, 130, 22, 2, 20, 1),
        OptionLoot(0.5, 2, 4, 132, 22, 2, 20, 1),
    )
    
    option_battle = OptionBattle(
        chance,
        amount_min,
        amount_max,
        enemy_id,
        loot,
    )
    
    output = hash(option_battle)
    vampytest.assert_instance(output, int)
