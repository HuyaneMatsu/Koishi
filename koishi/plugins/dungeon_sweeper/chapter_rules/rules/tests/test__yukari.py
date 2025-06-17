import vampytest
from hata import Component

from ....chapters import CHAPTER_YUKARI
from ....chapter_styles import CHAPTER_STYLE_YUKARI

from ..yukari import CHAPTER_RULE_YUKARI


def test__CHAPTER_RULE_YUKARI__component_builder():
    """
    Tests whether ``CHAPTER_STYLE_YUKARI.component_builder`` works as intended.
    """
    output = CHAPTER_RULE_YUKARI.component_builder(CHAPTER_YUKARI, CHAPTER_STYLE_YUKARI)
    vampytest.assert_instance(output, Component)
