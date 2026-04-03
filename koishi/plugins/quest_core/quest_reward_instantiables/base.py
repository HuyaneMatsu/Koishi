__all__ = ('QuestRewardInstantiableBase',)

from scarletio import copy_docs

from ..quest_reward_serialisables import QuestRewardSerialisableBase
from ..quest_reward_types import QUEST_REWARD_TYPE_NONE
from ..sub_type_bases import QuestSubTypeInstantiable


class QuestRewardInstantiableBase(QuestSubTypeInstantiable):
    """
    Base type for quest rewards.
    """
    TYPE = QUEST_REWARD_TYPE_NONE
    
    __slots__ = ()
    
    @copy_docs(QuestSubTypeInstantiable.instantiate)
    def instantiate(self):
        return QuestRewardSerialisableBase()
