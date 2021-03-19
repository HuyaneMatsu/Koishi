# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from hata import Client
from hata import BUILTIN_EMOJIS

EMOJI_STAR = BUILTIN_EMOJIS['star']

Koishi: Client

ORIGINS = {}
CHARACTERS = {}
CARD_PACKS = {}

CARD_PACK_ID_NONE = 0
CARD_PACK_ID_ACCELERATION_PACK = 1
CARD_PACK_ID_EXPANSION_PACK = 2
CARD_PACK_ID_COMMUNITY_PACK = 3
CARD_PACK_ID_COMMUNITY_PACK_2 = 4
CARD_PACK_ID_BASE_PACK = 5
CARD_PACK_ID_PUDDING_PACK = 6
CARD_PACK_ID_MIXED_BOOSTER_PACK = 7

CARDS = {}

CARD_RARITY_NONE = 0
CARD_RARITY_COMMON = 1
CARD_RARITY_RARE = 2
CARD_RARITY_UNCOMMON = 3

CARD_TYPE_BATTLE = 1<<0
CARD_TYPE_BOOST = 1<<1
CARD_TYPE_EVENT = 1<<2
CARD_TYPE_GIFT = 1<<3
CARD_TYPE_TRAP = 1<<4
CARD_TYPE_HYPER = 1<<7

CARD_COST_TYPE_STATIC = 0
CARD_COST_TYPE_DIV_STARS = 1
CARD_COST_TYPE_MUL_LEVEL = 2
CARD_COST_TYPE_MUL_CARDS = 3
CARD_COST_TYPE_MUL_OTHERS_CARDS = 4
CARD_COST_TYPE_ALL_STARS = 5

class OJCardCost(object):
    __slots__ = ('type', 'factor')
    def __new__(cls, type_, factor):
        self = object.__new__(cls)
        self.type = type_
        self.factor = factor
        return self
    
    def __gt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        self_type = self.type
        other_type = other.type
        if self_type > other_type:
            return True
        
        if self_type < other_type:
            return False
        
        if self.factor > other.factor:
            return True
        
        return False

    def __ge__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        self_type = self.type
        other_type = other.type
        if self_type > other_type:
            return True
        
        if self_type < other_type:
            return False
        
        if self.factor >= other.factor:
            return True
        
        return False
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.type != other.type:
            return False
        
        if self.factor != other.factor:
            return False
        
        return True
    
    def __ne__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self.type != other.type:
            return True
        
        if self.factor != other.factor:
            return True
        
        return False
    
    def __le__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        self_type = self.type
        other_type = other.type
        if self_type < other_type:
            return True
        
        if self_type > other_type:
            return False
        
        if self.factor <= other.factor:
            return True
        
        return False

    def __lt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        self_type = self.type
        other_type = other.type
        if self_type < other_type:
            return True
        
        if self_type > other_type:
            return False
        
        if self.factor < other.factor:
            return True
        
        return False


class OJEntitySorter(object):
    __slots__ = ('character', 'key', )
    def __new__(cls, character, key):
        self = object.__new__(cls)
        self.character = character
        self.key = key
        return self
    
    def __gt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.key > other.key
    
    def __ge__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.key >= other.key
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.key == other.key
    
    def __ne__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.key != other.key
    
    def __le__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.key <= other.key
    
    def __lt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.key < other.key

class OJEntityBase(object):
    __slots__ = ('id', 'name')
    
    def __gt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.id > other.id
    
    def __ge__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.id >= other.id
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.id == other.id
    
    def __ne__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.id != other.id
    
    def __le__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.id <= other.id
    
    def __lt__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return self.id < other.id
    
    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}, name={self.name!r}>'

class OJOrigin(OJEntityBase):
    __slots__ = ()
    def __new__(cls, identifier, name):
        self = object.__new__(cls)
        self.id = identifier
        self.name = name
        
        ORIGINS[identifier] = self
        return self

class OJCharacter(OJEntityBase):
    __slots__ = ('description', 'hyper_card_ids', 'origin', 'attack', 'defense', 'evasion', 'name', 'recovery', 'hp',
        'card_name',)
    def __new__(cls, identifier, name, hp, attack, defense, evasion, recovery, origin, description, hyper_card_ids,
            card_name=None):
        self = object.__new__(cls)
        self.id = identifier
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.evasion = evasion
        self.recovery = recovery
        self.origin = origin
        self.description = description
        self.hyper_card_ids = hyper_card_ids
        self.card_name = card_name
        CHARACTERS[identifier] = self
        
        return self
    
    def get_sort_key(self, order):
        return OJEntitySorter(self, tuple(self._generate_sort_key(order)))
    
    def _generate_sort_key(self, order):
        if (order is not None):
            for name in order:
                yield CHARACTER_ATTRIBUTE_GETTERS[name]
        
        yield self.id

CHARACTER_ATTRIBUTE_GETTERS = {}

for attribute_name in ('attack', 'defense', 'evasion', 'name', 'recovery', 'hp', 'origin'):
    CHARACTER_ATTRIBUTE_GETTERS[attribute_name] = getattr(OJCharacter, attribute_name)

del attribute_name


def get_characters(order, reverse):
    character_sorters = [character.get_sort_key(order) for character in CHARACTERS]
    character_sorters.sort(reverse=reverse)
    return [character_sorter.character for character_sorter in character_sorters]

class OJCardPack(OJEntityBase):
    __slots__ = ('cost', )
    def __new__(cls, identifier, name, cost):
        self = object.__new__(cls)
        self.id = identifier
        self.name = name
        self.cost = cost
        
        ORIGINS[identifier] = self
        return self

class OJCard(OJEntityBase):
    __slots__ = ('name', 'cost', 'description', 'level', 'type', 'events', 'quote', 'limit', 'card_name')
    def __new__(cls, identifier, name, level, cost, limit, type_, pack, rarity, description, quote, events,
            card_name=None):
        self = object.__new__(cls)
        self.id = identifier
        self.name = name
        self.cost = cost
        self.description = description
        self.type = type_
        self.level = level
        self.events = events
        self.quote = quote
        self.limit = limit
        self.card_name = card_name
        return self


#### #### #### #### ORIGINS #### #### #### ####

ORIGIN_QP_SHOOTING = OJOrigin(1,
    'QP Shooting',
        )

ORIGIN_SUGURI = OJOrigin(2,
    'Suguri',
        )

ORIGIN_FLYING_RED_BARREL = OJOrigin(3,
    'Flying Red Barrel',
        )

ORIGIN_100_ORANGE_JUICE = OJOrigin(4,
    '100% Orange Juice',
        )

ORIGIN_CHRISTMAS_SHOOTING = OJOrigin(5,
    'Christmas Shooting',
        )

ORIGIN_SORA = OJOrigin(6,
    'Sora',
        )

ORIGIN_QP_SHOOTING_DANGEROUS = OJOrigin(7,
    'QP Shooting - Dangerous!!',
        )

ORIGIN_QP_KISS = OJOrigin(8,
    'QP Kiss',
        )

ORIGIN_XMAS_SHOOTING_SCRAMBLE = OJOrigin(9,
    'Xmas Shooting - Scramble!!',
        )

ORIGIN_ACCELERATION_OF_SUGURI = OJOrigin(10,
    'Acceleration of Suguri',
        )

ORIGIN_ALICIANRONE = OJOrigin(11,
    'Alicianrone',
        )

ORIGIN_200_MIXED_JUICE = OJOrigin(12,
    '200% Mixed Juice!',
        )

ORIGIN_ACCELERATION_OF_SUGURI_2 = OJOrigin(13,
    'Acceleration of SUGURI 2',
        )

#### #### #### #### CARD PACKS #### #### #### ####

CARD_PACK_ACCELERATION_PACK = OJCardPack(1,
    'Acceleration Pack',
    320,
        )

CARD_PACK_EXPANSION_PACK = OJCardPack(2,
    'Expansion Pack',
    240,
        )

CARD_PACK_COMMUNITY_PACK = OJCardPack(3,
    'Community Pack',
    540,
        )

CARD_PACK_COMMUNITY_PACK_2 = OJCardPack(4,
    'Community Pack 2',
    1080,
        )

CARD_PACK_BASE_PACK = OJCardPack(5,
    'Base Pack',
    180,
        )

CARD_PACK_PUDDING_PACK = OJCardPack(6,
    'Pudding Pack',
    320,
        )

CARD_PACK_MIXED_BOOSTER_PACK = OJCardPack(7,
    'Mixed Booster Pack',
    280,
        )

#### #### #### #### CARD COSTS #### #### #### ####

CARD_COST_0 = OJCardCost(CARD_COST_TYPE_STATIC, 0)
CARD_COST_3 = OJCardCost(CARD_COST_TYPE_STATIC, 3)
CARD_COST_5 = OJCardCost(CARD_COST_TYPE_STATIC, 5)
CARD_COST_10 = OJCardCost(CARD_COST_TYPE_STATIC, 10)
CARD_COST_13 = OJCardCost(CARD_COST_TYPE_STATIC, 13)
CARD_COST_20 = OJCardCost(CARD_COST_TYPE_STATIC, 20)
CARD_COST_30 = OJCardCost(CARD_COST_TYPE_STATIC, 30)
CARD_COST_40 = OJCardCost(CARD_COST_TYPE_STATIC, 40)
CARD_COST_50 = OJCardCost(CARD_COST_TYPE_STATIC, 50)

CARD_COST_Stp10 = OJCardCost(CARD_COST_TYPE_DIV_STARS, 10)

CARD_COST_Lvx3 = OJCardCost(CARD_COST_TYPE_MUL_LEVEL, 3)
CARD_COST_Lvx5 = OJCardCost(CARD_COST_TYPE_MUL_LEVEL, 5)
CARD_COST_Lvx10 = OJCardCost(CARD_COST_TYPE_MUL_LEVEL, 10)

CARD_COST_HCx5 = OJCardCost(CARD_COST_TYPE_MUL_CARDS, 5)
CARD_COST_OCx5 = OJCardCost(CARD_COST_TYPE_MUL_OTHERS_CARDS, 5)

CARD_COST_StALL = OJCardCost(CARD_COST_TYPE_ALL_STARS, 0)

#### #### #### #### EVENTS #### #### #### ####

EVENT_CHOCOLATE_FOR_THE_SWEET_GODS = None
EVENT_RETURN = None
EVENT_SANTA_SCRAMBLE = None
EVENT_SHROOM_ZOOM = None
EVENT_BEACH_PARTY = None

#### #### #### #### NORMAL CARDS #### #### #### ####

CARD_ACCEL_HYPER = OJCard(1,
    'Accel Hyper',
    4, CARD_COST_30, 1, CARD_TYPE_BATTLE, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_RARE,
    'Roll double dice for attack.',
    '"Unlimited Charge!" —Sora',
    None,
    'Accel_Hyper.png',
        )

CARD_BIG_MAGNUM = OJCard(2,
    'Big Magnum',
    3, CARD_COST_20, 3, CARD_TYPE_BATTLE, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Pay 1 HP when you use this card. During this battle, gain 2 ATK. If you would suffer KO from using this card, '
    'the card cannot be used.',
    '"Go! Big Magnum!" —Captain Tequila',
    None,
    'Big_Magnum.png',
        )

CARD_DARK_SIDE_OF_BUSINESS = OJCard(3,
    'Dark Side of Business',
    2, CARD_COST_10, 3, CARD_TYPE_BATTLE, CARD_PACK_COMMUNITY_PACK, CARD_RARITY_UNCOMMON,
    'Gain +2 ATK, enemy gains -2 DEF. For every point of damage you would deal, steal 5 stars from your opponent '
    'instead.',
    '"Go! Big Magnum!" —Captain Tequila',
    None,
    'Dark_Side_of_Business.png',
        )

CARD_DESPERATE_MODIFICATION = OJCard(4,
    'Desperate Modification',
    2, CARD_COST_10, 3, CARD_TYPE_BATTLE, CARD_PACK_COMMUNITY_PACK_2, CARD_RARITY_COMMON,
    'For this battle, randomly roll either a natural 1 or 6 for each attack, defense and evasion.',
    '"Poor Blue Crow. You loaded him with all that heavy stuff!" —Marc',
    None,
    'Desperate_Modification.png',
        )

CARD_EXTENSION = OJCard(5,
    'Extension',
    4, CARD_COST_10, 3, CARD_TYPE_BATTLE, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_UNCOMMON,
    'Play one randomly chosen Battle card (including Hyper cards) for no additional cost.',
    '"It\'s my job to kill you." —Nath',
    None,
    'Extension.png',
        )

