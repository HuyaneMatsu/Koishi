import vampytest

from ..quest import Quest
from ..quest_batch import QuestBatch
from ..quest_template_ids import QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY


def _assert_fields_set(quest_batch):
    """
    Asserts whether the quest batch has all of its fields set.
    
    Parameters
    ----------
    quest_batch : ``QuestBatch``
        The quest batch to test.
    """
    vampytest.assert_instance(quest_batch, QuestBatch)
    vampytest.assert_instance(quest_batch.id, int)
    vampytest.assert_instance(quest_batch.quests, tuple)


def test__QuestBatch__new():
    """
    Tests whether ``QuestBatch.__new__`` works as intended.
    """
    duration = 3600 * 24 * 3
    amount = 4
    reward_balance = 2600
    reward_credibility = 4
    template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    
    quest = Quest(
        template_id,
        amount,
        duration,
        reward_credibility,
        reward_balance,
    )
    
    quest_batch_id = 26663
    
    quest_batch = QuestBatch(
        quest_batch_id,
        (quest,),
    )
    _assert_fields_set(quest_batch)
    
    vampytest.assert_eq(quest_batch.id, quest_batch_id)
    vampytest.assert_eq(quest_batch.quests, (quest,))


def test__QuestBatch__repr():
    """
    Tests whether ``QuestBatch.__repr__`` works as intended.
    """
    duration = 3600 * 24 * 3
    amount = 4
    reward_balance = 2600
    reward_credibility = 4
    template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    
    quest = Quest(
        template_id,
        amount,
        duration,
        reward_credibility,
        reward_balance,
    )
    
    quest_batch_id = 26663
    
    quest_batch = QuestBatch(
        quest_batch_id,
        (quest,),
    )
    
    output = repr(quest_batch)
    vampytest.assert_instance(output, str)
