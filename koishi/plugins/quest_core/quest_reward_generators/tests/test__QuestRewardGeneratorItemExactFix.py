from random import Random

import vampytest

from ...quest_reward_instantiables import QuestRewardInstantiableItemExact
from ...quest_reward_types import QUEST_REWARD_TYPE_ITEM_EXACT

from ..item_exact_fix import QuestRewardGeneratorItemExactFix


def _assert_fields_set(quest_reward_generator_item_exact_fix):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_reward_generator_item_exact_fix : ``QuestRewardGeneratorItemExactFix``
        The instance to check.
    """
    vampytest.assert_instance(quest_reward_generator_item_exact_fix, QuestRewardGeneratorItemExactFix)
    vampytest.assert_eq(quest_reward_generator_item_exact_fix.TYPE, QUEST_REWARD_TYPE_ITEM_EXACT)
    vampytest.assert_instance(quest_reward_generator_item_exact_fix.item_id, int)
    vampytest.assert_instance(quest_reward_generator_item_exact_fix.amount_base, int)


def test__QuestRewardGeneratorItemExactFix__new():
    """
    Tests whether ``QuestRewardGeneratorItemExactFix.__new__`` works as intended.
    """
    item_id = 4
    amount_base = 3600
    
    quest_reward_generator_item_exact_fix = QuestRewardGeneratorItemExactFix(
        item_id,
        amount_base,
    )
    _assert_fields_set(quest_reward_generator_item_exact_fix)
    
    vampytest.assert_eq(quest_reward_generator_item_exact_fix.item_id, item_id)
    vampytest.assert_eq(quest_reward_generator_item_exact_fix.amount_base, amount_base)


def test__QuestRewardGeneratorItemExactFix__repr():
    """
    Tests whether ``QuestRewardGeneratorItemExactFix.__repr__`` works as intended.
    """
    item_id = 4
    amount_base = 3600
    
    quest_reward_generator_item_exact_fix = QuestRewardGeneratorItemExactFix(
        item_id,
        amount_base,
    )
    
    output = repr(quest_reward_generator_item_exact_fix)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    item_id = 4
    amount_base = 3600
    
    yield (
        (
            item_id,
            amount_base,
        ),
        (
            item_id,
            amount_base,
        ),
        True,
    )
    
    yield (
        (
            item_id,
            amount_base,
        ),
        (
            2,
            amount_base,
        ),
        False,
    )
    
    yield (
        (
            item_id,
            amount_base,
        ),
        (
            item_id,
            7200,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRewardGeneratorItemExactFix__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRewardGeneratorItemExactFix.__eq__`` works as intended.
    
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
    quest_reward_generator_item_exact_fix_0 = QuestRewardGeneratorItemExactFix(*position_parameters_0)
    quest_reward_generator_item_exact_fix_1 = QuestRewardGeneratorItemExactFix(*position_parameters_1)
    
    output = quest_reward_generator_item_exact_fix_0 == quest_reward_generator_item_exact_fix_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRewardGeneratorItemExactFix__generate_with_diversion():
    """
    Tests whether ``QuestRewardGeneratorItemExactFix.generate_with_diversion`` works as intended.
    """
    item_id = 4
    amount_base = 3600
    
    quest_reward_generator_item_exact_fix = QuestRewardGeneratorItemExactFix(
        item_id,
        amount_base,
    )
    
    random_number_generator = Random(5)
    accumulated_diversion = 2.0
    
    generated, diversion = quest_reward_generator_item_exact_fix.generate_with_diversion(
        random_number_generator, accumulated_diversion
    )
    
    vampytest.assert_eq(
        generated,
        QuestRewardInstantiableItemExact(
            item_id,
            3600,
        ),
    )
    
    vampytest.assert_eq(
        diversion,
        1.0,
    )
