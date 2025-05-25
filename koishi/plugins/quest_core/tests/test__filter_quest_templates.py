import vampytest

from ..quest_batch_generation import filter_quest_templates
from ..quest_template import QuestTemplate
from ..quest_templates import QUEST_TEMPLATE_MYSTIA_PEACH


def test__filter_quest_templates():
    """
    Tests whether ``filter_quest_templates`` works as intended.
    """
    level_limit = 2
    exclude = {QUEST_TEMPLATE_MYSTIA_PEACH.id}
    
    output = filter_quest_templates(level_limit, exclude)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, QuestTemplate)
    
    for element in output:
        vampytest.assert_true(element.level <= level_limit)
        vampytest.assert_not_in(element.id, exclude)
