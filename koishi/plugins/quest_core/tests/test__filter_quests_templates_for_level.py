import vampytest

from ..quest_batch_generation import filter_quest_templates_for_level
from ..quest_template import QuestTemplate


def test__filter_quest_templates_for_level():
    """
    Tests whether ``filter_quest_templates_for_level`` works as intended.
    """
    excluded_quest_template_ids = set()
    level = 1
    
    output = filter_quest_templates_for_level(excluded_quest_template_ids, level)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, QuestTemplate)
    
    for element in output:
        vampytest.assert_eq(element.level, level)
