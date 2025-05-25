__all__ = (
    'QUEST_TYPE_NONE', 'QUEST_TYPE_ITEM_SUBMISSION', 'QUEST_TYPE_MONSTER_SUBJUGATION_LOCATED',
    'QUEST_TYPE_MONSTER_SUBJUGATION_SELECTED', 'get_quest_type_name'
)

from .constants import QUEST_TYPE_NAME_DEFAULT

QUEST_TYPE_NONE = 0
QUEST_TYPE_ITEM_SUBMISSION = 1
QUEST_TYPE_MONSTER_SUBJUGATION_SELECTED = 2
QUEST_TYPE_MONSTER_SUBJUGATION_LOCATED = 3


QUEST_TYPE_NAMES = {
    QUEST_TYPE_NONE : 'none',
    QUEST_TYPE_ITEM_SUBMISSION : 'item submission',
    QUEST_TYPE_MONSTER_SUBJUGATION_SELECTED : 'monster subjugation (selected)',
    QUEST_TYPE_MONSTER_SUBJUGATION_LOCATED : 'monster subjugation (located)',
}


def get_quest_type_name(quest_type):
    """
    Gets the name of the given quest type.
    
    Parameters
    ----------
    quest_type : `int`
        Quest type to get name of.
    
    Returns
    -------
    quest_type_name : `str`
    """
    return QUEST_TYPE_NAMES.get(quest_type, QUEST_TYPE_NAME_DEFAULT)
