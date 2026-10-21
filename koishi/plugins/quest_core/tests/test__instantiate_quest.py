import vampytest

from ..linked_quest import LinkedQuest
from ..utils import instantiate_quest

from .helpers import _create_linked_quest_additional_input_fields, _create_quest


def test__instantiate_quest():
    """
    Tests whether ``instantiate_quest`` works as intended.
    """
    now = 1000000
    
    user_id = 202602230000
    guild_id = 202602230001
    batch_id = 202602230002
    
    quest = _create_quest()
    
    def unix_time_seconds_get():
        nonlocal now
        return now
    
    mocked = vampytest.mock_globals(
        instantiate_quest,
        unix_time_seconds_get = unix_time_seconds_get,
    )
    
    output = mocked(
        user_id,
        guild_id,
        batch_id,
        quest,
    )
    
    template_id, requirements, rewards = _create_linked_quest_additional_input_fields()
    
    vampytest.assert_instance(output, LinkedQuest)
    vampytest.assert_eq(output.user_id, user_id)
    vampytest.assert_eq(output.guild_id, guild_id)
    vampytest.assert_eq(output.batch_id, batch_id)
    vampytest.assert_eq(output.template_id, template_id)
    vampytest.assert_eq(output.requirements, requirements)
    vampytest.assert_eq(output.rewards, rewards)
