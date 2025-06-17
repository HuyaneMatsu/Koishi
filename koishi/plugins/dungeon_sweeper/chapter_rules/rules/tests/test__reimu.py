import vampytest
from hata import Component

from ....chapters import CHAPTER_REIMU
from ....chapter_styles import CHAPTER_STYLE_REIMU

from ..reimu import CHAPTER_RULE_REIMU


def test__CHAPTER_RULE_REIMU__component_builder():
    """
    Tests whether ``CHAPTER_STYLE_REIMU.component_builder`` works as intended.
    """
    output = CHAPTER_RULE_REIMU.component_builder(CHAPTER_REIMU, CHAPTER_STYLE_REIMU)
    vampytest.assert_instance(output, Component)
