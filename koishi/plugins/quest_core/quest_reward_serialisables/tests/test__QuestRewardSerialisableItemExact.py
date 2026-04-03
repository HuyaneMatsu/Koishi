import vampytest

from ...quest_reward_types import QUEST_REWARD_TYPE_ITEM_EXACT

from ..item_exact import QuestRewardSerialisableItemExact


def _assert_fields_set(quest_reward_serialisable_item_exact):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_reward_serialisable_item_exact : ``QuestRewardSerialisableItemExact``
        The instance to check.
    """
    vampytest.assert_instance(
        quest_reward_serialisable_item_exact, QuestRewardSerialisableItemExact
    )
    vampytest.assert_eq(quest_reward_serialisable_item_exact.TYPE, QUEST_REWARD_TYPE_ITEM_EXACT)
    vampytest.assert_instance(quest_reward_serialisable_item_exact.amount_given, int)
    vampytest.assert_instance(quest_reward_serialisable_item_exact.item_id, int)


def test__QuestRewardSerialisableItemExact__new():
    """
    Tests whether ``QuestRewardSerialisableItemExact.__new__`` works as intended.
    """
    item_id = 4
    amount_given = 5
    
    quest_reward_serialisable_item_exact = QuestRewardSerialisableItemExact(
        item_id,
        amount_given,
    )
    _assert_fields_set(quest_reward_serialisable_item_exact)
    
    vampytest.assert_eq(quest_reward_serialisable_item_exact.item_id, item_id)
    vampytest.assert_eq(quest_reward_serialisable_item_exact.amount_given, amount_given)


def test__QuestRewardSerialisableItemExact__repr():
    """
    Tests whether ``QuestRewardSerialisableItemExact.__repr__`` works as intended.
    """
    item_id = 4
    amount_given = 5
    
    quest_reward_serialisable_item_exact = QuestRewardSerialisableItemExact(
        item_id,
        amount_given,
    )
    
    output = repr(quest_reward_serialisable_item_exact)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    item_id = 44
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
            12,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRewardSerialisableItemExact__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRewardSerialisableItemExact.__eq__`` works as intended.
    
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
    quest_reward_serialisable_item_exact_0 = QuestRewardSerialisableItemExact(*position_parameters_0)
    quest_reward_serialisable_item_exact_1 = QuestRewardSerialisableItemExact(*position_parameters_1)
    
    output = quest_reward_serialisable_item_exact_0 == quest_reward_serialisable_item_exact_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRewardSerialisableItemExact__deserialise():
    """
    Tests whether ``QuestRewardSerialisableItemExact.deserialise`` works as as intended.
    """
    item_id = 4
    amount_given = 5
    
    data = b''.join([
        item_id.to_bytes(4, 'little'),
        amount_given.to_bytes(8, 'little'),
    ])
    start_index = 0
    
    quest_reward_serialisable_item_exact, end_index = QuestRewardSerialisableItemExact.deserialise(
        data, start_index
    )
    
    _assert_fields_set(quest_reward_serialisable_item_exact)
    vampytest.assert_eq(end_index, 12)
    
    vampytest.assert_eq(quest_reward_serialisable_item_exact.item_id, item_id)
    vampytest.assert_eq(quest_reward_serialisable_item_exact.amount_given, amount_given)


def test__QuestRewardSerialisableItemExact__serialise():
    """
    Tests whether ``QuestRewardSerialisableItemExact.serialise`` works as intended.
    """
    item_id = 4
    amount_given = 5
    
    quest_reward_serialisable_item_exact = QuestRewardSerialisableItemExact(
        item_id,
        amount_given,
    )
    
    output = [*quest_reward_serialisable_item_exact.serialise()]
    
    for element in output:
        vampytest.assert_instance(element, bytes)
    
    vampytest.assert_eq(
        b''.join(output),
        b''.join([
            item_id.to_bytes(4, 'little'),
            amount_given.to_bytes(8, 'little'),
        ]),
    )
