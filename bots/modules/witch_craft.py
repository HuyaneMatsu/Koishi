# -*- coding: utf-8 -*-
from hata import BUILTIN_EMOJIS

ITEMS = {}

class CookingFactor(object):
    __slots__ = ('flavor', 'fruit', 'meat', 'monster', 'mushroom', 'vegetable')
    def __new__(cls, *, flavor=0, fruit=0, meat=0, monster=0, mushroom=0, vegetable=0):
        self = object.__new__(cls)
        
        self.flavor = flavor
        self.fruit = fruit
        self.meat = meat
        self.monster = monster
        self.vegetable = vegetable
        self.mushroom = mushroom
        
        return self
    
    def __repr__(self):
        result = ['<', self.__class__.__name__]
        
        flavor = self.flavor
        if flavor:
            result.append(' flavor=')
            result.append(repr(flavor))
            
            should_add_comma = True
        else:
            should_add_comma = False
        
        fruit = self.fruit
        if fruit:
            if should_add_comma:
                result.append(',')
            else:
                should_add_comma = True
            
            result.append(' fruit=')
            result.append(repr(fruit))
        
        meat = self.meat
        if meat:
            if should_add_comma:
                result.append(',')
            else:
                should_add_comma = True
            
            result.append(' meat=')
            result.append(repr(meat))
        
        monster = self.monster
        if monster:
            if should_add_comma:
                result.append(',')
            else:
                should_add_comma = True
            
            result.append(' monster=')
            result.append(repr(monster))
        
        mushroom = self.mushroom
        if mushroom:
            if should_add_comma:
                result.append(',')
            else:
                should_add_comma = True
            
            result.append(' mushroom=')
            result.append(repr(mushroom))
        
        vegetable = self.vegetable
        if vegetable:
            if should_add_comma:
                result.append(',')
            
            result.append(' vegetable=')
            result.append(repr(vegetable))
        
        result.append('>')
        
        return ''.join(result)
    
    def get_raw_cost(self):
        cost = 0.0
        
        flavor = self.flavor
        cost += (flavor*flavor)*0.4
        
        fruit = self.fruit
        cost += fruit*fruit
        
        meat = self.meat
        cost += meat*meat
        
        vegetable = self.vegetable
        cost += vegetable*vegetable
        
        mushroom = self.mushroom
        cost += (mushroom*mushroom)*2.0
        
        monster = self.monster
        cost += monster*monster
        
        return cost


class EdibilityFactor(object):
    __slots__ = ('health', 'hunger', 'sanity')
    def __new__(cls, *, health=0, hunger=0, sanity=0):
        self = object.__new__(cls)
        self.health = health
        self.hunger = hunger
        self.sanity = sanity
        return self
    
    def __repr__(self):
        result = ['<', self.__class__.__name__]
        
        health = self.health
        if health:
            result.append(' health=')
            result.append(repr(health))
            
            should_add_comma = True
        else:
            should_add_comma = False
        
        hunger = self.hunger
        if hunger:
            if should_add_comma:
                result.append(',')
            else:
                should_add_comma = True
            
            result.append(' hunger=')
            result.append(repr(hunger))
        
        sanity = self.sanity
        if sanity:
            if should_add_comma:
                result.append(',')
            
            result.append(' sanity=')
            result.append(repr(sanity))
        
        result.append('>')
        
        return ''.join(result)
    
    def get_raw_cost(self):
        cost = 0.0
        health = self.health
        cost += health*health
        
        hunger = self.hunger
        cost += hunger*hunger
        
        sanity = self.sanity
        cost += sanity*sanity
        
        return cost


class Item(object):
    __slots__ = ('cost', 'cooking', 'edibility', 'emoji', 'id', 'name')
    def __new__(cls, id_, name, emoji, *, cooking=None, edibility=None):
        cost = 0
        if (cooking is not None):
            cost += cooking.get_raw_cost()
        
        if (edibility is not None):
            cost += cooking.get_raw_cost()
        
        cost = int(cost**0.5)
        
        self = object.__new__(cls)
        self.id = id_
        self.name = name
        self.emoji = emoji
        self.cost = cost
        
        self.cooking = cooking
        self.edibility = edibility
        
        ITEMS[id_] = self
        return self
    
    def __repr__(self):
        result = ['<', self.__class__.__name__]
        
        result.append(' id=')
        result.append(repr(self.id))
        
        result.append(', name=')
        result.append(repr(self.name))
        
        result.append(', emoji=')
        result.append(repr(self.emoji.name))
        
        result.append(', cost=')
        result.append(repr(self.cost))
        
        cooking = self.cooking
        if (cooking is not None):
            result.append(', cooking=')
            result.append(repr(cooking))
        
        edibility = self.edibility
        if (edibility is not None):
            result.append(', edibility=')
            result.append(repr(edibility))
        
        result.append('>')
        
        return ''.join(result)



ITEM_DUCK = Item(1, 'Duck', BUILTIN_EMOJIS['duck'],
    cooking=CookingFactor(flavor=100, meat=100, monster=20),
    edibility=EdibilityFactor(hunger=40, sanity=-20),
        )

ITEM_SALT = Item(2, 'Flavor crystal', BUILTIN_EMOJIS['salt'],
    cooking=CookingFactor(flavor=100),
    edibility=EdibilityFactor(health=-20, hunger=0, sanity=-20),
        )

ITEM_ONION = Item(3, 'Organic tear gas', BUILTIN_EMOJIS['onion'],
    cooking=CookingFactor(flavor=50, vegetable=40),
    edibility=EdibilityFactor(health=5, hunger=5, sanity=-10),
        )

ITEM_EGG = Item(4, 'Next generation (capsule)', BUILTIN_EMOJIS['egg'],
    cooking=CookingFactor(flavor=50, meat=50),
    edibility=EdibilityFactor(health=5, hunger=10),
        )

ITEM_RED_MUSHROOM = Item(5, 'Witch hallucinogen', BUILTIN_EMOJIS['mushroom'],
    cooking=CookingFactor(flavor=50, mushroom=100),
    edibility=EdibilityFactor(health=-20, hunger=10, sanity=-5),
        )

ITEM_GARLIC = Item(6, 'Anti-vampire grenade', BUILTIN_EMOJIS['garlic'],
    cooking=CookingFactor(flavor=100, vegetable=30),
    edibility=EdibilityFactor(health=10, hunger=5, sanity=-10),
        )

ITEM_OIL = Item(7, 'Pan slipper', BUILTIN_EMOJIS['oil'],
    cooking=CookingFactor(flavor=30, vegetable=20, fruit=20),
    edibility=EdibilityFactor(hunger=5, sanity=-10),
        )

ITEM_OLIVE = Item(8, 'Slipper fruit', BUILTIN_EMOJIS['olive'],
    cooking=CookingFactor(flavor=30, fruit=30),
    edibility=EdibilityFactor(health=10, hunger=10),
        )

BUYABLE = [
    ITEM_SALT,
    ITEM_ONION,
    ITEM_RED_MUSHROOM,
    ITEM_GARLIC,
    ITEM_OLIVE,
        ]





