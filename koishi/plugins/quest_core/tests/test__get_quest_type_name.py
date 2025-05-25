import vampytest

from ..quest_types import QUEST_TYPE_MONSTER_SUBJUGATION_LOCATED, get_quest_type_name


def _iter_options():
    yield -1
    yield QUEST_TYPE_MONSTER_SUBJUGATION_LOCATED


@vampytest._(vampytest.call_from(_iter_options()))
def test__get_quest_type_name(quest_type):
    """
    Tests whether the ``get_quest_type_name`` works as intended.
    
    Parameters
    ----------
    quest_type : `int`
        Quest type to get name of.
    """
    output = get_quest_type_name(quest_type)
    vampytest.assert_instance(output, str)
