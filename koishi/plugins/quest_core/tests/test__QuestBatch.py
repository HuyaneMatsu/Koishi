import vampytest

from ..quest_batch import QuestBatch, quest_batch_create

from .helpers import _create_quest


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


def test__QuestBatch__repr():
    """
    Tests whether ``QuestBatch.__repr__`` works as intended.
    """
    quest = _create_quest()
    
    quest_batch_id = 26663
    
    quest_batch = quest_batch_create(
        quest_batch_id,
        (quest,),
    )
    
    output = repr(quest_batch)
    vampytest.assert_instance(output, str)


def test__quest_batch_create():
    quest = _create_quest()
    
    quest_batch_id = 26663
    
    quest_batch = quest_batch_create(
        quest_batch_id,
        (quest,),
    )
    _assert_fields_set(quest_batch)
    
    vampytest.assert_eq(quest_batch.id, quest_batch_id)
    vampytest.assert_eq(quest_batch.quests, (quest,))
