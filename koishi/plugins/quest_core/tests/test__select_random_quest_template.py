from random import Random
import vampytest

from ..quest_batch_generation import select_random_quest_template
from ..quest_template import QuestTemplate
from ..quest_templates import QUEST_TEMPLATE_SAKUYA_BLUEBERRY


def test__select_random_quest_template():
    """
    tests whether ``select_random_quest_template`` works as intended.
    """
    random_number_generator = Random()
    quest_template = QUEST_TEMPLATE_SAKUYA_BLUEBERRY
    
    output = select_random_quest_template(random_number_generator, [quest_template])
    vampytest.assert_instance(output, QuestTemplate)
    vampytest.assert_is(output, quest_template)