CARD_FINAL_BATTLE = OJCard(6,
    'Final Battle',
    4, CARD_COST_30, 1, CARD_TYPE_BATTLE, CARD_PACK_BASE_PACK, CARD_RARITY_RARE,
    'This battle will last until either unit suffers KO (Maximum of 10 rounds).',
    '"To protect everyone!" —Suguri & Hime',
    None,
    'Final_Battle.png',
        )

CARD_IM_ON_FIRE = OJCard(7,
    'I\'m on Fire!',
    1, CARD_COST_5, 3, CARD_TYPE_BATTLE, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'During this battle, gain +1 ATK and -1 DEF.',
    '"Let\'s play our lives away!" —Kae',
    None,
    'I\'m_on_Fire!.png',
        )

CARD_PORTABLE_PUDDING = OJCard(8,
    'Portable Pudding',
    2, CARD_COST_20, 1, CARD_TYPE_BATTLE, CARD_PACK_PUDDING_PACK, CARD_RARITY_UNCOMMON,
    'At the start of this battle, reset your HP to your max HP.',
    '"I\'ve got pudding for lunch today!" ―QP',
    None,
    'Portable_Pudding.png',
        )

CARD_QUICK_RESTORATION = OJCard(9,
    'Quick Restoration',
    2, CARD_COST_10, 3, CARD_TYPE_BATTLE, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_COMMON,
    'All damage taken during the battle will be healed after the battle. Effect is cancelled if the player is KO\'d',
    '"I\'m not going to die." —Suguri',
    None,
    'Quick_Restoration.png',
        )

CARD_RAINBOW_COLORED_CIRCLE = OJCard(10,
    2, CARD_COST_5, 3, CARD_TYPE_BATTLE, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'Rainbow-Colored Circle',
    'During this battle, gain +2 EVD and -1 DEF.',
    '"Like drawing a rainbow-colored circle."',
    None,
    'Rainbow-Colored_Circle.png',
        )

CARD_RBITS = OJCard(11,
    'Rbits',
    2, CARD_COST_3, 3, CARD_TYPE_BATTLE, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'During this battle, gain +2 DEF. You may not use the Evade command.',
    '"Formation Orbit!" —QP',
    None,
    'Rbits.png',
        )

CARD_REVERSE_ATTRIBUTE_FIELDS = OJCard(12,
    'Reverse Attribute Field',
    3, CARD_COST_10, 1, CARD_TYPE_BATTLE, CARD_PACK_EXPANSION_PACK, CARD_RARITY_RARE,
    'During this battle, the positive and negative values of each ability of both units are inverted after adjustment.',
    '"Aren\'t you too serious about this game? You\'re so da... I mean, far too immature!" —Mei',
    None,
    'Reverse_Attribute_Field.png',
        )

CARD_SERIOUS_BATTLE = OJCard(13,
    'Serious Battle',
    3, CARD_COST_0, 3, CARD_TYPE_BATTLE, CARD_PACK_PUDDING_PACK, CARD_RARITY_COMMON,
    'During this battle, ATK, DEF and EVD of both units will be 0.',
    '"This battle will be a true test of strength!" ―Tomomo',
    None,
    'Serious_Battle.png',
        )

CARD_SHIELD = OJCard(14,
    'Shield',
    3, CARD_COST_5, 3, CARD_TYPE_BATTLE, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Gain +3 DEF during this battle. However, you may not attack. This card can only be used by the player who attacks '
    'second.',
    '"The most important thing is: make it back here alive." —Sham',
    None,
        )

CARD_SHIELD_COUNTER = OJCard(15,
    'Shield Counter',
    4, CARD_COST_20, 1, CARD_TYPE_BATTLE, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_UNCOMMON,
    'Deal damage to attacker equal to their ATK - DEF (min. 1). You take no damage. No attacks take place. May only be '
    'played by the defender.',
    '"Shield, invert!" —Sora',
    None,
        )

CARD_SINK_OR_SWIM = OJCard(16,
    'Sink or Swim',
    4, CARD_COST_10, 3, CARD_TYPE_BATTLE, CARD_PACK_PUDDING_PACK, CARD_RARITY_RARE,
    'Gain -1 ATK, -1 DEF and -1 EVD. If you win this battle, take 50% more of your opponent\'s stars.',
    '"Alright, it\'s time to play the long odds!" ―Yuki',
    None,
        )

CARD_TACTICAL_RETREAT = OJCard(17,
    'Tactical Retreat',
    1, CARD_COST_Lvx5, 3, CARD_TYPE_BATTLE, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_COMMON,
    'End this battle. Attacker gains this card\'s cost. May only be used by the defender. If opponent plays a battle '
    'card, this effect is void.',
    '"Farewell!" —Tomato',
    None,
        )

CARD_AMBUSH = OJCard(18,
    'Ambush',
    3, CARD_COST_20, 3, CARD_TYPE_BOOST, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_COMMON,
    'Engage in battle with another player or players on your panel. Once these battles are over, your turn is over.',
    '"Owwwww!" —Sham',
    None,
        )

CARD_BACKDOOR_TRADE = OJCard(19,
    'Backdoor Trade',
    1, CARD_COST_Lvx5, 1, CARD_TYPE_BOOST, CARD_PACK_PUDDING_PACK, CARD_RARITY_UNCOMMON,
    'Perform a Norma check, then your turn ends. Can only be used by the player with the lowest level. Cannot be used '
    'at Norma level 5.',
    '"Here\'s what you asked for." ―Captain Tequila\n'
    '"Great work! I knew I could count on a real villain like you!" ―Mimyuu',
    None,
        )

CARD_COMPLETION_REWARD = OJCard(20,
    'Completion Reward',
    1, CARD_COST_0, 1, CARD_TYPE_BOOST, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_COMMON,
    'Gain 7 stars for every trap you have set and someone has stepped on.',
    '"Yay, I\'ve got my pay!" —Chris\n'
    '"Don\'t waste it, okay?" —Manager',
    None
        )

CARD_DASH = OJCard(21,
    'Dash!',
    1, CARD_COST_3, 3, CARD_TYPE_BOOST, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'For this turn, roll two dice for movement.',
    '"Faster!" —Suguri',
    None,
        )

CARD_EXTEND = OJCard(22,
    'Extend',
    3, CARD_COST_10, 1, CARD_TYPE_BOOST, CARD_PACK_EXPANSION_PACK, CARD_RARITY_RARE,
    'Stock Effect After suffering KO, you will revive on the following turn.',
    '"All good for now!" —Marc',
    None,
        )

CARD_FLIP_OUT = OJCard(23,
    'Flip Out',
    1, CARD_COST_0, 3, CARD_TYPE_BOOST, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'Stock Effect Next time you land on a drop panel, the player(s) with the highest number of stars will lose the '
    'same number of stars as you.',
    '"......!" —Mei',
    None,
        )

CARD_GENTLEMANS_BATTLE = OJCard(24,
    'Gentleman\'s Battle',
    3, CARD_COST_10, 3, CARD_TYPE_BOOST, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_COMMON,
    'Choose a player with full HP and battle them. Your turn ends after the battle.',
    '"Take this!" —Guildmaster',
    None,
        )

CARD_LONELY_CHARIOT = OJCard(25,
    'Lonely Chariot',
    3, CARD_COST_30, 3, CARD_TYPE_BOOST, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_COMMON,
    'Stock Effect Always roll 5 to move. After your turn, take 1 damage. Effect expires on KO. If you suffer KO from '
    'this effect, pay Lvl x5 stars.',
    '"You guys? You\'re mistaken...\n'
    'I ride alone!" —Lone Rider',
    None,
        )

CARD_LONG_DISTANCE_SHOT = OJCard(26,
    'Long-Distance Shot',
    1 , CARD_COST_5, 3, CARD_TYPE_BOOST, CARD_PACK_EXPANSION_PACK, CARD_RARITY_COMMON,
    'Deals 1 damage to the selected enemy unit.',
    '"I can hit you from anywhere." —Iru',
    None,
        )

CARD_MIMIC = OJCard(27,
    'Mimic',
    3, CARD_COST_5, 3, CARD_TYPE_BOOST, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_RARE,
    'Choose a player. All hyper cards in your hand become the type that that player uses.',
    'Marie Poppo is trying to become something else.',
    None,
        )

CARD_NICE_JINGLE = OJCard(28,
    'Nice Jingle',
    1, CARD_COST_0, 1, CARD_TYPE_BOOST, CARD_PACK_BASE_PACK, CARD_RARITY_UNCOMMON,
    'Stock Effect. The next bonus panel gives you twice as many stars.',
    '"We\'ve got a bunch." —Aru',
    None,
        )

CARD_NICE_PRESENT = OJCard(29,
    'Nice Present',
    2, CARD_COST_10, 1, CARD_TYPE_BOOST, CARD_PACK_BASE_PACK, CARD_RARITY_UNCOMMON,
    'Draw 2 cards.',
    '"You\'re going to help me deliver the presents." —Aru',
    None,
        )

CARD_PASSIONATE_RESEARCH = OJCard(30,
    'Passionate Research',
    2, CARD_COST_5, 1, CARD_TYPE_BOOST, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_UNCOMMON,
    'Look at the first 3 cards of the deck. If there are any hyper cards, take them. Return the rest of the cards to '
    'the deck in the same order.',
    '"Well, this sort of thing happens all the time. It was quite fun, anyway!" —Scholar',
    None,
        )

CARD_PATH_BLOCKERS = OJCard(31,
    'Path Blockers',
    1, CARD_COST_13, 3, CARD_TYPE_BOOST, CARD_PACK_COMMUNITY_PACK_2, CARD_RARITY_COMMON,
    'Stock Effect (1). Choose a unit. If that unit moves onto a panel with a set Trap, they must stop on that panel.',
    '"Nobody will get past Waruda!" —Tomato',
    None,
        )

CARD_PRESIDENTS_PRIVILEGE = OJCard(32,
    'President\'s Privilege',
    4, CARD_COST_10, 3, CARD_TYPE_BOOST, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_COMMON,
    'Effect Duration: 1 chapter You may play cards without paying their cost. You may play 1 additional card this '
    'turn.',
    '"There you guys are... Come to the Student Council Office after school, will you?" —Himeji',
    None,
        )

CARD_PRINCESSS_PRIVILEGE = OJCard(33,
    'Princess\'s Privilege',
    4, CARD_COST_20, 1, CARD_TYPE_BOOST, CARD_PACK_EXPANSION_PACK, CARD_RARITY_RARE,
    'Discard all cards in your hand. Draw 3 new cards. Can only be used when you have at least 3 cards in your hand.',
    '"You may come and visit my house some day." —Fernet',
    None,
        )

CARD_PUDDING = OJCard(34,
    'Pudding',
    4, CARD_COST_0, 3, CARD_TYPE_BOOST, CARD_PACK_BASE_PACK, CARD_RARITY_RARE,
    'Fully restore HP.',
    '"Hooray!" —QP',
    None,
        )

CARD_SAKIS_COOKIE = OJCard(35,
    'Saki\'s Cookie',
    1, CARD_COST_0, 3, CARD_TYPE_BOOST, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'Heals 1 HP.',
    '"Have a cookie!" —Saki',
    None,
        )

CARD_STIFF_CRYSTAL = OJCard(36,
    'Stiff Crystal',
    2, CARD_COST_20, 1, CARD_TYPE_BOOST, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Stock Effect This card negates the effect of a trap card. Gain 5 stars per level of cancelled trap.',
    '"Such a pain in the neck." —Kyoko',
    None,
        )

CARD_SWEET_DESTROYER = OJCard(37,
    'Sweet Destroyer',
    3, CARD_COST_20, 1, CARD_TYPE_BOOST, CARD_PACK_PUDDING_PACK, CARD_RARITY_RARE,
    'Steal a random "pudding" card from each other player. You can play another card this turn. At the end of your '
    'turn, discard as many cards as you gained.',
    '"The sweets that bring harm to the world... I will destroy them all!" ―Sweet Breaker',
    None,
        )

CARD_TREASURE_THIEF = OJCard(38,
    'Treasure Thief',
    2, CARD_COST_10, 3, CARD_TYPE_BOOST, CARD_PACK_COMMUNITY_PACK, CARD_RARITY_COMMON,
    'Steal a random card from all players on the same tile as you.',
    '"Pokya Po! (Treasure, get!)" ―Marie Poppo',
    None,
        )

CARD_ACCELERATING_SKY = OJCard(39,
    'Accelerating Sky',
    3, CARD_COST_30, 3, CARD_TYPE_EVENT, CARD_PACK_COMMUNITY_PACK_2, CARD_RARITY_UNCOMMON,
    'Effect Duration: 3 chapters. All players gain +1 EVD and -1 DEF.',
    '"Girls are leaping through the sky...?"',
    None,
        )

