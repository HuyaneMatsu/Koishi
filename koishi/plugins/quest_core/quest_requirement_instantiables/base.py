__all__ = ('QuestRequirementInstantiableBase',)

from scarletio import copy_docs

from ..quest_requirement_serialisables import QuestRequirementSerialisableBase
from ..quest_requirement_types import QUEST_REQUIREMENT_TYPE_NONE
from ..sub_type_bases import QuestSubTypeInstantiable


class QuestRequirementInstantiableBase(QuestSubTypeInstantiable):
    """
    Base type for quest requirements.
    """
    TYPE = QUEST_REQUIREMENT_TYPE_NONE
    
    __slots__ = ()
    
    @copy_docs(QuestSubTypeInstantiable.instantiate)
    def instantiate(self):
        return QuestRequirementSerialisableBase()
