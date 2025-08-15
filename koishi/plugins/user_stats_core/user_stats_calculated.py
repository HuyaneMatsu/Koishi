__all__ = ()

from scarletio import RichAttributeErrorBaseType

from ..item_core import get_item_nullable
from ..item_modifier_core import (
    MODIFIER_ID__BUTCHERING, MODIFIER_ID__ENERGY, MODIFIER_ID__FISHING, MODIFIER_ID__FORAGING, MODIFIER_ID__GARDENING,
    MODIFIER_ID__HEALTH, MODIFIER_ID__HUNTING, MODIFIER_ID__INVENTORY, MODIFIER_ID__MOVEMENT,
    MODIFIER_ID__STAT_BEDROOM, MODIFIER_ID__STAT_CHARM, MODIFIER_ID__STAT_CUTENESS, MODIFIER_ID__STAT_HOUSEWIFE,
    MODIFIER_ID__STAT_LOYALTY, accumulate_modifier_values, apply_modifiers
)

from .calculations import (
    calculate_butchering, accumulate_item_weight, calculate_energy, calculate_fishing, calculate_foraging,
    calculate_health, calculate_hunting, calculate_gardening, calculate_inventory, calculate_movement
)


class UserStatsCalculated(RichAttributeErrorBaseType):
    """
    Represents calculated stats of a user.
    
    Attributes
    ----------
    extra_butchering : `int`
        The user's butchering skills.
    
    extra_energy : `int`
        The user's energy.
    
    extra_fishing : `int`
        The user's fishing skills.
    
    extra_foraging : `int`
        The user's foraging skills.
    
    extra_gardening : `int`
        The user's gardening skills.
    
    extra_health : `int`
        The user's health.
    
    extra_hunting : `int`
        The user's hunting skills.
    
    extra_inventory : `int`
        The user's inventory size (grams).
    
    extra_movement : `int`
        The user's movement speed (mm / s).
    
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
        'extra_butchering', 'extra_energy', 'extra_fishing', 'extra_foraging', 'extra_gardening', 'extra_health',
        'extra_hunting', 'extra_inventory', 'extra_movement', 'item_costume', 'item_head', 'item_species',
        'item_weapon', 'stat_bedroom', 'stat_charm', 'stat_cuteness', 'stat_housewife', 'stat_loyalty',
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
        
        # extra movement
        extra_movement = calculate_movement(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty)
        extra_movement = apply_modifiers(extra_movement, modifiers, MODIFIER_ID__MOVEMENT)
        
        # extra health
        extra_health = calculate_health(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty)
        extra_health = apply_modifiers(extra_health, modifiers, MODIFIER_ID__HEALTH)
        
        # extra energy
        extra_energy = calculate_energy(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty)
        extra_energy = apply_modifiers(extra_energy, modifiers, MODIFIER_ID__ENERGY)
        
        # extra butchering
        extra_butchering = calculate_butchering(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty)
        extra_butchering = apply_modifiers(extra_butchering, modifiers, MODIFIER_ID__BUTCHERING)
        
        # extra fishing
        extra_fishing = calculate_fishing(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty)
        extra_fishing = apply_modifiers(extra_fishing, modifiers, MODIFIER_ID__FISHING)
        
        # extra foraging
        extra_foraging = calculate_foraging(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty)
        extra_foraging = apply_modifiers(extra_foraging, modifiers, MODIFIER_ID__FORAGING)
        
        # extra gardening
        extra_gardening = calculate_gardening(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty)
        extra_gardening = apply_modifiers(extra_gardening, modifiers, MODIFIER_ID__GARDENING)
        
        # extra hunting
        extra_hunting = calculate_hunting(stat_bedroom, stat_charm, stat_cuteness, stat_housewife, stat_loyalty)
        extra_hunting = apply_modifiers(extra_hunting, modifiers, MODIFIER_ID__HUNTING)
        
        
        # Construct
        self = object.__new__(cls)
        
        self.stat_bedroom = stat_bedroom
        self.stat_charm = stat_charm
        self.stat_cuteness = stat_cuteness
        self.stat_housewife = stat_housewife
        self.stat_loyalty = stat_loyalty
        
        self.item_costume = item_costume
        self.item_head = item_head
        self.item_species = item_species
        self.item_weapon = item_weapon
        
        self.extra_inventory = extra_inventory
        self.extra_movement = extra_movement
        self.extra_energy = extra_energy
        self.extra_health = extra_health
        
        self.extra_butchering = extra_butchering
        self.extra_fishing = extra_fishing
        self.extra_foraging = extra_foraging
        self.extra_gardening = extra_gardening
        self.extra_hunting = extra_hunting
        
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        # stats
        
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
        
        # items
        
        # item_costume
        item_costume = self.item_costume
        if (item_costume is not None):
            repr_parts.append(', item_costume = ')
            repr_parts.append(repr(self.item_costume))
        
        # item_head
        item_head = self.item_head
        if (item_head is not None):
            repr_parts.append(', item_head = ')
            repr_parts.append(repr(item_head))
        
        # item_species
        item_species = self.item_species
        if (item_species is not None):
            repr_parts.append(', item_species = ')
            repr_parts.append(repr(item_species))
        
        # item_weapon
        item_weapon = self.item_weapon
        if (item_weapon is not None):
            repr_parts.append(', item_weapon = ')
            repr_parts.append(repr(item_weapon))
        
        # extra
        
        # extra_inventory
        repr_parts.append(', extra_inventory = ')
        repr_parts.append(repr(self.extra_inventory))
        
        # extra_movement
        repr_parts.append(', extra_movement = ')
        repr_parts.append(repr(self.extra_movement))
        
        # extra_health
        repr_parts.append(', extra_health = ')
        repr_parts.append(repr(self.extra_health))
        
        # extra_energy
        repr_parts.append(', extra_energy = ')
        repr_parts.append(repr(self.extra_energy))
        
        # extra_butchering
        repr_parts.append(', extra_butchering = ')
        repr_parts.append(repr(self.extra_butchering))
        
        # extra_fishing
        repr_parts.append(', extra_fishing = ')
        repr_parts.append(repr(self.extra_fishing))
        
        # extra_foraging
        repr_parts.append(', extra_foraging = ')
        repr_parts.append(repr(self.extra_foraging))
        
        # extra_gardening
        repr_parts.append(', extra_gardening = ')
        repr_parts.append(repr(self.extra_gardening))
        
        # extra_hunting
        repr_parts.append(', extra_hunting = ')
        repr_parts.append(repr(self.extra_hunting))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
