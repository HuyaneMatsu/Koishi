__all__ = ('QuestRewardSerialisableBase',)

from ..quest_reward_types import QUEST_REWARD_TYPE_NONE
from ..sub_type_bases import QuestSubTypeSerialisable


class QuestRewardSerialisableBase(QuestSubTypeSerialisable):
    """
    Base type for reward completion state.
    """
    TYPE = QUEST_REWARD_TYPE_NONE
    
    __slots__ = ()