CARD_CLOUD_OF_SEAGULL = OJCard(40,
    ' Cloud of Seagulls',
    1, CARD_COST_0, 3, CARD_TYPE_EVENT, CARD_PACK_EXPANSION_PACK, CARD_RARITY_COMMON,
    'A randomly chosen unit will receive 2 damage.',
    '"Squaawk!" —Seagull',
    None,
        )

CARD_DINNER = OJCard(41,
    'Dinner',
    3, CARD_COST_10, 3, CARD_TYPE_EVENT, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Heals all units for 3 HP.',
    '"Let\'s have supper together." —Natsumi',
    None,
        )

CARD_FORCED_REVIVAL = OJCard(42,
    'Forced Revival',
    3, CARD_COST_30, 3, CARD_TYPE_EVENT, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'All units suffering KO are revived with 1 HP.',
    '"You\'ll all be up in a jiffy." —Kiriko',
    None,
        )

CARD_GIFT_EXCHANGE = OJCard(43,
    'Gift Exchange',
    3, CARD_COST_10, 3, CARD_TYPE_EVENT, CARD_PACK_BASE_PACK, CARD_RARITY_UNCOMMON,
    'All cards are gathered from the players and dealt back randomly. The total number of each player\'s card remains '
    'unchanged.',
    '"A gift exchange? Let\'s do it!" —Rbit, Red, and Blue',
    None,
        )

CARD_HERE_AND_THERE = OJCard(44,
    'Here and There',
    2, CARD_COST_10, 3, CARD_TYPE_EVENT, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'All players are moved to randomly chosen panels.',
    '"To the next world!" —Marie Poppo',
    None,
        )

CARD_HOLY_NIGHT = OJCard(45,
    'Holy Night',
    1, CARD_COST_0, 1, CARD_TYPE_EVENT, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'Permanent Effect. Start-of-chapter bonus stars are increased by one.',
    '"Aha, that\'s why it\'s a party night." —Hime',
    None,
        )

CARD_INDISCRIMINATE_FIRE_SUPPORT = OJCard(46,
    'Indiscriminate Fire Support',
    2, CARD_COST_10, 3, CARD_TYPE_EVENT, CARD_PACK_PUDDING_PACK, CARD_RARITY_RARE,
    'Effect Duration: Infinite. A random unit takes 1 damage. At the start of your turn, repeat this effect. The '
    'effect ends when a unit suffers KO.',
    '"......" ―Sora',
    None,
        )

CARD_LITTLE_WAR = OJCard(47,
    'Little War',
    4, CARD_COST_50, 1, CARD_TYPE_EVENT, CARD_PACK_BASE_PACK, CARD_RARITY_RARE,
    'Effect Duration: 3 chapters Offense and defense will happen twice in all battles.',
    '"I believe... I have the power to stop this..." —Suguri',
    None,
        )

CARD_MIX_PHENOMENON = OJCard(48,
    'Mix Phenomenon',
    2, CARD_COST_10, 1, CARD_TYPE_EVENT, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_RARE,
    'Effect Duration: 3 chapters All panels other than the home panels become random panels.',
    '"A hole in a wall-like force between dimensions...It would appear that this phenomenon is mixing the worlds '
    'themselves together." —Yukito',
    None,
        )

CARD_OH_MY_FRIEND = OJCard(49,
    'Oh My Friend',
    1, CARD_COST_30, 1, CARD_TYPE_EVENT, CARD_PACK_EXPANSION_PACK, CARD_RARITY_RARE,
    'A boss will show up.',
    '"Machines have friends too." —NoName',
    None,
        )

CARD_OUT_OF_AMMO = OJCard(50,
    'Out of Ammo',
    2, CARD_COST_5, 3, CARD_TYPE_EVENT, CARD_PACK_BASE_PACK, CARD_RARITY_UNCOMMON,
    'Effect Duration: 1 chapter No player may use any cards.',
    '"Ran out of ammo!" —Peat',
    None,
        )

CARD_PARTY_TIME = OJCard(51,
    'Party Time',
    3, CARD_COST_20, 3, CARD_TYPE_EVENT, CARD_PACK_COMMUNITY_PACK, CARD_RARITY_COMMON,
    'All units are randomly warped onto the same panel. End your turn.',
    '"At tonight\'s banquet, the Beasts of Darkness shall dance wildly." ―Krilalaris',
    None,
        )

CARD_PLAY_OF_GODS = OJCard(52,
    'Play of the Gods',
    1, CARD_COST_10, 1, CARD_TYPE_EVENT, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_RARE,
    'Play one random event card (including Hyper cards) from any player\'s hand or the deck, at no additional cost',
    '"We will get golden eggs!" —QP\n'
    '"And make the best pudding out of them!" —Saki',
    None,
        )

CARD_SCARY_SOLICITATION = OJCard(53,
    'Scary Solicitation',
    3, CARD_COST_30, 1, CARD_TYPE_EVENT, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_UNCOMMON,
    'All players except the one who played this card must draw cards, paying 15 stars per card, up to their card '
    'maximum.',
    '"You\'ll buy it, of course. You\'ll buy it, won\'t you?" —Merchant',
    None,
        )

CARD_SCRAMBLE_EVE = OJCard(54,
    'Scrambled Eve',
    3, CARD_COST_5, 1, CARD_TYPE_EVENT, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_UNCOMMON,
    'All players return their hand to the deck, and the deck is shuffled. Players gain 5 stars for each returned card.',
    '"Wait! Give me back the presents!" —Aru',
    None,
        )

CARD_SEALED_GUARDIAN = OJCard(55,
    'Sealed Guardian',
    5, CARD_COST_50, 1, CARD_TYPE_EVENT, CARD_PACK_EXPANSION_PACK, CARD_RARITY_RARE,
    'Every unit\'s HP becomes 1.',
    '"Meet the guardian angel of this vessel." —Shifu',
    None,
        )

CARD_SERENE_HUSH = OJCard(56,
    'Serene Hush',
    2, CARD_COST_10, 1, CARD_TYPE_EVENT, CARD_PACK_PUDDING_PACK, CARD_RARITY_COMMON,
    'Effect Duration: 1 Chapter. No battles can take place.',
    '"We have nothing to do..." ―Sumika\n'
    '"Let\'s enjoy the peace and quiet." ―Suguri',
    None,
        )

CARD_STAR_BLASTING_LIGHT = OJCard(57,
    'Star-Blasting Light',
    4, CARD_COST_50, 1, CARD_TYPE_EVENT, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_RARE,
    'All trap cards on the field are discarded. Trap setters take 1 damage for each discarded trap.',
    '"A light capable of burning down the city... even the planet... I can tell its source is up there in the sky." '
    '—Sora',
    None,
        )

CARD_SUPER_ALL_OUT_MODE = OJCard(58,
    'Super All-Out Mode',
    3, CARD_COST_30, 3, CARD_TYPE_EVENT, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Stock Effect All units gain +2 ATK during their next battle.',
    '"This is gonna hurt even if you know it\'s coming!!" —Tomomo',
    None,
        )

CARD_UNPAID_WORK = OJCard(59,
    'Unpaid Work',
    2, CARD_COST_0, 1, CARD_TYPE_EVENT, CARD_PACK_PUDDING_PACK, CARD_RARITY_COMMON,
    'Effect Duration: 1 Chapter. No units will gain stars from any sources.',
    '"Where\'s my payment!" ―Chris',
    None,
        )

CARD_WE_ARE_WARUDA = OJCard(60,
    'We Are Waruda',
    2, CARD_COST_5, 3, CARD_TYPE_EVENT, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Move all trap cards onto randomly chosen panels.',
    '"Useless. No one can beat Tomato." —Tomato',
    None,
        )

CARD_BLOODLUST = OJCard(61,
    'Bloodlust',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, CARD_PACK_COMMUNITY_PACK_2, CARD_RARITY_RARE,
    'Lose 1 HP at the start of your turn. Heal 1 HP for every damage you deal. Cannot Norma while holding this card. '
    'This card is discarded upon KO or use.',
    '"The true power of my beast... I wonder if it\'s like this." —Krila',
    None,
        )

CARD_LOST_CHILD = OJCard(62,
    'Lost Child',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, CARD_PACK_COMMUNITY_PACK, CARD_RARITY_COMMON,
    'Move backwards while this card is held. Cannot Norma while holding this card. This card is discarded upon KO or '
    'use.',
    '"Where am I?" ―Tsih',
    None,
        )

CARD_LUCKY_CHARM = OJCard(63,
    'Lucky Charm',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, CARD_PACK_PUDDING_PACK, CARD_RARITY_UNCOMMON,
    'Gain Lvl x1 stars at the start of your turn. You cannot use any other cards. This card is discarded upon use. On '
    'defeat, give Lvl x 3 more stars.',
    '"Woo-hoo, so many stars! Today\'s my day!!" ―Tomomo',
    None,
        )

CARD_METALLIC_MONOCOQUE = OJCard(64,
    'Metallic Monocoque',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, CARD_PACK_PUDDING_PACK, CARD_RARITY_COMMON,
    'When a non-battle effect deals any damage to you, that damage is reduced by 1, and you lose Lvl x 2 stars.',
    '"What a timid generation we live in." ―Sherry',
    None,
        )

CARD_POPPO_THE_SNATCHER = OJCard(65,
    'Poppo the Snatcher',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, CARD_PACK_COMMUNITY_PACK_2, CARD_RARITY_UNCOMMON,
    'Gain -1 DEF. Whenever passing another unit on your turn, steal target Lvl x3 stars from them. Cannot Norma while '
    'holding this card. This card is discarded upon KO or use.',
    '"Pokyakya!!" —Poppo',
    None,
        )

CARD_PRICE_OF_POWER = OJCard(66,
    'Price of Power',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, CARD_PACK_COMMUNITY_PACK, CARD_RARITY_RARE,
    'You may play cards one level higher than your current level. All card costs are increased by 5. This card is '
    'discarded on use.',
    '"Even if I survive the war... With this body, there\'s nothing I can do." ―Nath',
    None,
        )

CARD_UNLUCKY_CHARM = OJCard(67,
    'Unlucky Charm',
    1, CARD_COST_Lvx5, 1, CARD_TYPE_GIFT, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_UNCOMMON,
    'Lose Lvl x 1 stars at the start of your turn. Using this card sends it to another player. If Cost is higher than '
    'your star count, you may use this card for free.',
    '"Pitch black darkness disrupts my slumber, hence I yearn for light..." —Krilalaris',
    None,
        )

CARD_WINDY_ENCHANTMENT = OJCard(68,
    'Windy Enchantment',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_RARE,
    'Gain +1 MOV. Cannot Norma while holding this card. Discard upon use.',
    'People call her Barefoot Alicianrone.',
    None,
        )

CARD_ASSAULT = OJCard(69,
    'Assault',
    2, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_BASE_PACK, CARD_RARITY_UNCOMMON,
    'Battle the player who set this card, starting with their attack.',
    '"I\'ll make you leave the guild today for sure!" —Peat',
    None,
        )

CARD_BAD_PUDDING = OJCard(70,
    'Bad Pudding',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'Discard a random card.',
    '"Pudding with soy sauce, tastes like sea urchin!" —Yuki',
    None,
        )

CARD_BRUTAL_PRANK = OJCard(71,
    3, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_COMMON,
    'Brutal Prank',
    'Discard all Hyper cards in hand. Lose 10 stars and heal 1 HP for each discarded card.',
    '"Noooo, Mr. Cow! Mr. Frog!" —Yuuki\n'
    '"Hahahaha! Wail and weep!!" —Yuki',
    None,
        )

CARD_DANGEROUS_PUDDING = OJCard(72,
    'Dangerous Pudding',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'Stock Effect Your next turn will be skipped.',
    '"One glance is all it took for that pudding to steal my heart."',
    None,
        )

CARD_ENCORE = OJCard(73,
    'Encore',
    3, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_PUDDING_PACK, CARD_RARITY_UNCOMMON,
    'When this card is activated either on Bonus, Drop, Draw or Encounter, that panel\'s effect takes place twice.',
    '"Encore! Encore!"',
    None,
        )

CARD_EXCHANGE = OJCard(74,
    'Exchange',
    2, CARD_COST_0, 1, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Exchange the cards in your hand, your stars and your current panel position with the player who has set this '
    'card.',
    '"Heavy..." —Suguri\n'
    '"So drafty without my cap..." —Marc',
    None,
        )

