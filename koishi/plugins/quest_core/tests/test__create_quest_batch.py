import vampytest

from ..quest_batch_generation import create_quest_batch
from ..quest_batch import QuestBatch


def test__create_quest_batch():
    """
    Tests whether ``create_quest_batch`` works as intended.
    """
    guild_id = 399127636661422121
    batch_id = 69999
    level_limit = 2
    amount = 5
    
    output = create_quest_batch(guild_id, batch_id, level_limit, amount)
    vampytest.assert_instance(output, QuestBatch)
    vampytest.assert_eq(output.id, batch_id)
    vampytest.assert_eq(len(output.quests), amount)
