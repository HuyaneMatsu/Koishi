__all__ = ('OptionBattle',)

from scarletio import copy_docs

from .base import OptionBase


class OptionBattle(OptionBase):
    """
    Represents battled enemies for completing an action.
    
    Attributes
    ----------
    amount_base : `int`
        The base amount that is always given.
    
    amount_interval : `int`
        The interval between the base amount and the maximal amount that can be given.
    
    chance_in : `int`
        The chance to be chosen in.
    
    chance_out : `int`
        The chance to be chosen out of.
    
    enemy_id : `int`
        The given enemy's identifier.
    
    loot : ``None | tuple<LootOption>``
        Additional role options for battled enemies.
    """
    __slots__ = ('enemy_id', 'loot')
    
    def __new__(cls, chance_in, chance_out, amount_min, amount_max, enemy_id, loot):
        """
        Creates a new battle option.
        
        Parameters
        ----------
        chance_in : `int`
            The chance to be chosen in.
        
        chance_out : `int`
            The chance to be chosen out of.
        
        amount_min : `int`
            The minimal amount to battle.
        
        amount_max : `int`
            The maximal amount to battle.
        
        enemy_id : `int`
            The given enemy's identifier.
        
        loot : ``None | tuple<LootOption>``
            Additional role options for battled enemies.
        """
        self = OptionBase.__new__(cls, chance_in, chance_out, amount_min, amount_max)
        self.enemy_id = enemy_id
        self.loot = loot
        return self
    
    
    @copy_docs(OptionBase._produce_nested_repr_parts)
    def _produce_nested_repr_parts(self):
        yield from OptionBase._produce_nested_repr_parts(self)
        
        # enemy_id
        yield ', enemy_id = '
        yield repr(self.enemy_id)
        
        # loot
        yield ', loot = '
        yield repr(self.loot)
    
    
    @copy_docs(OptionBase._is_equal_same_type)
    def _is_equal_same_type(self, other):
        if not OptionBase._is_equal_same_type(self, other):
            return False
        
        # enemy_id
        if self.enemy_id != other.enemy_id:
            return False
        
        # loot
        if self.loot != other.loot:
            return False
        
        return True
    
    
    @copy_docs(OptionBase.__hash__)
    def __hash__(self):
        hash_value = OptionBase.__hash__(self)
        
        # enemy_id
        hash_value ^= self.enemy_id
        
        # loot
        loot = self.loot
        if (loot is not None):
            hash_value ^= len(loot) << 34
            for loot_option in loot:
                hash_value ^= hash(loot_option)
        
        return hash_value
