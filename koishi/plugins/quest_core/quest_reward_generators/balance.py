__all__ = ('QuestRewardGeneratorBalance',)

from scarletio import copy_docs

from ..generation_helpers import get_random_value_and_diversity_with_variance
from ..quest_reward_instantiables import QuestRewardInstantiableBalance
from ..quest_reward_types import QUEST_REWARD_TYPE_BALANCE

from .base import QuestRewardGeneratorBase


class QuestRewardGeneratorBalance(QuestRewardGeneratorBase):
    """
    Represents a quest reward generator with fix balance.
    
    Attributes
    ----------
    balance_base : `int`
        The balance given by the quest.
    
    balance_require_multiple_of : `int`
        Value to require the balance to be multiple of.
    
    balance_variance_percentage_lower_threshold : `int`
        Lower threshold of for balance variance in percentage.
    
    balance_variance_percentage_upper_threshold : `int`
        Upper threshold of for balance variance in percentage.
    """
    TYPE = QUEST_REWARD_TYPE_BALANCE
    
    __slots__ = (
        'balance_base', 'balance_require_multiple_of', 'balance_variance_percentage_lower_threshold',
        'balance_variance_percentage_upper_threshold',
    )
    
    def __new__(
        cls,
        balance_base,
        balance_require_multiple_of,
        balance_variance_percentage_lower_threshold,
        balance_variance_percentage_upper_threshold,
    ):
        """
        Creates a new balance reward generator.
        
        Parameters
        ----------
        balance_base : `int`
            The balance given by the quest.
        
        balance_require_multiple_of : `int`
            Value to require the balance to be multiple of.
        
        balance_variance_percentage_lower_threshold : `int`
            Lower threshold of for balance variance in percentage.
        
        balance_variance_percentage_upper_threshold : `int`
            Upper threshold of for balance variance in percentage.
        """
        self = object.__new__(cls)
        self.balance_base = balance_base
        self.balance_require_multiple_of = balance_require_multiple_of
        self.balance_variance_percentage_lower_threshold = balance_variance_percentage_lower_threshold
        self.balance_variance_percentage_upper_threshold = balance_variance_percentage_upper_threshold
        return self
    
    
    @copy_docs(QuestRewardGeneratorBase._produce_representation_middle)
    def _produce_representation_middle(self):
        # balance_base
        yield ' balance_base = '
        yield repr(self.balance_base)
        
        # balance_require_multiple_of
        yield ', balance_require_multiple_of = '
        yield repr(self.balance_require_multiple_of)
        
        # balance_variance_percentage_lower_threshold
        yield ', balance_variance_percentage_lower_threshold = '
        yield repr(self.balance_variance_percentage_lower_threshold)
        
        # balance_variance_percentage_upper_threshold
        yield ', balance_variance_percentage_upper_threshold = '
        yield repr(self.balance_variance_percentage_upper_threshold)
    
    
    @copy_docs(QuestRewardGeneratorBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        # balance_base
        if self.balance_base != other.balance_base:
            return False
        
        # balance_require_multiple_of
        if self.balance_require_multiple_of != other.balance_require_multiple_of:
            return False
        
        # balance_variance_percentage_lower_threshold
        if self.balance_variance_percentage_lower_threshold != other.balance_variance_percentage_lower_threshold:
            return False
        
        # balance_variance_percentage_upper_threshold
        if self.balance_variance_percentage_upper_threshold != other.balance_variance_percentage_upper_threshold:
            return False
        
        return True
    
    
    @copy_docs(QuestRewardGeneratorBase.generate_with_diversion)
    def generate_with_diversion(self, random_number_generator, accumulated_diversion):

        balance, diversion = get_random_value_and_diversity_with_variance(
            random_number_generator,
            round(self.balance_base * accumulated_diversion),
            self.balance_require_multiple_of,
            self.balance_variance_percentage_lower_threshold,
            self.balance_variance_percentage_upper_threshold,
        )
        
        return (
            QuestRewardInstantiableBalance(balance),
            (1.0 / diversion),
        )
