import vampytest

from ..quest_batch_generation import quest_batch_generate
from ..quest_batch import QuestBatch


def test__quest_batch_generate():
    guild_id = 399127636661422121
    batch_id = 69999
    level_limit = 2
    amount = 5
    
    output = quest_batch_generate(guild_id, batch_id, level_limit, amount)
    vampytest.assert_instance(output, QuestBatch)
    vampytest.assert_eq(output.id, batch_id)
    vampytest.assert_eq(len(output.quests), amount)
