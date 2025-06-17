import vampytest

from ..chapters import Chapter
from ..component_building import iter_chapters_ordered


def test__iter_chapters_ordered():
    """
    Tests whether ``iter_chapters_ordered`` works as intended.
    """
    output = [*iter_chapters_ordered()]
    
    for element in output:
        vampytest.assert_instance(element, Chapter)
    
    vampytest.assert_eq(
        [element.id for element in output],
        [1, 2, 3],
    )