CARD_FLAMETHROWER = OJCard(75,
    'Flamethrower',
     3, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'KO\'s a player. If the player has any cards in their hand, they will lose all of them instead of suffering KO.',
    '"Heeehaaaaah!" —Punk',
    None,
        )

CARD_FOR_THE_FUTURE_OF_THE_TOY_STORE = OJCard(76,
    ' For the Future of the Toy Store',
    2, CARD_COST_0, 1, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_RARE,
    'Lose half your stars. The player who set this card will gain the lost stars. This card can only be used with '
    'less than 50 stars.',
    '"If only! If only there was no Santa!!" —Arthur',
    None,
        )

CARD_GO_AWAY = OJCard(77,
    'Go Away',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_COMMON,
    'You are moved to a randomly chosen panel.',
    '"Ahaha, I like this." —Nanako',
    None,
        )

CARD_HEAT_300 = OJCard(78,
    'Heat 300%',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_COMMON,
    'Effect Duration: 3 chapters In battle, gain -2 DEF.',
    '"All I need to do is dodge every attack!" —Suguri',
    None,
        )

CARD_INVASION = OJCard(79,
    'Invasion',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_COMMON,
    'You will have an encounter. The enemy will attack first.',
    '"What, I was attacked...?" —Suguri',
    None,
        )

CARD_I_WANNA_SEE_YOU = OJCard(80,
    'I Wanna See You',
    2, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_PUDDING_PACK, CARD_RARITY_COMMON,
    'The player who set this trap moves to the panel on which the trap was activated. The player who activated the '
    'trap then gains this card instead of it being discarded.',
    '"Kyupita... I want to see you." ―Kyousuke',
    None,
        )

CARD_MIMYUUS_HAMMER = OJCard(81,
    'Mimyuu\'s Hammer',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'Deals 1 damage.',
    '"Thank you for dying!" —Mimyuu',
    None,
        )

CARD_PIGGY_BANK = OJCard(82,
    'Piggy Bank',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_COMMON,
    'Gain stars equal to five times the number of chapters passed since this card was set.',
    '"Dad, can\'t I break the piggy yet?" —Mescal',
    None,
        )

CARD_PIYOPIYO_PROCESSION = OJCard(83,
    'Piyopiyo Procession',
    2, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_RARE,
    'Player suffers 3 random encounters (the player attacks first).',
    '"Piyopiyopiyopiyopiyopiyopiyopiyopiyooo!" —Colored Piyo Army',
    None,
        )

CARD_POPPOFORMATION = OJCard(84,
    'Poppoformation',
    2, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_COMMUNITY_PACK_2, CARD_RARITY_COMMON,
    'Stock Effect (1). ATK, DEF, and EVD become -1 in your next battle.',
    '"Poppo! Poppopopo!!!" —Everyone',
    None,
        )

CARD_PRESENT_THIEF = OJCard(85,
    'Present Thief',
    3, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_UNCOMMON,
    'Steals all the cards from the first player to step on the trap. Gives all the stolen cards to the second player '
    'to step on the trap.',
    '"These do no good!" —Niko',
    None,
        )

CARD_SEALED_MEMORIES = OJCard(86,
    'Sealed Memories',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_UNCOMMON,
    'For 3 turns, target sees all cards face down, and other players can see their cards.',
    '"Order within the world...? What the heck does pudding have to do with that!?" —QP',
    None,
        )

CARD_SKY_RESTAURANT_PURES = OJCard(87,
    ' Sky Restaurant \'Pures\'',
    4, CARD_COST_0, 1, CARD_TYPE_TRAP, CARD_PACK_BASE_PACK, CARD_RARITY_RARE,
    'Lose half your stars and fully restore HP.',
    '"We have a guest to treat!" —Chris',
    None,
        )

CARD_TRAGEDY_IN_THE_DEAD_OF_NIGHT = OJCard(88,
    'Tragedy in the Dead of Night',
    3, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Discard a random card. That card will go to the player who has set this card.',
    '"Such happiness will be snatched away just like that."',
    None,
        )

CARD_WANTED = OJCard(89,
    'Wanted',
    3, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_COMMUNITY_PACK, CARD_RARITY_UNCOMMON,
    'Stock Effect You give double wins on KO from battle. Effect expires on KO.',
    '"Over here! My nose is never wrong!" ―QP',
    None,
        )

#### #### #### #### HYPER #### #### #### ####

CARD_ANOTHER_ULTIMATE_WEAPON = OJCard(90,
    'Another Ultimate Weapon',
    3, CARD_COST_StALL, -1, CARD_TYPE_HYPER|CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'Gain +1 ATK and DEF and an additional +1 ATK and DEF for every 20 stars spent on this card.',
    '"With you gone, I am their ultimate weapon now." - Nath',
    None,
        )

CARD_BEYOND_HELL = OJCard(91,
    'Beyond Hell',
    1, CARD_COST_0, -1, CARD_TYPE_HYPER|CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'During this battle, gain +1 to ATK, DEF and EVD for every HP you are missing.',
    '"Syura\'s powers go beyond Hell itself! Allow me to demonstrate!" ―Syura',
    None,
        )

CARD_BLUE_CROW_THE_SECOND = OJCard(92,
    'Blue Crow the Second',
    2, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'During this battle, gain ATK and DEF but lose EVD equal to the number of cards in your hand.',
    '"I\'m gonna settle this!" - Peat',
    None,
        )

CARD_DEPLOY_BITS = OJCard(93,
    'Deploy Bits',
    2, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'During this battle, gain a total of +7 points to ATK, DEF, and/or EVD, distributed randomly.',
    '"No matter what, you can\'t escape my Bits." - Nanako',
    None,
        )

CARD_HYPER_MODE = OJCard(94,
    'Hyper Mode',
    1, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'Gain +2 ATK during this battle. If your unit suffers KO during this battle, you give no stars or Wins and the '
    'unit will revive next turn.',
    '"HYPER MODE!" - QP',
    None,
        )

CARD_INTELLIGENCE_OFFICER = OJCard(95,
    'Intelligence Officer',
    2, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'Gain one of the following effects depending on the top-of-the-deck card: '
    'Event +3 ATK\n'
    'Boost +3 DEF\n'
    'Others +3 EVD',
    '"I can see through everything!" - Arnelle',
    None,
        )

CARD_REFLECTIVE_SHELL = OJCard(96,
    'Reflective Shell',
    1, CARD_COST_5, -1, CARD_TYPE_HYPER|CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'Base ATK is 0 in this battle. Absorb up to 2 damage. Gain an additional +2 ATK for every damage absorbed.\n'
    'Can only be used when defending.',
    '"Enemy detected. Destroying." ―Robo Ball',
    None,
        )

CARD_SELF_DESTRUCT = OJCard(97,
    'Self-Destruct',
    3, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'On KO, also KO the opponent. Enemy gains no stars or wins, and loses half their stars.',
    '"I\'m sorry...I can\'t make it back..." - Alte',
    None,
        )

CARD_WARUDA_MACHINE_BLAST_OFF = OJCard(98,
    'Waruda Machine, Blast Off!',
    3, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'During this battle, gain ATK and DEF but lose EVD equal to the number of cards in your opponent\'s hand.',
    '"Revenge!" -Tomato',
    None,
        )

CARD_ACCELERATOR = OJCard(99,
    'Accelerator',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Effect Duration: 1 chapter Roll two dice for movement, battle, bonus and drop.',
    '"I\'m accelerating." ―Suguri',
    None,
        )

CARD_ANGEL_HAND = OJCard(100,
    'Angel Hand',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Heal target player to full HP and gain 10 stars per healed HP. In even-numbered chapters, this card turns into '
    'Devil Hand.',
    '"This is the power of mercy." ―Yuuki',
    None,
        )

CARD_AWAKENING_OF_TALENT = OJCard(101,
    'Awakening of Talent',
    2, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST|CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'Until end of turn, roll 5 for move, battle, bonus or drop. This card can also be used as a Battle Card.',
    '"I\'ll commence... my operation now." -Sora',
    None,
        )

CARD_BIG_ROCKET_CANNON = OJCard(102,
    'Big Rocket Cannon',
    2, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Deal 3 damage to target enemy. If KO\'d, you gain wins as though KO\'d in battle. This card becomes '
    '"Rocket Cannon" when you use another card or you suffer KO.',
    '"Go!" ―Marc',
    None,
        )

CARD_BLAZING = OJCard(103,
    'Blazing!',
    3, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Inflicts Blazing! on units within 2 panels, and refreshes the duration of existing Blazing! Effect Duration: 3 '
    'Chapters. ATK +1, DEF -1. Effect expires on KO.',
    '"Good! Good! This feeling really is the best!" ―Kae',
    None,
        )

CARD_BRANCH_EXPANSION_STRATEGY = OJCard(104,
    'Branch Expansion Strategy',
    3, CARD_COST_HCx5, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Turn all your cards, including this one, into "Rbit Hobby Shop." You may play one more card in this turn.',
    '"Phaaw..." ―Arthur',
    None,
        )

CARD_CAST_OFF = OJCard(105,
    'Cast Off',
    2, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Stock Effect Swap unit\'s base ATK and DEF. Lasts until KO, or Cast Off is used again.',
    '"This calls for a good distraction..." ―Kyousuke',
    None,
        )

CARD_CHEF_I_COULD_USE_SOME_HELP = OJCard(106,
    'Chef, I Could Use Some Help!',
    2, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Summon Chef. Fights battles on behalf of your unit. Gives 2 Wins on KO. Gives stars gained in battle to your '
    'unit. Effect ends with Chef\'s KO. This card turns to "Manager, I Could Use Some Help!" if you have 4 or more '
    'Store Manager Counters and your Lvl is 4 or higher.',
    '"Chef! I\'m going to need your help!" ―Chris',
    None,
        )

CARD_CRYSTAL_BARRIER = OJCard(107,
    'Crystal Barrier',
    1, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Stock Effect (3) Cancel a trap, a battle, or drop panel. Take 1 damage. Consumes 1 stack. Effect expires on KO.',
    '"What a piece of junk, huh..." - Kyoko',
    None,
        )

CARD_ELLIES_MIRACLE = OJCard(108,
    'Ellie\'s Miracle',
    2, CARD_COST_Lvx10, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Cost: Level x10 stars. Effect Duration: 2 chapters. Gain +X ATK, +Y DEF, and +Z EVD, where X = Your total Norma '
    'completed, Y = your number of Wins Norma completed, and Z = your number of Stars Norma completed.',
    '"Receive my miracle!" - Ellie',
    None,
        )

CARD_EXTENDED_PHOTON_RIFLE = OJCard(109,
    'Extended Photon Rifle',
    1, CARD_COST_Lvx5, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Deal 1 damage to another random unit. If KO\'d, gain 1 win. Repeat as many times as your current level.',
    '"I\'ll shoot you all down." ―Iru',
    None,
        )

CARD_EXTRAORDINARY_SPECS = OJCard(110,
    'Extraordinary Specs',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Effect Duration: 1 chapter Roll 6 for movement, battle, bonus and drop.',
    '"I\'d appreciate it if you dropped your weapons." -Sora',
    None
        )

CARD_FULL_SPEED_ALICIANRONE = OJCard(111,
    'Full Speed Alicianrone',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Roll a die and move result x 3 panels. Deal damage equal to the result to each unit you pass during the move. If '
    'they are KO\'d by the damage, gain Wins as though from a normal battle. After this effect, your turn ends.',
    '"I\'ll go fast and cut my way through!" - Alicianrone',
    None,
        )

CARD_IMMOVABLE_OBJECT = OJCard(112,
    'Immovable Object',
    3, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Effect Duration: 2 Chapters Cannot move. Gain +2 DEF. Can counterattack. Enemies who move into the same panel '
    'must battle you.',
    '"With this power, everything in the sky will be ours." -Guild Master',
    None,
        )

CARD_JONATHAN_RUSH = OJCard(113,
    'Jonathan Rush',
    3, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Move to an enemy and attack them. Target gains -1 DEF. After the battle, your turn ends.',
    '"Squaawk!" ―Seagull',
    None,
        )

CARD_LEAP_THROUGH_SPACE = OJCard(114,
    'Leap Through Space',
    2, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Warp to the marked panel and unmark it. Apply Binding Smoke to enemies within 1 panel radius. If no marked panels '
    'exist, this card becomes "Leap through Space (Marking)."',
    '"Poof." ―Mira',
    None,
        )

CARD_LEAP_THROUGH_SPACE_MARKING = OJCard(115,
    'Leap Through Space (Marking)',
    1, CARD_COST_0, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Mark the panel where your unit is. When a marked panel exists, this card becomes "Leap through Space." This card '
    'is not discarded upon use.',
    '"Poof." ―Mira',
    None,
        )

