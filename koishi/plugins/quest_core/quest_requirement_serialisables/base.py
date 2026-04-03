__all__ = ('QuestRequirementSerialisableBase',)

from ..quest_requirement_types import QUEST_REQUIREMENT_TYPE_NONE
from ..sub_type_bases import QuestSubTypeSerialisable


class QuestRequirementSerialisableBase(QuestSubTypeSerialisable):
    """
    Base type for requirement completion state.
    """
    TYPE = QUEST_REQUIREMENT_TYPE_NONE
    
    __slots__ = ()
