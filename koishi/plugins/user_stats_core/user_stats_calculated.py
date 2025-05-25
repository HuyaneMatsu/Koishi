__all__ = ()

from scarletio import RichAttributeErrorBaseType

from ..item_core import get_item_nullable
from ..item_modifier_core import (
    MODIFIER_ID__FISHING, MODIFIER_ID__INVENTORY, MODIFIER_ID__STAT_BEDROOM, MODIFIER_ID__STAT_CHARM,
    MODIFIER_ID__STAT_CUTENESS, MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_ID__STAT_LOYALTY, accumulate_modifier_values,
    apply_modifiers
)

from .calculations import accumulate_item_weight, calculate_fishing, calculate_inventory


class UserStatsCalculated(RichAttributeErrorBaseType):
    """
    Represents calculated stats of a user.
    
    Attributes
    ----------
    extra_fishing : `int`
        The user's fishing skills.
    
    extra_inventory : `int`
        The user's inventory size (grams).
    
    item_costume : ``None | Item``
        The user's costume.
    
    item_head : ``None | Item``
        The user's head item.
    
    item_species : ``None | Item``
        The user's species.
    
    item_weapon : ``None | Item``
        The user's weapon item.
    
    stat_bedroom : `int`
        The user's bedroom skills.
    
    stat_charm : `int`
        The user's charm.
    
    stat_cuteness : `int`
        The user's cuteness.
    
    stat_housewife : `int`
        The user's housewife capabilities.
    
    stat_loyalty : `int`
        The user's loyalty.
    """
    __slots__ = (
        'extra_fishing', 'extra_inventory', 'item_costume', 'item_head', 'item_species', 'item_weapon', 'stat_bedroom',
        'stat_charm', 'stat_cuteness', 'stat_housewife', 'stat_loyalty',
    )
    
    def __new__(cls, stats):
        """
        Creates a new stats calculated instance.
        
        Parameters
        ----------
        stats : ``UserStats``
        """
        item_costume = get_item_nullable(stats.item_id_costume)
        item_head = get_item_nullable(stats.item_id_head)
        item_species = get_item_nullable(stats.item_id_species)
        item_weapon = get_item_nullable(stats.item_id_weapon)
        
        modifiers = accumulate_modifier_values(item_costume, item_head, item_species, item_weapon)
        
        stat_bedroom = apply_modifiers(stats.stat_bedroom, modifiers, MODIFIER_ID__STAT_BEDROOM)
        stat_charm = apply_modifiers(stats.stat_charm, modifiers, MODIFIER_ID__STAT_CHARM)
        stat_cuteness = apply_modifiers(stats.stat_cuteness, modifiers, MODIFIER_ID__STAT_CUTENESS)
        stat_housewife = apply_modifiers(stats.stat_housewife, modifiers, MODIFIER_ID__STAT_HOUSEWIFE)
        stat_loyalty = apply_modifiers(stats.stat_loyalty, modifiers, MODIFIER_ID__STAT_LOYALTY)
        
        # extra inventory
        extra_inventory = calculate_inventory(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty)
        extra_inventory = apply_modifiers(extra_inventory, modifiers, MODIFIER_ID__INVENTORY)
        extra_inventory -= accumulate_item_weight(item_costume, item_head, item_species, item_weapon)
        
        # extra fishing
        extra_fishing = calculate_fishing(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty)
        extra_fishing = apply_modifiers(extra_fishing, modifiers, MODIFIER_ID__FISHING)
        
        
        self = object.__new__(cls)
        self.extra_fishing = extra_fishing
        self.extra_inventory = extra_inventory
        self.item_costume = item_costume
        self.item_head = item_head
        self.item_species = item_species
        self.item_weapon = item_weapon
        self.stat_bedroom = stat_bedroom
        self.stat_charm = stat_charm
        self.stat_cuteness = stat_cuteness
        self.stat_housewife = stat_housewife
        self.stat_loyalty = stat_loyalty
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        field_added = False
        
        # items
        
        # item_costume
        item_costume = self.item_costume
        if (item_costume is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' item_costume = ')
            repr_parts.append(repr(self.item_costume))
        
        # item_head
        item_head = self.item_head
        if (item_head is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' item_head = ')
            repr_parts.append(repr(item_head))
        
        # item_species
        item_species = self.item_species
        if (item_species is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' item_species = ')
            repr_parts.append(repr(item_species))
        
        # item_weapon
        item_weapon = self.item_weapon
        if (item_weapon is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' item_weapon = ')
            repr_parts.append(repr(item_weapon))
        
        # stats
        
        if field_added:
            repr_parts.append(',')
        
        # stat_bedroom
        repr_parts.append(' stat_bedroom = ')
        repr_parts.append(repr(self.stat_bedroom))
        
        # stat_charm
        repr_parts.append(', stat_charm = ')
        repr_parts.append(repr(self.stat_charm))
        
        # stat_cuteness
        repr_parts.append(', stat_cuteness = ')
        repr_parts.append(repr(self.stat_cuteness))
        
        # stat_housewife
        repr_parts.append(', stat_housewife = ')
        repr_parts.append(repr(self.stat_housewife))
        
        # stat_loyalty
        repr_parts.append(', stat_loyalty = ')
        repr_parts.append(repr(self.stat_loyalty))
        
        # extra
        
        # extra_fishing
        repr_parts.append(', extra_fishing = ')
        repr_parts.append(repr(self.extra_fishing))
        
        # extra_inventory
        repr_parts.append(', extra_inventory = ')
        repr_parts.append(repr(self.extra_inventory))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