CARD_LULUS_LUCKY_EGG = OJCard(116,
    'Lulu\'s Lucky Egg',
    2, CARD_COST_40, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Can only be played with 2 HP or less. Gain one of the following effects at random: - Roll a die and gain the die '
    'number x 20 stars. - Draw 5 cards. - Heal to full HP and permanently gain +1 ATK, +1 DEF, and +1 EVD. This effect '
    'can only trigger once.',
    '"Ugh... Lulu\'s about to lay an egg..." - Lulu',
    None,
        )

CARD_MANAGER_I_COULD_USE_SOME_HELP = OJCard(117,
    'Manager, I Could Use Some Help!',
    4, CARD_COST_40, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Summon Store Manager. Fights battles on behalf of your unit. Gives 2 Wins on KO. Gives stars gained in battle to '
    'your unit. Effect ends with Store Manager\'s KO, and your Store Manager Counters reset to 0. This card turns to '
    '"Chef, I Could Use Some Help!" if you have less than 4 Store Manager Counters.',
    '"Manager, help me!" ―Chris',
    None,
        )

CARD_MIRACLE_WALKER = OJCard(118,
    'Miracle Walker',
    3, CARD_COST_HCx5, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Turn all your cards, including this one, into random Hyper cards. You may play one more card this turn.',
    '"Hooray! Nico will try her best!" ―Nico',
    None,
        )

CARD_OBSERVER_OF_ETERNITY = OJCard(119,
    'Observer of Eternity',
    3, CARD_COST_0, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Add 2 random Boost/Event cards that deal damage to your hand.',
    '"Now then, let\'s see how this will turn out." - Suguri',
    None,
        )

