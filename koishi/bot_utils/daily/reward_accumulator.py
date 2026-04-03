__all__ = ('RewardAccumulator',)

from scarletio import RichAttributeErrorBaseType


class RewardAccumulator(RichAttributeErrorBaseType):
    """
    Accumulates rewards.
    
    Attributes
    ----------
    base : `int`
        Base reward.
    
    extra_limit : `int`
        Extra reward extra_limit.
    
    extra_per_streak : `int`
        Extra reward for each streak.
    """
    __slots__ = ('base', 'extra_limit', 'extra_per_streak')
    
    def __new__(cls):
        """
        Creates a new reward accumulator.
        """
        self = object.__new__(cls)
        self.base = 0
        self.extra_limit = 0
        self.extra_per_streak = 0
        return self
    
    
    def __repr__(self):
        """Returns repr(self)"""
        repr_parts = ['<', type(self).__name__]
        
        # base
        repr_parts.append(' base = ')
        repr_parts.append(repr(self.base))
        
        # limit
        repr_parts.append(', extra_limit = ')
        repr_parts.append(repr(self.extra_limit))
        
        # extra_per_streak
        repr_parts.append(', extra_per_streak = ')
        repr_parts.append(repr(self.extra_per_streak))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def add_rewards(self, rewards, user):
        """
        Accumulates the rewards.
        
        Parameters
        ----------
        rewards : `tuple<Reward>`
            Rewards to accumulate from.
        
        user : ``ClientUserBase``
            Respective user for additional checks.
        """
        for reward in rewards:
            self.add_reward(reward, user)
    
    
    def add_reward(self, reward, user):
        """
        Adds a single reward to self.
        
        Parameters
        ----------
        reward : `Reward`
            Reward to add.
        
        user : ``ClientUserBase``
            Respective user for additional checks.
        
        Returns
        -------
        added : `bool`
        """
        condition = reward.condition
        if (condition is not None) and (not condition(user)):
            return False
        
        self.base += reward.base
        self.extra_limit += reward.extra_limit
        self.extra_per_streak += reward.extra_per_streak
        return True
    
    
    def sum_rewards(self, streak):
        """
        Sums the accumulated rewards with the given streak.
        
        Parameters
        ----------
        streak : `int`
            The streak of the user.
        
        Returns
        -------
        sum : `int`
        """
        return self.base + min(streak * self.extra_per_streak, self.extra_limit) + streak
