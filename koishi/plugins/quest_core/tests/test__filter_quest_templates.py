import vampytest

from ..quest_batch_generation import filter_quest_templates
from ..quest_template import QuestTemplate
from ..quest_templates import QUEST_TEMPLATE_MYSTIA_PEACH


def test__filter_quest_templates():
    """
    Tests whether ``filter_quest_templates`` works as intended.
    """
    level_limit = 2
    excluded_quest_template_ids = {QUEST_TEMPLATE_MYSTIA_PEACH.id}
    
    output = filter_quest_templates(excluded_quest_template_ids, level_limit)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, QuestTemplate)
    
    for element in output:
        vampytest.assert_true(element.level <= level_limit)
        vampytest.assert_not_in(element.id, excluded_quest_template_ids)