CARD_PROTAGONISTS_PRIVILEGE = OJCard(120,
    'Protagonist\'s Privilege',
    3, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Effect Duration: 3 chapters When you are allowed to attack first, the opposing unit cannot attack (once per '
    'combat).',
    '"This is the privilege of the main character!" - Kai',
    None,
        )

CARD_RAGING_MADNESS = OJCard(121,
    'Raging Madness',
    2, CARD_COST_30, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Gain +1 Rage Counter. Target another active unit and enter Raging Mode: gain +X ATK and +X EVD where X is the '
    'number of your Rage Counters. Raging Mode ends and Rage Counters become 0 upon target\'s KO. Gain +2 Wins if you '
    'KO target in battle, and -50% Stars and Wins if you KO any other unit.',
    '"Gyaoooh!" - Maynie',
    None,
        )

CARD_REPRODUCTION_OF_RECORDS = OJCard(122,
    'Reproduction of Records',
    2, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Add a copy of the two most recent cards in the discard pile that aren\'t "Reproduction of Records" to your hand. '
    'Those cards will be treated as being Level 1 and having no base cost while in your hand.',
    '"Sumika\'s sweet memory!" - Sumika',
    None,
        )

CARD_RIVAL = OJCard(123,
    'Rival',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Challenge target player. You attack first. During battle, gain +1 ATK.',
    '"Just like you... I have my battles to fight." - Islay',
    None,
        )

CARD_ROCKET_CANNON = OJCard(124,
    'Rocket Cannon',
    1, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Choose one of the following two effects to activate: 1. This card becomes "Big Rocket Cannon". 2. Deal 1 damage '
    'to target enemy. If KO\'d, you gain wins as though KO\'d in battle.',
    '"Red Barrel... It\'s time to use that!" ―Marc',
    None,
        )

CARD_SAINT_EYES = OJCard(125,
    'Saint Eyes',
    1, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Stock Effect (3). In a battle where you attack first, gain -1 ATK and +1 DEF for every 2 stock, and +1 ATK per '
    'stock. This effect can stack.',
    '"I\'m going to use my saint eyes!" - Kyupita',
    None,
        )

CARD_SOLID_WITCH = OJCard(126,
    'Solid Witch',
    2, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Effect Duration: 1 chapter. Take no damage.',
    '"No flimsy attacks can hurt me!" ―Miusaki',
    None,
        )

CARD_SPECIAL_STAGE = OJCard(127,
    'Special Stage',
    1, CARD_COST_Lvx10, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Go to Live Mode for (your Lvl) turns. Gain -3 MOV, can only trigger movement type panels and cannot use cards. '
    'Cannot be challenged or be the target of Boost cards. If an opponent ends their turn in 2 panel radius, steal '
    '(your Lvl) x5 stars from them. Ends on KO.',
    '"We are the strongest idols!" ―Sora & Sham',
    None,
        )

CARD_STEALTH_ON = OJCard(128,
    'Stealth On',
    2, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Effect Duration: 3 chapters. Cannot be challenged to battle or targeted by boost cards by other players. Effect '
    'expires on entering battle. Gain +2 ATK when entering battle.',
    '"Look at me vanish!" ―Tsih',
    None,
        )

CARD_SWEET_GUARDIAN = OJCard(129,
    'Sweet Guardian',
    3, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Draw 2 cards with "Pudding" in their name from the center deck.',
    '"My little... pudding..." ―QP',
    None,
        )

CARD_TURBO_CHARGED = OJCard(130,
    'Turbo Charged',
    2, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Drop to 1 HP. Gain +1 ATK per lost HP. Effect Duration: As many Chapters as lost HP. Lose 1 ATK per turn for the '
    'duration. Effect expires on KO.',
    '"Rumble rumble rumble." -Shifu Robot',
    None,
        )

CARD_UBIQUITOUS = OJCard(131,
    'Ubiquitous',
    1, CARD_COST_0, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Move to target unit\'s panel. In addition, steal stars equal to 10x their level.',
    '"Poppo! Poppopopopopo!" ―Marie Poppo',
    None,
        )

CARD_WITCHS_HAIR_LOCK = OJCard(132,
    'Witch\'s Hair Lock',
    1, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Stop target unit\'s next move action.',
    '"No one can get out of Repa\'s hair." ―Ceoreparque',
    None,
        )

CARD_X16_BIG_ROCKET = OJCard(133,
    'x16 Big Rocket',
    1, CARD_COST_Lvx10, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Deal damage equal to your level to target unit. A KO from this effect gives you 2 Wins.',
    '"Charged! Go!" - Marc',
    None,
        )

CARD_AIR_STRIKE = OJCard(134,
    'Air Strike',
    2, CARD_COST_30, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Every unit except your own receives 1 to 3 damage. Gain 15 stars on every KO',
    '"Hmph, go down, all of you." - Fernet',
    None,
        )

CARD_BINDING_CHAINS = OJCard(135,
    'Binding Chains',
    3, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Stock Effect All Units except yours will skip their next turn. Apply "Bound" to all active enemies. Effect '
    'Duration: 2 Chapters. Gain -2 EVD and -1 MOV.',
    '"I don\'t like this sort of thing." -Hime',
    None,
        )

CARD_COOKING_TIME = OJCard(136,
    'Cooking Time',
    1, CARD_COST_Lvx5, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'All players recover your Lvl x HP. Gain 5 stars for each HP recovered.',
    '"It\'s meal time!" ―Natsumi',
    None,
        )

CARD_DELTA_FIELD = OJCard(137,
    'Delta Field',
    2, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'All other units receive the following effect until your next turn: All dice rolls will be 1.',
    '"If you insist on staying here, I\'ll take you back no matter how!" ―Sham',
    None,
        )

CARD_DEVIL_HAND = OJCard(138,
    'Devil Hand',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Lower a random player\'s HP to 1 and gain 10 stars per lowered HP. In odd-numbered chapters, this card turns '
    'into Angel Hand.',
    '"Eat the power of the devil!" ―Yuuki',
    None,
        )

CARD_DO_PIRATES_FLY_IN_THE_SKY = OJCard(139,
    'Do Pirates Fly in the Sky?',
    3, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Set "Flying Pirate" on 2-3 random panels.',
    '"There ain\'t no law against pirates flying in the sky." ―Tequila',
    None,
        )

CARD_EVIL_MASTERMIND = OJCard(140,
    'Evil Mastermind',
    2, CARD_COST_13, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Draw a trap card from the deck. Set all trap cards in hand on random panels. If not holding any trap cards, draw '
    '3 from the deck and set a random one on your current panel.',
    '"Fear my powers!" -Yuki',
    None,
        )

CARD_EVIL_SPY_WORK_PREPARATION = OJCard(141,
    'Evil Spy Work - Preparation',
    2, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Place 4 "Evil Spy Work - Execution" cards at random positions in the Center Deck.',
    '"Fear Mimyuu\'s pranks." -Mimyuu',
    None,
        )

CARD_FINAL_SURGERY = OJCard(142,
    'Final Surgery',
    2, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'KO all units with 1 HP and gain stars equal to 25x the number of KO\'d units.',
    '"Just hold still, I\'ll fix you up real quick." - Kiriko',
    None,
        )

CARD_GAMBLE = OJCard(143,
    'Gamble!',
    3, CARD_COST_13, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'A randomly chosen unit is KO\'d.',
    '"Why not use this to decide whose turn it is?" - Yuki',
    None,
        )

CARD_MAGICAL_INFERNO = OJCard(144,
    'Magical Inferno',
    3, CARD_COST_50, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'KO all units on any other panel in the same uninterrupted column or row as the panel your unit is on. You gain'
    'stars from each KO\'d unit as though KO\'d in battle. Then end your turn.',
    '"Inferno!" ―Mio',
    None,
        )

CARD_MAGICAL_MASSACRE = OJCard(145,
    'Magical Massacre',
    4, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'All units whose HP is full or higher will suffer KO. Gain -1 REC on next Revive roll for each enemy KO\'d.',
    '"Disappear." -Tomomo',
    None,
        )

CARD_MAGICAL_REVENGE = OJCard(146,
    'Magical Revenge',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'For each missing HP, random enemy takes 1 damage. If a unit is KO\'d, you gain 1 Win. When not held by Tomomo '
    '(Sweet Eater), this card becomes Miracle Red Bean Ice Cream.',
    '"It\'s Magical Revenge time!" ―Tomomo',
    None
        )

CARD_MELTING_MEMORIES = OJCard(147,
    'Melting Memories',
    3, CARD_COST_OCx5, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'All other players discard and replace a card from their hand. Reverse all enemy cards.',
    '"How foolish you are to have challenged a God. Prepare to taste your bitter defeat!" - Sweet Breaker',
    None,
        )

CARD_OVERSEER = OJCard(148,
    'Overseer',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT|CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'A boss appears. If a boss is already on the field, treat this card as a battle card: End the battle. Opponent '
    'fights the boss instead. Can only use against players.',
    '"Hahaha! Here comes my friend!" ―NoName',
    None,
        )

CARD_PLUSHIE_MASTER = OJCard(149,
    'Plushie Master',
    2, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Set "Dance, Long-Eared Beasts!" trap on 3-5 random panels.',
    '"Dance, long-eared beasts!" -Krilalaris',
    None,
        )

CARD_PRESENT_FOR_YOU = OJCard(150,
    'Present for You',
    2, CARD_COST_30, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'All players draw cards until they have a full hand. Those with full hand draw 1 card instead. Gain stars equal '
    'to 10x the number of all cards drawn.',
    '"Presents for good boys and girls." -Aru',
    None,
        )

CARD_REVIVAL_OF_STARS = OJCard(151,
    'Revival of Stars',
     1, CARD_COST_Lvx3, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Effect Duration: 3 Chapters. Turn all Drop Panels into Bonus Panels and Encounter and Boss Panels into Draw '
    'Panels. -1 ATK when on a marked panel.',
    '"The dream you protected has spread across the whole planet." ―Suguri',
    None,
        )

CARD_STAR_BLASTING_FUSE = OJCard(152,
    'Star Blasting Fuse',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Set "Invisible Bomb" on 3-5 random panels',
    '"Because I am Star Breaker, the blasting fuse to the world\'s end." -Star Breaker',
    None,
        )

CARD_SUBSPACE_TUNNEL = OJCard(153,
    'Subspace Tunnel',
    1, CARD_COST_Lvx5, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Effect Duration: Player level Turn 4-6 panels into Warp Move panels and then warp to one of them.',
    '"Po! Po! Po! Popoppo!!" ―Marie Poppo',
    None,
        )

CARD_TRUE_WHITE_CHRISTSMASHER = OJCard(154,
    'True White Christsmasher',
    3, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Deal 4 damage to players within 1 panel of you. For each player KO\'d, gain 2 wins and KO\'d Player\'s Lvl x10 '
    'stars. When not carrying "Red & Blue", this card becomes "White Christsmasher".',
    '"White Christsmasher!" ―Mei, Red & Blue',
    None,
        )

CARD_WHIMSICAL_WINDMILL = OJCard(155,
    'Whimsical Windmill',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Fight all other players in order. The enemy goes first. During battle, gain +1 EVD.',
    '"We just want to fly around freely." - Sherry',
    None,
        )

CARD_WHITE_CHRISTSMASHER = OJCard(156,
    'White Christsmasher',
    2, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Deal 2 damage to players on the same panel as you. For each player KO\'d, gain a win and KO\'d Player\'s Lvl x5 '
    'stars. When carrying "Red & Blue", this card becomes "True White Christsmasher".',
    '"White Christsmasher!" ―Mei',
    None,
        )

CARD_BANNER_FOR_LIFE = OJCard(157,
    'Banned for Life',
    1, CARD_COST_Stp10, -1, CARD_TYPE_HYPER|CARD_TYPE_GIFT, None, CARD_RARITY_NONE,
    'Can only play Gift cards. Using this card sends it to another player. Discards entire hand upon discard.',
    '"Manager, it\'s your turn!!" -Chris',
    None,
        )

CARD_BEAST_WITCH = OJCard(158,
    'Beast Witch',
    1, CARD_COST_0, -1, CARD_TYPE_HYPER|CARD_TYPE_GIFT, None, CARD_RARITY_NONE,
    'When another player loses stars from an Encounter panel battle and those stars would go to the Encounter panel '
    'unit, you will receive them instead. If this effect is triggered, discard this card at the end of your turn. If '
    'several players carry Beast Witch, the stars are split between them.',
    '"All beasts! Obey me!" - Teotoratta',
    None,
        )

CARD_EVIL_SPY_WORK_EXECUTION = OJCard(159,
    'Evil Spy Work - Execution',
    1, CARD_COST_0, -1, CARD_TYPE_HYPER|CARD_TYPE_GIFT, None, CARD_RARITY_NONE,
    'This card cannot be played. When holding this card, take 3 damage at the end of your turn, and remove this card '
    'from the game.',
    '"You fell for it! Eat it!!" -Mimyuu',
    None,
        )

CARD_MIRACLE_RED_BEAN_ICE_CREAM = OJCard(160,
    ' Miracle Red Bean Ice Cream',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER|CARD_TYPE_GIFT, None, CARD_RARITY_NONE,
    '+1 ATK while this card is held. Tomomo (Casual): When played, turn into Tomomo (Sweet Eater) and fully restore '
    'HP. Tomomo (Sweet Eater): When held, this card becomes Magical Revenge. Discard upon use or KO in battle.',
    '"Miracle red bean ice cream!" ―Tomomo',
    None,
        )

CARD_SANTAS_JOB = OJCard(161,
    'Santa\'s Job',
    1, CARD_COST_0, -1, CARD_TYPE_HYPER|CARD_TYPE_GIFT, None, CARD_RARITY_NONE,
    'After your turn, send a card of usable Lvl from your hand to a random player. Gain stars equal to Card Lvl x5. '
    'Target cannot challenge players to a battle until your next turn. This card is discarded upon KO or use',
    '"Children of the world, we are coming for you!" ―Aru',
    None,
        )

CARD_BIG_BANG_BELL = OJCard(162,
    'Big Bang Bell',
    3, CARD_COST_0, -1, CARD_TYPE_HYPER|CARD_TYPE_TRAP, None, CARD_RARITY_NONE,
    'Every unit on this and 2 adjacent squares takes 2 damage, +1 for every 2 chapters since setting the trap. On KO, '
    'half of their stars go to the player who set this trap.',
    '"Mauuuuuryaaaaaaahh!" ―Saki',
    None,
        )

CARD_DANCE_LONG_EARED_BEASTS = OJCard(163,
    'Dance, Long-Eared Beasts!',
    2, CARD_COST_0, -1, CARD_TYPE_HYPER|CARD_TYPE_TRAP, None, CARD_RARITY_NONE,
    'Set "Dance, Long-Eared Beasts!" trap on 3-5 random panels.',
    '"Dance, long-eared beasts!" -Krilalaris',
    None,
        )

CARD_FLYING_PIRATE = OJCard(164,
    'Flying Pirate',
    3, CARD_COST_0, -1, CARD_TYPE_HYPER|CARD_TYPE_TRAP, None, CARD_RARITY_NONE,
    'Fight a Pirate Crew Member summoned by the player who set this card. The enemy will attack first. No effect on '
    'the player who set this card.',
    '"Captain～!" - Pirate Minion',
    None,
        )

CARD_GOLDEN_EGG = OJCard(165,
    'Golden Egg',
    2, CARD_COST_0, -1, CARD_TYPE_HYPER|CARD_TYPE_TRAP, None, CARD_RARITY_NONE,
    'If target is Chicken, Stock Effect (3). Drop Panels will act as Bonus Panels. Otherwise, Stock Effect (3). '
    'Bonus Panels will act as Drop Panels.',
    '"Cluuuuck!" ―Chicken',
    None,
        )

CARD_INVISIBLE_BOMB = OJCard(166,
    'Invisible Bomb',
    3, CARD_COST_0, -1, CARD_TYPE_HYPER|CARD_TYPE_TRAP, None, CARD_RARITY_NONE,
    'Reduces HP to 1. Does not affect the player who set the trap. Only visible to the player who used this card.',
    '"Because I am Star Breaker, the blasting fuse to the world\'s end." -Star Breaker',
    None,
        )

CARD_RBIT_HOBBY_SHOP = OJCard(167,
    'Rbit Hobby Shop',
    1, CARD_COST_0, -1, CARD_TYPE_HYPER|CARD_TYPE_TRAP, None, CARD_RARITY_NONE,
    'Pay X stars to the player who set this card, where X is the Lvl of the player who set this card. Draw a card from '
    'the deck. This card remains on board when triggered but can be replaced by a new trap. No effect on the player '
    'who set this trap.',
    '"All right, it\'s time to open the shop." ―Arthur',
    None,
        )

#### #### #### #### EVENT CARDS #### #### ####

CARD_SWEET_BATTLE = OJCard(168,
    'Sweet Battle!',
    1, CARD_COST_0, 6, CARD_TYPE_GIFT|CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'When held: Pick up 2x chocolate. When played in battle: Steal 200 chocolate for each damage dealt. This card is '
    'discarded upon KO or use.',
    '"Here comes another cute and sweet battle!" ―QP',
    (EVENT_CHOCOLATE_FOR_THE_SWEET_GODS, EVENT_RETURN,),
        )

CARD_SNOWBALL_REFLECTOR = OJCard(169,
    'Snowball Reflector',
    2, CARD_COST_10, 4, CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'On this defense turn, any snowball that would hit you will hit the unit that threw them instead. Ignore unit '
    'effects that would prevent this card from being played.',
    '"A-and it comes right back at you!" ―Aru',
    (EVENT_SANTA_SCRAMBLE, EVENT_RETURN),
        )

CARD_GROWN_UP_SNOWBALL_FIGHT = OJCard(170,
    'Grown-up Snowball Fight',
    3, CARD_COST_10, 4, CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'On this attack turn, select two panels to target with snowballs. Ignore unit effects that would prevent this card '
    'from being played.',
    '"Are you prepared for this?" ―Arthur',
    (EVENT_SANTA_SCRAMBLE, EVENT_RETURN),
        )

CARD_LEGENDARY_MUSHROOM = OJCard(171,
    'Legendary Mushroom',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, None, CARD_RARITY_NONE,
    'Smells notoriously funky. / Smells eerily funky.',
    None,
    (EVENT_SHROOM_ZOOM,),
        )

#### #### #### #### EVENT CARDS DEPRECATED #### #### ####

CARD_ULTIMATE_WEAPON_IN_THE_SUN = OJCard(172,
    'Ultimate Weapon in the Sun',
    5, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'During this battle, gain 2 ATK.',
    'I\'ll commence... my vacation now." ―Sora',
    (EVENT_BEACH_PARTY,),
        )

CARD_LIFEGUARD_ON_THE_WHITE_BEACH = OJCard(173,
    'Lifeguard on the White Beach',
    5, CARD_COST_10, -1, CARD_TYPE_HYPER|CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'All allies gain a damage reduction of 2 during their next battle.',
    '"Geez, you\'re going overboard." ―Suguri',
    (EVENT_BEACH_PARTY,),
        )

CARD_GUARDIAN_OF_BLOOMING_FLOWERS = OJCard(174,
    'Guardian of Blooming Flowers',
    5, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Revive one KO\'d ally with full HP',
    '"You\'re fine now. The pain\'s gone." ―Hime',
    (EVENT_BEACH_PARTY,),
        )

CARD_UNFORGIVING_AVENGER = OJCard(175,
    'Unforgiving Avenger',
    5, CARD_COST_20, -1, CARD_TYPE_HYPER|CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'During this battle, damage taken by both sides is doubled.',
    '"Mimyuu! Who did this to you..." ―Tomato',
    (EVENT_BEACH_PARTY,),
        )

#### #### #### #### OTHER CARDS #### #### ####

CARD_RED_AND_BLUE = OJCard(176,
    'Red & Blue',
    1, CARD_COST_0, -1, CARD_TYPE_GIFT, None, CARD_RARITY_NONE,
    'When holding this card, gain +1 ATK, DEF and EVD in battle. On Discard or KO, this card is removed from the game.',
    '"We can\'t do this anymore!" ―Red & Blue',
    None,
        )

CARD_MUSHROOM_BOOST = OJCard(177,
    'Mushroom',
    1, CARD_COST_0, -1, CARD_TYPE_BOOST|CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'Smells funky.',
    None,
    None,
        )


CHARACTER_QP = OJCharacter(1,
    'QP',
    5, 0, 0, 0, 5,
    ORIGIN_QP_SHOOTING,
    None,
    (CARD_HYPER_MODE,),
    'QP_(unit).png',
        )

CHARACTER_SUGURI = OJCharacter(2,
    'Suguri',
    4, 1, -1, 2, 5,
    ORIGIN_SUGURI,
    None,
    (CARD_ACCELERATOR,),
    'Suguri_(unit).png',
        )

CHARACTER_MARC = OJCharacter(3,
    'Marc',
    4, 1, 1, -1, 5,
    ORIGIN_FLYING_RED_BARREL,
    None,
    (CARD_X16_BIG_ROCKET,),
    'Marc_(unit).png',
        )

CHARACTER_KAI = OJCharacter(4,
    'Kai',
    5, 1, 0, 0, 5,
    ORIGIN_100_ORANGE_JUICE,
    None,
    (CARD_PROTAGONISTS_PRIVILEGE,),
    'Kai_(unit).png',
        )

CHARACTER_YUKI = OJCharacter(5,
    'Yuki',
    5, 2, -1, -1, 5,
    ORIGIN_QP_SHOOTING,
    None,
    (CARD_GAMBLE,),
    'Yuki_(unit).png',
        )

CHARACTER_ARU = OJCharacter(6,
    'Aru',
    5, -1, -1, 2, 5,
    ORIGIN_CHRISTMAS_SHOOTING,
    'Can hold 4 cards.',
    (CARD_PRESENT_FOR_YOU,),
    'Aru_(unit).png',
        )

CHARACTER_HIME = OJCharacter(7,
    'Hime',
    5, 1, -1, 1, 5,
    ORIGIN_SUGURI,
    None,
    (CARD_BINDING_CHAINS,),
    'Hime_(unit).png',
        )

CHARACTER_SORA = OJCharacter(8,
    'Sora',
    4, 1, 0, 1, 5,
    ORIGIN_SORA,
    None,
    (CARD_EXTRAORDINARY_SPECS,),
    'Sora_(unit).png',
        )

CHARACTER_FERNET = OJCharacter(9,
    'Fernet',
    6, -1, 2, -2, 5,
    ORIGIN_FLYING_RED_BARREL,
    None,
    (CARD_AIR_STRIKE,),
    'Fernet_(unit).png',
        )

CHARACTER_PEAT = OJCharacter(10,
    'Peat',
    3, 1, 1, 1, 4,
    ORIGIN_FLYING_RED_BARREL,
    None,
    (CARD_BLUE_CROW_THE_SECOND,),
    'Peat_(unit).png',
        )

CHARACTER_MARIE_POPPO = OJCharacter(11,
    'Marie Poppo',
    7, -1, -1, -1, 5,
    ORIGIN_100_ORANGE_JUICE,
    None,
    (CARD_UBIQUITOUS,),
    'Marie_Poppo_(unit).png',
        )

CHARACTER_TOMOMO_UNSOFTENED = OJCharacter(12,
    'Tomomo (Unsoftened)',
    6, 2, 0, 1, 6,
    ORIGIN_100_ORANGE_JUICE,
    None,
    (CARD_MAGICAL_MASSACRE,),
    'Tomomo_(Softened)_(unit).png',
        )

CHARACTER_TOMOMO_SOFTENED = OJCharacter(13,
    'Tomomo (Softened)',
    4, 2, 0, 0, 6,
    ORIGIN_100_ORANGE_JUICE,
    'Softened: Tomomo is playing with friends, and has lowered her attributes.',
    (CARD_MAGICAL_MASSACRE,),
    'Tomomo_(Softened)_(unit).png',
        )

CHARACTER_MIO = OJCharacter(14,
    'Mio',
    6, 0, -1, 1, 4,
    ORIGIN_100_ORANGE_JUICE,
    None,
    (CARD_MAGICAL_INFERNO,),
    'Mio_(unit).png',
        )

CHARACTER_SYURA = OJCharacter(15,
    'Syura',
    4, 0, 1, 0, 4,
    ORIGIN_QP_SHOOTING_DANGEROUS,
    'When at 1 HP at the start of a battle, gain +1 ATK and +1 EVD until the end of the battle.',
    (CARD_BEYOND_HELL,),
    'Syura_(unit).png',
        )

CHARACTER_NANAKO = OJCharacter(16,
    'Nanako',
    3, 0, 2, 1, 4,
    ORIGIN_SUGURI,
    None,
    (CARD_DEPLOY_BITS,),
    'Nanako_(unit).png',
        )

CHARACTER_SAKI = OJCharacter(17,
    'Saki',
    4, 0, 0, 1, 4,
    ORIGIN_SUGURI,
    None,
    (CARD_BIG_BANG_BELL,),
    'Saki_(unit).png',
        )

CHARACTER_KYOUSUKE = OJCharacter(18,
    'Kyousuke',
    5, -1, 2, 0, 5,
    ORIGIN_QP_KISS,
    None,
    (CARD_CAST_OFF,),
    'Kyousuke_(unit).png',
        )

CHARACTER_KRILA = OJCharacter(19,
    'Krila',
    6, 0, 0, -1, 5,
    ORIGIN_QP_SHOOTING_DANGEROUS,
    None,
    (CARD_PLUSHIE_MASTER, CARD_DANCE_LONG_EARED_BEASTS),
    'Krila_(unit).png',
        )

CHARACTER_KAE = OJCharacter(20,
    'Kae',
    4, 0, -1, 1, 4,
    ORIGIN_SUGURI,
    'Add reverse value of DEF to ATK. Gain -1 DEF when attacking.',
    (CARD_BLAZING,),
    'Kae_(unit).png',
        )

CHARACTER_ALTE = OJCharacter(21,
    'Alte',
    5, 0, -1, 1, 5,
    ORIGIN_SORA,
    'In battle, see a random card from the opponent\'s hand. On Self-destruct, gain +1 ATK (up to +3).',
    (CARD_SELF_DESTRUCT,),
    'Alte_(unit).png',
        )

CHARACTER_KYOKO = OJCharacter(22,
    'Kyoko',
    5, -1, 3, -2, 5,
    ORIGIN_SUGURI,
    'Cannot use the Evade command in battle.',
    (CARD_CRYSTAL_BARRIER,),
    'Kyoko_(unit).png',
        )

CHARACTER_SHAM = OJCharacter(23,
    'Sham',
    4, 0, 1, 1, 5,
    ORIGIN_SORA,
    None,
    (CARD_DELTA_FIELD,),
    'Sham_(unit).png',
        )

CHARACTER_SHERRY = OJCharacter(24,
    'Sherry',
    5, 1, 1, 1, 5,
    ORIGIN_FLYING_RED_BARREL,
    'Enemy always goes first. If the enemy is Sherry, ignore this effect.',
    (CARD_WHIMSICAL_WINDMILL,),
    'Sherry_(unit).png',
        )

CHARACTER_STAR_BREAKER = OJCharacter(25,
    'Star Breaker',
    5, 2, 0, -1, 5,
    ORIGIN_SORA,
    'can only choose Wins norma.',
    (CARD_STAR_BLASTING_FUSE, CARD_INVISIBLE_BOMB),
    'Star_Breaker_(unit).png',
        )

CHARACTER_SWEET_BREAKER = OJCharacter(26,
    'Sweet breaker',
    6, 0, 0, 0, 6,
    ORIGIN_QP_SHOOTING_DANGEROUS,
    'When battling a player with reversed cards, gain +1 to ATK, DEF and EVD for each.',
    (CARD_MELTING_MEMORIES,),
    'Sweet_Breaker_(unit).png',
        )

CHARACTER_NATH = OJCharacter(27,
    'Nath',
    5, -1, -1, 1, 5,
    ORIGIN_SORA,
    'Gain 1 stack of Active Extension in each battle where a battle card is played (max 3). Lose 1 stack on KO. '
    'Stock Effect: gain +1 ATK, +1 DEF, and -1 EVD.',
    (CARD_ANOTHER_ULTIMATE_WEAPON,),
    'Nath_(unit).png',
        )

CHARACTER_MIMYUU = OJCharacter(28,
    'Mimyuu',
    3, -1, 0, 1, 1,
    ORIGIN_QP_SHOOTING,
    'Revive as Tomato and act on revival. Lose 1/4 stars and given 1 WIN when KO\'d in battle.',
    (CARD_EVIL_SPY_WORK_EXECUTION,),
    'Mimyuu_(unit).png',
        )

CHARACTER_TOMATO = OJCharacter(29,
    'Tomato',
    3, 1, 0, 0, 3,
    ORIGIN_QP_SHOOTING,
    'Revive as Mimyuu and act on revival. Draw Evil Spy Work - Execution cards as Waruda Machine, Blast Off!',
    (CARD_WARUDA_MACHINE_BLAST_OFF,),
    'Tomato_(unit).png',
        )

CHARACTER_KIRIKO = OJCharacter(30,
    'Kiriko',
    8, 0, -1, 0, 5,
    ORIGIN_XMAS_SHOOTING_SCRAMBLE,
    'Ignore healing effects. When playing a battle card, gain +1 ATK & EVD in battle, and MAX HP is reduced by 1 '
    '(To a minimum of 2).',
    (CARD_FINAL_SURGERY,),
    'Kiriko_(unit).png',
        )

CHARACTER_NONAME = OJCharacter(31,
    'NoName',
    5, 1, -1, 0, 6,
    ORIGIN_ACCELERATION_OF_SUGURI,
    'If KO\'d, turn into NoName (Head) instead. Give no stars or Wins if KO\'d in battle.',
    (CARD_OVERSEER,),
    'NoName_(unit).png',
        )

CHARACTER_NONAME_HEAD = OJCharacter(32,
    'NoName (Head)',
    2, -1, -1, -1, 6,
    ORIGIN_ACCELERATION_OF_SUGURI,
    'Change into NoName after reaching a home or getting KO\'d. Gain -1 MOV.',
    (CARD_OVERSEER,),
    'NoName_(Head)_(unit).png',
        )

CHARACTER_MIUSAKI = OJCharacter(33,
    'Miusaki',
    4, 1, -2, 0, 5,
    ORIGIN_ALICIANRONE,
    'When using Defend in battle, never take more than 2 damage at once.',
    (CARD_SOLID_WITCH,),
    'Miusaki_(unit).png',
        )

CHARACTER_CEOREPARQUE = OJCharacter(34,
    'Ceoreparque',
    4, 0, 0, 1, 5,
    ORIGIN_ALICIANRONE,
    'On successful Evasion, deal 1 damage to opponent.',
    (CARD_WITCHS_HAIR_LOCK,),
    'Ceoreparque_(unit).png',
        )

CHARACTER_YUKI_DANGEROUS = OJCharacter(35,
    'Yuki (Dangerous)',
    5, 1, -2, 0, 5,
    ORIGIN_QP_SHOOTING_DANGEROUS,
    'Permanently turn every help card with Pudding in name into Tragedy in the Dead of Night.\n'
    'When someone else triggers your trap, gain 1 Win. Gain no wins from fighting neutral enemies.',
    (CARD_EVIL_MASTERMIND,),
    'Yuki_(Dangerous)_(unit).png',
        )

CHARACTER_TOMOMO_CASUAL = OJCharacter(36,
    'Tomomo (Casual)',
    4, -1, 0, 1, 5,
    ORIGIN_100_ORANGE_JUICE,
    None,
    (CARD_MIRACLE_RED_BEAN_ICE_CREAM,),
    'Tomomo_(Casual)_(unit).png',
        )

CHARACTER_TOMOMO_SWEET_EATER = OJCharacter(37,
    'Tomomo (Sweet Eater)',
    6, 3, 0, 0, 6,
    ORIGIN_100_ORANGE_JUICE,
    'When KO\'d, discard your hand and turn back to Tomomo (Casual).',
    (CARD_MAGICAL_REVENGE,),
    'Tomomo_(Sweet_Eater)_(unit).png',
        )

CHARACTER_TEQUILA = OJCharacter(38,
    'Tequila',
    5, 0, 1, -3, 6,
    ORIGIN_FLYING_RED_BARREL,
    'A Pirate Crew Member appears as enemy unit. Gain +1 ATK for every HP lost during a battle.',
    (CARD_DO_PIRATES_FLY_IN_THE_SKY, CARD_FLYING_PIRATE),
    'Tequila_(unit).png',
        )

CHARACTER_TSIH = OJCharacter(39,
    'Tsih',
    4, 0, -2, 2, 5,
    ORIGIN_SORA,
    'Gain +2ATK if holding a Gift card.',
    (CARD_STEALTH_ON,),
    'Tsih_(unit).png',
        )

CHARACTER_MEI = OJCharacter(40,
    'Mei',
    4, 0, 0, 0, 5,
    ORIGIN_QP_SHOOTING,
    'Gain "Red & Blue" when holding no cards at the end of turn.',
    (CARD_TRUE_WHITE_CHRISTSMASHER, CARD_WHITE_CHRISTSMASHER),
    'Mei_(unit).png',
        )

CHARACTER_NATSUMI = OJCharacter(41,
    'Natsumi',
    5, 0, -1, 0, 5,
    ORIGIN_XMAS_SHOOTING_SCRAMBLE,
    'If not KO\'d and standing on the same panel with other players at the end of your turn, each unit on the panel '
    'recovers 1 HP. For each other players you heal, gain 5 stars.',
    (CARD_COOKING_TIME,),
    'Natsumi_(unit).png',
        )

CHARACTER_NICO = OJCharacter(42,
    'Nico',
    4, 0, 0, 1, 5,
    ORIGIN_XMAS_SHOOTING_SCRAMBLE,
    'No effect from Gift cards. Gain X additional stars from all sources, where X is the number of Gift cards in hand. '
    'Can hold 4 cards.',
    (CARD_MIRACLE_WALKER,),
    'Nico_(unit).png',
        )

CHARACTER_ARTHUR = OJCharacter(43,
    'Arthur',
    7, 0, -1, -1, 6,
    ORIGIN_CHRISTMAS_SHOOTING,
    'Gain X additional stars from all sources, where X is the number of Shops in play, up to current Lvl.',
    (CARD_BRANCH_EXPANSION_STRATEGY, CARD_RBIT_HOBBY_SHOP),
    'Arthur_(unit).png',
        )

CHARACTER_IRU = OJCharacter(44,
    'Iru',
    5, 0, -1, 0, 5,
    ORIGIN_SUGURI,
    'When challenging an enemy, they take 1 damage and attack first if no other effect affect turn order. KO from this '
    'effect counts as battle KO.',
    (CARD_EXTENDED_PHOTON_RIFLE,),
    'Iru_(unit).png',
        )

CHARACTER_MIRA = OJCharacter(45,
    'Mira',
    5, 1, -1, 1, 5,
    ORIGIN_SORA,
    'Your traps triggered by enemies add the following additional effect: Binding Smoke (For 2 chapters: Move rolls '
    'are limited to 1, 2, or 3).',
    (CARD_LEAP_THROUGH_SPACE, CARD_LEAP_THROUGH_SPACE_MARKING),
    'Mira_(unit).png',
        )

CHARACTER_CUTIES = OJCharacter(46,
    'Cuties',
    4, 0, 0, 1, 5,
    ORIGIN_SORA,
    'Can only choose Stars norma. Gain X additional stars from all sources, where X is the number of different Event '
    'cards you played. In battle, randomly gain +1 ATK or DEF.',
    (CARD_SPECIAL_STAGE,),
    'Sora_&_Sham_(Cuties)_(unit).png',
        )

CHARACTER_YUUKI = OJCharacter(47,
    'Yuuki',
    4, 0, 0, 0, 5,
    ORIGIN_QP_SHOOTING,
    'In odd-numbered chapters, gain -1 ATK and +2 in DEF. In even-numbered chapters, gain +2 ATK and -1 DEF.',
    (CARD_ANGEL_HAND, CARD_DEVIL_HAND),
    'Yuuki_(unit).png',
        )

CHARACTER_ISLAY = OJCharacter(48,
    'Islay',
    5, 1, 1, 1, 5,
    ORIGIN_FLYING_RED_BARREL,
    'cannot challenge other players when meeting them on the field.',
    (CARD_RIVAL,),
    'Islay_(unit).png',
        )

CHARACTER_SUGURI_46_BILLION_YEARS = OJCharacter(49,
    'Suguri (46 Billion Years)',
    5, 1, 1, 1, 5,
    ORIGIN_FLYING_RED_BARREL,
    'When choosing a damage dealing Boost/Event card to play, you may pay double its cost to double the damage on use. '
    'If you do, gain +1 die to your next movement roll.',
    (CARD_OBSERVER_OF_ETERNITY,),
    'Suguri_(46_Billion_Years)_(unit).png',
        )

CHARACTER_SUMIKA = OJCharacter(50,
    'Sumika',
    5, 1, -1, 1, 5,
    ORIGIN_200_MIXED_JUICE,
    None,
    (CARD_REPRODUCTION_OF_RECORDS,),
    'Sumika_(unit).png',
        )

CHARACTER_ELLIE = OJCharacter(51,
    'Ellie',
    5, 1, 0, 0, 5,
    ORIGIN_100_ORANGE_JUICE,
    None,
    (CARD_ELLIES_MIRACLE,),
    'Ellie_(unit).png',
        )

CHARACTER_LULU = OJCharacter(52,
    'Lulu',
    5, 0, 1, -1, 5,
    ORIGIN_100_ORANGE_JUICE,
    None,
    (CARD_LULUS_LUCKY_EGG,),
    'Lulu_(unit).png',
        )

CHARACTER_ALICIANRONE = OJCharacter(53,
    'Alicianrone',
    4, 1, -1, 1, 5,
    ORIGIN_ALICIANRONE,
    'When battling an opponent with more than +1 ATK, gain +1 EVD, until end of battle. If they have more than +2 ATK, '
    'gain an additional +1 EVD.',
    (CARD_FULL_SPEED_ALICIANRONE,),
    'Alicianrone_(unit).png',
        )

CHARACTER_TEOTORATTA = OJCharacter(54,
    'Teotoratta',
    5, 0, 0, 1, 4,
    ORIGIN_ALICIANRONE,
    'Do not trigger Encounter panels.',
    (CARD_BEAST_WITCH,),
    'Teotoratta_(unit).png',
        )

CHARACTER_ARNELLE = OJCharacter(55,
    'Arnelle',
    5, 1, -1, 0, 5,
    ORIGIN_100_ORANGE_JUICE,
    'Can see the card on the top of the deck when holding Intelligence Officer in hand.',
    (CARD_INTELLIGENCE_OFFICER,),
    'Arnelle_(unit).png',
        )

CHARACTER_MAYNIE = OJCharacter(56,
    'Maynie',
    4, 0, 1, 0, 5,
    ORIGIN_100_ORANGE_JUICE,
    'When not in Raging Mode, gain a rage Counter upon taking damage and lose a rage Counter upon healing.',
    (CARD_RAGING_MADNESS,),
    'Maynie_(unit).png',
        )

CHARACTER_CHRIS = OJCharacter(57,
    'Chris',
    5, -1, 0, 0, 5,
    ORIGIN_QP_SHOOTING,
    'Can hold 4 cards. Cannot challenge to battles without Chef or Store manager active. Gain a Store manager Counter '
    'upon using a Max 1 copy limit non-Gift card.',
    (CARD_CHEF_I_COULD_USE_SOME_HELP, CARD_MANAGER_I_COULD_USE_SOME_HELP),
    'Chris_(unit).png',
        )

CHARACTER_KYUPITA = OJCharacter(58,
    'Kyupita',
    5, 0, 0, 0, 5,
    ORIGIN_QP_KISS,
    None,
    (CARD_SAINT_EYES,),
    'Kyupita_(unit).png',
        )

CHARACTER_QP_DANGEROUS = OJCharacter(59,
    'QP (Dangerous)',
    5, 0, 0, -1, 5,
    ORIGIN_QP_SHOOTING_DANGEROUS,
    'Gain combat bonuses from carrying cards with \'Pudding\' in their name.\n'
    'Dangerous Pudding (+1ATK)\n'
    'Bad Pudding (+1DEF)\n'
    'Pudding (+1EVD)\n'
    'Portable Pudding (+1MAXHP).',
    (CARD_SWEET_GUARDIAN,),
    'QP_(Dangerous)_(unit).png',
        )

CHARACTER_MARIE_POPPO_MIXED = OJCharacter(60,
    'Marie Poppo (Mixed)',
    7, -1, -1, -1, 5,
    ORIGIN_200_MIXED_JUICE,
    'When warping from any effect: If player level is odd, gain Lvl x3 in stars. If player level is even, draw a card.',
    (CARD_SUBSPACE_TUNNEL,),
    'Marie_Poppo_(Mixed)_(unit).png',
        )

CHARACTER_SORA_MILITARY = OJCharacter(61,
    'Sora (Military)',
    4, 1, 0, 1, 5,
    ORIGIN_SORA,
    'When KO\'d in battle, revive with 2 HP on the next turn.',
    (CARD_AWAKENING_OF_TALENT,),
    'Sora_(Military)_(unit).png',
        )

CHARACTER_ARU_SCRAMBLE = OJCharacter(62,
    'Aru (Scramble)',
    5, -1, -1, 2, 5,
    ORIGIN_XMAS_SHOOTING_SCRAMBLE,
    'Can hold 4 cards.',
    (CARD_SANTAS_JOB,),
    'Aru_(Scramble)_(unit).png',
        )
        
CHARACTER_SUGURI_VER_2 = OJCharacter(63,
    'Suguri (Ver.2)',
    5, 1, -1, 2, 5,
    ORIGIN_ACCELERATION_OF_SUGURI_2,
    'Can hold 2 cards. Restore 1 HP at the start of every turn.',
    (CARD_REVIVAL_OF_STARS,),
    'Suguri_(Ver.2)_(unit).png',
        )
        
CHARACTER_MARC_PILOT = OJCharacter(64,
    'Marc (Pilot)',
    4, 1, 1, 1, 5,
    ORIGIN_FLYING_RED_BARREL,
    None,
    (CARD_BIG_ROCKET_CANNON, CARD_ROCKET_CANNON),
    'Marc_(Pilot)_(unit).png',
        )
        
CHARACTER_CHICKEN = OJCharacter(65,
    'Chicken',
    3, -1, -1, 1, 3,
    ORIGIN_QP_SHOOTING,
    'Lose 1/4 stars and given 1 WIn when KO\'d in battle.',
    (CARD_GOLDEN_EGG,),
    'Chicken_(unit).png',
        )
        
CHARACTER_ROBO_BALL = OJCharacter(66,
    'Robo Ball',
    3, -1, 1, -1, 4,
    ORIGIN_SUGURI,
    'Lose 1/4 stars and given 1 WIn when KO\'d in battle.',
    (CARD_REFLECTIVE_SHELL,),
    'Robo_Ball_(unit).png',
        )
        
CHARACTER_SEAGULL = OJCharacter(67,
    'SeaGull',
    3, -1, 1, -1, 4,
    ORIGIN_FLYING_RED_BARREL,
    'Lose 1/4 stars and given 1 WIn when KO\'d in battle.',
    (CARD_JONATHAN_RUSH,),
    'Seagull_(unit).png',
        )
        
CHARACTER_STORE_MANAGER = OJCharacter(68,
    'Store Manager',
    6, 2, 0, -1, 6,
    ORIGIN_QP_SHOOTING,
    'No stars from bonus panel. Can only use Gift type cards. Takes 1 damage on card discard.',
    (CARD_BANNER_FOR_LIFE,),
    'Store_Manager_(unit).png',
        )
        
CHARACTER_SHIFU_ROBOT = OJCharacter(69,
    'Shifu Robot',
    5, 1, 0, -1, 0,
    ORIGIN_SUGURI,
    'Starts and Revives with 1 HP Auto-repair (Recover 1 HP every 3 chapters or after being KO\'d.',
    (CARD_TURBO_CHARGED,),
    'Shifu_Robot_(unit).png',
        )

CHARACTER_FLYING_CASTLE = OJCharacter(70,
    'Flying Castle',
    8, 1, -1, -2, 6,
    ORIGIN_FLYING_RED_BARREL,
    'Immune to Battle Cards when defending Cannot Counterattack.',
    (CARD_IMMOVABLE_OBJECT,),
    'Flying_Castle_(unit).png',
        )


class CharacterDescription(object):
    __slots__ = ('title', 'description_parts', 'sub_parts')
    def __new__(cls, title):
        self = object.__new__(cls)
        self.title = title
        self.description_parts = None
        self.sub_parts = None
        return self
    
    def add_description_part(self, description_part):
        description_parts = self.description_parts
        if description_parts is None:
            description_parts = self.description_parts = []
        
        description_parts.append(description_part)
    
    def add_1st_tier_sub_part(self, title):
        sub_parts = self.sub_parts
        if sub_parts is None:
            sub_parts = self.sub_parts = []
        
        sub_part = CharacterDescription(title)
        sub_parts.append(sub_part)
        return sub_part
    
    def add_2nd_tier_sub_part(self, title):
        sub_parts = self.sub_parts
        if sub_parts is None:
            sub_parts = self.sub_parts = []
            sub_part = CharacterDescription(title)
            sub_parts.append(sub_part)
        else:
            sub_part = sub_parts[-1]
        
        return sub_part.add_1st_tier_sub_part(title)
    
    def add_3rd_tier_sub_part(self, title):
        sub_parts = self.sub_parts
        if sub_parts is None:
            sub_parts = self.sub_parts = []
            sub_part = CharacterDescription(title)
            sub_parts.append(sub_part)
        else:
            sub_part = sub_parts[-1]
        
        return sub_part.add_2nd_tier_sub_part(title)
    
    def get_bottom_part(self):
        sub_parts = self.sub_parts
        if sub_parts is None:
            return self
        
        return sub_parts[-1].get_bottom_part()
    
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__, ' title=', repr(self.title)]
        
        description_parts = self.description_parts
        if description_parts is not None:
            description_part_count = len(description_parts)
            repr_parts.append(', description_part_count=')
            repr_parts.append(repr(description_part_count))
            
            description_total_length = 0
            for description_part in description_parts:
                description_total_length += len(description_part)
            
            repr_parts.append(', description_total_length=')
            repr_parts.append(repr(description_total_length))
        
        sub_parts = self.sub_parts
        if sub_parts is not None:
            repr_parts.append('sub_parts=')
            repr_parts.append(repr(sub_parts))
        
        repr_parts.append('>')
        return ''.join(repr_parts)

