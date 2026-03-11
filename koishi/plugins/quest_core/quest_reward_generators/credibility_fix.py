__all__ = ('QuestRewardGeneratorCredibilityFix',)

from scarletio import copy_docs

from ..quest_reward_instantiables import QuestRewardInstantiableCredibility

from .credibility import QuestRewardGeneratorCredibility


class QuestRewardGeneratorCredibilityFix(QuestRewardGeneratorCredibility):
    """
    Represents a quest reward generator with fix credibility.
    
    Attributes
    ----------
    credibility_base : `int`
        The credibility given by the quest.
    """
    __slots__ = ()
   
    @copy_docs(QuestRewardGeneratorCredibility.generate_with_diversion)
    def generate_with_diversion(self, random_number_generator, accumulated_diversion):
        return (
            QuestRewardInstantiableCredibility(self.credibility_base),
            1.0,
        )
