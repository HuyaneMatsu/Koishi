import vampytest

from ...quest_reward_serialisables import QuestRewardSerialisableItemExact
from ...quest_reward_types import QUEST_REWARD_TYPE_ITEM_EXACT

from ..item_exact import QuestRewardInstantiableItemExact


def _assert_fields_set(quest_reward_instantiable_item_exact):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_reward_instantiable_item_exact : ``QuestRewardInstantiableItemExact``
        The instance to check.
    """
    vampytest.assert_instance(quest_reward_instantiable_item_exact, QuestRewardInstantiableItemExact)
    vampytest.assert_eq(quest_reward_instantiable_item_exact.TYPE, QUEST_REWARD_TYPE_ITEM_EXACT)
    vampytest.assert_instance(quest_reward_instantiable_item_exact.amount_given, int)
    vampytest.assert_instance(quest_reward_instantiable_item_exact.item_id, int)


def test__QuestRewardInstantiableItemExact__new():
    """
    Tests whether ``QuestRewardInstantiableItemExact.__new__`` works as intended.
    """
    item_id = 4
    amount_given = 5
    
    quest_reward_instantiable_item_exact = QuestRewardInstantiableItemExact(
        item_id,
        amount_given,
    )
    _assert_fields_set(quest_reward_instantiable_item_exact)
    
    vampytest.assert_eq(quest_reward_instantiable_item_exact.item_id, item_id)
    vampytest.assert_eq(quest_reward_instantiable_item_exact.amount_given, amount_given)


def test__QuestRewardInstantiableItemExact__repr():
    """
    Tests whether ``QuestRewardInstantiableItemExact.__repr__`` works as intended.
    """
    item_id = 4
    amount_given = 5
    
    quest_reward_instantiable_item_exact = QuestRewardInstantiableItemExact(
        item_id,
        amount_given,
    )
    
    output = repr(quest_reward_instantiable_item_exact)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    item_id = 4
    amount_given = 5
    
    yield (
        (
            item_id,
            amount_given,
        ),
        (
            item_id,
            amount_given,
        ),
        True,
    )
    
    yield (
        (
            item_id,
            amount_given,
        ),
        (
            2,
            amount_given,
        ),
        False,
    )
    
    yield (
        (
            item_id,
            amount_given,
        ),
        (
            item_id,
            10,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRewardInstantiableItemExact__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRewardInstantiableItemExact.__eq__`` works as intended.
    
    Parameters
    ----------
    position_parameters_0 : `tuple<object>`
        Positional parameters to create instance form.
    
    position_parameters_1 : `tuple<object>`
        Positional parameters to create instance form.
    
    Returns
    -------
    output : `bool`
    """
    quest_reward_instantiable_item_exact_0 = QuestRewardInstantiableItemExact(*position_parameters_0)
    quest_reward_instantiable_item_exact_1 = QuestRewardInstantiableItemExact(*position_parameters_1)
    
    output = quest_reward_instantiable_item_exact_0 == quest_reward_instantiable_item_exact_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRewardInstantiableItemExact__instantiate():
    """
    Tests whether ``QuestRewardInstantiableItemExact.instantiate`` works as intended.
    """
    item_id = 4
    amount_given = 5
    
    quest_reward_instantiable_item_exact = QuestRewardInstantiableItemExact(
        item_id,
        amount_given,
    )
    
    output = quest_reward_instantiable_item_exact.instantiate()
    
    vampytest.assert_instance(output, QuestRewardSerialisableItemExact)
    vampytest.assert_eq(output.item_id, item_id)
    vampytest.assert_eq(output.amount_given, amount_given)
