import vampytest
from hata import Component

from ....chapters import CHAPTER_FLANDRE
from ....chapter_styles import CHAPTER_STYLE_FLANDRE

from ..flandre import CHAPTER_RULE_FLANDRE


def test__CHAPTER_RULE_FLANDRE__component_builder():
    """
    Tests whether ``CHAPTER_STYLE_FLANDRE.component_builder`` works as intended.
    """
    output = CHAPTER_RULE_FLANDRE.component_builder(CHAPTER_FLANDRE, CHAPTER_STYLE_FLANDRE)
    vampytest.assert_instance(output, Component)
