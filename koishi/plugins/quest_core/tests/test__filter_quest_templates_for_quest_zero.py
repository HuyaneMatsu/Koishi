import vampytest

from ..quest_batch_generation import filter_quest_templates_for_quest_zero
from ..quest_template import QuestTemplate
from ..quest_types import QUEST_TYPE_ITEM_SUBMISSION


def test__filter_quest_templates_for_quest_zero():
    """
    Tests whether ``filter_quest_templates_for_quest_zero`` works as intended.
    """
    output = filter_quest_templates_for_quest_zero()
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, QuestTemplate)
    
    for element in output:
        vampytest.assert_eq(element.type, QUEST_TYPE_ITEM_SUBMISSION)
        vampytest.assert_eq(element.level, 0)
