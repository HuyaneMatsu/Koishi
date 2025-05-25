from random import Random

import vampytest

from ..quest import Quest
from ..quest_batch_generation import create_quest_from_template
from ..quest_templates import QUEST_SAKUYA_STRAWBERRY


def test__create_quest_from_template():
    """
    Tests whether ``create_quest_from_template`` works as intended.
    """
    random_number_generator = Random()
    quest_template = QUEST_SAKUYA_STRAWBERRY
    
    quest = create_quest_from_template(random_number_generator, quest_template)
    
    vampytest.assert_instance(quest, Quest)
    vampytest.assert_eq(quest.template_id, quest_template.id)
