__all__ = ('QuestRewardGeneratorBase',)

from scarletio import copy_docs

from ..quest_reward_instantiables import QuestRewardInstantiableBase
from ..quest_reward_types import QUEST_REWARD_TYPE_NONE
from ..sub_type_bases import QuestSubTypeGenerator


class QuestRewardGeneratorBase(QuestSubTypeGenerator):
    """
    Base type for quest reward generation.
    """
    TYPE = QUEST_REWARD_TYPE_NONE
    
    __slots__ = ()
    
    @copy_docs(QuestSubTypeGenerator.generate)
    def generate(self, random_number_generator):
        return self.generate_with_diversion(1.0)
    
    
    @copy_docs(QuestSubTypeGenerator.generate_with_diversion)
    def generate_with_diversion(self, random_number_generator, accumulated_diversion):
        return (
            QuestRewardInstantiableBase(),
            1.0,
        )