def parse_character_page(character_name, response_data):
    soup = BeautifulSoup(response_data, 'html.parser')
    main_block = soup.find_all('div', class_='tabber')
    tabs = main_block.find_all('div', {'class': 'tabbertab'})
    
    character_description = CharacterDescription(character_name)
    
    for tab in tabs:
        title = tab.title
        character_description.add_1st_tier_sub_part(title)
        
        for element in main_block.contents:
            element_name = element.name
            if element_name is None:
                continue # linebreak
            
            if element_name == 'h2':
                title = element.text
                character_description.add_2nd_tier_sub_part(title)
                continue
            
            if element_name == 'h3':
                title =  element.text
                character_description.add_3rd_tier_sub_part(title)
                continue
            
            if element_name == 'p':
                description = element.text
                character_description.get_bottom_part().add_description_part(description)
                continue
            
            if element_name == 'dl':
                dl_parts = []
                for dl_element in element.contents:
                    dl_element_name = dl_element.name
                    if dl_element_name == 'dt':
                        part = dl_element.text
                        dl_parts.append(f'**{part}**')
                        continue
                    
                    if dl_element_name == 'dd':
                        part = dl_element.text
                        dl_parts.append(part)
                        continue
                
                description = '\n'.join(dl_parts)
                character_description.get_bottom_part().add_description_part(description)
                continue
    
    return CharacterDescription

























