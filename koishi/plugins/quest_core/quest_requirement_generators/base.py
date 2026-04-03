__all__ = ('QuestRequirementGeneratorBase',)

from scarletio import copy_docs

from ..quest_requirement_types import QUEST_REQUIREMENT_TYPE_NONE
from ..quest_requirement_instantiables import QuestRequirementInstantiableBase
from ..sub_type_bases import QuestSubTypeGenerator


class QuestRequirementGeneratorBase(QuestSubTypeGenerator):
    """
    Base type for quest requirement generation.
    """
    TYPE = QUEST_REQUIREMENT_TYPE_NONE
    
    __slots__ = ()
    
    @copy_docs(QuestSubTypeGenerator.generate)
    def generate(self, random_number_generator):
        return (
            QuestRequirementInstantiableBase(),
            1.0,
        )
