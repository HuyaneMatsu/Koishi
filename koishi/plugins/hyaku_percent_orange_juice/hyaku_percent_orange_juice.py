__all__ = ()

from os.path import join as join_paths, exists
from re import compile as re_compile, I as re_ignore_case, escape as re_escape
from functools import partial as partial_func

from scarletio.web_common import quote
from scarletio import ReuAsyncIO
from hata import BUILTIN_EMOJIS, Embed, StringSelectOption, create_string_select
from hata.ext.slash import abort, InteractionResponse

from ...bot_utils.constants import GUILD__STORAGE, PATH__KOISHI
from ...bots import FEATURE_CLIENTS, MAIN_CLIENT


EMOJI_STAR = BUILTIN_EMOJIS['star']

ORIGINS = {}
EVENTS = {}
CHARACTERS = {}
CARD_PACKS = {}
CARDS = {}
CARD_COST_STRING_TO_ENTITY = {}


CARD_RARITY_NONE = 0
CARD_RARITY_COMMON = 1
CARD_RARITY_RARE = 2
CARD_RARITY_UNCOMMON = 3

CARD_RARITY_NAME_NONE = 'none'
CARD_RARITY_NAME_COMMON = 'common'
CARD_RARITY_NAME_RARE = 'rare'
CARD_RARITY_NAME_UNCOMMON = 'uncommon'

CARD_RARITY_VALUE_TO_NAME = {
    CARD_RARITY_NONE: CARD_RARITY_NAME_NONE,
    CARD_RARITY_COMMON: CARD_RARITY_NAME_COMMON,
    CARD_RARITY_RARE: CARD_RARITY_NAME_RARE,
    CARD_RARITY_UNCOMMON: CARD_RARITY_NAME_UNCOMMON,
}

CARD_RARITY_FILTERABLE_NAMES = [
    CARD_RARITY_NAME_COMMON,
    CARD_RARITY_NAME_RARE,
    CARD_RARITY_NAME_UNCOMMON,
]

CARD_RARITY_NAME_TO_VALUE = {value:key for key, value in CARD_RARITY_VALUE_TO_NAME.items()}

CARD_TYPE_BATTLE = 1 << 0
CARD_TYPE_BOOST = 1 << 1
CARD_TYPE_EVENT = 1 << 2
CARD_TYPE_GIFT = 1 << 3
CARD_TYPE_TRAP = 1 << 4
CARD_TYPE_HYPER = 1 << 7

CARD_TYPE_NAME_BATTLE = 'BATTLE'
CARD_TYPE_NAME_BOOST = 'BOOST'
CARD_TYPE_NAME_EVENT = 'EVENT'
CARD_TYPE_NAME_GIFT = 'GIFT'
CARD_TYPE_NAME_TRAP = 'TRAP'
CARD_TYPE_NAME_HYPER = 'HYPER'

CARD_TYPE_GENERIC_MASK_NAME_PAIRS = (
    (CARD_TYPE_BATTLE, CARD_TYPE_NAME_BATTLE),
    (CARD_TYPE_BOOST, CARD_TYPE_NAME_BOOST),
    (CARD_TYPE_EVENT ,CARD_TYPE_NAME_EVENT),
    (CARD_TYPE_GIFT, CARD_TYPE_NAME_GIFT),
    (CARD_TYPE_TRAP, CARD_TYPE_NAME_TRAP),
)

CARD_TYPE_NAME_TO_MASK = {
    CARD_TYPE_NAME_BATTLE: CARD_TYPE_BATTLE,
    CARD_TYPE_NAME_BOOST: CARD_TYPE_BOOST,
    CARD_TYPE_NAME_EVENT: CARD_TYPE_EVENT,
    CARD_TYPE_NAME_GIFT: CARD_TYPE_GIFT,
    CARD_TYPE_NAME_TRAP: CARD_TYPE_TRAP,
    CARD_TYPE_NAME_HYPER: CARD_TYPE_HYPER,
}

CARD_TYPE_FILTERABLE_NAMES = [
    CARD_TYPE_NAME_BATTLE,
    CARD_TYPE_NAME_BOOST,
    CARD_TYPE_NAME_EVENT,
    CARD_TYPE_NAME_GIFT,
    CARD_TYPE_NAME_TRAP,
]

CARD_COST_TYPE_STATIC = 0
CARD_COST_TYPE_DIV_STARS = 1
CARD_COST_TYPE_MUL_LEVEL = 2
CARD_COST_TYPE_MUL_CARDS = 3
CARD_COST_TYPE_MUL_OTHERS_CARDS = 4
CARD_COST_TYPE_ALL_STARS = 5
CARD_COST_TYPE_MUL_X = 6

CARD_LEVEL_FILTERABLE_STRINGS = ['0', '1', '2', '3', '4', '5']
CARD_LIMIT_FILTERABLE_STRINGS = ['1', '3']

class OJCardCost:
    __slots__ = ('type', 'factor', 'string')
    def __new__(cls, type_, factor):
        
        if type_ == CARD_COST_TYPE_STATIC:
            string = f'{factor} {EMOJI_STAR}'
        elif type_ == CARD_COST_TYPE_DIV_STARS:
            string = f'stars / {factor} {EMOJI_STAR}'
        elif type_ == CARD_COST_TYPE_MUL_LEVEL:
            string = f'level x {factor} {EMOJI_STAR}'
        elif type_ == CARD_COST_TYPE_MUL_CARDS:
            string = f'cards held x {factor} {EMOJI_STAR}'
        elif type_ == CARD_COST_TYPE_MUL_OTHERS_CARDS:
            string = f'cards held by others x {factor} {EMOJI_STAR}'
        elif type_ == CARD_COST_TYPE_ALL_STARS:
            string = f'all held {EMOJI_STAR}'
        elif type_ == CARD_COST_TYPE_MUL_X:
            string = f'(X) x {factor} {EMOJI_STAR}'
        else:
            string = 'undefined'
        
        self = object.__new__(cls)
        self.type = type_
        self.factor = factor
        self.string = string
        
        CARD_COST_STRING_TO_ENTITY[string] = self
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


class OJEntitySorter:
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

class OJEntityBase:
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
        return f'<{self.__class__.__name__} id = {self.id}, name = {self.name!r}>'


class OJOrigin(OJEntityBase):
    __slots__ = ()
    def __new__(cls, identifier, name):
        self = object.__new__(cls)
        self.id = identifier
        self.name = name
        
        ORIGINS[identifier] = self
        return self

class OJEvent(OJEntityBase):
    __slots__ = ()
    
    def __new__(cls, identifier, name):
        self = object.__new__(cls)
        self.id = identifier
        self.name = name
        
        EVENTS[identifier] = self
        return self


class OJCharacter(OJEntityBase):
    __slots__ = (
        'description', 'hyper_cards', 'origin', 'attack', 'defense', 'evasion', 'recovery', 'hp', 'card_name'
    )
    
    def __new__(
        cls,
        identifier,
        name,
        hp,
        attack,
        defense,
        evasion,
        recovery,
        origin,
        description,
        hyper_cards,
        card_name = None,
    ):
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
        self.hyper_cards = hyper_cards
        self.card_name = card_name
        CHARACTERS[identifier] = self
        
        return self
    
    
    @property
    def url(self):
        return f'https://100orangejuice.fandom.com/wiki/{quote(self.name)}'


def match_attack(value, character):
    return value == character.attack
    
def match_defense(value, character):
    return value == character.defense

def match_evasion(value, character):
    return value == character.evasion

def match_recovery(value, character):
    return value == character.recovery

def match_hp(value, character):
    return value == character.hp


def get_character_filter_keys(attack, defense, evasion, recovery, hp):
    filters = []
    
    if (attack is not None):
        filters.append(partial_func(match_attack, attack))
    
    if (defense is not None):
        filters.append(partial_func(match_defense, defense))
    
    if (evasion is not None):
        filters.append(partial_func(match_evasion, evasion))
    
    if (recovery is not None):
        filters.append(partial_func(match_recovery, recovery))
    
    if (hp is not None):
        filters.append(partial_func(match_hp, hp))
    
    return filters

def apply_filters(character, filters):
    for filter in filters:
        if not filter(character):
            return False
    
    return True

def create_string_filter_options(values):
    return [(f'+{value}' if (value > 0) else str(value)) for value in sorted(values, reverse = True)]

def create_character_filter_options():
    attack_values = set()
    defense_values = set()
    evasion_values = set()
    recovery_values = set()
    hp_values = set()
    
    for character in CHARACTERS.values():
        attack_values.add(character.attack)
        defense_values.add(character.defense)
        evasion_values.add(character.evasion)
        recovery_values.add(character.recovery)
        hp_values.add(character.hp)
    
    return (
        create_string_filter_options(attack_values),
        create_string_filter_options(defense_values),
        create_string_filter_options(evasion_values),
        create_string_filter_options(recovery_values),
        create_string_filter_options(hp_values),
    )


class OJCardPack(OJEntityBase):
    __slots__ = ('cost', )
    def __new__(cls, identifier, name, cost):
        self = object.__new__(cls)
        self.id = identifier
        self.name = name
        self.cost = cost
        
        CARD_PACKS[identifier] = self
        return self

class OJCard(OJEntityBase):
    __slots__ = ('cost', 'description', 'level', 'type', 'events', 'quote', 'limit', 'card_name', 'pack', 'rarity')
    def __new__(
        cls, identifier, name, level, cost, limit, type_, pack, rarity, description, quote, events, card_name
    ):
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
        self.pack = pack
        self.rarity = rarity
        CARDS[identifier] = self
        return self
    
    @property
    def url(self):
        return f'https://100orangejuice.fandom.com/wiki/{quote(self.name)}'
    
    @property
    def type_string(self):
        string_parts = []
        type_ = self.type
        
        is_hyper = type_ & CARD_TYPE_HYPER
        if is_hyper:
            string_parts.append(CARD_TYPE_NAME_HYPER)
            string_parts.append('(')
        
        field_added = False
        
        for mask, name in CARD_TYPE_GENERIC_MASK_NAME_PAIRS:
            if type_ & mask:
                if field_added:
                    string_parts.append('/')
                else:
                    field_added = True
                
                string_parts.append(name)
        
        if is_hyper:
            string_parts.append(')')
        
        return ''.join(string_parts)


def match_level(value, card):
    return value == card.level
    
def match_cost(value, card):
    cost = card.cost
    if cost.type != value.type:
        return False
    
    if cost.factor != value.factor:
        return False
    
    return True

def match_limit(value, card):
    return value == card.limit

def match_type(value, card):
    return value & card.type

def match_pack(value, card):
    return value is card.pack

def match_rarity(value, card):
    return value == card.rarity

def get_card_filter_keys(level, cost, limit, type_, pack, rarity):
    filters = []
    
    if (level is not None):
        filters.append(partial_func(match_level, level))
    
    if (cost is not None):
        try:
            cost_entity = CARD_COST_STRING_TO_ENTITY[cost]
        except KeyError:
            pass
        else:
            filters.append(partial_func(match_cost, cost_entity))
    
    if (limit is not None):
        filters.append(partial_func(match_limit, limit))
    
    if (type_ is not None):
        try:
            type_mask = CARD_TYPE_NAME_TO_MASK[type_]
        except KeyError:
            pass
        else:
            filters.append(partial_func(match_type, type_mask))
    
    if (pack is not None):
        try:
            pack_entity = CARD_PACK_BY_NAME[pack]
        except KeyError:
            pass
        else:
            filters.append(partial_func(match_pack, pack_entity))
    
    if (rarity is not None):
        try:
            rarity_value = CARD_RARITY_NAME_TO_VALUE[rarity]
        except KeyError:
            pass
        else:
            filters.append(partial_func(match_rarity, rarity_value))
    
    return filters


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

CARD_PACK_ACCELERATION_PACK = OJCardPack(
    1,
    'Acceleration Pack',
    320,
)

CARD_PACK_EXPANSION_PACK = OJCardPack(
    2,
    'Expansion Pack',
    240,
)

CARD_PACK_COMMUNITY_PACK_1 = OJCardPack(
    3,
    'Community Pack 1',
    580,
)

CARD_PACK_COMMUNITY_PACK_2 = OJCardPack(
    4,
    'Community Pack 2',
    580,
)

CARD_PACK_BASE_PACK = OJCardPack(5,
    'Base Pack',
    180,
)

CARD_PACK_PUDDING_PACK = OJCardPack(
    6,
    'Pudding Pack',
    320,
)

CARD_PACK_MIXED_BOOSTER_PACK = OJCardPack(
    7,
    'Mixed Booster Pack',
    280,
)

CARD_PACK_COMMUNITY_PACK_3 = OJCardPack(
    8,
    'Community Pack 3',
    580,
)

CARD_PACK_COMMUNITY_PACK_4 = OJCardPack(
    9,
    'Community Pack 4',
    1080,
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

CARD_COST_Lvx2 = OJCardCost(CARD_COST_TYPE_MUL_LEVEL, 2)
CARD_COST_Lvx3 = OJCardCost(CARD_COST_TYPE_MUL_LEVEL, 3)
CARD_COST_Lvx5 = OJCardCost(CARD_COST_TYPE_MUL_LEVEL, 5)
CARD_COST_Lvx7 = OJCardCost(CARD_COST_TYPE_MUL_LEVEL, 7)
CARD_COST_Lvx10 = OJCardCost(CARD_COST_TYPE_MUL_LEVEL, 10)

CARD_COST_HCx5 = OJCardCost(CARD_COST_TYPE_MUL_CARDS, 5)
CARD_COST_OCx5 = OJCardCost(CARD_COST_TYPE_MUL_OTHERS_CARDS, 5)

CARD_COST_StALL = OJCardCost(CARD_COST_TYPE_ALL_STARS, 0)

CARD_COST_Xx10 = OJCardCost(CARD_COST_TYPE_MUL_X, 10)

#### #### #### #### EVENTS #### #### #### ####

EVENT_CHOCOLATE_FOR_THE_SWEET_GODS = OJEvent(
    1,
    'Chocolate for the Sweet Gods',
)

EVENT_CHOCOLATE_FOR_THE_SWEET_GODS_RERUN = OJEvent(
    2,
    'Rerun',
)

EVENT_SANTA_SCRAMBLE = OJEvent(
    3,
    'Santa Scramble',
)

EVENT_SHROOM_ZOOM = OJEvent(
    4,
    'Shroom Zoom',
)

EVENT_BEACH_PARTY = OJEvent(
    5,
    'Beach Party',
)

EVENT_EVENT_SANTA_SCRAMBLE_RERUN = OJEvent(
    6,
    'Rerun',
)

#### #### #### #### NORMAL CARDS #### #### #### ####

CARD_ACCEL_HYPER = OJCard(1,
    'Accel Hyper',
    4, CARD_COST_30, 1, CARD_TYPE_BATTLE, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_RARE,
    'Roll double dice for attack.',
    '"Unlimited Charge!" —Sora',
    None,
    'Accel_Hyper',
)

CARD_BIG_MAGNUM = OJCard(2,
    'Big Magnum',
    3, CARD_COST_20, 3, CARD_TYPE_BATTLE, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Pay 1 HP when you use this card. During this battle, gain 2 ATK. If you would suffer KO from using this card, '
    'the card cannot be used.',
    '"Go! Big Magnum!" —Captain Tequila',
    None,
    'Big_Magnum',
)

CARD_DARK_SIDE_OF_BUSINESS = OJCard(3,
    'Dark Side of Business',
    2, CARD_COST_10, 3, CARD_TYPE_BATTLE, CARD_PACK_COMMUNITY_PACK_1, CARD_RARITY_UNCOMMON,
    'Gain +2 ATK, enemy gains -2 DEF. For every point of damage you would deal, steal 5 stars from your opponent '
    'instead.',
    '"Go! Big Magnum!" —Captain Tequila',
    None,
    'Dark_Side_of_Business',
)

CARD_DESPERATE_MODIFICATION = OJCard(4,
    'Desperate Modification',
    2, CARD_COST_10, 3, CARD_TYPE_BATTLE, CARD_PACK_COMMUNITY_PACK_2, CARD_RARITY_COMMON,
    'For this battle, randomly roll either a natural 1 or 6 for each attack, defense and evasion.',
    '"Poor Blue Crow. You loaded him with all that heavy stuff!" —Marc',
    None,
    'Desperate_Modification',
)

CARD_EXTENSION = OJCard(5,
    'Extension',
    4, CARD_COST_10, 3, CARD_TYPE_BATTLE, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_UNCOMMON,
    'Gain the effect of one randomly chosen Battle card (including Hyper cards).',
    '"It\'s my job to kill you." —Nath',
    None,
    'Extension',
)

CARD_FINAL_BATTLE = OJCard(6,
    'Final Battle',
    4, CARD_COST_30, 1, CARD_TYPE_BATTLE, CARD_PACK_BASE_PACK, CARD_RARITY_RARE,
    'This battle will last until either unit suffers KO (Maximum of 10 rounds).',
    '"To protect everyone!" —Suguri & Hime',
    None,
    'Final_Battle',
)

CARD_IM_ON_FIRE = OJCard(7,
    'I\'m on Fire!',
    1, CARD_COST_5, 3, CARD_TYPE_BATTLE, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'During this battle, gain +1 ATK and -1 DEF.',
    '"Let\'s play our lives away!" —Kae',
    None,
    'I\'m_on_Fire!',
)

CARD_PORTABLE_PUDDING = OJCard(
    8,
    'Portable Pudding',
    2,
    CARD_COST_20,
    1,
    CARD_TYPE_BATTLE,
    CARD_PACK_PUDDING_PACK,
    CARD_RARITY_UNCOMMON,
    'At the start of this battle, reset your HP to your max HP.',
    '"I\'ve got pudding for lunch today!" ―QP',
    None,
    'Portable_Pudding',
)

CARD_QUICK_RESTORATION = OJCard(9,
    'Quick Restoration',
    2, CARD_COST_10, 3, CARD_TYPE_BATTLE, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_COMMON,
    'All damage taken during the battle will be healed after the battle. Effect is cancelled if the player is KO\'d',
    '"I\'m not going to die." —Suguri',
    None,
    'Quick_Restoration',
)

CARD_RAINBOW_COLORED_CIRCLE = OJCard(10,
    'Rainbow-Colored Circle',
    2, CARD_COST_5, 3, CARD_TYPE_BATTLE, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'During this battle, gain +2 EVD and -1 DEF.',
    '"Like drawing a rainbow-colored circle."',
    None,
    'Rainbow-Colored_Circle',
)

CARD_RBITS = OJCard(11,
    'Rbits',
    2, CARD_COST_3, 3, CARD_TYPE_BATTLE, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'During this battle, gain +2 DEF. You may not use the Evade command.',
    '"Formation Orbit!" —QP',
    None,
    'Rbits',
)

CARD_REVERSE_ATTRIBUTE_FIELDS = OJCard(12,
    'Reverse Attribute Field',
    3, CARD_COST_10, 1, CARD_TYPE_BATTLE, CARD_PACK_EXPANSION_PACK, CARD_RARITY_RARE,
    'During this battle, the positive and negative values of each ability of both units are inverted after adjustment.',
    '"Aren\'t you too serious about this game? You\'re so da... I mean, far too immature!" —Mei',
    None,
    'Reverse_Attribute_Field',
)

CARD_SERIOUS_BATTLE = OJCard(13,
    'Serious Battle',
    3, CARD_COST_0, 3, CARD_TYPE_BATTLE, CARD_PACK_PUDDING_PACK, CARD_RARITY_COMMON,
    'During this battle, ATK, DEF and EVD of both units will be 0.',
    '"This battle will be a true test of strength!" ―Tomomo',
    None,
    'Serious_Battle',
)

CARD_SHIELD = OJCard(14,
    'Shield',
    3, CARD_COST_5, 3, CARD_TYPE_BATTLE, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Gain +3 DEF during this battle. However, you may not attack. This card can only be used by the player who attacks '
    'second.',
    '"The most important thing is: make it back here alive." —Sham',
    None,
    'Shield',
)

CARD_SHIELD_COUNTER = OJCard(
    15,
    'Shield Counter',
    4,
    CARD_COST_20,
    1,
    CARD_TYPE_BATTLE,
    CARD_PACK_MIXED_BOOSTER_PACK,
    CARD_RARITY_UNCOMMON,
    (
        'Deal damage to attacker equal to their ATK - DEF (min. 1). Then end the battle. '
        'A KO from this damage does not count as a defeat. May only be used by the defender.'
    ),
    '"Shield, invert!" —Sora',
    None,
    'Shield_Counter',
)

CARD_SINK_OR_SWIM = OJCard(16,
    'Sink or Swim',
    4, CARD_COST_10, 3, CARD_TYPE_BATTLE, CARD_PACK_PUDDING_PACK, CARD_RARITY_RARE,
    'Gain -1 ATK, -1 DEF and -1 EVD. If you win this battle, take 50% more of your opponent\'s stars.',
    '"Alright, it\'s time to play the long odds!" ―Yuki',
    None,
    'Sink_or_Swim',
)

CARD_TACTICAL_RETREAT = OJCard(17,
    'Tactical Retreat',
    1, CARD_COST_Lvx5, 3, CARD_TYPE_BATTLE, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_COMMON,
    'End this battle. Attacker gains this card\'s cost. May only be used by the defender. If opponent plays a battle '
    'card, this effect is void.',
    '"Farewell!" —Tomato',
    None,
    'Tactical_Retreat',
)

CARD_AMBUSH = OJCard(
    18,
    'Ambush',
    3,
    CARD_COST_20,
    3,
    CARD_TYPE_BOOST,
    CARD_PACK_MIXED_BOOSTER_PACK,
    CARD_RARITY_COMMON,
    'Engage in battle with an enemy or enemies on your panel. Once these battles are over, your turn is over.',
    '"Owwwww!" —Sham',
    None,
    'Ambush',
)

CARD_BACKDOOR_TRADE = OJCard(19,
    'Backdoor Trade',
    1, CARD_COST_Lvx5, 1, CARD_TYPE_BOOST, CARD_PACK_PUDDING_PACK, CARD_RARITY_UNCOMMON,
    'Perform a Norma check, then your turn ends. Can only be used by the player with the lowest level. Cannot be used '
    'at Norma level 5.',
    '"Here\'s what you asked for." ―Captain Tequila\n'
    '"Great work! I knew I could count on a real villain like you!" ―Mimyuu',
    None,
    'Backdoor_Trade',
)

CARD_COMPLETION_REWARD = OJCard(20,
    'Completion Reward',
    1, CARD_COST_0, 1, CARD_TYPE_BOOST, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_COMMON,
    'Gain 7 stars for every trap you have set and someone has stepped on.',
    '"Yay, I\'ve got my pay!" —Chris\n'
    '"Don\'t waste it, okay?" —Manager',
    None,
    'Completion_Reward',
)

CARD_DASH = OJCard(21,
    'Dash!',
    1, CARD_COST_3, 3, CARD_TYPE_BOOST, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'For this turn, roll two dice for movement.',
    '"Faster!" —Suguri',
    None,
    'Dash!',
    
)

CARD_EXTEND = OJCard(22,
    'Extend',
    3, CARD_COST_10, 1, CARD_TYPE_BOOST, CARD_PACK_EXPANSION_PACK, CARD_RARITY_RARE,
    'Stock Effect After suffering KO, you will revive on the following turn.',
    '"All good for now!" —Marc',
    None,
    'Extend',
)

CARD_FLIP_OUT = OJCard(23,
    'Flip Out',
    1, CARD_COST_0, 3, CARD_TYPE_BOOST, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'Stock Effect Next time you land on a drop panel, the player(s) with the highest number of stars will lose the '
    'same number of stars as you.',
    '"......!" —Mei',
    None,
    'Flip_Out',
)

CARD_GENTLEMANS_BATTLE = OJCard(24,
    'Gentleman\'s Battle',
    3, CARD_COST_10, 3, CARD_TYPE_BOOST, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_COMMON,
    'Choose a player with full HP and battle them. Your turn ends after the battle.',
    '"Take this!" —Guildmaster',
    None,
    'Gentleman\'s_Battle',
)

CARD_LONELY_CHARIOT = OJCard(25,
    'Lonely Chariot',
    3, CARD_COST_30, 3, CARD_TYPE_BOOST, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_COMMON,
    'Stock Effect Always roll 5 to move. After your turn, take 1 damage. Effect expires on KO. If you suffer KO from '
    'this effect, pay Lvl x5 stars.',
    '"You guys? You\'re mistaken...\n'
    'I ride alone!" —Lone Rider',
    None,
    'Lonely_Chariot',
)

CARD_LONG_DISTANCE_SHOT = OJCard(26,
    'Long-Distance Shot',
    1 , CARD_COST_5, 3, CARD_TYPE_BOOST, CARD_PACK_EXPANSION_PACK, CARD_RARITY_COMMON,
    'Deals 1 damage to the selected enemy unit.',
    '"I can hit you from anywhere." —Iru',
    None,
    'Long-Distance_Shot',
)

CARD_MIMIC = OJCard(27,
    'Mimic',
    3, CARD_COST_5, 3, CARD_TYPE_BOOST, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_RARE,
    'Choose a player. All hyper cards in your hand become the type that that player uses.',
    'Marie Poppo is trying to become something else.',
    None,
    'Mimic',
)

CARD_NICE_JINGLE = OJCard(28,
    'Nice Jingle',
    1, CARD_COST_0, 1, CARD_TYPE_BOOST, CARD_PACK_BASE_PACK, CARD_RARITY_UNCOMMON,
    'Stock Effect. The next bonus panel gives you twice as many stars.',
    '"We\'ve got a bunch." —Aru',
    None,
    'Nice_Jingle',
)

CARD_NICE_PRESENT = OJCard(29,
    'Nice Present',
    2, CARD_COST_10, 1, CARD_TYPE_BOOST, CARD_PACK_BASE_PACK, CARD_RARITY_UNCOMMON,
    'Draw 2 cards.',
    '"You\'re going to help me deliver the presents." —Aru',
    None,
    'Nice_Present',
)

CARD_PASSIONATE_RESEARCH = OJCard(30,
    'Passionate Research',
    2, CARD_COST_5, 1, CARD_TYPE_BOOST, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_UNCOMMON,
    'Look at the first 3 cards of the deck. If there are any hyper cards, take them. Return the rest of the cards to '
    'the deck in the same order.',
    '"Well, this sort of thing happens all the time. It was quite fun, anyway!" —Scholar',
    None,
    'Passionate_Research',
)

CARD_PATH_BLOCKERS = OJCard(31,
    'Path Blockers',
    1, CARD_COST_13, 3, CARD_TYPE_BOOST, CARD_PACK_COMMUNITY_PACK_2, CARD_RARITY_COMMON,
    (
        'Stock Effect (1). Choose an active unit. '
        'If that unit moves onto a panel with a set Trap, they must stop on that panel.'
    ),
    '"Nobody will get past Waruda!" —Tomato',
    None,
    'Path_Blockers',
)

CARD_PRESIDENTS_PRIVILEGE = OJCard(32,
    'President\'s Privilege',
    4, CARD_COST_10, 3, CARD_TYPE_BOOST, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_COMMON,
    'Effect Duration: 1 chapter You may play cards without paying their cost. You may play 1 additional card this '
    'turn.',
    '"There you guys are... Come to the Student Council Office after school, will you?" —Himeji',
    None,
    'President\'s_Privilege',
)

CARD_PRINCESS_PRIVILEGE = OJCard(33,
    'Princess\'s Privilege',
    4, CARD_COST_20, 1, CARD_TYPE_BOOST, CARD_PACK_EXPANSION_PACK, CARD_RARITY_RARE,
    (
        'Discard all cards in your hand and draw 3 cards.\n'
        'Can only be used when holding only Princess\'s Privilege or you have at least 3 cards in your hand.'
    ),
    '"You may come and visit my house some day." —Fernet',
    None,
    'Princess\'s_Privilege',
)

CARD_PUDDING = OJCard(34,
    'Pudding',
    4, CARD_COST_0, 3, CARD_TYPE_BOOST, CARD_PACK_BASE_PACK, CARD_RARITY_RARE,
    'Fully restore HP.',
    '"Hooray!" —QP',
    None,
    'Pudding',
)

CARD_SAKIS_COOKIE = OJCard(35,
    'Saki\'s Cookie',
    1, CARD_COST_0, 3, CARD_TYPE_BOOST, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'Heals 1 HP.',
    '"Have a cookie!" —Saki',
    None,
    'Saki\'s_Cookie'
)

CARD_STIFF_CRYSTAL = OJCard(36,
    'Stiff Crystal',
    2, CARD_COST_20, 1, CARD_TYPE_BOOST, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Stock Effect This card negates the effect of a trap card. Gain 5 stars per level of cancelled trap.',
    '"Such a pain in the neck." —Kyoko',
    None,
    'Stiff_Crystal',
)

CARD_SWEET_DESTROYER = OJCard(
    37,
    'Sweet Destroyer',
    3,
    CARD_COST_20,
    1,
    CARD_TYPE_EVENT,
    CARD_PACK_PUDDING_PACK,
    CARD_RARITY_RARE,
    (
        'Steal a random "pudding" card from each other player. You may play another card this turn. '
        'For 3 chapters, all non-Hyper Sweets type cards drawn are permanently transformed '
        'at random into Dangerous Pudding or Bad Pudding.'
    ),
    '"The sweets that bring harm to the world... I will destroy them all!" ―Sweet Breaker',
    None,
    'Sweet_Destroyer',
)

CARD_TREASURE_THIEF = OJCard(38,
    'Treasure Thief',
    2, CARD_COST_10, 3, CARD_TYPE_BOOST, CARD_PACK_COMMUNITY_PACK_1, CARD_RARITY_COMMON,
    'Steal a random card from all players on the same tile as you.',
    '"Pokya Po! (Treasure, get!)" ―Marie Poppo',
    None,
    'Treasure_Thief',
)

CARD_ACCELERATING_SKY = OJCard(39,
    'Accelerating Sky',
    3, CARD_COST_20, 3, CARD_TYPE_EVENT, CARD_PACK_COMMUNITY_PACK_2, CARD_RARITY_UNCOMMON,
    'Effect Duration: 3 chapters. All players gain +1 EVD and -1 DEF.',
    '"Girls are leaping through the sky...?"',
    None,
    'Accelerating_Sky',
)

CARD_CLOUD_OF_SEAGULL = OJCard(40,
    ' Cloud of Seagulls',
    1, CARD_COST_0, 3, CARD_TYPE_EVENT, CARD_PACK_EXPANSION_PACK, CARD_RARITY_COMMON,
    'A randomly chosen unit will receive 2 damage.',
    '"Squaawk!" —Seagull',
    None,
    'Cloud_of_Seagulls',
)

CARD_DINNER = OJCard(41,
    'Dinner',
    3, CARD_COST_10, 3, CARD_TYPE_EVENT, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Heals all units for 3 HP.',
    '"Let\'s have supper together." —Natsumi',
    None,
    'Dinner',
)

CARD_FORCED_REVIVAL = OJCard(42,
    'Forced Revival',
    3, CARD_COST_30, 3, CARD_TYPE_EVENT, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'All units suffering KO are revived with 1 HP.',
    '"You\'ll all be up in a jiffy." —Kiriko',
    None,
    'Forced_Revival',
)

CARD_GIFT_EXCHANGE = OJCard(43,
    'Gift Exchange',
    3, CARD_COST_10, 3, CARD_TYPE_EVENT, CARD_PACK_BASE_PACK, CARD_RARITY_UNCOMMON,
    'All cards are gathered from the players and dealt back randomly. The total number of each player\'s card remains '
    'unchanged.',
    '"A gift exchange? Let\'s do it!" —Rbit, Red, and Blue',
    None,
    'Gift_Exchange',
)

CARD_HERE_AND_THERE = OJCard(
    44,
    'Here and There',
    2,
    CARD_COST_10,
    3,
    CARD_TYPE_EVENT,
    CARD_PACK_BASE_PACK,
    CARD_RARITY_COMMON,
    'All units are moved to randomly chosen panels.',
    '"To the next world!" —Marie Poppo',
    None,
    'Here_and_There',
)

CARD_HOLY_NIGHT = OJCard(45,
    'Holy Night',
    1, CARD_COST_0, 1, CARD_TYPE_EVENT, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'Permanent Effect. Start-of-chapter bonus stars are increased by one.',
    '"Aha, that\'s why it\'s a party night." —Hime',
    None,
    'Holy_Night',
)

CARD_INDISCRIMINATE_FIRE_SUPPORT = OJCard(46,
    'Indiscriminate Fire Support',
    2, CARD_COST_10, 3, CARD_TYPE_EVENT, CARD_PACK_PUDDING_PACK, CARD_RARITY_RARE,
    'Effect Duration: Infinite. A random unit takes 1 damage. At the start of your turn, repeat this effect. The '
    'effect ends when a unit suffers KO.',
    '"......" ―Sora',
    None,
    'Indiscriminate_Fire_Support',
)

CARD_LITTLE_WAR = OJCard(47,
    'Little War',
    4, CARD_COST_50, 1, CARD_TYPE_EVENT, CARD_PACK_BASE_PACK, CARD_RARITY_RARE,
    'Effect Duration: 3 chapters Offense and defense will happen twice in all battles.',
    '"I believe... I have the power to stop this..." —Suguri',
    None,
    'Little_War',
)

CARD_MIX_PHENOMENON = OJCard(48,
    'Mix Phenomenon',
    2, CARD_COST_10, 1, CARD_TYPE_EVENT, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_RARE,
    'Effect Duration: 3 chapters All panels other than the home panels become random panels.',
    '"A hole in a wall-like force between dimensions...It would appear that this phenomenon is mixing the worlds '
    'themselves together." —Yukito',
    None,
    'Mix_Phenomenon',
)

CARD_OH_MY_FRIEND = OJCard(49,
    'Oh My Friend',
    1, CARD_COST_30, 1, CARD_TYPE_EVENT, CARD_PACK_EXPANSION_PACK, CARD_RARITY_RARE,
    'A boss will show up.',
    '"Machines have friends too." —NoName',
    None,
    'Oh_My_Friend',
)

CARD_OUT_OF_AMMO = OJCard(50,
    'Out of Ammo',
    2, CARD_COST_5, 3, CARD_TYPE_EVENT, CARD_PACK_BASE_PACK, CARD_RARITY_UNCOMMON,
    'Effect Duration: 1 chapter No player may use any cards.',
    '"Ran out of ammo!" —Peat',
    None,
    'Out_of_Ammo',
)

CARD_PARTY_TIME = OJCard(51,
    'Party Time',
    3, CARD_COST_20, 3, CARD_TYPE_EVENT, CARD_PACK_COMMUNITY_PACK_1, CARD_RARITY_COMMON,
    'All units are randomly warped onto the same panel. End your turn.',
    '"At tonight\'s banquet, the Beasts of Darkness shall dance wildly." ―Krilalaris',
    None,
    'Party_Time',
)

CARD_PLAY_OF_GODS = OJCard(52,
    'Play of the Gods',
    1, CARD_COST_10, 1, CARD_TYPE_EVENT, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_RARE,
    'Play one random event card (including Hyper cards) from any player\'s hand or the deck, at no additional cost',
    '"We will get golden eggs!" —QP\n'
    '"And make the best pudding out of them!" —Saki',
    None,
    'Play_of_the_Gods',
)

CARD_SCARY_SOLICITATION = OJCard(53,
    'Scary Solicitation',
    3, CARD_COST_30, 1, CARD_TYPE_EVENT, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_UNCOMMON,
    'All players except the one who played this card must draw cards, paying 15 stars per card, up to their card '
    'maximum.',
    '"You\'ll buy it, of course. You\'ll buy it, won\'t you?" —Merchant',
    None,
    'Scary_Solicitation',
)

CARD_SCRAMBLE_EVE = OJCard(54,
    'Scrambled Eve',
    3, CARD_COST_5, 1, CARD_TYPE_EVENT, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_UNCOMMON,
    'All players return their hand to the deck, and the deck is shuffled. Players gain 5 stars for each returned card.',
    '"Wait! Give me back the presents!" —Aru',
    None,
    'Scrambled_Eve',
)

CARD_SEALED_GUARDIAN = OJCard(55,
    'Sealed Guardian',
    5, CARD_COST_50, 1, CARD_TYPE_EVENT, CARD_PACK_EXPANSION_PACK, CARD_RARITY_RARE,
    'Every unit\'s HP becomes 1.',
    '"Meet the guardian angel of this vessel." —Shifu',
    None,
    'Sealed_Guardian',
)

CARD_SERENE_HUSH = OJCard(56,
    'Serene Hush',
    2, CARD_COST_10, 1, CARD_TYPE_EVENT, CARD_PACK_PUDDING_PACK, CARD_RARITY_COMMON,
    'Effect Duration: 1 Chapter. No battles can take place.',
    '"We have nothing to do..." ―Sumika\n'
    '"Let\'s enjoy the peace and quiet." ―Suguri',
    None,
    'Serene_Hush',
)

CARD_STAR_BLASTING_LIGHT = OJCard(57,
    'Star-Blasting Light',
    4, CARD_COST_50, 1, CARD_TYPE_EVENT, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_RARE,
    'All trap cards on the field are discarded. Trap setters take 1 damage for each discarded trap.',
    '"A light capable of burning down the city... even the planet... I can tell its source is up there in the sky." '
    '—Sora',
    None,
    'Star-Blasting_Light',
)

CARD_SUPER_ALL_OUT_MODE = OJCard(58,
    'Super All-Out Mode',
    3, CARD_COST_30, 3, CARD_TYPE_EVENT, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Stock Effect All units gain +2 ATK during their next battle.',
    '"This is gonna hurt even if you know it\'s coming!!" —Tomomo',
    None,
    'Super_All-Out_Mode',
)

CARD_UNPAID_WORK = OJCard(59,
    'Unpaid Work',
    2, CARD_COST_0, 1, CARD_TYPE_EVENT, CARD_PACK_PUDDING_PACK, CARD_RARITY_COMMON,
    'Effect Duration: 1 Chapter. No units will gain stars from any sources.',
    '"Where\'s my payment!" ―Chris',
    None,
    'Unpaid_Work',
)

CARD_WE_ARE_WARUDA = OJCard(60,
    'We Are Waruda',
    2, CARD_COST_5, 3, CARD_TYPE_EVENT, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Move all trap cards onto randomly chosen panels.',
    '"Useless. No one can beat Tomato." —Tomato',
    None,
    'We_Are_Waruda',
)

CARD_BLOODLUST = OJCard(61,
    'Bloodlust',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, CARD_PACK_COMMUNITY_PACK_2, CARD_RARITY_RARE,
    'Lose 1 HP at the start of your turn. Heal 1 HP for every damage you deal. Cannot Norma while holding this card. '
    'This card is discarded upon KO or use.',
    '"The true power of my beast... I wonder if it\'s like this." —Krilalaris',
    None,
    'Bloodlust',
)

CARD_LOST_CHILD = OJCard(62,
    'Lost Child',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, CARD_PACK_COMMUNITY_PACK_1, CARD_RARITY_COMMON,
    'Move backwards while this card is held. Cannot Norma while holding this card. This card is discarded upon KO or '
    'use.',
    '"Where am I?" ―Tsih',
    None,
    'Lost_Child',
)

CARD_LUCKY_CHARM = OJCard(63,
    'Lucky Charm',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, CARD_PACK_PUDDING_PACK, CARD_RARITY_UNCOMMON,
    'Gain Lvl x1 stars at the start of your turn. You cannot use any other cards. This card is discarded upon use. On '
    'defeat, give Lvl x 3 more stars.',
    '"Woo-hoo, so many stars! Today\'s my day!!" ―Tomomo',
    None,
    'Lucky_Charm',
)

CARD_METALLIC_MONOCOQUE = OJCard(64,
    'Metallic Monocoque',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, CARD_PACK_PUDDING_PACK, CARD_RARITY_COMMON,
    'When a non-battle effect deals any damage to you, that damage is reduced by 1, and you lose Lvl x 2 stars.',
    '"What a timid generation we live in." ―Sherry',
    None,
    'Metallic_Monocoque',
)

CARD_POPPO_THE_SNATCHER = OJCard(
    65,
    'Poppo the Snatcher',
    1,
    CARD_COST_0,
    1,
    CARD_TYPE_GIFT,
    CARD_PACK_COMMUNITY_PACK_2,
    CARD_RARITY_UNCOMMON,
    (
        'Gain -1 DEF. Whenever passing an enemy on your turn, steal target Lvl x3 stars from them. '
        'Cannot Norma while holding this card. This card is discarded upon KO or use.'
    ),
    '"Pokyakya!!" —Poppo',
    None,
    'Poppo_the_Snatcher',
)

CARD_PRICE_OF_POWER = OJCard(66,
    'Price of Power',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, CARD_PACK_COMMUNITY_PACK_1, CARD_RARITY_RARE,
    'You may play cards one level higher than your current level. All card costs are increased by 5. This card is '
    'discarded on use.',
    '"Even if I survive the war... With this body, there\'s nothing I can do." ―Nath',
    None,
    'Price_of_Power',
)

CARD_UNLUCKY_CHARM = OJCard(67,
    'Unlucky Charm',
    1, CARD_COST_Lvx5, 1, CARD_TYPE_GIFT, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_UNCOMMON,
    'Lose Lvl x 1 stars at the start of your turn. Using this card sends it to another player. If Cost is higher than '
    'your star count, you may use this card for free.',
    '"Pitch black darkness disrupts my slumber, hence I yearn for light..." —Krilalaris',
    None,
    'Unlucky_Charm',
)

CARD_WINDY_ENCHANTMENT = OJCard(68,
    'Windy Enchantment',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_RARE,
    'Gain +1 MOV. Cannot Norma while holding this card. Discard upon use.',
    'People call her Barefoot Alicianrone.',
    None,
    'Windy_Enchantment',
)

CARD_ASSAULT = OJCard(69,
    'Assault',
    2, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_BASE_PACK, CARD_RARITY_UNCOMMON,
    'Battle the player who set this card, starting with their attack.',
    '"I\'ll make you leave the guild today for sure!" —Peat',
    None,
    'Assault',
)

CARD_BAD_PUDDING = OJCard(70,
    'Bad Pudding',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'Discard a random card.',
    '"Pudding with soy sauce, tastes like sea urchin!" —Yuki',
    None,
    'Bad_Pudding',
)

CARD_BRUTAL_PRANK = OJCard(71,
    'Brutal Prank',
    3, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_ACCELERATION_PACK, CARD_RARITY_COMMON,
    'Discard all Hyper cards in hand. Lose 10 stars and heal 1 HP for each discarded card.',
    '"Noooo, Mr. Cow! Mr. Frog!" —Yuuki\n'
    '"Hahahaha! Wail and weep!!" —Yuki',
    None,
    'Brutal_Prank',
)

CARD_DANGEROUS_PUDDING = OJCard(72,
    'Dangerous Pudding',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'Stock Effect Your next turn will be skipped.',
    '"One glance is all it took for that pudding to steal my heart."',
    None,
    'Dangerous_Pudding',
)

CARD_ENCORE = OJCard(73,
    'Encore',
    3, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_PUDDING_PACK, CARD_RARITY_UNCOMMON,
    'When this card is activated either on Bonus, Drop, Draw or Encounter, that panel\'s effect takes place twice.',
    '"Encore! Encore!"',
    None,
    'Encore',
)

CARD_EXCHANGE = OJCard(74,
    'Exchange',
    2, CARD_COST_0, 1, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Exchange the cards in your hand, your stars and your current panel position with the player who has set this '
    'card.',
    '"Heavy..." —Suguri\n'
    '"So drafty without my cap..." —Marc',
    None,
    'Exchange',
)

CARD_FLAMETHROWER = OJCard(75,
    'Flamethrower',
     3, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'KO\'s a player. If the player has any cards in their hand, they will lose all of them instead of suffering KO.',
    '"Heeehaaaaah!" —Punk',
    None,
    'Flamethrower',
)

CARD_FOR_THE_FUTURE_OF_THE_TOY_STORE = OJCard(76,
    'For the Future of the Toy Store',
    2, CARD_COST_0, 1, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_RARE,
    'Lose half your stars. The player who set this card will gain the lost stars. This card can only be used with '
    'less than 50 stars.',
    '"If only! If only there was no Santa!!" —Arthur',
    None,
    'For_the_Future_of_the_Toy_Store',
)

CARD_GO_AWAY = OJCard(77,
    'Go Away',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_COMMON,
    'You are moved to a randomly chosen panel.',
    '"Ahaha, I like this." —Nanako',
    None,
    'Go_Away',
)

CARD_HEAT_300 = OJCard(78,
    'Heat 300%',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_COMMON,
    'Effect Duration: 3 chapters In battle, gain -2 DEF.',
    '"All I need to do is dodge every attack!" —Suguri',
    None,
    'Heat_300%',
)

CARD_INVASION = OJCard(79,
    'Invasion',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_COMMON,
    'You will have an encounter. The enemy will attack first.',
    '"What, I was attacked...?" —Suguri',
    None,
    'Invasion',
)

CARD_I_WANNA_SEE_YOU = OJCard(80,
    'I Wanna See You',
    2, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_PUDDING_PACK, CARD_RARITY_COMMON,
    'The player who set this trap moves to the panel on which the trap was activated. The player who activated the '
    'trap then gains this card instead of it being discarded.',
    '"Kyupita... I want to see you." ―Kyousuke',
    None,
    'I_Wanna_See_You',
)

CARD_MIMYUUS_HAMMER = OJCard(81,
    'Mimyuu\'s Hammer',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_BASE_PACK, CARD_RARITY_COMMON,
    'Deals 1 damage.',
    '"Thank you for dying!" —Mimyuu',
    None,
    'Mimyuu\'s_Hammer',
)

CARD_PIGGY_BANK = OJCard(82,
    'Piggy Bank',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_COMMON,
    'Gain stars equal to five times the number of chapters passed since this card was set.',
    '"Dad, can\'t I break the piggy yet?" —Mescal',
    None,
    'Piggy_Bank',
)

CARD_PIYOPIYO_PROCESSION = OJCard(83,
    'Piyopiyo Procession',
    2, CARD_COST_0, 1, CARD_TYPE_TRAP, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_RARE,
    'Player suffers 3 random encounters (the player attacks first).',
    '"Piyopiyopiyopiyopiyopiyopiyopiyopiyooo!" —Colored Piyo Army',
    None,
    'Piyopiyo_Procession',
)

CARD_POPPOFORMATION = OJCard(84,
    'Poppoformation',
    2, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_COMMUNITY_PACK_2, CARD_RARITY_COMMON,
    'Stock Effect (1). ATK, DEF, and EVD become -1 in your next battle.',
    '"Poppo! Poppopopo!!!" —Everyone',
    None,
    'Poppoformation',
)

CARD_PRESENT_THIEF = OJCard(
    85,
    'Present Thief',
    3,
    CARD_COST_0,
    3,
    CARD_TYPE_TRAP,
    CARD_PACK_ACCELERATION_PACK,
    CARD_RARITY_UNCOMMON,
    (
        'The first unit to activate this trap loses all their cards. '
        'If any cards were lost, the trap stays on board and '
        'the lost cards are given to the next player to trigger the trap.'
    ),
    '"These do no good!" —Niko',
    None,
    'Present_Thief',
)

CARD_SEALED_MEMORIES = OJCard(86,
    'Sealed Memories',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_MIXED_BOOSTER_PACK, CARD_RARITY_UNCOMMON,
    'For 3 turns, target sees all cards face down, and other players can see their cards.',
    '"Order within the world...? What the heck does pudding have to do with that!?" —QP',
    None,
    'Sealed_Memories',
)

CARD_SKY_RESTAURANT_PURES = OJCard(87,
    ' Sky Restaurant \'Pures\'',
    4, CARD_COST_0, 1, CARD_TYPE_TRAP, CARD_PACK_BASE_PACK, CARD_RARITY_RARE,
    'Lose half your stars and fully restore HP.',
    '"We have a guest to treat!" —Chris',
    None,
    'Sky_Restaurant_\'Pures\''
)

CARD_TRAGEDY_IN_THE_DEAD_OF_NIGHT = OJCard(88,
    'Tragedy in the Dead of Night',
    3, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_EXPANSION_PACK, CARD_RARITY_UNCOMMON,
    'Discard a random card. That card will go to the player who has set this card.',
    '"Such happiness will be snatched away just like that."',
    None,
    'Tragedy_in_the_Dead_of_Night',
)

CARD_WANTED = OJCard(89,
    'Wanted',
    3, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_COMMUNITY_PACK_1, CARD_RARITY_UNCOMMON,
    'Stock Effect You give double wins on KO from battle. Effect expires on KO.',
    '"Over here! My nose is never wrong!" ―QP',
    None,
    'Wanted',
)

#### #### #### #### HYPER #### #### #### ####

CARD_ANOTHER_ULTIMATE_WEAPON = OJCard(90,
    'Another Ultimate Weapon',
    3, CARD_COST_StALL, -1, CARD_TYPE_HYPER | CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'Gain +1 ATK and DEF and an additional +1 ATK and DEF for every 20 stars spent on this card.',
    '"With you gone, I am their ultimate weapon now." ―YNath',
    None,
    'Another_Ultimate_Weapon',
)

CARD_BEYOND_HELL = OJCard(91,
    'Beyond Hell',
    1, CARD_COST_0, -1, CARD_TYPE_HYPER | CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'During this battle, gain +1 to ATK, DEF and EVD for every HP you are missing.',
    '"Syura\'s powers go beyond Hell itself! Allow me to demonstrate!" ―Syura',
    None,
    'Beyond_Hell',
)

CARD_BLUE_CROW_THE_SECOND = OJCard(92,
    'Blue Crow the Second',
    2, CARD_COST_10, -1, CARD_TYPE_HYPER | CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'During this battle, gain ATK and DEF but lose EVD equal to the number of cards in your hand.',
    '"I\'m gonna settle this!" ―Peat',
    None,
    'Blue_Crow_the_Second',
)

CARD_DEPLOY_BITS = OJCard(93,
    'Deploy Bits',
    2, CARD_COST_20, -1, CARD_TYPE_HYPER | CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'During this battle, gain a total of +7 points to ATK, DEF, and/or EVD, distributed randomly.',
    '"No matter what, you can\'t escape my Bits." ―YNanako',
    None,
    'Deploy_Bits',
)

CARD_HYPER_MODE = OJCard(94,
    'Hyper Mode',
    1, CARD_COST_10, -1, CARD_TYPE_HYPER | CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'Gain +2 ATK during this battle. If your unit suffers KO during this battle, you give no stars or Wins and the '
    'unit will revive next turn.',
    '"HYPER MODE!" ―YQP',
    None,
    'Hyper_Mode',
)

CARD_INTELLIGENCE_OFFICER = OJCard(
    95,
    'Intelligence Officer',
    2,
    CARD_COST_10,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BATTLE,
    None,
    CARD_RARITY_NONE,
    (
        'Gain one of the following effects depending on the top-of-the-deck card: '
        'Event +3 ATK\n'
        'Boost +3 DEF\n'
        'Others +3 EVD'
    ),
    '"I can see through everything!" ―YArnelle',
    None,
    'Intelligence_Officer',
)

CARD_REFLECTIVE_SHELL = OJCard(96,
    'Reflective Shell',
    1, CARD_COST_5, -1, CARD_TYPE_HYPER | CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'Base ATK is 0 in this battle. Absorb up to 2 damage. Gain an additional +2 ATK for every damage absorbed.\n'
    'Can only be used when defending.',
    '"Enemy detected. Destroying." ―Robo Ball',
    None,
    'Reflective_Shell',
)

CARD_SELF_DESTRUCT = OJCard(97,
    'Self-Destruct',
    3, CARD_COST_10, -1, CARD_TYPE_HYPER | CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'On KO, also KO the opponent. Enemy gains no stars or wins, and loses half their stars.',
    '"I\'m sorry...I can\'t make it back..." ―Alte',
    None,
    'Self-Destruct',
)

CARD_WARUDA_MACHINE_BLAST_OFF = OJCard(
    98,
    'Waruda Machine, Blast Off!',
    3,
    CARD_COST_10,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BATTLE,
    None,
    CARD_RARITY_NONE,
    'During this battle, gain ATK and DEF but lose EVD equal to the number of cards in your opponent\'s hand.',
    '"Revenge!" ―Tomato',
    None,
    'Waruda_Machine,_Blast_Off!',
)

CARD_ACCELERATOR = OJCard(99,
    'Accelerator',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Effect Duration: 1 chapter Roll two dice for movement, battle, bonus and drop.',
    '"I\'m accelerating." ―Suguri',
    None,
    'Accelerator',
)

CARD_ANGEL_HAND = OJCard(100,
    'Angel Hand',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Heal target player to full HP and gain 10 stars per healed HP. In even-numbered chapters, this card turns into '
    'Devil Hand.',
    '"This is the power of mercy." ―Yuuki',
    None,
    'Angel_Hand',
)

CARD_AWAKENING_OF_TALENT = OJCard(101,
    'Awakening of Talent',
    2, CARD_COST_20, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST | CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'Until end of turn, roll 5 for move, battle, bonus or drop. This card can also be used as a Battle Card.',
    '"I\'ll commence... my operation now." ―Sora',
    None,
    'Awakening_of_Talent',
)

CARD_BIG_ROCKET_CANNON = OJCard(102,
    'Big Rocket Cannon',
    2, CARD_COST_10, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Deal 3 damage to target enemy. If KO\'d, you gain wins as though KO\'d in battle. This card becomes '
    '"Rocket Cannon" when you use another card or you suffer KO.',
    '"Go!" ―Marc',
    None,
    'Big_Rocket_Cannon',
)

CARD_BLAZING = OJCard(103,
    'Blazing!',
    3, CARD_COST_10, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Inflicts Blazing! on units within 2 panels, and refreshes the duration of existing Blazing! Effect Duration: 3 '
    'Chapters. ATK +1, DEF -1. Effect expires on KO.',
    '"Good! Good! This feeling really is the best!" ―Kae',
    None,
    'Blazing!',
)

CARD_BRANCH_EXPANSION_STRATEGY = OJCard(104,
    'Branch Expansion Strategy',
    3, CARD_COST_HCx5, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Turn all your cards, including this one, into "Rbit Hobby Shop." You may play one more card in this turn.',
    '"Phaaw..." ―Arthur',
    None,
    'Branch_Expansion_Strategy',
)

CARD_CAST_OFF = OJCard(105,
    'Cast Off',
    2, CARD_COST_10, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Stock Effect Swap unit\'s base ATK and DEF. Lasts until KO, or Cast Off is used again.',
    '"This calls for a good distraction..." ―Kyousuke',
    None,
    'Cast_Off',
)

CARD_CHEF_I_COULD_USE_SOME_HELP = OJCard(106,
    'Chef, I Could Use Some Help!',
    2, CARD_COST_20, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Summon Chef. Fights battles on behalf of your unit. Gives 2 Wins on KO. Gives stars gained in battle to your '
    'unit. Effect ends with Chef\'s KO. This card turns to "Manager, I Could Use Some Help!" if you have 4 or more '
    'Store Manager Counters and your Lvl is 4 or higher.',
    '"Chef! I\'m going to need your help!" ―Chris',
    None,
    'Chef,_I_Could_Use_Some_Help!',
)

CARD_CRYSTAL_BARRIER = OJCard(107,
    'Crystal Barrier',
    1, CARD_COST_20, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Stock Effect (3) Cancel a trap, a battle, or drop panel. Take 1 damage. Consumes 1 stack. Effect expires on KO.',
    '"What a piece of junk, huh...―Kyoko',
    None,
    'Crystal_Barrier',
)

CARD_ELLIES_MIRACLE = OJCard(108,
    'Ellie\'s Miracle',
    2, CARD_COST_Lvx10, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Cost: Level x10 stars. Effect Duration: 2 chapters. Gain +X ATK, +Y DEF, and +Z EVD, where X = Your total Norma '
    'completed, Y = your number of Wins Norma completed, and Z = your number of Stars Norma completed.',
    '"Receive my miracle!" ―Ellie',
    None,
    'Ellie\'s_Miracle',
)

CARD_EXTENDED_PHOTON_RIFLE = OJCard(
    109,
    'Extended Photon Rifle',
    1,
    CARD_COST_Lvx5,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    'Deal 1 damage to a random enemy. If KO\'d, gain 1 win. Repeat as many times as your current level.',
    '"I\'ll shoot you all down." ―Iru',
    None,
    'Extended_Photon_Rifle',
)

CARD_EXTRAORDINARY_SPECS = OJCard(110,
    'Extraordinary Specs',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Effect Duration: 1 chapter Roll 6 for movement, battle, bonus and drop.',
    '"I\'d appreciate it if you dropped your weapons." ―Sora',
    None,
    'Extraordinary_Specs',
)

CARD_FULL_SPEED_ALICIANRONE = OJCard(
    111,
    'Full Speed Alicianrone',
    3,
    CARD_COST_30,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Roll a die and move result x 3 panels. '
        'Deal damage equal to the result to each enemy you pass during the move. '
        'If they are KO\'d by the damage, gain Wins as though from a normal battle. '
        'After this effect, your turn ends.'
    ),
    '"I\'ll go fast and cut my way through!" ―Alicianrone',
    None,
    'Full_Speed_Alicianrone',
)

CARD_IMMOVABLE_OBJECT = OJCard(112,
    'Immovable Object',
    3, CARD_COST_20, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Effect Duration: 2 Chapters Cannot move. Gain +2 DEF. Can counterattack. Enemies who move into the same panel '
    'must battle you.',
    '"With this power, everything in the sky will be ours." ―Guild Master',
    None,
    'Immovable_Object',
)

CARD_JONATHAN_RUSH = OJCard(113,
    'Jonathan Rush',
    3, CARD_COST_20, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Move to an enemy and attack them. Target gains -1 DEF. After the battle, your turn ends.',
    '"Squaawk!" ―Seagull',
    None,
    'Jonathan_Rush',
)

CARD_LEAP_THROUGH_SPACE = OJCard(114,
    'Leap Through Space',
    2, CARD_COST_10, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Warp to the marked panel and unmark it. Apply Binding Smoke to enemies within 1 panel radius. If no marked panels '
    'exist, this card becomes "Leap through Space (Marking)."',
    '"Poof." ―Mira',
    None,
    'Leap_Through_Space',
)

CARD_LEAP_THROUGH_SPACE_MARKING = OJCard(115,
    'Leap Through Space (Marking)',
    1, CARD_COST_0, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Mark the panel where your unit is. When a marked panel exists, this card becomes "Leap through Space." This card '
    'is not discarded upon use.',
    '"Poof." ―Mira',
    None,
    'Leap_Through_Space_(Marking)',
)

CARD_LULUS_LUCKY_EGG = OJCard(116,
    'Lulu\'s Lucky Egg',
    2, CARD_COST_40, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Can only be played with 2 HP or less. Gain one of the following effects at random: - Roll a die and gain the die '
    'number x 20 stars. - Draw 5 cards. - Heal to full HP and permanently gain +1 ATK, +1 DEF, and +1 EVD. This effect '
    'can only trigger once.',
    '"Ugh... Lulu\'s about to lay an egg..." ―Lulu',
    None,
    'Lulu\'s_Lucky_Egg',
)

CARD_MANAGER_I_COULD_USE_SOME_HELP = OJCard(117,
    'Manager, I Could Use Some Help!',
    4, CARD_COST_40, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Summon Store Manager. Fights battles on behalf of your unit. Gives 2 Wins on KO. Gives stars gained in battle to '
    'your unit. Effect ends with Store Manager\'s KO, and your Store Manager Counters reset to 0. This card turns to '
    '"Chef, I Could Use Some Help!" if you have less than 4 Store Manager Counters.',
    '"Manager, help me!" ―Chris',
    None,
    'Manager,_I_Could_Use_Some_Help!',
)

CARD_MIRACLE_WALKER = OJCard(
    118,
    'Miracle Walker',
    3,
    CARD_COST_0,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    'Turn all your cards, including this one, into random Hyper cards. You may play one more card this turn.',
    '"Hooray! Nico will try her best!" ―Nico',
    None,
    'Miracle_Walker',
)

CARD_OBSERVER_OF_ETERNITY = OJCard(119,
    'Observer of Eternity',
    3, CARD_COST_0, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    (
        'Add 2 random Boost/Event cards that deal damage to your hand.\n'
        'You may play another card this turn.'
    ),
    '"Now then, let\'s see how this will turn out." ―Suguri',
    None,
    'Observer_of_Eternity',
)

CARD_PROTAGONISTS_PRIVILEGE = OJCard(120,
    'Protagonist\'s Privilege',
    3, CARD_COST_20, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Effect Duration: 3 chapters When you are allowed to attack first, the opposing unit cannot attack (once per '
    'combat).',
    '"This is the privilege of the main character!" ―Kai',
    None,
    'Protagonist\'s_Privilege',
)

CARD_RAGING_MADNESS = OJCard(
    121,
    'Raging Madness',
    2,
    CARD_COST_30,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Gain +1 Rage Counter. Target another active player and enter Raging Mode: '
        'gain +X ATK and +X EVD where X is the number of your Rage Counters. '
        'Raging Mode ends and Rage Counters become 0 upon target\'s KO. Gain +2 Wins if you KO target in battle, '
        'and -50% Stars and Wins if you KO any other unit.'
    ),
    '"Gyaoooh!" ―Maynie',
    None,
    'Raging_Madness',
)

CARD_REPRODUCTION_OF_RECORDS = OJCard(
    122,
    'Reproduction of Records',
    2,
    CARD_COST_20,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Add a copy of the two most recent cards in the discard pile that aren\'t '
        '"Reproduction of Records" to your hand. '
        'Those cards will be treated as being Level 1 and having no base cost while in your hand.'
    ),
    '"Sumika\'s sweet memory!" ―Sumika',
    None,
    'Reproduction_of_Records',
)

CARD_RIVAL = OJCard(
    123,
    'Rival',
    3,
    CARD_COST_30,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    'Battle target player. You attack first. During battle, gain +1 ATK.',
    '"Just like you... I have my battles to fight." ―Islay',
    None,
    'Rival',
)

CARD_ROCKET_CANNON = OJCard(124,
    'Rocket Cannon',
    1, CARD_COST_10, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Choose one of the following two effects to activate: 1. This card becomes "Big Rocket Cannon". 2. Deal 1 damage '
    'to target enemy. If KO\'d, you gain wins as though KO\'d in battle.',
    '"Red Barrel... It\'s time to use that!" ―Marc',
    None,
    'Rocket_Cannon',
)

CARD_SAINT_EYES = OJCard(125,
    'Saint Eyes',
    1, CARD_COST_10, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Stock Effect (3). In a battle where you attack first, gain -1 ATK and +1 DEF for every 2 stock, and +1 ATK per '
    'stock. This effect can stack.',
    '"I\'m going to use my saint eyes!" ―Kyupita',
    None,
    'Saint_Eyes',
)

CARD_SOLID_WITCH = OJCard(126,
    'Solid Witch',
    2, CARD_COST_20, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Effect Duration: 1 chapter. Take no damage.',
    '"No flimsy attacks can hurt me!" ―Miusaki',
    None,
    'Solid_Witch',
)

CARD_SPECIAL_STAGE = OJCard(127,
    'Special Stage',
    1, CARD_COST_Lvx10, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Go to Live Mode for (your Lvl) turns. Gain -3 MOV, can only trigger movement type panels and cannot use cards. '
    'Cannot be challenged or be the target of Boost cards. If an opponent ends their turn in 2 panel radius, steal '
    '(your Lvl) x5 stars from them. Ends on KO.',
    '"We are the strongest idols!" ―Sora & Sham',
    None,
    'Special_Stage',
)

CARD_STEALTH_ON = OJCard(
    128,
    'Stealth On',
    2,
    CARD_COST_10,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Effect Duration: 3 chapters.\n'
        'Cannot be challenged to battle, or targeted by Boost cards by other players.\n'
        'Do not trigger Encounter or Boss panels.\n'
        'Effect expires on entering battle.\n'
        'Gain +2 ATK when entering battle.'
    ),
    '"Look at me vanish!" ―Tsih',
    None,
    'Stealth_On',
)

CARD_SWEET_GUARDIAN = OJCard(
    129,
    'Sweet Guardian',
    3,
    CARD_COST_20,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Draw 2 cards with "Pudding" in their name from the center deck. '
        'If there are no cards with "pudding" in their name in the deck, '
        'instead randomly gain 1 Dangerous Pudding or Bad Pudding.'
    ),
    '"My little... pudding..." ―QP',
    None,
    'Sweet_Guardian',
)

CARD_TURBO_CHARGED = OJCard(130,
    'Turbo Charged',
    2, CARD_COST_20, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Drop to 1 HP. Gain +1 ATK per lost HP. Effect Duration: As many Chapters as lost HP. Lose 1 ATK per turn for the '
    'duration. Effect expires on KO.',
    '"Rumble rumble rumble." ―Shifu Robot',
    None,
    'Turbo_Charged',
)

CARD_UBIQUITOUS = OJCard(
    131,
    'Ubiquitous',
    1,
    CARD_COST_0,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    'Warp to target active enemy\'s panel. In addition, steal stars equal to 10x their level.',
    '"Poppo! Poppopopopopo!" ―Marie Poppo',
    None,
    'Ubiquitous',
)

CARD_WITCHS_HAIR_LOCK = OJCard(
    132,
    'Witch\'s Hair Lock',
    1,
    CARD_COST_0,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    'Stop target unit\'s next move action.',
    '"No one can get out of Repa\'s hair." ―Ceoreparque',
    None,
    'Witch\'s_Hair_Lock',
)

CARD_X16_BIG_ROCKET = OJCard(
    133,
    'x16 Big Rocket',
    1,
    CARD_COST_Lvx10,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    'Deal damage equal to your level to target enemy. A KO from this effect gives you 2 Wins.',
    '"Charged! Go!" ―Marc',
    None,
    'X16_Big_Rocket',
)

CARD_AIR_STRIKE = OJCard(134,
    'Air Strike',
    2, CARD_COST_30, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'All enemies take 1 to 3 damage. Gain 15 stars on every KO.',
    '"Hmph, go down, all of you." ―Fernet',
    None,
    'Air_Strike',
)

CARD_BINDING_CHAINS = OJCard(135,
    'Binding Chains',
    3, CARD_COST_10, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Stock Effect All Units except yours will skip their next turn. Apply "Bound" to all active enemies. Effect '
    'Duration: 2 Chapters. Gain -2 EVD and -1 MOV.',
    '"I don\'t like this sort of thing." ―Hime',
    None,
    'Binding_Chains',
)

CARD_COOKING_TIME = OJCard(136,
    'Cooking Time',
    1, CARD_COST_Lvx5, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'All players recover your Lvl x HP. Gain 5 stars for each HP recovered.',
    '"It\'s meal time!" ―Natsumi',
    None,
    'Cooking_Time',
)

CARD_DELTA_FIELD = OJCard(
    137,
    'Delta Field',
    2,
    CARD_COST_20,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_EVENT,
    None,
    CARD_RARITY_NONE,
    'All enemies receive the following effect until your next turn: All dice rolls will be 1.',
    '"If you insist on staying here, I\'ll take you back no matter how!" ―Sham',
    None,
    'Delta_Field',
)

CARD_DEVIL_HAND = OJCard(138,
    'Devil Hand',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Lower a random player\'s HP to 1 and gain 10 stars per lowered HP. In odd-numbered chapters, this card turns '
    'into Angel Hand.',
    '"Eat the power of the devil!" ―Yuuki',
    None,
    'Devil_Hand',
)

CARD_DO_PIRATES_FLY_IN_THE_SKY = OJCard(139,
    'Do Pirates Fly in the Sky?',
    3, CARD_COST_20, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Set "Flying Pirate" on 2-3 random panels.',
    '"There ain\'t no law against pirates flying in the sky." ―Tequila',
    None,
    'Do_Pirates_Fly_in_the_Sky_',
)

CARD_EVIL_MASTERMIND = OJCard(140,
    'Evil Mastermind',
    2, CARD_COST_13, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Draw a trap card from the deck. Set all trap cards in hand on random panels. If not holding any trap cards, draw '
    '3 from the deck and set a random one on your current panel.',
    '"Fear my powers!" ―Yuki',
    None,
    'Evil_Mastermind',
)

CARD_EVIL_SPY_WORK_PREPARATION = OJCard(
    141,
    'Evil Spy Work - Preparation',
    2,
    CARD_COST_13,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_EVENT,
    None,
    CARD_RARITY_NONE,
    'Place 4 "Evil Spy Work - Execution" cards at random positions in the Center Deck.',
    '"Fear Mimyuu\'s pranks." ―Mimyuu',
    None,
    'Evil_Spy_Work_―_Preparation',
)

CARD_FINAL_SURGERY = OJCard(142,
    'Final Surgery',
    2, CARD_COST_10, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'KO all units with 1 HP and gain stars equal to 25x the number of KO\'d units.',
    '"Just hold still, I\'ll fix you up real quick." ―Kiriko',
    None,
    'Final_Surgery',
)

CARD_GAMBLE = OJCard(143,
    'Gamble!',
    3, CARD_COST_13, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'A randomly chosen unit is KO\'d.',
    '"Why not use this to decide whose turn it is?" ―Yuki',
    None,
    'Gamble!',
)

CARD_MAGICAL_INFERNO = OJCard(
    144,
    'Magical Inferno',
    3,
    CARD_COST_50,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_EVENT,
    None,
    CARD_RARITY_NONE,
    (
        'KO all enemies on any other panel in the same uninterrupted column or row as the panel your unit is on. '
        'You gain stars from each KO\'d enemy as though KO\'d in battle. Then end your turn.'
    ),
    '"Inferno!" ―Mio',
    None,
    'Magical_Inferno',
)

CARD_MAGICAL_MASSACRE = OJCard(
    145,
    'Magical Massacre',
    4,
    CARD_COST_20,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_EVENT,
    None,
    CARD_RARITY_NONE,
    (
        'All units whose HP is full or higher will suffer KO. Gain -1 REC on next Revive roll per unit KO\'d '
        '(other than yourself).'
    ),
    '"Disappear." ―Tomomo',
    None,
    'Magical_Massacre',
)

CARD_MAGICAL_REVENGE = OJCard(146,
    'Magical Revenge',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'For each missing HP, random enemy takes 1 damage. If a unit is KO\'d, you gain 1 Win. When not held by Tomomo '
    '(Sweet Eater), this card becomes Miracle Red Bean Ice Cream.',
    '"It\'s Magical Revenge time!" ―Tomomo',
    None,
    'Magical_Revenge',
)

CARD_MELTING_MEMORIES = OJCard(147,
    'Melting Memories',
    3, CARD_COST_OCx5, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'All other players discard and replace a card from their hand. Reverse all enemy cards.',
    '"How foolish you are to have challenged a God. Prepare to taste your bitter defeat!" ―Sweet Breaker',
    None,
    'Melting_Memories',
)

CARD_OVERSEER = OJCard(148,
    'Overseer',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT | CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'A boss appears. If a boss is already on the field, treat this card as a battle card: End the battle. Opponent '
    'fights the boss instead. Can only use against players.',
    '"Hahaha! Here comes my friend!" ―NoName',
    None,
    'Overseer',
)

CARD_PLUSHIE_MASTER = OJCard(149,
    'Plushie Master',
    2, CARD_COST_10, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Set "Dance, Long-Eared Beasts!" trap on 3-5 random panels.',
    '"Dance, long-eared beasts!" ―Krilalaris',
    None,
    'Plushie_Master',
)

CARD_PRESENT_FOR_YOU = OJCard(150,
    'Present for You',
    2, CARD_COST_30, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'All players draw cards until they have a full hand. Those with full hand draw 1 card instead. Gain stars equal '
    'to 10x the number of all cards drawn.',
    '"Presents for good boys and girls." ―Aru',
    None,
    'Present_for_You',
)

CARD_REVIVAL_OF_STARS = OJCard(151,
    'Revival of Stars',
     1, CARD_COST_Lvx3, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Effect Duration: 3 Chapters. Turn all Drop Panels into Bonus Panels and Encounter and Boss Panels into Draw '
    'Panels. -1 ATK when on a marked panel.',
    '"The dream you protected has spread across the whole planet." ―Suguri',
    None,
    'Revival_of_Stars',
)

CARD_STAR_BLASTING_FUSE = OJCard(152,
    'Star Blasting Fuse',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Set "Invisible Bomb" on 3-5 random panels',
    '"Because I am Star Breaker, the blasting fuse to the world\'s end." ―Star Breaker',
    None,
    'Star_Blasting_Fuse',
)

CARD_SUBSPACE_TUNNEL = OJCard(153,
    'Subspace Tunnel',
    1, CARD_COST_Lvx5, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Effect Duration: Player level Turn 4-6 panels into Warp Move panels and then warp to one of them.',
    '"Po! Po! Po! Popoppo!!" ―Marie Poppo',
    None,
    'Subspace_Tunnel',
)

CARD_TRUE_WHITE_CHRISTSMASHER = OJCard(
    154,
    'True White Christsmasher',
    3,
    CARD_COST_20,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_EVENT,
    None,
    CARD_RARITY_NONE,
    (
        'Deal 4 damage to players within 2 panels of you.'
        'For each player KO\'d, gain 2 wins and KO\'d Player\'s Lvl x10 stars.\n'
        'When not carrying "Red & Blue", this card becomes "White Christsmasher".'
    ),
    '"White Christsmasher!" ―Mei, Red & Blue',
    None,
    'True_White_Christsmasher',
)

CARD_WHIMSICAL_WINDMILL = OJCard(155,
    'Whimsical Windmill',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'Fight all other players in order. The enemy goes first. During battle, gain +1 EVD.',
    '"We just want to fly around freely." ―Sherry',
    None,
    'Whimsical_Windmill',
)

CARD_WHITE_CHRISTSMASHER = OJCard(
    156,
    'White Christsmasher',
    2,
    CARD_COST_10,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_EVENT,
    None,
    CARD_RARITY_NONE,
    (
        'Discard your current hand and deal 2 damage to players within 1 panel of you.\n'
        'For each player KO\'d, gain a win and KO\'d Player\'s Lvl x5 stars.\n'
        'When carrying "Red & Blue", this card becomes "True White Christsmasher".'
    ),
    '"White Christsmasher!" ―Mei',
    None,
    'White_Christsmasher',
)

CARD_BANNER_FOR_LIFE = OJCard(157,
    'Banned for Life',
    1, CARD_COST_Stp10, -1, CARD_TYPE_HYPER | CARD_TYPE_GIFT, None, CARD_RARITY_NONE,
    'Can only play Gift cards. Using this card sends it to another player. Discards entire hand upon discard.',
    '"Manager, it\'s your turn!!" ―Chris',
    None,
    'Banned_for_Life',
)

CARD_BEAST_WITCH = OJCard(158,
    'Beast Witch',
    1, CARD_COST_0, -1, CARD_TYPE_HYPER | CARD_TYPE_GIFT, None, CARD_RARITY_NONE,
    'When another player loses stars from an Encounter panel battle and those stars would go to the Encounter panel '
    'unit, you will receive them instead. If this effect is triggered, discard this card at the end of your turn. If '
    'several players carry Beast Witch, the stars are split between them.',
    '"All beasts! Obey me!" ―Teotoratta',
    None,
    'Beast_Witch',
)

CARD_EVIL_SPY_WORK_EXECUTION = OJCard(
    159,
    'Evil Spy Work - Execution',
    1,
    CARD_COST_0,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_GIFT,
    None,
    CARD_RARITY_NONE,
    (
        'This card cannot be played.\n'
        'When holding this card, take 3 damage at the end of your turn, and remove this card from the game.'
    ),
    '"You fell for it! Eat it!!" ―Mimyuu',
    None,
    'Evil_Spy_Work_―_Execution',
)

CARD_MIRACLE_RED_BEAN_ICE_CREAM = OJCard(160,
    'Miracle Red Bean Ice Cream',
    3, CARD_COST_30, -1, CARD_TYPE_HYPER | CARD_TYPE_GIFT, None, CARD_RARITY_NONE,
    (
        '+1 ATK while this card is held. Tomomo (Casual): When played, turn into Tomomo (Sweet Eater) and fully '
        'restore HP.\n'
        'Tomomo (Sweet Eater): When held, this card becomes Magical Revenge. Discard upon use.'
    ),
    '"Miracle red bean ice cream!" ―Tomomo',
    None,
    'Miracle_Red_Bean_Ice_Cream',
)

CARD_SANTAS_JOB = OJCard(
    161,
    'Santa\'s Job',
    1,
    CARD_COST_0,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_GIFT,
    None,
    CARD_RARITY_NONE,
    (
        'During standby, you may choose another card of usable Lvl to send to another random player. '
        'Gain stars equal to Card Lvl x5. Target cannot challenge players to a battle until your next turn. '
        'This card is discarded upon KO or use.'
    ),
    '"Children of the world, we are coming for you!" ―Aru',
    None,
    'Santa\'s_Job',
)

CARD_BIG_BANG_BELL = OJCard(162,
    'Big Bang Bell',
    3, CARD_COST_0, -1, CARD_TYPE_HYPER | CARD_TYPE_TRAP, None, CARD_RARITY_NONE,
    'Every unit on this and 2 adjacent squares takes 2 damage, +1 for every 2 chapters since setting the trap. On KO, '
    'half of their stars go to the player who set this trap.',
    '"Mauuuuuryaaaaaaahh!" ―Saki',
    None,
    'Big_Bang_Bell',
)

CARD_DANCE_LONG_EARED_BEASTS = OJCard(163,
    'Dance, Long-Eared Beasts!',
    2, CARD_COST_0, -1, CARD_TYPE_HYPER | CARD_TYPE_TRAP, None, CARD_RARITY_NONE,
    'Set "Dance, Long-Eared Beasts!" trap on 3-5 random panels.',
    '"Dance, long-eared beasts!" ―Krilalaris',
    None,
    'Dance,_Long-Eared_Beasts!',
)

CARD_FLYING_PIRATE = OJCard(164,
    'Flying Pirate',
    3, CARD_COST_0, -1, CARD_TYPE_HYPER | CARD_TYPE_TRAP, None, CARD_RARITY_NONE,
    'Fight a Pirate Crew Member summoned by the player who set this card. The enemy will attack first. No effect on '
    'the player who set this card.',
    '"Captain～!" ―Pirate Minion',
    None,
    'Flying_Pirate',
)

CARD_GOLDEN_EGG = OJCard(165,
    'Golden Egg',
    2, CARD_COST_0, -1, CARD_TYPE_HYPER | CARD_TYPE_TRAP, None, CARD_RARITY_NONE,
    'If target is Chicken, Stock Effect (3). Drop Panels will act as Bonus Panels. Otherwise, Stock Effect (3). '
    'Bonus Panels will act as Drop Panels.',
    '"Cluuuuck!" ―Chicken',
    None,
    'Golden_Egg',
)

CARD_INVISIBLE_BOMB = OJCard(166,
    'Invisible Bomb',
    3, CARD_COST_0, -1, CARD_TYPE_HYPER | CARD_TYPE_TRAP, None, CARD_RARITY_NONE,
    'Reduces HP to 1. Does not affect the player who set the trap. Only visible to the player who used this card.',
    '"Because I am Star Breaker, the blasting fuse to the world\'s end." ―Star Breaker',
    None,
    'Invisible_Bomb',
)

CARD_RBIT_HOBBY_SHOP = OJCard(167,
    'Rbit Hobby Shop',
    1, CARD_COST_0, -1, CARD_TYPE_HYPER | CARD_TYPE_TRAP, None, CARD_RARITY_NONE,
    'Pay X stars to the player who set this card, where X is the Lvl of the player who set this card. Draw a card from '
    'the deck. This card remains on board when triggered but can be replaced by a new trap. No effect on the player '
    'who set this trap.',
    '"All right, it\'s time to open the shop." ―Arthur',
    None,
    'Rbit_Hobby_Shop',
)

#### #### #### #### EVENT CARDS #### #### #### ####

CARD_SWEET_BATTLE = OJCard(168,
    'Sweet Battle!',
    1, CARD_COST_0, 6, CARD_TYPE_GIFT | CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'When held: Pick up 2x chocolate. When played in battle: Steal 200 chocolate for each damage dealt. This card is '
    'discarded upon KO or use.',
    '"Here comes another cute and sweet battle!" ―QP',
    (EVENT_CHOCOLATE_FOR_THE_SWEET_GODS, EVENT_CHOCOLATE_FOR_THE_SWEET_GODS_RERUN,),
    'Sweet_Battle!',
)

CARD_SNOWBALL_REFLECTOR = OJCard(169,
    'Snowball Reflector',
    2, CARD_COST_10, 4, CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'On this defense turn, any snowball that would hit you will hit the unit that threw them instead. Ignore unit '
    'effects that would prevent this card from being played.',
    '"A-and it comes right back at you!" ―Aru',
    (EVENT_SANTA_SCRAMBLE, EVENT_EVENT_SANTA_SCRAMBLE_RERUN),
    'Snowball_Reflector',
)

CARD_GROWN_UP_SNOWBALL_FIGHT = OJCard(170,
    'Grown-up Snowball Fight',
    3, CARD_COST_10, 4, CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'On this attack turn, select two panels to target with snowballs. Ignore unit effects that would prevent this card '
    'from being played.',
    '"Are you prepared for this?" ―Arthur',
    (EVENT_SANTA_SCRAMBLE, EVENT_EVENT_SANTA_SCRAMBLE_RERUN),
    'Grown-up_Snowball_Fight',
)

CARD_LEGENDARY_MUSHROOM = OJCard(171,
    'Legendary Mushroom',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, None, CARD_RARITY_NONE,
    'Smells notoriously funky. / Smells eerily funky.',
    None,
    (EVENT_SHROOM_ZOOM,),
    'Legendary_Red_Mushroom',
)

#### #### #### #### EVENT CARDS DEPRECATED #### #### #### #### ####

CARD_ULTIMATE_WEAPON_IN_THE_SUN = OJCard(172,
    'Ultimate Weapon in the Sun',
    5, CARD_COST_20, -1, CARD_TYPE_HYPER | CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'During this battle, gain 2 ATK.',
    'I\'ll commence... my vacation now." ―Sora',
    (EVENT_BEACH_PARTY,),
    'Ultimate_Weapon_in_the_Sun_(Original)',
)

CARD_LIFEGUARD_ON_THE_WHITE_BEACH = OJCard(173,
    'Lifeguard on the White Beach',
    5, CARD_COST_10, -1, CARD_TYPE_HYPER | CARD_TYPE_EVENT, None, CARD_RARITY_NONE,
    'All allies gain a damage reduction of 2 during their next battle.',
    '"Geez, you\'re going overboard." ―Suguri',
    (EVENT_BEACH_PARTY,),
    'Lifeguard_on_the_White_Beach_(Original)',
)

CARD_GUARDIAN_OF_BLOOMING_FLOWERS = OJCard(174,
    'Guardian of Blooming Flowers',
    5, CARD_COST_20, -1, CARD_TYPE_HYPER | CARD_TYPE_BOOST, None, CARD_RARITY_NONE,
    'Revive one KO\'d ally with full HP',
    '"You\'re fine now. The pain\'s gone." ―Hime',
    (EVENT_BEACH_PARTY,),
    'Guardian_of_Blooming_Flowers_(Original)',
)

CARD_UNFORGIVING_AVENGER = OJCard(175,
    'Unforgiving Avenger',
    5, CARD_COST_20, -1, CARD_TYPE_HYPER | CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'During this battle, damage taken by both sides is doubled.',
    '"Mimyuu! Who did this to you..." ―Tomato',
    (EVENT_BEACH_PARTY,),
    'Unforgiving_Avenger_(Original)',
)

#### #### #### #### OTHER CARDS #### #### #### ####

CARD_RED_AND_BLUE = OJCard(176,
    'Red & Blue',
    1, CARD_COST_0, -1, CARD_TYPE_GIFT, None, CARD_RARITY_NONE,
    'When holding this card, gain +1 ATK, DEF and EVD in battle. On Discard or KO, this card is removed from the game.',
    '"We can\'t do this anymore!" ―Red & Blue',
    None,
    'Red_&_Blue',
)

CARD_MUSHROOM_BOOST = OJCard(177,
    'Mushroom',
    1, CARD_COST_0, -1, CARD_TYPE_BOOST | CARD_TYPE_BATTLE, None, CARD_RARITY_NONE,
    'Smells funky.',
    None,
    None,
    'Blue_Mushroom_(Boost)',
)

#### #### #### #### COMMUNITY PACK 3 #### #### #### ####

CARD_DETECTIVE_DISARMING = OJCard(178,
    'Deceptive Disarming',
    3, CARD_COST_10, 1, CARD_TYPE_BATTLE, CARD_PACK_COMMUNITY_PACK_3, CARD_RARITY_RARE,
    'If opponent uses a battle card in this battle, if not restricted by player order its effect is applied as though '
    'you played it instead. If successful, opponent does not pay the card cost.',
    '"The train\'s full of dangerous stuff?!" ―Tomato',
    None,
    'Deceptive_Disarming',
)

CARD_OVERTIME = OJCard(179,
    'Overtime',
    3, CARD_COST_10, 1, CARD_TYPE_BOOST, CARD_PACK_COMMUNITY_PACK_3, CARD_RARITY_COMMON,
    'For this turn, roll 3 dice for movement. Skip next turn.',
    '"I-I have no complaints as long as I get paid..." —Chris',
    None,
    'Overtime',
)

CARD_PET_SNACK = OJCard(180,
    'Pet Snacks',
    1, CARD_COST_5, 3, CARD_TYPE_EVENT, CARD_PACK_COMMUNITY_PACK_3, CARD_RARITY_COMMON,
    'Each different wild unit gains +1/+1/+1 during its next battle. This effect can stack.',
    '"Guys, it\'s snack time! Come eat!" —Syura',
    None,
    'Pet_Snacks',
)

CARD_HOME_IMPROVEMENT = OJCard(181,
    'Home Improvement',
    1, CARD_COST_5, 3, CARD_TYPE_EVENT, CARD_PACK_COMMUNITY_PACK_3, CARD_RARITY_UNCOMMON,
    'At the start of your next turn, randomly swap home panel positions. The first player to land on each home draws '
    'a card.',
    '"Sumika\'s going to build herself a nice and cozy home." —Sumika',
    None,
    'Home_Improvement',
)

CARD_HOME_LUCKY_SEVENS = OJCard(182,
    'Lucky Sevens',
    1, CARD_COST_0, 1, CARD_TYPE_GIFT, CARD_PACK_COMMUNITY_PACK_3, CARD_RARITY_UNCOMMON,
    'While holding this card, your natural die rolls can range from 0 to 7, and the minimum roll result is 0 when '
    'rolling 0.\n'
    'Cannot perform a Norma check after rolling a 0 for move on the same turn.',
    '"I can even control my dice rolls." —Yuki',
    None,
    'Lucky_Sevens',
)

CARD_BANA_NANA = OJCard(183,
    'Lucky Sevens',
    1, CARD_COST_0, 3, CARD_TYPE_TRAP, CARD_PACK_COMMUNITY_PACK_3, CARD_RARITY_COMMON,
    'Roll to move again without activating this panel.',
    '"Thought you\'d found a banana? Too bad, it was just me, Nanako!" —Nanako',
    None,
    'BanaNana',
)

#### #### #### #### DLC 30 #### #### #### ####

CARD_SAFE_JOURNEY = OJCard(
    184,
    'Safe Journey',
    3,
    CARD_COST_5,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Lose 5 stars at the start of each turn. Ignore Drop panels, traps, and card effect damage. This effect ends '
        'when you stop on your own Home panel or have less than 5 stars.'
    ),
    '"Now, let\'s get going." ―Halena',
    None,
    'Safe_Journey',
)

CARD_GUIDANCE_OF_THE_WEATHERCOCK = OJCard(
    185,
    'Guidance of the Weathercock',
    3,
    CARD_COST_30,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Roll 2 dice for everything except for battle. This effect ends when you stop on your own Home panel. Can only '
        'check Norma on own Home panel.'
    ),
    '"*Cheep cheep*! Cook wants to go this way." ―Cook',
    None,
    'Guidance_of_the_Weathercock',
)

#### #### #### #### DLC 31 #### #### #### ####

CARD_UPSHIFT = OJCard(
    186,
    'Upshift',
    2,
    CARD_COST_30,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Stock Effect (2).\n'
        'Gain +1 MOV. This effect can be stacked (max 6).\n'
        'If you end your turn without moving to the end of your final move roll, lose a stack of Upshift.'
    ),
    '"...Don\'t follow me." ―Lone Rider',
    None,
    'Upshift',
)

CARD_ZEALOUS_SALESMAN = OJCard(
    187,
    'Zealous Salesman',
    1,
    CARD_COST_30,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Gain Freight cards equal to your level. With Freight cards in your hand, this card can be played as a Battle '
        'card: During this battle, gain +1 ATK for every Freight card in your hand.'
    ),
    '"Breaking the load regulations, you say? I have a permit right here!" ―Merchant',
    None,
    'Zealous_Salesman',
)

CARD_FREIGHT = OJCard(
    188,
    'Freight',
    1,
    CARD_COST_0,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BATTLE,
    None,
    CARD_RARITY_NONE,
    (
        'If the opponent has not played a Battle card, give them this card and cancel the battle. '
        'May only be used by the defender.\n'
        'When stopping on your Home panel, discard this card and gain 5 Stars.'
    ),
    '"You may keep all that freight, yes you may." ―Merchant',
    None,
    'Freight',
)

#### #### #### #### DLC 32 #### #### #### ####

CARD_NEW_NOBILITY = OJCard(
    189,
    'New Nobility',
    2,
    CARD_COST_0,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_EVENT,
    None,
    CARD_RARITY_NONE,
    (
        'Stock Effect: All opposing units randomly gain -1 ATK, DEF or EVD during their next battle.\n'
        'If held by Fernet, this card can be transformed into "Affluence (1)" instead.'
    ),
    '"Pleased to make your acquaintance. I hope we can get along well in the future." ―Fernet',
    None,
    'New_Nobility',
)

CARD_AFFLUENCE_X = OJCard(
    190,
    'Affluence (X)',
    2,
    CARD_COST_Xx10,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'If this card is Affluence (4): Active players battle you in a random order. They gain -3 ATK. If you are not '
        'KO\'d, opponent gives you (their Lvl) x 10 stars.\n'
        'If not Affluence (4): Upgrade this card.\n'
        'If not held by Fernet, this card becomes New Nobility.'
    ),
    '"You wish to ask me for a favor...? My my, of course I\'d be ever so happy to help a friend." ―Fernet',
    None,
    'Affluence_(X)',
)

CARD_DANCE_IN_THE_MOONLIT_NIGHT = OJCard(
    191,
    'Dance in the Moonlit Night',
    2,
    CARD_COST_20,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BATTLE,
    None,
    CARD_RARITY_NONE,
    (
        'On successful Evasion, deal damage to the opponent equal to what you would have taken from them.\n'
        'If used by Hime (Moonlight) during full moon (every 5 chapters), deal double that damage but cannot use the '
        'Defend command.'
    ),
    '"Now let us dance." ―Hime',
    None,
    'Dance_in_the_Moonlit_Night',
)


#### #### #### #### DLC 33 #### #### #### ####

CARD_TWILIGHT_COLORED_DREAM = OJCard(
    192,
    'Twilight-Colored Dream',
    2,
    CARD_COST_Lvx7,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_EVENT,
    None,
    CARD_RARITY_NONE,
    (
        'Effect Duration: (Your Lvl) x Chapters\n'
        'Turn all Bonus and Draw panels into Encounter panels. If an enemy moves onto an Encounter or Boss panel with '
        'a Battle card you set as a Trap, they must stop on that panel.'
    ),
    '"Look at all those countless planes crossing the sky... It\'s like watching a dream, is it not?" ―Malt',
    None,
    'Twilight-Colored_Dream',
)

CARD_LITTLE_MAGNUM = OJCard(
    193,
    'Twilight-Colored Dream',
    2,
    CARD_COST_10,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_EVENT,
    None,
    CARD_RARITY_NONE,
    (
        'During this battle, gain +1 ATK. Additionally, gain +X ATK where X is the damage you have taken during this '
        'battle.'
    ),
    '"Stop bullying Daddy!" ―Mescal',
    None,
    'Little_Magnum',
)

#### #### #### #### DLC 34 #### #### #### ####

CARD_IDEAL_WORLD = OJCard(
    194,
    'Ideal World',
    2,
    CARD_COST_20,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_EVENT,
    None,
    CARD_RARITY_NONE,
    (
        'Place an Invasion trap on each Home panel that has no active trap.\n'
        'Each player will battle a robotic wild unit during their next 2 encounters, '
        'and this robotic unit will gain +1 ATK. This effect can stack.'
    ),
    '"Everything\'s under my control." ―Shifu',
    None,
    'Ideal_World',
)

CARD_STAR_COLLECTOR = OJCard(
    195,
    'Star Collector',
    2,
    CARD_COST_0,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Effect Duration: 3 Chapters.\n'
        'Whenever another unit gains stars from a panel or battle KO, they gain up to your Lvl fewer stars, '
        'and you gain your Lvl stars. Effect expires on KO.'
    ),
    '"Fufufu, look how many stars I have here." ―Reika',
    None,
    'Star_Collector',
)


#### #### #### #### DLC 36 #### #### #### ####

CARD_TORRENT_OF_MAGIC = OJCard(
    196,
    'Torrent of Magic',
    2,
    CARD_COST_10,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Effect Duration: 3 Chapters.\n'
        'Gain +2 DEF. The maximum stacks of Hardened Scales are increased to 10.\n'
        'If you gain 10 stacks of Hardened Scales, all other players suffer KO.'
    ),
    '"Th-that\'s dangerous... I\'m sorry." ―Watty',
    None,
    'Torrent_of_Magic',
)

CARD_GOODEST_BOY = OJCard(
    197,
    'Goodest Boy',
    2,
    CARD_COST_20,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Effect duration: 3 Chapters\n'
        'Immune to instant KO effects. '
        'When staying on a panel with another player at the end of either player\'s turn, '
        'gain a copy of a random card in their hand. '
        'You can neither challenge nor be challenged; instead, opponents may stop to Pet you. Effect expires on KO.'
    ),
    '"*Whimper*" ―Pomeranius',
    None,
    'Goodest_Boy',
)


#### #### #### #### DLC 37 #### #### #### ####

CARD_OPERATION_A_MOUNTAIN_OF_SWEETS = OJCard(
    198,
    'Operation: A Mountain of Sweets',
    3,
    CARD_COST_0,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    'Draw 3 Boost cards from the deck. You can play up to 3 more Boost cards this turn for 1/3 of their cost.',
    '"Ehehe, let\'s have a lot of delicious sweets." ―Natsumi',
    None,
    'Operation_A_Mountain_of_Sweets',
)

CARD_SWEET_MAKERS_MAGIC = OJCard(
    199,
    'Sweet Maker\'s Magic',
    1,
    CARD_COST_10,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BATTLE,
    None,
    CARD_RARITY_NONE,
    'Heal 1 HP and gain +2 ATK per Sweets type card in hand during this battle. Discard all Sweets type cards.',
    '"Sweets power is the best!" ―Saki',
    None,
    'Sweet_Maker\'s_Magic',
)

CARD_SWEET_INDULGENCE = OJCard(
    200,
    'Sweet Indulgence',
    2,
    CARD_COST_0,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_TRAP,
    None,
    CARD_RARITY_NONE,
    'Turn all your cards into random non-Hyper, Sweets type cards.',
    '"I am about to stuff you with sweets, whether you like it or not." ―Sweet Creator',
    None,
    'Sweet_Indulgence',
)

CARD_SWEET_PARADISE = OJCard(
    201,
    'Sweet Paradise',
    2,
    CARD_COST_0,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_EVENT,
    None,
    CARD_RARITY_NONE,
    (
        'Move to your Home panel without activating it. '
        'Cannot be challenged or be the target of other players\' Boost cards. '
        'Immune to Trap cards, instant KO effects, and card damage from other players. '
        'Roll 2 dice for movement. Effect ends after traveling 20 panels.'
    ),
    '"This is the power of a Sweet God!" ―Sweet Creator',
    None,
    'Sweet_Paradise',
)


#### #### #### #### BASE GAME #### #### #### ####


CARD_CHRISTMAS_INFERNO = OJCard(
    202,
    'Christmas Inferno',
    3,
    CARD_COST_20,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_EVENT,
    None,
    CARD_RARITY_NONE,
    (
        'Lower your HP to 1. Deal damage to all other players equal to the HP you lost. '
        'Gain a Mio\'s Christmas Cake card for each player KO\'d by this effect.'
    ),
    '"I\'ll show you all hell." ―Mio',
    None,
    'Christmas_Inferno',
)


#### #### #### #### DLC 38 #### #### #### ####

CARD_MAKE_BELIEVE_PRISON_BREAK = OJCard(
    203,
    'Make-Believe Prison Break',
    1,
    CARD_COST_13,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Lower your HP to 1. Deal damage to all other players equal to the HP you lost. '
        'Gain a Mio\'s Christmas Cake card for each player KO\'d by this effect.'
    ),
    '"Pitter-patter, pitter-patter!" ―Mimyuu',
    None,
    'Make-Believe_Prison_Break',
)

CARD_THREATS_TO_MY_SLUMBER = OJCard(
    204,
    'Threats to My Slumber',
    1,
    CARD_COST_13,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_GIFT,
    None,
    CARD_RARITY_NONE,
    (
        'When you cancel exactly 1 damage in battle while holding this card, gain a stock of Waking. '
        '(Max 4. Does not stack.)\n'
        'Transform to When My Slumber Breaks upon use.'
    ),
    '"I suggest you keep quiet for your own safety..." ―Krilalaris',
    None,
    'Threats_to_My_Slumber',
)

CARD_WHEN_MY_SLUMBER_BREAKS = OJCard(
    205,
    'When My Slumber Breaks',
    2,
    CARD_COST_13,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_EVENT,
    None,
    CARD_RARITY_NONE,
    (
        'When you cancel exactly 1 damage in battle while holding this card, gain a stock of Waking. '
        '(Max 4. Does not stack.)\n'
        'Transform to When My Slumber Breaks upon use.'
    ),
    '"The time is about to come for me to say good morning..." ―Krilalaris',
    None,
    'When_My_Slumber_Breaks',
)


#### #### #### #### DLC 39 #### #### #### ####

CARD_MOTHER_POWER = OJCard(
    206,
    'Mother Power',
    1,
    CARD_COST_Lvx2,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Effect Duration: Player level.\n'
        'Gain Lvl x1 stars for every point of damage you take. '
        'If the effect ends or is replaced while active, heal to full HP.\n'
        'Effect ends on KO.'
    ),
    '"This is a Mother\'s love, poppo." ―Mother Poppo',
    None,
    'Mother_Power',
)

CARD_LULU_IS_AN_UNLUCKY_DRAGON = OJCard(
    207,
    'Lulu is an Unlucky Dragon',
    1,
    CARD_COST_10,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_EVENT,
    None,
    CARD_RARITY_NONE,
    (
        'Can only be played with 2 HP or less. Trigger one of the following effects at random:\n'
        '- Roll a die. All other players lose the die number x (their Lvl) stars.\n'
        '- All other players discard a card at random.\n'
        '- All other players\' HP is lowered to 2.'
    ),
    '"Lulu is... an unlucky dragon..." ―Dark Lulu',
    None,
    'Lulu_is_an_Unlucky_Dragon',
)


#### #### #### #### DLC 41 #### #### #### ####

CARD_ELLIES_HYPER_MIRACLE = OJCard(
    208,
    'Ellie\'s_Hyper_Miracle',
    3,
    CARD_COST_40,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Effect Duration: 2 chapters. '
        'Gain +X ATK in battle when attacker, and +X DEF and +X EVD when defender. '
        'X = your total Norma completed.'
    ),
    '"I\'ll show you my strongest power ♡" ―Hyper Ellie',
    None,
    'Ellie\'s_Hyper_Miracle',
)

CARD_EX_PROTAGONISTS_MOMENT_OF_GLORY = OJCard(
    209,
    'Ex-Protagonist\'s Moment of Glory',
    2,
    CARD_COST_Lvx10,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    'Lower your HP to 1. Effect Duration: 3 chapters. Gain +4 ATK and +5 EVD.',
    '"You can\'t make an adult go overboard." ―Hero Kai',
    None,
    'Ex-Protagonist\'s_Moment_of_Glory',
)


#### #### #### #### COMMUNITY CARD PACK 4 #### #### #### ####

CARD_NANAKOS_BITS = OJCard(
    210,
    'Nanako\'s Bit',
    1,
    CARD_COST_0,
    1,
    CARD_TYPE_GIFT,
    CARD_PACK_COMMUNITY_PACK_4,
    CARD_RARITY_UNCOMMON,
    (
        'Randomly gain +1 ATK, +1 DEF, or +1 EVD at the start of battle while this card is held, and lose 7 stars. '
        'This card is discarded upon KO or use.'
    ),
    '"What the heck are you doing!" ―Nanako',
    None,
    'Nanako\'s_Bit',
)

CARD_REBELLION = OJCard(
    211,
    'Rebellion',
    2,
    CARD_COST_20,
    1,
    CARD_TYPE_EVENT,
    CARD_PACK_COMMUNITY_PACK_4,
    CARD_RARITY_COMMON,
    (
        'Effect Duration: 3 chapters.\n'
        'All players will receive +1 ATK, +1 DEF, and +1 EVD when fighting a player with a higher Lvl than them.'
    ),
    '"The Guild will betray you before too long... Keep that in mind." ―Sherry',
    None,
    'Rebellion',
)

CARD_BANK_OF_POPPO = OJCard(
    212,
    'Bank of Poppo',
    1,
    CARD_COST_0,
    3,
    CARD_TYPE_TRAP,
    CARD_PACK_COMMUNITY_PACK_4,
    CARD_RARITY_COMMON,
    (
        'The first unit to activate this trap loses Lvl x10 stars. '
        'If any stars were lost, '
        'the trap stays on board and the lost stars are given to the next player to trigger the trap.'
    ),
    '"My money...!" ―Kai',
    None,
    'Bank_of_Poppo',
)

CARD_CONTENT_OF_CUTENESS = OJCard(
    213,
    'Contest of Cuteness',
    3,
    CARD_COST_5,
    1,
    CARD_TYPE_BATTLE,
    CARD_PACK_COMMUNITY_PACK_4,
    CARD_RARITY_UNCOMMON,
    (
        'May only be used by the attacker. The battle is decided by a contest of cuteness.\n'
        'Cuteness = 10 - Max HP - ATK + EVD, but no less than 0.\n'
        'Instead of rolling for attack, both units roll two dice and add the total to their Cuteness. '
        'If one unit has a higher Cuteness, they steal 5x the loser\'s Lvl stars and gain 1 Win. '
        'Then end the battle.\n'
        'Can only use against players.'
    ),
    '"Now tell us, who is the cutest here!?" ―Saki',
    None,
    'Contest_of_Cuteness',
)

CARD_MY_WILD_FRIENDS = OJCard(
    214,
    'My Wild Friends',
    2,
    CARD_COST_10,
    3,
    CARD_TYPE_BOOST,
    CARD_PACK_COMMUNITY_PACK_4,
    CARD_RARITY_COMMON,
    (
        'Summon a random friendly unit on your panel that is an available wild unit type. It gains 1 HP.\n'
        'The summon will challenge any enemies and gives half of the stars it gains to the summoner. '
        'Replaces any previous summon.'
    ),
    '"It\'s nice to relax once in a while." ―Teotoratta',
    None,
    'My_Wild_Friends',
)

CARD_WARP_CONTROL = OJCard(
    215,
    'Warp Control',
    1,
    CARD_COST_Lvx5,
    1,
    CARD_TYPE_BOOST,
    CARD_PACK_COMMUNITY_PACK_4,
    CARD_RARITY_RARE,
    'Upon activating the next Warp or Warp Move panel, choose another Warp or Warp Move panel to warp to.',
    '"There\'s a nice wind blowing around here!" ―Cook',
    None,
    'Warp_Control',
)

#### #### #### #### DLC 41 #### #### #### ####


CARD_HEART_OF_RESISTANCE = OJCard(
    216,
    'Heart of Resistance',
    2,
    CARD_COST_20,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_BOOST,
    None,
    CARD_RARITY_NONE,
    (
        'Target another active player. '
        'Next time they are challenged or challenge a unit while you are active, take their place in the battle. '
        'Gain +3 ATK, DEF and EVD at the start of the battle. '
        'You may only have this effect on one player at a time.'
    ),
    '"We just want to fly in the sky the way we want." ―Bourbon',
    None,
    'Heart_of_Resistance',
)

CARD_ALL_GUNS_AT_THE_READY = OJCard(
    217,
    'All Guns at the Ready',
    3,
    CARD_COST_30,
    -1,
    CARD_TYPE_HYPER | CARD_TYPE_EVENT,
    None,
    CARD_RARITY_NONE,
    (
        'Pay all stocked Cannonball Counters. Deal 1 damage to a random enemy. '
        'If the enemy is KO\'d, gain 1 Win and Stars equal to 10x their level. '
        'Repeat this once for every Cannonball Counter paid.'
    ),
    '"All guns at the ready... FIRE!" ―Grain',
    None,
    'All_Guns_at_the_Ready',
)

#### #### #### #### CHARACTERS #### #### #### ####

CHARACTER_QP = OJCharacter(1,
    'QP',
    5, 0, 0, 0, 5,
    ORIGIN_QP_SHOOTING,
    None,
    (CARD_HYPER_MODE,),
    'QP_(unit)',
)

CHARACTER_SUGURI = OJCharacter(2,
    'Suguri',
    4, 1, -1, 2, 5,
    ORIGIN_SUGURI,
    None,
    (CARD_ACCELERATOR,),
    'Suguri_(unit)',
)

CHARACTER_MARC = OJCharacter(3,
    'Marc',
    4, 1, 1, -1, 5,
    ORIGIN_FLYING_RED_BARREL,
    None,
    (CARD_X16_BIG_ROCKET,),
    'Marc_(unit)',
)

CHARACTER_KAI = OJCharacter(4,
    'Kai',
    5, 1, 0, 0, 5,
    ORIGIN_100_ORANGE_JUICE,
    None,
    (CARD_PROTAGONISTS_PRIVILEGE,),
    'Kai_(unit)',
)

CHARACTER_YUKI = OJCharacter(5,
    'Yuki',
    5, 2, -1, -1, 5,
    ORIGIN_QP_SHOOTING,
    None,
    (CARD_GAMBLE,),
    'Yuki_(unit)',
)

CHARACTER_ARU = OJCharacter(6,
    'Aru',
    5, -1, -1, 2, 5,
    ORIGIN_CHRISTMAS_SHOOTING,
    'Can hold 4 cards.',
    (CARD_PRESENT_FOR_YOU,),
    'Aru_(unit)',
)

CHARACTER_HIME = OJCharacter(7,
    'Hime',
    5, 1, -1, 1, 5,
    ORIGIN_SUGURI,
    None,
    (CARD_BINDING_CHAINS,),
    'Hime_(unit)',
)

CHARACTER_SORA = OJCharacter(8,
    'Sora',
    4, 1, 0, 1, 5,
    ORIGIN_SORA,
    None,
    (CARD_EXTRAORDINARY_SPECS,),
    'Sora_(unit)',
)

CHARACTER_FERNET = OJCharacter(9,
    'Fernet',
    6, -1, 2, -2, 5,
    ORIGIN_FLYING_RED_BARREL,
    None,
    (CARD_AIR_STRIKE,),
    'Fernet_(unit)',
)

CHARACTER_PEAT = OJCharacter(10,
    'Peat',
    3, 1, 1, 1, 4,
    ORIGIN_FLYING_RED_BARREL,
    None,
    (CARD_BLUE_CROW_THE_SECOND,),
    'Peat_(unit)',
)

CHARACTER_MARIE_POPPO = OJCharacter(11,
    'Marie Poppo',
    7, -1, -1, -1, 5,
    ORIGIN_100_ORANGE_JUICE,
    None,
    (CARD_UBIQUITOUS,),
    'Marie_Poppo_(unit)',
)

CHARACTER_TOMOMO_UNSOFTENED = OJCharacter(12,
    'Tomomo (Unsoftened)',
    6, 2, 0, 1, 6,
    ORIGIN_100_ORANGE_JUICE,
    None,
    (CARD_MAGICAL_MASSACRE,),
    'Tomomo_(Softened)_(unit)',
)

CHARACTER_TOMOMO_SOFTENED = OJCharacter(13,
    'Tomomo (Softened)',
    4, 2, 0, 0, 6,
    ORIGIN_100_ORANGE_JUICE,
    'Softened: Tomomo is playing with friends, and has lowered her attributes.',
    (CARD_MAGICAL_MASSACRE,),
    'Tomomo_(Softened)_(unit)',
)

CHARACTER_MIO = OJCharacter(14,
    'Mio',
    6, 0, -1, 1, 4,
    ORIGIN_100_ORANGE_JUICE,
    None,
    (CARD_MAGICAL_INFERNO,),
    'Mio_(unit)',
)

CHARACTER_SYURA = OJCharacter(15,
    'Syura',
    4, 0, 1, 0, 4,
    ORIGIN_QP_SHOOTING_DANGEROUS,
    'When at 1 HP at the start of a battle, gain +1 ATK and +1 EVD until the end of the battle.',
    (CARD_BEYOND_HELL,),
    'Syura_(unit)',
)

CHARACTER_NANAKO = OJCharacter(16,
    'Nanako',
    3, 0, 2, 1, 4,
    ORIGIN_SUGURI,
    None,
    (CARD_DEPLOY_BITS,),
    'Nanako_(unit)',
)

CHARACTER_SAKI = OJCharacter(17,
    'Saki',
    4, 0, 0, 1, 4,
    ORIGIN_SUGURI,
    None,
    (CARD_BIG_BANG_BELL,),
    'Saki_(unit)',
)

CHARACTER_KYOUSUKE = OJCharacter(18,
    'Kyousuke',
    5, -1, 2, 0, 5,
    ORIGIN_QP_KISS,
    None,
    (CARD_CAST_OFF,),
    'Kyousuke_(unit)',
)

CHARACTER_KRILALARIS = OJCharacter(19,
    'Krilalaris',
    6, 0, 0, -1, 5,
    ORIGIN_QP_SHOOTING_DANGEROUS,
    None,
    (CARD_PLUSHIE_MASTER, CARD_DANCE_LONG_EARED_BEASTS),
    'Krilalaris_(unit)',
)

CHARACTER_KAE = OJCharacter(20,
    'Kae',
    4, 0, -1, 1, 4,
    ORIGIN_SUGURI,
    'Add reverse value of DEF to ATK. Gain -1 DEF when attacking.',
    (CARD_BLAZING,),
    'Kae_(unit)',
)

CHARACTER_ALTE = OJCharacter(21,
    'Alte',
    5, 0, -1, 1, 5,
    ORIGIN_SORA,
    'In battle, see a random card from the opponent\'s hand. On Self-destruct, gain +1 ATK (up to +3).',
    (CARD_SELF_DESTRUCT,),
    'Alte_(unit)',
)

CHARACTER_KYOKO = OJCharacter(22,
    'Kyoko',
    5, -1, 3, -2, 5,
    ORIGIN_SUGURI,
    'Cannot use the Evade command in battle.',
    (CARD_CRYSTAL_BARRIER,),
    'Kyoko_(unit)',
)

CHARACTER_SHAM = OJCharacter(23,
    'Sham',
    4, 0, 1, 1, 5,
    ORIGIN_SORA,
    None,
    (CARD_DELTA_FIELD,),
    'Sham_(unit)',
)

CHARACTER_SHERRY = OJCharacter(24,
    'Sherry',
    5, 1, 1, 1, 5,
    ORIGIN_FLYING_RED_BARREL,
    'Enemy always goes first. If the enemy is Sherry, ignore this effect.',
    (CARD_WHIMSICAL_WINDMILL,),
    'Sherry_(unit)',
)

CHARACTER_STAR_BREAKER = OJCharacter(25,
    'Star Breaker',
    5, 2, 0, -1, 5,
    ORIGIN_SORA,
    'Can only choose Wins norma.',
    (CARD_STAR_BLASTING_FUSE, CARD_INVISIBLE_BOMB),
    'Star_Breaker_(unit)',
)

CHARACTER_SWEET_BREAKER = OJCharacter(26,
    'Sweet breaker',
    6, 0, 0, 0, 6,
    ORIGIN_QP_SHOOTING_DANGEROUS,
    'When battling a player with reversed cards, gain +1 to ATK, DEF and EVD for each.',
    (CARD_MELTING_MEMORIES,),
    'Sweet_Breaker_(unit)',
)

CHARACTER_NATH = OJCharacter(27,
    'Nath',
    5, -1, -1, 1, 5,
    ORIGIN_SORA,
    'Gain 1 stack of Active Extension in each battle where a battle card is played (max 3). Lose 1 stack on KO. '
    'Stock Effect: gain +1 ATK, +1 DEF, and -1 EVD.',
    (CARD_ANOTHER_ULTIMATE_WEAPON,),
    'Nath_(unit)',
)

CHARACTER_MIMYUU = OJCharacter(
    28,
    'Mimyuu',
    3,
    -1,
    0,
    1,
    1,
    ORIGIN_QP_SHOOTING,
    (
        'Revive as Tomato. When you do, you may challenge any enemies on the same panel. '
        'Lose 1/4 stars and give 1 Win when KO\'d in battle.'
    ),
    (CARD_EVIL_SPY_WORK_PREPARATION, CARD_EVIL_SPY_WORK_EXECUTION,),
    'Mimyuu_(unit)',
)

CHARACTER_TOMATO = OJCharacter(
    29,
    'Tomato',
    3,
    1,
    0,
    0,
    3,
    ORIGIN_QP_SHOOTING,
    (
        'Revive as Mimyuu and act on revival.\n'
        'Lose 1/3 stars when KO\'d in battle. Draw Evil Spy Work - Execution cards as Waruda Machine, Blast Off!'
    ),
    (CARD_WARUDA_MACHINE_BLAST_OFF,),
    'Tomato_(unit)',
)

CHARACTER_KIRIKO = OJCharacter(30,
    'Kiriko',
    8, 0, -1, 0, 5,
    ORIGIN_XMAS_SHOOTING_SCRAMBLE,
    'Ignore healing effects. When playing a battle card, gain +1 ATK & EVD in battle, and MAX HP is reduced by 1 '
    '(To a minimum of 2).',
    (CARD_FINAL_SURGERY,),
    'Kiriko_(unit)',
)

CHARACTER_NONAME = OJCharacter(31,
    'NoName',
    5, 1, -1, 0, 6,
    ORIGIN_ACCELERATION_OF_SUGURI,
    'If KO\'d, turn into NoName (Head) instead. Give no stars or Wins if KO\'d in battle.',
    (CARD_OVERSEER,),
    'NoName_(unit)',
)

CHARACTER_NONAME_HEAD = OJCharacter(32,
    'NoName (Head)',
    2, -1, -1, -1, 6,
    ORIGIN_ACCELERATION_OF_SUGURI,
    'Change into NoName after reaching a home or getting KO\'d. Gain -1 MOV.',
    (CARD_OVERSEER,),
    'NoName_(Head)_(unit)',
)

CHARACTER_MIUSAKI = OJCharacter(33,
    'Miusaki',
    4, 1, -2, 0, 5,
    ORIGIN_ALICIANRONE,
    'When using Defend in battle, never take more than 2 damage at once.',
    (CARD_SOLID_WITCH,),
    'Miusaki_(unit)',
)

CHARACTER_CEOREPARQUE = OJCharacter(34,
    'Ceoreparque',
    4, 0, 0, 1, 5,
    ORIGIN_ALICIANRONE,
    'On successful Evasion, deal 1 damage to opponent.',
    (CARD_WITCHS_HAIR_LOCK,),
    'Ceoreparque_(unit)',
)

CHARACTER_YUKI_DANGEROUS = OJCharacter(35,
    'Yuki (Dangerous)',
    5, 1, -2, 0, 5,
    ORIGIN_QP_SHOOTING_DANGEROUS,
    'Permanently turn every help card with Pudding in name into Tragedy in the Dead of Night.\n'
    'When someone else triggers your trap, gain 1 Win. Gain no wins from fighting neutral enemies.',
    (CARD_EVIL_MASTERMIND,),
    'Yuki_(Dangerous)_(unit)',
)

CHARACTER_TOMOMO_CASUAL = OJCharacter(36,
    'Tomomo (Casual)',
    4, -1, 0, 1, 5,
    ORIGIN_100_ORANGE_JUICE,
    None,
    (CARD_MIRACLE_RED_BEAN_ICE_CREAM,),
    'Tomomo_(Casual)_(unit)',
)

CHARACTER_TOMOMO_SWEET_EATER = OJCharacter(37,
    'Tomomo (Sweet Eater)',
    6, 3, 0, 0, 6,
    ORIGIN_100_ORANGE_JUICE,
    'When KO\'d, discard your hand and turn back to Tomomo (Casual).',
    (CARD_MAGICAL_REVENGE,),
    'Tomomo_(Sweet_Eater)_(unit)',
)

CHARACTER_TEQUILA = OJCharacter(38,
    'Tequila',
    5, 0, 1, -3, 6,
    ORIGIN_FLYING_RED_BARREL,
    'A Pirate Crew Member appears as enemy unit. Gain +1 ATK for every HP lost during a battle.',
    (CARD_DO_PIRATES_FLY_IN_THE_SKY, CARD_FLYING_PIRATE),
    'Tequila_(unit)',
)

CHARACTER_TSIH = OJCharacter(39,
    'Tsih',
    4, 0, -1, 2, 5,
    ORIGIN_SORA,
    'Gain +2 ATK if holding a Gift card.',
    (CARD_STEALTH_ON,),
    'Tsih_(unit)',
)

CHARACTER_MEI = OJCharacter(40,
    'Mei',
    4, 0, 0, 0, 5,
    ORIGIN_QP_SHOOTING,
    'Gain "Red & Blue" when holding no cards at the end of turn.',
    (CARD_TRUE_WHITE_CHRISTSMASHER, CARD_WHITE_CHRISTSMASHER),
    'Mei_(unit)',
)

CHARACTER_NATSUMI = OJCharacter(41,
    'Natsumi',
    5, 0, -1, 0, 5,
    ORIGIN_XMAS_SHOOTING_SCRAMBLE,
    'If not KO\'d and standing on the same panel with other players at the end of your turn, each unit on the panel '
    'recovers 1 HP. For each other players you heal, gain 5 stars.',
    (CARD_COOKING_TIME,),
    'Natsumi_(unit)',
)

CHARACTER_NICO = OJCharacter(42,
    'Nico',
    4, 0, 0, 1, 5,
    ORIGIN_XMAS_SHOOTING_SCRAMBLE,
    'No effect from Gift cards. Gain X additional stars from all sources, where X is the number of Gift cards in hand. '
    'Can hold 4 cards.',
    (CARD_MIRACLE_WALKER,),
    'Nico_(unit)',
)

CHARACTER_ARTHUR = OJCharacter(43,
    'Arthur',
    7, 0, -1, -1, 6,
    ORIGIN_CHRISTMAS_SHOOTING,
    'Gain X additional stars from Bonus panels and Shops, where X is the number of Shops in play, up to current Lvl.',
    (CARD_BRANCH_EXPANSION_STRATEGY, CARD_RBIT_HOBBY_SHOP),
    'Arthur_(unit)',
)

CHARACTER_IRU = OJCharacter(44,
    'Iru',
    5, 0, 0, 0, 5,
    ORIGIN_SUGURI,
    'When challenging an enemy, they take 1 damage. KO from this effect counts as battle KO.',
    (CARD_EXTENDED_PHOTON_RIFLE,),
    'Iru_(unit)',
)

CHARACTER_MIRA = OJCharacter(45,
    'Mira',
    5, 1, -1, 1, 5,
    ORIGIN_SORA,
    'Your traps triggered by enemies add the following additional effect: Binding Smoke (For 2 chapters: Move rolls '
    'are limited to 1, 2, or 3).',
    (CARD_LEAP_THROUGH_SPACE, CARD_LEAP_THROUGH_SPACE_MARKING),
    'Mira_(unit)',
)

CHARACTER_CUTIES = OJCharacter(46,
    'Cuties',
    4, 0, 0, 1, 5,
    ORIGIN_SORA,
    (
        'Can only choose Stars norma. Gain X additional stars from bonus panels, '
        'where X is the number of different Event cards you played. In battle, randomly gain +1 ATK or DEF.'
    ),
    (CARD_SPECIAL_STAGE,),
    'Sora_&_Sham_(Cuties)_(unit)',
)

CHARACTER_YUUKI = OJCharacter(47,
    'Yuuki',
    4, 0, 0, 0, 5,
    ORIGIN_QP_SHOOTING,
    'In odd-numbered chapters, gain -1 ATK and +2 in DEF. In even-numbered chapters, gain +2 ATK and -1 DEF.',
    (CARD_ANGEL_HAND, CARD_DEVIL_HAND),
    'Yuuki_(unit)',
)

CHARACTER_ISLAY = OJCharacter(48,
    'Islay',
    5, 1, 1, 1, 5,
    ORIGIN_FLYING_RED_BARREL,
    'Cannot challenge to battle.',
    (CARD_RIVAL,),
    'Islay_(unit)',
)

CHARACTER_SUGURI_46_BILLION_YEARS = OJCharacter(
    49,
    'Suguri (46 Billion Years)',
    4,
    0,
    0,
    2,
    5,
    ORIGIN_200_MIXED_JUICE,
    (
        'When playing a damage dealing Boost/Event card, '
        'gain +1 ATK until end of turn and +1 die to your next movement roll. '
        'You may pay 1.5x its cost (rounded up) to double its damage.'
    ),
    (CARD_OBSERVER_OF_ETERNITY,),
    'Suguri_(46_Billion_Years)_(unit)',
)

CHARACTER_SUMIKA = OJCharacter(50,
    'Sumika',
    5, 1, -1, 1, 5,
    ORIGIN_200_MIXED_JUICE,
    None,
    (CARD_REPRODUCTION_OF_RECORDS,),
    'Sumika_(unit)',
)

CHARACTER_ELLIE = OJCharacter(51,
    'Ellie',
    5, 1, 0, 0, 5,
    ORIGIN_100_ORANGE_JUICE,
    None,
    (CARD_ELLIES_MIRACLE,),
    'Ellie_(unit)',
)

CHARACTER_LULU = OJCharacter(52,
    'Lulu',
    5, 0, 1, -1, 5,
    ORIGIN_100_ORANGE_JUICE,
    None,
    (CARD_LULUS_LUCKY_EGG,),
    'Lulu_(unit)',
)

CHARACTER_ALICIANRONE = OJCharacter(53,
    'Alicianrone',
    4, 1, -1, 1, 5,
    ORIGIN_ALICIANRONE,
    (
        'When battling an opponent with +1 or more ATK, gain +1 EVD until end of battle. If they have more +2 or more '
        'ATK, gain an additional +1 EVD.'
    ),
    (CARD_FULL_SPEED_ALICIANRONE,),
    'Alicianrone_(unit)',
)

CHARACTER_TEOTORATTA = OJCharacter(54,
    'Teotoratta',
    5, 0, 0, 1, 4,
    ORIGIN_ALICIANRONE,
    'Do not trigger Encounter panels.',
    (CARD_BEAST_WITCH,),
    'Teotoratta_(unit)',
)

CHARACTER_ARNELLE = OJCharacter(55,
    'Arnelle',
    5, 1, -1, 0, 5,
    ORIGIN_100_ORANGE_JUICE,
    'Can see the card on the top of the deck when holding Intelligence Officer in hand.',
    (CARD_INTELLIGENCE_OFFICER,),
    'Arnelle_(unit)',
)

CHARACTER_MAYNIE = OJCharacter(56,
    'Maynie',
    4, 0, 1, 0, 5,
    ORIGIN_100_ORANGE_JUICE,
    'When not in Raging Mode, gain a rage Counter upon taking damage and lose a rage Counter upon healing.',
    (CARD_RAGING_MADNESS,),
    'Maynie_(unit)',
)

CHARACTER_CHRIS = OJCharacter(57,
    'Chris',
    5, -1, 0, 0, 5,
    ORIGIN_QP_SHOOTING,
    'Can hold 4 cards. Cannot challenge to battles without Chef or Store manager active. Gain a Store manager Counter '
    'upon using a Max 1 copy limit non-Gift card.',
    (CARD_CHEF_I_COULD_USE_SOME_HELP, CARD_MANAGER_I_COULD_USE_SOME_HELP),
    'Chris_(unit)',
)

CHARACTER_KYUPITA = OJCharacter(58,
    'Kyupita',
    5, 0, 0, 0, 5,
    ORIGIN_QP_KISS,
    None,
    (CARD_SAINT_EYES,),
    'Kyupita_(unit)',
)

CHARACTER_QP_DANGEROUS = OJCharacter(
    59,
    'QP (Dangerous)',
    5,
    0,
    0,
    -1,
    5,
    ORIGIN_QP_SHOOTING_DANGEROUS,
    (
        'Gain combat bonuses from carrying cards with \'Pudding\' in their name.\n'
        'Dangerous Pudding (+1ATK) Bad Pudding (+1DEF) Pudding (+1EVD) Portable Pudding (Heal 1 for battle KO)'
    ),
    (CARD_SWEET_GUARDIAN,),
    'QP_(Dangerous)_(unit)',
)

CHARACTER_MARIE_POPPO_MIXED = OJCharacter(60,
    'Marie Poppo (Mixed)',
    7, -1, -1, -1, 5,
    ORIGIN_200_MIXED_JUICE,
    'When warping from any effect: If player level is odd, gain Lvl x3 in stars. If player level is even, draw a card.',
    (CARD_SUBSPACE_TUNNEL,),
    'Marie_Poppo_(Mixed)_(unit)',
)

CHARACTER_SORA_MILITARY = OJCharacter(61,
    'Sora (Military)',
    4, 1, 0, 1, 5,
    ORIGIN_SORA,
    'When KO\'d in battle, revive with 2 HP on the next turn.',
    (CARD_AWAKENING_OF_TALENT,),
    'Sora_(Military)_(unit)',
)

CHARACTER_ARU_SCRAMBLE = OJCharacter(62,
    'Aru (Scramble)',
    5, -1, -1, 2, 5,
    ORIGIN_XMAS_SHOOTING_SCRAMBLE,
    'Can hold 4 cards.',
    (CARD_SANTAS_JOB,),
    'Aru_(Scramble)_(unit)',
)
        
CHARACTER_SUGURI_VER_2 = OJCharacter(63,
    'Suguri (Ver.2)',
    5, 1, -1, 2, 5,
    ORIGIN_ACCELERATION_OF_SUGURI_2,
    'Can hold 2 cards. Restore 1 HP at the start of every turn.',
    (CARD_REVIVAL_OF_STARS,),
    'Suguri_(Ver.2)_(unit)',
)
        
CHARACTER_MARC_PILOT = OJCharacter(64,
    'Marc (Pilot)',
    4, 1, 1, 1, 5,
    ORIGIN_FLYING_RED_BARREL,
    None,
    (CARD_BIG_ROCKET_CANNON, CARD_ROCKET_CANNON),
    'Marc_(Pilot)_(unit)',
)
        
CHARACTER_CHICKEN = OJCharacter(65,
    'Chicken',
    3, -1, -1, 1, 3,
    ORIGIN_QP_SHOOTING,
    'Lose 1/4 stars and given 1 WIn when KO\'d in battle.',
    (CARD_GOLDEN_EGG,),
    'Chicken_(unit)',
)
        
CHARACTER_ROBO_BALL = OJCharacter(66,
    'Robo Ball',
    3, -1, 1, -1, 4,
    ORIGIN_SUGURI,
    'Lose 1/4 stars and given 1 WIn when KO\'d in battle.',
    (CARD_REFLECTIVE_SHELL,),
    'Robo_Ball_(unit)',
)
        
CHARACTER_SEAGULL = OJCharacter(67,
    'SeaGull',
    3, -1, 1, -1, 4,
    ORIGIN_FLYING_RED_BARREL,
    'Lose 1/4 stars and given 1 WIn when KO\'d in battle.',
    (CARD_JONATHAN_RUSH,),
    'Seagull_(unit)',
)
        
CHARACTER_STORE_MANAGER = OJCharacter(68,
    'Store Manager',
    6, 2, 0, -1, 6,
    ORIGIN_QP_SHOOTING,
    'No stars from bonus panel. Can only use Gift type cards. Takes 1 damage on card discard.',
    (CARD_BANNER_FOR_LIFE,),
    'Store_Manager_(unit)',
)
        
CHARACTER_SHIFU_ROBOT = OJCharacter(69,
    'Shifu Robot',
    5, 1, 0, -1, 0,
    ORIGIN_SUGURI,
    (
        'Start and Auto-Revive with 1 HP and a 1 HP Absorptive Shell.\n'
        'Auto-Repair: At the start of your turn, every 3rd chapter, heal 1 HP and remove Absorptive Shell.\n'
        'Revive with -1 MOV for 2 chapters.'
    ),
    (CARD_TURBO_CHARGED,),
    'Shifu_Robot_(unit)',
)

CHARACTER_FLYING_CASTLE = OJCharacter(70,
    'Flying Castle',
    8, 1, -1, -2, 6,
    ORIGIN_FLYING_RED_BARREL,
    'Immune to Battle Cards when defending Cannot Counterattack.',
    (CARD_IMMOVABLE_OBJECT,),
    'Flying_Castle_(unit)',
)

#### #### #### #### DLC 30 #### #### #### ####

CHARACTER_HALENA = OJCharacter(71,
    'Halena',
    5, -1, +1, +1, 5,
    ORIGIN_100_ORANGE_JUICE,
    'Gain Lvl x2 stars after landing on your own home.',
    (CARD_SAFE_JOURNEY,),
    'Halena_(unit)',
)

CHARACTER_COOK = OJCharacter(72,
    'Cook',
    4, 0, -1, +3, 5,
    ORIGIN_100_ORANGE_JUICE,
    'Gain a stack of Hungry when using Evade (max 3). With 3 Hungry, gain -1 EVD. Lose all Hungry when landing on '
    'your own home.',
    (CARD_GUIDANCE_OF_THE_WEATHERCOCK,),
    'Cook_(unit)',
)

#### #### #### #### DLC 31 #### #### #### ####

CHARACTER_LONE_RIDER = OJCharacter(73,
    'Lone Rider',
    5, 0, 0, -1, 5,
    ORIGIN_FLYING_RED_BARREL,
    'If your Move roll result is higher than 6, gain +1 ATK, +1 DEF and +2 EVD until the start of your next turn.',
    (CARD_UPSHIFT,),
    'Lone_Rider_(unit)',
)

CHARACTER_MERCHANT = OJCharacter(74,
    'Merchant',
    5, 0, 0, 0, 6,
    ORIGIN_FLYING_RED_BARREL,
    'Can hold 4 cards.\n'
    'Gain a Freight card when stopping on another player\'s Home panel.',
    (CARD_ZEALOUS_SALESMAN,),
    'Merchant_(unit)',
)

#### #### #### #### DLC 32 #### #### #### ####

CHARACTER_HIME_MOONLIGHT = OJCharacter(75,
    'Hime (Moonlight)',
    5, +1, -2, +2, 5,
    ORIGIN_SUGURI,
    'During full moon (every 5 chapters), base attributes are -1 ATK, -1 DEF, +3 EVD..',
    (CARD_DANCE_IN_THE_MOONLIT_NIGHT,),
    'Hime_(Moonlight)_(unit)',
)

FERNET_NOBLE = OJCharacter(76,
    'Fernet (Noble)',
    6, -1, +1, -1, 5,
    ORIGIN_FLYING_RED_BARREL,
    'Any player challenging you on the field must pay their Lvl x Stars to do so.',
    (CARD_NEW_NOBILITY, CARD_AFFLUENCE_X,),
    'Fernet_(Noble)_(unit)',
)


#### #### #### #### DLC 33 #### #### #### ####

CHARACTER_MALT = OJCharacter(
    77,
    'Malt',
    5,
    +1,
    +1,
    +1,
    5,
    ORIGIN_FLYING_RED_BARREL,
    (
        'Give 3 Wins when KO\'d in battle. Cannot challenge other units when meeting them on the field. '
        'Can set a Battle card without special use requirements as a Trap card without paying its '
        'cost. When another enemy steps on it, they will battle you and both player units gain the card\'s effect. '
        'No other battle cards can be played in this battle.'
    ),
    (CARD_TWILIGHT_COLORED_DREAM,),
    'Lone_Rider_(unit)',
)

CHARACTER_MESCAL = OJCharacter(
    78,
    'Mescal',
    4,
    0,
    +1,
    +1,
    5,
    ORIGIN_FLYING_RED_BARREL,
    (
        'When challenged to a battle, there is a 50% chance a Pirate Crew Member will fight in your place. '
        'If this Pirate Crew Member is KO\'d in battle, it will not fight for you for 3 chapters. '
        'Pirate Crew Member gives 1 Win on KO and gives stars gained in battle to your unit.'
    ),
    (CARD_LITTLE_MAGNUM,),
    'Mescal_(unit)',
)


#### #### #### #### DLC 34 #### #### #### ####

CHARACTER_SHIFU = OJCharacter(
    79,
    'Shifu',
    8,
    0,
    -2,
    0,
    5,
    ORIGIN_SUGURI,
    'Deal +2 battle damage to robotic wild units. When a robotic wild unit defeats an opposing player, gain 1 Win.',
    (CARD_IDEAL_WORLD,),
    'Shifu_(unit)',
)


CHARACTER_HOSHINO_REIKA = OJCharacter(
    80,
    'Hoshino Reika',
    3,
    +2,
    0,
    0,
    5,
    ORIGIN_200_MIXED_JUICE,
    (
        'Can only choose Stars norma.\n'
        'Gain +1 star from all sources except for chapter bonus or from Star Collector.'
    ),
    (CARD_STAR_COLLECTOR,),
    'Hoshino_Reika_(unit)',
)


#### #### #### #### DLC 36 #### #### #### ####

CHARACTER_WATTY = OJCharacter(
    81,
    'Watty',
    5,
    -3,
    +1,
    0,
    5,
    ORIGIN_100_ORANGE_JUICE,
    (
        'After battle, gain 1 stack of Hardened Scales for each point of damage reduced by using Defend (max 5).\n'
        '(For 3 Chapters: gain +1 ATK per stack. Effect expires on KO).'
    ),
    (CARD_TORRENT_OF_MAGIC,),
    'Watty_(unit)',
)

CHARACTER_POMERANIUS = OJCharacter(
    82,
    'Pomeranius',
    5,
    +1,
    -1,
    0,
    5,
    ORIGIN_100_ORANGE_JUICE,
    'Ignore any Trap card landed on when your HP is full or higher.',
    (CARD_GOODEST_BOY,),
    'Pomeranius_(unit)',
)


#### #### #### #### DLC 37 #### #### #### ####

CHARACTER_NATSUMI_SWEET_BLOGGER = OJCharacter(
    83,
    'Natsumi (Sweet Blogger)',
    5,
    -1,
    +1,
    +1,
    5,
    ORIGIN_XMAS_SHOOTING_SCRAMBLE,
    (
        'All Sweets type cards are free to play. '
        'If active after activating a Drop panel, draw a Sweets type card of usable level.'
    ),
    (CARD_OPERATION_A_MOUNTAIN_OF_SWEETS,),
    'Natsumi_(Sweet_Blogger)_(unit)',
)

CHARACTER_SAKE_SWEET_MAKER = OJCharacter(
    84,
    'Saki (Sweet Maker)',
    5,
    0,
    +1,
    -1,
    5,
    ORIGIN_SUGURI,
    'If active after activating an Encounter panel, draw a Sweets type card of usable level.',
    (CARD_SWEET_MAKERS_MAGIC,),
    'Saki_(Sweet_Maker)_(unit)',
)

CHARACTER_SWEET_CREATOR = OJCharacter(
    85,
    'Sweet Creator',
    4,
    0,
    +1,
    +1,
    5,
    ORIGIN_100_ORANGE_JUICE,
    (
        'When anyone else plays a Sweets type non-trap card, or activates a Sweets type trap card, '
        'gain stars equal to 2x Lvl of the card.'
    ),
    (CARD_SWEET_PARADISE, CARD_SWEET_INDULGENCE),
    'Sweet_Creator_(unit)',
)


#### #### #### #### BASE GAME #### #### #### ####

CHARACTER_MIO_FESTIVE = OJCharacter(
    86,
    'Mio (Festive)',
    5,
    +2,
    -2,
    0,
    5,
    ORIGIN_100_ORANGE_JUICE,
    None,
    (CARD_CHRISTMAS_INFERNO),
    'Mio_Festive_(unit)',
)


#### #### #### #### DLC 38 #### #### #### ####

CHARACTER_MIMYUU_JAILBIRD = OJCharacter(
    87,
    'Mimyuu (Jailbird)',
    4,
    +1,
    0,
    +1,
    4,
    ORIGIN_QP_SHOOTING,
    'When KO\'d in battle, move to your Home panel.',
    (CARD_MAKE_BELIEVE_PRISON_BREAK,),
    'Mimyuu_(Jailbird)_(unit)',
)

CHARACTER_KRILALARISLARIS_PAJAMAS = OJCharacter(
    88,
    'Krilalaris (Pajamas)',
    4,
    0,
    1,
    0,
    6,
    ORIGIN_QP_SHOOTING_DANGEROUS,
    (
        'Cannot use the Evade command in battle. '
        'If you would take 1 damage while using the Defend command, '
        'cancel that damage and pay your Lvl x stars to the opponent.'
    ),
    (CARD_THREATS_TO_MY_SLUMBER, CARD_WHEN_MY_SLUMBER_BREAKS),
    'Krilalaris_(Pajamas)_(unit)',
)


#### #### #### #### DLC 39 #### #### #### ####

CHARACTER_MOTHER_POPPO = OJCharacter(
    89,
    'Mother Poppo',
    7,
    -1,
    -1,
    -1,
    5,
    ORIGIN_100_ORANGE_JUICE,
    'When warping, take 1 damage. If active after warping, draw a card and gain Lvl x1 stars.',
    (CARD_MOTHER_POWER,),
    'Mother_Poppo_(unit)',
)

CHARACTER_DARK_LULU = OJCharacter(
    90,
    'Dark Lulu',
    5,
    +1,
    +1,
    -1,
    6,
    ORIGIN_100_ORANGE_JUICE,
    'Lose your Lvl x2 stars when declining a challenge.',
    (CARD_LULU_IS_AN_UNLUCKY_DRAGON,),
    'Dark_Lulu_(unit)',
)


#### #### #### #### DLC 41 #### #### #### ####

CHARACTER_HYPER_ELLIE = OJCharacter(
    91,
    'Hyper Ellie',
    4,
    +1,
    0,
    0,
    4,
    ORIGIN_100_ORANGE_JUICE,
    'Gain +1 ATK, -1 DEF and -1 EVD in battle when attacker.',
    (CARD_ELLIES_HYPER_MIRACLE,),
    'Hyper_Ellie_(unit)',
)

CHARACTER_KAI_HERO = OJCharacter(
    92,
    'Kai (Hero)',
    5,
    +1,
    0,
    0,
    5,
    ORIGIN_100_ORANGE_JUICE,
    (
        'If you would go under 1 HP from out of battle damage, stay on 1 HP. '
        'If you are still at 1 HP at the next end of your turn, suffer KO.'
    ),
    (CARD_EX_PROTAGONISTS_MOMENT_OF_GLORY,),
    'Kai_(Hero)_(unit)',
)


#### #### #### #### DLC 42 #### #### #### ####

CHARACTER_BOURBON = OJCharacter(
    93,
    'Bourbon',
    7,
    0,
    +1,
    -1,
    6,
    ORIGIN_FLYING_RED_BARREL,
    'Every time you take damage in battle, lose 1 max HP (down to 3) until KO\'d.',
    (CARD_HEART_OF_RESISTANCE,),
    'Bourbon_(unit)',
)

CHARACTER_GRAIN = OJCharacter(
    94,
    'Grain',
    5,
    +1,
    +2,
    -2,
    6,
    ORIGIN_FLYING_RED_BARREL,
    '-1 MOV. Gain a Cannonball Counter upon playing a card (max 9).',
    (CARD_ALL_GUNS_AT_THE_READY,),
    'Bourbon_(unit)',
)


#### #### #### #### COMMANDS #### #### #### ####

@MAIN_CLIENT.interactions(guild = GUILD__STORAGE)
async def create_images(client, event):
    await client.interaction_response_message_create(event, 'Starting to create images.\nIt may take some time.')
    
    relation = []
    
    for entity in (*CHARACTERS.values(), *CARDS.values()):
        card_name = entity.card_name
        
        image_path = join_paths(PATH__KOISHI, 'koishi', 'oj_data', card_name + '.png')
        
        if not exists(image_path):
            raise abort(f'{image_path!r} do not exists.')
        
        with (await ReuAsyncIO(image_path)) as io:
            message = await client.interaction_followup_message_create(event, file = io)
        
        relation.append((card_name, message.attachment.url))
    
    file_parts = []
    file_parts.append('RELATIONS = {\n')
    
    for card_name, url in relation:
        file_parts.append('    \'')
        file_parts.append(card_name.replace('\'', '\\\''))
        file_parts.append('\': ')
        file_parts.append(repr(url))
        file_parts.append(',\n')
    
    file_parts.append('}\n')
    
    file = ''.join(file_parts)
    
    await client.interaction_followup_message_create(
        event,
        'Please copy the file\'s content',
        file = ('relations.py', file),
    )


CHARACTERS_BY_NAME = {character.name: character for character in CHARACTERS.values()}
CARDS_BY_NAME = {card.name: card for card in CARDS.values()}
CARD_PACK_BY_NAME = {card_pack.name: card_pack for card_pack in CARD_PACKS.values()}

CARD_COSTS_NAMES_SORTED = [card_cost.string for card_cost in sorted(CARD_COST_STRING_TO_ENTITY.values())]

CARD_PACK_NAMES_SORTED_BY_COST = [
    card_pack.name for card_pack in
    sorted(
        CARD_PACKS.values(),
        key = lambda card_pack: card_pack.cost,
    )
]

RELATIONS = {
    'QP_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029146434605116/QP_unit.png',
    'Suguri_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029153330044948/Suguri_unit.png',
    'Marc_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029157021048862/Marc_unit.png',
    'Kai_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029160275824640/Kai_unit.png',
    'Yuki_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029164272975902/Yuki_unit.png',
    'Aru_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029167590674432/Aru_unit.png',
    'Hime_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029174851031050/Hime_unit.png',
    'Sora_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029178294558791/Sora_unit.png',
    'Fernet_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029182350426172/Fernet_unit.png',
    'Peat_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029186683150356/Peat_unit.png',
    'Marie_Poppo_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029190005063690/Marie_Poppo_unit.png',
    'Tomomo_(Softened)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029197420593192/Tomomo_Softened_unit.png',
    'Mio_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029206220238858/Mio_unit.png',
    'Syura_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029210393542656/Syura_unit.png',
    'Nanako_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029214034210826/Nanako_unit.png',
    'Saki_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029220606677042/Saki_unit.png',
    'Kyousuke_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029224167653376/Kyousuke_unit.png',
    'Kae_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029231285383168/Kae_unit.png',
    'Alte_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029235215466546/Alte_unit.png',
    'Kyoko_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029245969629194/Kyoko_unit.png',
    'Sham_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029249891307530/Sham_unit.png',
    'Sherry_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029253490040862/Sherry_unit.png',
    'Star_Breaker_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029257059401728/Star_Breaker_unit.png',
    'Sweet_Breaker_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029260750381106/Sweet_Breaker_unit.png',
    'Nath_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029266932760576/Nath_unit.png',
    'Mimyuu_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288589664676221014/Mimyuu_unit.png',
    'Tomato_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288589664998920294/Tomato_unit.png',
    'Kiriko_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029278232248330/Kiriko_unit.png',
    'NoName_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029400097746944/NoName_unit.png',
    'NoName_(Head)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029403855826994/NoName_Head_unit.png',
    'Miusaki_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029407840407552/Miusaki_unit.png',
    'Ceoreparque_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029411179073576/Ceoreparque_unit.png',
    'Yuki_(Dangerous)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029416082223114/Yuki_Dangerous_unit.png',
    'Tomomo_(Casual)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029420343635988/Tomomo_Casual_unit.png',
    'Tomomo_(Sweet_Eater)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029427188756480/Tomomo_Sweet_Eater_unit.png',
    'Tequila_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029431005552660/Tequila_unit.png',
    'Tsih_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901552305940344892/Tsih_unit.png',
    'Mei_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029438278471680/Mei_unit.png',
    'Natsumi_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029441956900884/Natsumi_unit.png',
    'Nico_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029449544392714/Nico_unit.png',
    'Arthur_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901551697829167124/Arthur_unit.png',
    'Iru_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288226933469089853/Iru_unit.png',
    'Mira_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029461816901642/Mira_unit.png',
    'Sora_&_Sham_(Cuties)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288230543187644509/Sora__Sham_Cuties_unit.png',
    'Yuuki_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029471962935296/Yuuki_unit.png',
    'Islay_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288223989000306859/Islay_unit.png',
    'Suguri_(46_Billion_Years)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288231049104588830/Suguri_46_Billion_Years_unit.png',
    'Sumika_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029484608778270/Sumika_unit.png',
    'Ellie_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029489163784232/Ellie_unit.png',
    'Lulu_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029494654132244/Lulu_unit.png',
    'Alicianrone_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901547493467250738/Alicianrone_unit.png',
    'Teotoratta_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029504003244042/Teotoratta_unit.png',
    'Arnelle_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029508138823700/Arnelle_unit.png',
    'Maynie_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029512618344458/Maynie_unit.png',
    'Chris_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029516883931187/Chris_unit.png',
    'Kyupita_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029521032085504/Kyupita_unit.png',
    'QP_(Dangerous)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288394048989827082/QP_Dangerous_unit.png',
    'Marie_Poppo_(Mixed)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029527352930304/Marie_Poppo_Mixed_unit.png',
    'Sora_(Military)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029653844754492/Sora_Military_unit.png',
    'Aru_(Scramble)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029658378776586/Aru_Scramble_unit.png',
    'Suguri_(Ver.2)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029662191403058/Suguri_Ver.2_unit.png',
    'Marc_(Pilot)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029665504903258/Marc_Pilot_unit.png',
    'Chicken_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029669514674176/Chicken_unit.png',
    'Robo_Ball_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029673650241576/Robo_Ball_unit.png',
    'Seagull_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029681049002034/Seagull_unit.png',
    'Store_Manager_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029684714827806/Store_Manager_unit.png',
    'Shifu_Robot_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288217504753123368/Shifu_Robot_unit.png',
    'Flying_Castle_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029692210053140/Flying_Castle_unit.png',
    'Halena_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901549023264141402/Halena_unit.png',
    'Cook_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901032911460003850/Cook_unit.png',
    'Lone_Rider_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901550313453006978/Lone_Rider_unit.png',
    'Merchant_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/901029711759675402/Merchant_unit.png',
    'Accel_Hyper': 'https://cdn.discordapp.com/attachments/568837922288173058/901029715480039424/Accel_Hyper.png',
    'Big_Magnum': 'https://cdn.discordapp.com/attachments/568837922288173058/901029719775014962/Big_Magnum.png',
    'Dark_Side_of_Business': 'https://cdn.discordapp.com/attachments/568837922288173058/901029726993391656/Dark_Side_of_Business.png',
    'Desperate_Modification': 'https://cdn.discordapp.com/attachments/568837922288173058/901029730273357844/Desperate_Modification.png',
    'Extension': 'https://cdn.discordapp.com/attachments/568837922288173058/1288224525988663346/Extension.png',
    'Final_Battle': 'https://cdn.discordapp.com/attachments/568837922288173058/901029738770989096/Final_Battle.png',
    'I\'m_on_Fire!': 'https://cdn.discordapp.com/attachments/568837922288173058/901029742810103818/Im_on_Fire.png',
    'Portable_Pudding': 'https://cdn.discordapp.com/attachments/568837922288173058/901029750456340480/Portable_Pudding.png',
    'Quick_Restoration': 'https://cdn.discordapp.com/attachments/568837922288173058/901029754017308702/Quick_Restoration.png',
    'Rainbow-Colored_Circle': 'https://cdn.discordapp.com/attachments/568837922288173058/901029757418897408/Rainbow-Colored_Circle.png',
    'Rbits': 'https://cdn.discordapp.com/attachments/568837922288173058/901029763982950451/Rbits.png',
    'Reverse_Attribute_Field': 'https://cdn.discordapp.com/attachments/568837922288173058/901029767992721408/Reverse_Attribute_Field.png',
    'Serious_Battle': 'https://cdn.discordapp.com/attachments/568837922288173058/901029773361430558/Serious_Battle.png',
    'Shield': 'https://cdn.discordapp.com/attachments/568837922288173058/901029777002078248/Shield.png',
    'Shield_Counter': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605441466699831/Shield_Counter.png',
    'Sink_or_Swim': 'https://cdn.discordapp.com/attachments/568837922288173058/901029783847194644/Sink_or_Swim.png',
    'Tactical_Retreat': 'https://cdn.discordapp.com/attachments/568837922288173058/901029907210068048/Tactical_Retreat.png',
    'Ambush': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605442414743592/Ambush.png',
    'Backdoor_Trade': 'https://cdn.discordapp.com/attachments/568837922288173058/901029914348765204/Backdoor_Trade.png',
    'Completion_Reward': 'https://cdn.discordapp.com/attachments/568837922288173058/901029917997809694/Completion_Reward.png',
    'Dash!': 'https://cdn.discordapp.com/attachments/568837922288173058/901029921449730058/Dash.png',
    'Extend': 'https://cdn.discordapp.com/attachments/568837922288173058/901029927216885770/Extend.png',
    'Flip_Out': 'https://cdn.discordapp.com/attachments/568837922288173058/901029934435295262/Flip_Out.png',
    'Gentleman\'s_Battle': 'https://cdn.discordapp.com/attachments/568837922288173058/901029941594951691/Gentlemans_Battle.png',
    'Lonely_Chariot': 'https://cdn.discordapp.com/attachments/568837922288173058/901029945273376799/Lonely_Chariot.png',
    'Long-Distance_Shot': 'https://cdn.discordapp.com/attachments/568837922288173058/901029949115359232/Long-Distance_Shot.png',
    'Mimic': 'https://cdn.discordapp.com/attachments/568837922288173058/901029952466595841/Mimic.png',
    'Nice_Jingle': 'https://cdn.discordapp.com/attachments/568837922288173058/901029956870635540/Nice_Jingle.png',
    'Nice_Present': 'https://cdn.discordapp.com/attachments/568837922288173058/901029960939089970/Nice_Present.png',
    'Passionate_Research': 'https://cdn.discordapp.com/attachments/568837922288173058/901029965846417418/Passionate_Research.png',
    'Path_Blockers': 'https://cdn.discordapp.com/attachments/568837922288173058/1288224871389724713/Path_Blockers.png',
    'President\'s_Privilege': 'https://cdn.discordapp.com/attachments/568837922288173058/901029972972539954/Presidents_Privilege.png',
    'Princess\'s_Privilege': 'https://cdn.discordapp.com/attachments/568837922288173058/1288221252410151055/Princesss_Privilege.png',
    'Pudding': 'https://cdn.discordapp.com/attachments/568837922288173058/901029985186365460/Pudding.png',
    'Saki\'s_Cookie': 'https://cdn.discordapp.com/attachments/568837922288173058/901029988495671316/Sakis_Cookie.png',
    'Stiff_Crystal': 'https://cdn.discordapp.com/attachments/568837922288173058/901029991901437972/Stiff_Crystal.png',
    'Sweet_Destroyer': 'https://cdn.discordapp.com/attachments/568837922288173058/1288392252682534966/Sweet_Destroyer.png',
    'Treasure_Thief': 'https://cdn.discordapp.com/attachments/568837922288173058/901030002047451146/Treasure_Thief.png',
    'Accelerating_Sky': 'https://cdn.discordapp.com/attachments/568837922288173058/924794756242997318/Accelerating_Sky.png',
    'Cloud_of_Seagulls': 'https://cdn.discordapp.com/attachments/568837922288173058/901030010066989066/Cloud_of_Seagulls.png',
    'Dinner': 'https://cdn.discordapp.com/attachments/568837922288173058/901030014018019348/Dinner.png',
    'Forced_Revival': 'https://cdn.discordapp.com/attachments/568837922288173058/901030017709010944/Forced_Revival.png',
    'Gift_Exchange': 'https://cdn.discordapp.com/attachments/568837922288173058/901030025615274015/Gift_Exchange.png',
    'Here_and_There': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605442175537214/Here_and_There.png',
    'Holy_Night': 'https://cdn.discordapp.com/attachments/568837922288173058/901030033395691540/Holy_Night.png',
    'Indiscriminate_Fire_Support': 'https://cdn.discordapp.com/attachments/568837922288173058/901030037896196096/Indiscriminate_Fire_Support.png',
    'Little_War': 'https://cdn.discordapp.com/attachments/568837922288173058/901030160885776434/Little_War.png',
    'Mix_Phenomenon': 'https://cdn.discordapp.com/attachments/568837922288173058/901030164501233675/Mix_Phenomenon.png',
    'Oh_My_Friend': 'https://cdn.discordapp.com/attachments/568837922288173058/901030169727365171/Oh_My_Friend.png',
    'Out_of_Ammo': 'https://cdn.discordapp.com/attachments/568837922288173058/901030174198493184/Out_of_Ammo.png',
    'Party_Time': 'https://cdn.discordapp.com/attachments/568837922288173058/901030177486815242/Party_Time.png',
    'Play_of_the_Gods': 'https://cdn.discordapp.com/attachments/568837922288173058/901030180838055956/Play_of_the_Gods.png',
    'Scary_Solicitation': 'https://cdn.discordapp.com/attachments/568837922288173058/901030188488458240/Scary_Solicitation.png',
    'Scrambled_Eve': 'https://cdn.discordapp.com/attachments/568837922288173058/901030192087191552/Scrambled_Eve.png',
    'Sealed_Guardian': 'https://cdn.discordapp.com/attachments/568837922288173058/901030195622969375/Sealed_Guardian.png',
    'Serene_Hush': 'https://cdn.discordapp.com/attachments/568837922288173058/901030199435595796/Serene_Hush.png',
    'Star-Blasting_Light': 'https://cdn.discordapp.com/attachments/568837922288173058/901030203722203176/Star-Blasting_Light.png',
    'Super_All-Out_Mode': 'https://cdn.discordapp.com/attachments/568837922288173058/901030210542116894/Super_All-Out_Mode.png',
    'Unpaid_Work': 'https://cdn.discordapp.com/attachments/568837922288173058/901030213872410624/Unpaid_Work.png',
    'We_Are_Waruda': 'https://cdn.discordapp.com/attachments/568837922288173058/901030217102020618/We_Are_Waruda.png',
    'Lost_Child': 'https://cdn.discordapp.com/attachments/568837922288173058/901030224689500160/Lost_Child.png',
    'Lucky_Charm': 'https://cdn.discordapp.com/attachments/568837922288173058/901030233195565067/Lucky_Charm.png',
    'Metallic_Monocoque': 'https://cdn.discordapp.com/attachments/568837922288173058/901030238107074570/Metallic_Monocoque.png',
    'Poppo_the_Snatcher': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605481413115965/Poppo_the_Snatcher.png',
    'Price_of_Power': 'https://cdn.discordapp.com/attachments/568837922288173058/901030246856392746/Price_of_Power.png',
    'Unlucky_Charm': 'https://cdn.discordapp.com/attachments/568837922288173058/901030251981840394/Unlucky_Charm.png',
    'Windy_Enchantment': 'https://cdn.discordapp.com/attachments/568837922288173058/901030256754982912/Windy_Enchantment.png',
    'Assault': 'https://cdn.discordapp.com/attachments/568837922288173058/901030261137997884/Assault.png',
    'Bad_Pudding': 'https://cdn.discordapp.com/attachments/568837922288173058/901030265340719164/Bad_Pudding.png',
    'Brutal_Prank': 'https://cdn.discordapp.com/attachments/568837922288173058/901030268146679858/Brutal_Prank.png',
    'Dangerous_Pudding': 'https://cdn.discordapp.com/attachments/568837922288173058/901030273385394236/Dangerous_Pudding.png',
    'Encore': 'https://cdn.discordapp.com/attachments/568837922288173058/901030279605530645/Encore.png',
    'Exchange': 'https://cdn.discordapp.com/attachments/568837922288173058/901030283879518238/Exchange.png',
    'Flamethrower': 'https://cdn.discordapp.com/attachments/568837922288173058/901030288988184596/Flamethrower.png',
    'For_the_Future_of_the_Toy_Store': 'https://cdn.discordapp.com/attachments/568837922288173058/901030293018935356/For_the_Future_of_the_Toy_Store.png',
    'Go_Away': 'https://cdn.discordapp.com/attachments/568837922288173058/901030414318198794/Go_Away.png',
    'Heat_300%': 'https://cdn.discordapp.com/attachments/568837922288173058/901030419661742120/Heat_300.png',
    'Invasion': 'https://cdn.discordapp.com/attachments/568837922288173058/901030423067500554/Invasion.png',
    'I_Wanna_See_You': 'https://cdn.discordapp.com/attachments/568837922288173058/901030426796245063/I_Wanna_See_You.png',
    'Mimyuu\'s_Hammer': 'https://cdn.discordapp.com/attachments/568837922288173058/901030430801809408/Mimyuus_Hammer.png',
    'Piggy_Bank': 'https://cdn.discordapp.com/attachments/568837922288173058/901030434702524448/Piggy_Bank.png',
    'Piyopiyo_Procession': 'https://cdn.discordapp.com/attachments/568837922288173058/901030440243195944/Piyopiyo_Procession.png',
    'Poppoformation': 'https://cdn.discordapp.com/attachments/568837922288173058/901030444542328842/Poppoformation.png',
    'Present_Thief': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605441202585750/Present_Thief.png',
    'Sealed_Memories': 'https://cdn.discordapp.com/attachments/568837922288173058/901030452171796500/Sealed_Memories.png',
    'Sky_Restaurant_\'Pures\'': 'https://cdn.discordapp.com/attachments/568837922288173058/901030455581765672/Sky_Restaurant_Pures.png',
    'Tragedy_in_the_Dead_of_Night': 'https://cdn.discordapp.com/attachments/568837922288173058/901030463202816000/Tragedy_in_the_Dead_of_Night.png',
    'Wanted': 'https://cdn.discordapp.com/attachments/568837922288173058/901030468353392650/Wanted.png',
    'Another_Ultimate_Weapon': 'https://cdn.discordapp.com/attachments/568837922288173058/901030473759866890/Another_Ultimate_Weapon.png',
    'Beyond_Hell': 'https://cdn.discordapp.com/attachments/568837922288173058/901030477534728212/Beyond_Hell.png',
    'Blue_Crow_the_Second': 'https://cdn.discordapp.com/attachments/568837922288173058/901030481565483078/Blue_Crow_the_Second.png',
    'Deploy_Bits': 'https://cdn.discordapp.com/attachments/568837922288173058/901030485659123722/Deploy_Bits.png',
    'Hyper_Mode': 'https://cdn.discordapp.com/attachments/568837922288173058/901030489765347358/Hyper_Mode.png',
    'Intelligence_Officer': 'https://cdn.discordapp.com/attachments/568837922288173058/1288385046767730729/Intelligence_Officer.png',
    'Reflective_Shell': 'https://cdn.discordapp.com/attachments/568837922288173058/901030497528983622/Reflective_Shell.png',
    'Self-Destruct': 'https://cdn.discordapp.com/attachments/568837922288173058/901030503589769256/Self-Destruct.png',
    'Waruda_Machine,_Blast_Off!': 'https://cdn.discordapp.com/attachments/568837922288173058/1288589663447027805/Waruda_Machine_Blast_Off.png',
    'Accelerator': 'https://cdn.discordapp.com/attachments/568837922288173058/901030513018556476/Accelerator.png',
    'Angel_Hand': 'https://cdn.discordapp.com/attachments/568837922288173058/901030516902469632/Angel_Hand.png',
    'Awakening_of_Talent': 'https://cdn.discordapp.com/attachments/568837922288173058/901030522225061918/Awakening_of_Talent.png',
    'Big_Rocket_Cannon': 'https://cdn.discordapp.com/attachments/568837922288173058/901030526125752340/Big_Rocket_Cannon.png',
    'Blazing!': 'https://cdn.discordapp.com/attachments/568837922288173058/901030532907946014/Blazing.png',
    'Branch_Expansion_Strategy': 'https://cdn.discordapp.com/attachments/568837922288173058/901030538196967424/Branch_Expansion_Strategy.png',
    'Cast_Off': 'https://cdn.discordapp.com/attachments/568837922288173058/901030542491918336/Cast_Off.png',
    'Chef,_I_Could_Use_Some_Help!': 'https://cdn.discordapp.com/attachments/568837922288173058/901030546459754516/Chef_I_Could_Use_Some_Help.png',
    'Crystal_Barrier': 'https://cdn.discordapp.com/attachments/568837922288173058/901030668962758686/Crystal_Barrier.png',
    'Ellie\'s_Miracle': 'https://cdn.discordapp.com/attachments/568837922288173058/901030673089974292/Ellies_Miracle.png',
    'Extended_Photon_Rifle': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605482986115112/Extended_Photon_Rifle.png',
    'Extraordinary_Specs': 'https://cdn.discordapp.com/attachments/568837922288173058/901030683709939772/Extraordinary_Specs.png',
    'Full_Speed_Alicianrone': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605480566001724/Full_Speed_Alicianrone.png',
    'Immovable_Object': 'https://cdn.discordapp.com/attachments/568837922288173058/901030692639637514/Immovable_Object.png',
    'Jonathan_Rush': 'https://cdn.discordapp.com/attachments/568837922288173058/901030696322215966/Jonathan_Rush.png',
    'Leap_Through_Space': 'https://cdn.discordapp.com/attachments/568837922288173058/901030700352933948/Leap_Through_Space.png',
    'Leap_Through_Space_(Marking)': 'https://cdn.discordapp.com/attachments/568837922288173058/901030705239322624/Leap_Through_Space_Marking.png',
    'Lulu\'s_Lucky_Egg': 'https://cdn.discordapp.com/attachments/568837922288173058/901030709303578654/Lulus_Lucky_Egg.png',
    'Manager,_I_Could_Use_Some_Help!': 'https://cdn.discordapp.com/attachments/568837922288173058/901030714013810718/Manager_I_Could_Use_Some_Help.png',
    'Miracle_Walker': 'https://cdn.discordapp.com/attachments/568837922288173058/1288236789823311912/Miracle_Walker.png',
    'Observer_of_Eternity': 'https://cdn.discordapp.com/attachments/568837922288173058/924797274272448562/Observer_of_Eternity.png',
    'Protagonist\'s_Privilege': 'https://cdn.discordapp.com/attachments/568837922288173058/901030729142640680/Protagonists_Privilege.png',
    'Raging_Madness': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605481782480977/Raging_Madness.png',
    'Reproduction_of_Records': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605481027502164/Reproduction_of_Records.png',
    'Rival': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605442645426257/Rival.png',
    'Rocket_Cannon': 'https://cdn.discordapp.com/attachments/568837922288173058/901030746133782568/Rocket_Cannon.png',
    'Saint_Eyes': 'https://cdn.discordapp.com/attachments/568837922288173058/901030749581500416/Saint_Eyes.png',
    'Solid_Witch': 'https://cdn.discordapp.com/attachments/568837922288173058/901030753075347476/Solid_Witch.png',
    'Special_Stage': 'https://cdn.discordapp.com/attachments/568837922288173058/901030757273862144/Special_Stage.png',
    'Stealth_On': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605482600370309/Stealth_On.png',
    'Sweet_Guardian': 'https://cdn.discordapp.com/attachments/568837922288173058/1288392941529858138/Sweet_Guardian.png',
    'Turbo_Charged': 'https://cdn.discordapp.com/attachments/568837922288173058/901030772817952818/Turbo_Charged.png',
    'Ubiquitous': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605482134536323/Ubiquitous.png',
    'Witch\'s_Hair_Lock': 'https://cdn.discordapp.com/attachments/568837922288173058/1288237220955951126/Witchs_Hair_Lock.png',
    'X16_Big_Rocket': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605441718489098/X16_Big_Rocket.png',
    'Air_Strike': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605441944977500/Air_Strike.png',
    'Binding_Chains': 'https://cdn.discordapp.com/attachments/568837922288173058/901030797325254696/Binding_Chains.png',
    'Cooking_Time': 'https://cdn.discordapp.com/attachments/568837922288173058/901030802157076490/Cooking_Time.png',
    'Delta_Field': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605440967708753/Delta_Field.png',
    'Devil_Hand': 'https://cdn.discordapp.com/attachments/568837922288173058/901030927935889448/Devil_Hand.png',
    'Do_Pirates_Fly_in_the_Sky_': 'https://cdn.discordapp.com/attachments/568837922288173058/901030932117606420/Do_Pirates_Fly_in_the_Sky_.png',
    'Evil_Mastermind': 'https://cdn.discordapp.com/attachments/568837922288173058/901030935502413844/Evil_Mastermind.png',
    'Evil_Spy_Work_―_Preparation': 'https://cdn.discordapp.com/attachments/568837922288173058/1288589664235556986/Evil_Spy_Work__Preparation.png',
    'Final_Surgery': 'https://cdn.discordapp.com/attachments/568837922288173058/901030945396760626/Final_Surgery.png',
    'Gamble!': 'https://cdn.discordapp.com/attachments/568837922288173058/901030951625306122/Gamble.png',
    'Magical_Inferno': 'https://cdn.discordapp.com/attachments/568837922288173058/1288605440736890910/Magical_Inferno.png',
    'Magical_Massacre': 'https://cdn.discordapp.com/attachments/568837922288173058/1288218811044069447/Magical_Massacre.png',
    'Magical_Revenge': 'https://cdn.discordapp.com/attachments/568837922288173058/901030967198761021/Magical_Revenge.png',
    'Melting_Memories': 'https://cdn.discordapp.com/attachments/568837922288173058/901030972148043796/Melting_Memories.png',
    'Overseer': 'https://cdn.discordapp.com/attachments/568837922288173058/901030976371716117/Overseer.png',
    'Plushie_Master': 'https://cdn.discordapp.com/attachments/568837922288173058/901030980008169502/Plushie_Master.png',
    'Present_for_You': 'https://cdn.discordapp.com/attachments/568837922288173058/901030984424779796/Present_for_You.png',
    'Revival_of_Stars': 'https://cdn.discordapp.com/attachments/568837922288173058/901030987889266698/Revival_of_Stars.png',
    'Star_Blasting_Fuse': 'https://cdn.discordapp.com/attachments/568837922288173058/901030994403000340/Star_Blasting_Fuse.png',
    'Subspace_Tunnel': 'https://cdn.discordapp.com/attachments/568837922288173058/901030998236622878/Subspace_Tunnel.png',
    'True_White_Christsmasher': 'https://cdn.discordapp.com/attachments/568837922288173058/1288229942123040889/True_White_Christsmasher.png',
    'Whimsical_Windmill': 'https://cdn.discordapp.com/attachments/568837922288173058/901031007711543296/Whimsical_Windmill.png',
    'White_Christsmasher': 'https://cdn.discordapp.com/attachments/568837922288173058/1288229470964023397/White_Christsmasher.png',
    'Banned_for_Life': 'https://cdn.discordapp.com/attachments/568837922288173058/901031017480089600/Banned_for_Life.png',
    'Beast_Witch': 'https://cdn.discordapp.com/attachments/568837922288173058/901031021426933800/Beast_Witch.png',
    'Evil_Spy_Work_―_Execution': 'https://cdn.discordapp.com/attachments/568837922288173058/1288589663862521927/Evil_Spy_Work__Execution.png',
    'Miracle_Red_Bean_Ice_Cream': 'https://cdn.discordapp.com/attachments/568837922288173058/924797785906225233/Miracle_Red_Bean_Ice_Cream.png',
    'Santa\'s_Job': 'https://cdn.discordapp.com/attachments/568837922288173058/1288237499591954494/Santas_Job.png',
    'Big_Bang_Bell': 'https://cdn.discordapp.com/attachments/568837922288173058/901031040641011732/Big_Bang_Bell.png',
    'Dance,_Long-Eared_Beasts!': 'https://cdn.discordapp.com/attachments/568837922288173058/901031044134879232/Dance_Long-Eared_Beasts.png',
    'Flying_Pirate': 'https://cdn.discordapp.com/attachments/568837922288173058/901031048358539294/Flying_Pirate.png',
    'Golden_Egg': 'https://cdn.discordapp.com/attachments/568837922288173058/901031052338954270/Golden_Egg.png',
    'Invisible_Bomb': 'https://cdn.discordapp.com/attachments/568837922288173058/901031057091080202/Invisible_Bomb.png',
    'Rbit_Hobby_Shop': 'https://cdn.discordapp.com/attachments/568837922288173058/901031176322580490/Rbit_Hobby_Shop.png',
    'Sweet_Battle!': 'https://cdn.discordapp.com/attachments/568837922288173058/901031180776902686/Sweet_Battle.png',
    'Snowball_Reflector': 'https://cdn.discordapp.com/attachments/568837922288173058/901031185143201792/Snowball_Reflector.png',
    'Grown-up_Snowball_Fight': 'https://cdn.discordapp.com/attachments/568837922288173058/901031188586696724/Grown-up_Snowball_Fight.png',
    'Legendary_Red_Mushroom': 'https://cdn.discordapp.com/attachments/568837922288173058/901031193141706772/Legendary_Red_Mushroom.png',
    'Ultimate_Weapon_in_the_Sun_(Original)': 'https://cdn.discordapp.com/attachments/568837922288173058/901031197013057546/Ultimate_Weapon_in_the_Sun_Original.png',
    'Lifeguard_on_the_White_Beach_(Original)': 'https://cdn.discordapp.com/attachments/568837922288173058/901031205011587133/Lifeguard_on_the_White_Beach_Original.png',
    'Guardian_of_Blooming_Flowers_(Original)': 'https://cdn.discordapp.com/attachments/568837922288173058/901031209134604358/Guardian_of_Blooming_Flowers_Original.png',
    'Unforgiving_Avenger_(Original)': 'https://cdn.discordapp.com/attachments/568837922288173058/901031212880101386/Unforgiving_Avenger_Original.png',
    'Red_&_Blue': 'https://cdn.discordapp.com/attachments/568837922288173058/901031216961163324/Red__Blue.png',
    'Blue_Mushroom_(Boost)': 'https://cdn.discordapp.com/attachments/568837922288173058/901031220035608586/Blue_Mushroom_Boost.png',
    'Deceptive_Disarming': 'https://cdn.discordapp.com/attachments/568837922288173058/901031227753103380/Deceptive_Disarming.png',
    'Overtime': 'https://cdn.discordapp.com/attachments/568837922288173058/901031231188250634/Overtime.png',
    'Pet_Snacks': 'https://cdn.discordapp.com/attachments/568837922288173058/901031234577235978/Pet_Snacks.png',
    'Home_Improvement': 'https://cdn.discordapp.com/attachments/568837922288173058/901031238276632586/Home_Improvement.png',
    'Lucky_Sevens': 'https://cdn.discordapp.com/attachments/568837922288173058/901031242940702750/Lucky_Sevens.png',
    'BanaNana': 'https://cdn.discordapp.com/attachments/568837922288173058/901031249852919838/BanaNana.png',
    'Safe_Journey': 'https://cdn.discordapp.com/attachments/568837922288173058/901031253636186112/Safe_Journey.png',
    'Guidance_of_the_Weathercock': 'https://cdn.discordapp.com/attachments/568837922288173058/901031257201340426/Guidance_of_the_Weathercock.png',
    'Upshift': 'https://cdn.discordapp.com/attachments/568837922288173058/901031261106216980/Upshift.png',
    'Zealous_Salesman': 'https://cdn.discordapp.com/attachments/568837922288173058/901031264444882974/Zealous_Salesman.png',
    'Freight': 'https://cdn.discordapp.com/attachments/568837922288173058/901031272489578496/Freight.png',
    'New_Nobility': 'https://cdn.discordapp.com/attachments/568837922288173058/924786225456513044/New_Nobility.png',
    'Affluence_(X)': 'https://cdn.discordapp.com/attachments/568837922288173058/924787732646068224/Affluence_X.png',
    'Dance_in_the_Moonlit_Night': 'https://cdn.discordapp.com/attachments/568837922288173058/924788747848019988/Dance_in_the_Moonlit_Night.png',
    'Twilight-Colored_Dream': 'https://cdn.discordapp.com/attachments/568837922288173058/924789734377680896/Twilight-Colored_Dream.png',
    'Little_Magnum': 'https://cdn.discordapp.com/attachments/568837922288173058/924790500786049064/Little_Magnum.png',
    'Hime_(Moonlight)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/924791836747386890/Hime_Moonlight_unit.png',
    'Fernet_(Noble)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/924792474365468713/Fernet_Noble_unit.png',
    'Malt_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/924793528335364106/Malt_unit.png',
    'Mescal_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288226298518442077/Mescal_unit.png',
    'Shifu_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288231875365834924/Shifu_unit.png',
    'Ideal_World': 'https://cdn.discordapp.com/attachments/568837922288173058/1288232156627472517/Ideal_World.png',
    'Star_Collector': 'https://cdn.discordapp.com/attachments/568837922288173058/1288234572617617418/Star_Collector.png',
    'Hoshino_Reika_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288234854726762516/Hoshino_Reika_unit.png',
    'Torrent_of_Magic': 'https://cdn.discordapp.com/attachments/568837922288173058/1288387340322082869/Torrent_of_Magic.png',
    'Watty_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288389645461098559/Watty_unit.png',
    'Goodest_Boy': 'https://cdn.discordapp.com/attachments/568837922288173058/1288390008033640528/Goodest_Boy.png',
    'Pomeranius_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288391150566248468/Pomeranius_unit.png',
    'Operation_A_Mountain_of_Sweets': 'https://cdn.discordapp.com/attachments/568837922288173058/1288395200678465546/Operation_A_Mountain_of_Sweets.png',
    'Natsumi_(Sweet_Blogger)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288396193302581289/Natsumi_Sweet_Blogger_unit.png',
    'Sweet_Maker\'s_Magic': 'https://cdn.discordapp.com/attachments/568837922288173058/1288397219652829234/Sweet_Makers_Magic.png',
    'Saki_(Sweet_Maker)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288397380764565544/Saki_Sweet_Maker_unit.png',
    'Sweet_Creator_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288399333896486922/Sweet_Creator_unit.png',
    'Sweet_Paradise': 'https://cdn.discordapp.com/attachments/568837922288173058/1288399334169247774/Sweet_Paradise.png',
    'Sweet_Indulgence': 'https://cdn.discordapp.com/attachments/568837922288173058/1288399334399803413/Sweet_Indulgence.png',
    'Mio_(Festive)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288548055515402250/Mio_Festive_unit.png',
    'Christmas_Inferno': 'https://cdn.discordapp.com/attachments/568837922288173058/1288548055771123783/Christmas_Inferno.png',
    'Make-Believe_Prison_Break': 'https://cdn.discordapp.com/attachments/568837922288173058/1288568829416313016/Make-Believe_Prison_Break.png',
    'Mimyuu_(Jailbird)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288568829718298644/Mimyuu_Jailbird_unit.png',
    'When_My_Slumber_Breaks': 'https://cdn.discordapp.com/attachments/568837922288173058/1288571683539779594/When_My_Slumber_Breaks.png',
    'Threats_to_My_Slumber': 'https://cdn.discordapp.com/attachments/568837922288173058/1288571683787112489/Threats_to_My_Slumber.png',
    'Krilalaris_(Pajamas)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288571684130918503/Krilalaris_Pajamas_unit.png',
    'Mother_Power': 'https://cdn.discordapp.com/attachments/568837922288173058/1288577209786830899/Mother_Power.png',
    'Mother_Poppo_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288577210038484992/Mother_Poppo_unit.png',
    'Lulu_is_an_Unlucky_Dragon': 'https://cdn.discordapp.com/attachments/568837922288173058/1288580058830733354/Lulu_is_an_Unlucky_Dragon.png',
    'Dark_Lulu_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288580059233259520/Dark_Lulu_unit.png',
    'Ellie\'s_Hyper_Miracle': 'https://cdn.discordapp.com/attachments/568837922288173058/1288584288173821952/Ellies_Hyper_Miracle.png',
    'Hyper_Ellie_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288584288467554479/Hyper_Ellie_unit.png',
    'Ex-Protagonist\'s_Moment_of_Glory': 'https://cdn.discordapp.com/attachments/568837922288173058/1288587044637114511/Ex-Protagonists_Moment_of_Glory.png',
    'Kai_(Hero)_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288587044934647939/Kai_Hero_unit.png',
    'Nanako\'s_Bit': 'https://cdn.discordapp.com/attachments/568837922288173058/1288594456202842162/Nanakos_Bit.png',
    'Rebellion': 'https://cdn.discordapp.com/attachments/568837922288173058/1288594456534188085/Rebellion.png',
    'Bank_of_Poppo': 'https://cdn.discordapp.com/attachments/568837922288173058/1288594456785850518/Bank_of_Poppo.png',
    'Contest_of_Cuteness': 'https://cdn.discordapp.com/attachments/568837922288173058/1288594457025056937/Contest_of_Cuteness.png',
    'My_Wild_Friends': 'https://cdn.discordapp.com/attachments/568837922288173058/1288594457330974935/My_Wild_Friends.png',
    'Warp_Control': 'https://cdn.discordapp.com/attachments/568837922288173058/1288594457574379521/Warp_Control.png',
    'Heart_of_Resistance': 'https://cdn.discordapp.com/attachments/568837922288173058/1288608776219525214/Heart_of_Resistance.png',
    'Bourbon_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1288608776521388053/Bourbon_unit.png',
    'Krilalaris_(unit)': 'https://cdn.discordapp.com/attachments/568837922288173058/1308346754554400808/Krilalaris_unit.png',
    'Bloodlust': 'https://cdn.discordapp.com/attachments/568837922288173058/1308347588126183515/Bloodlust.png',
}


def autocomplete_key(entity_factor_pair):
    return entity_factor_pair[1]


def get_auto_complete_results(value, container):
    if value is None:
        names = []
        count = 0
        for entity in container.values():
            names.append(entity.name)
            count += 1
            if count == 20:
                break
    else:
        name_matches = []
        
        pattern = re_compile(re_escape(value), re_ignore_case)
        
        for entity in container.values():
            parsed = pattern.search(entity.name)
            if parsed is None:
                continue
            
            name_matches.append((entity, parsed.start()))
        
        name_matches.sort(key = autocomplete_key)
        
        names = []
        
        count = 0
        for entity_factor_pair in name_matches:
            names.append(entity_factor_pair[0].name)
            count += 1
            if count == 20:
                break
    
    return names


def get_simple_autocomplete_results(value, list_):
    if value is None:
        results = list_[:20]
    else:
        results = [result for result in list_ if value in result]
    
    return results


def filter_entities_by(filters, container, select_custom_id_enabled, select_custom_id_disabled, entity_type_name):
    if filters:
        entities = [entity for entity in container.values() if apply_filters(entity, filters)]
    else:
        entities =  list(container.values())
    
    
    if entities:
        del entities[20:]
        
        description_parts = []
        index = 0
        limit = len(entities)
        
        while True:
            entity = entities[index]
            index += 1
            description_parts.append(str(index))
            description_parts.append('.: ')
            description_parts.append(entity.name)
            
            if index == limit:
                break
            
            description_parts.append('\n')
            continue
        
        description = ''.join(description_parts)
    else:
        description = '*no matches*'
    
    embed = Embed(f'Matched {entity_type_name}s', description)
    
    if entities:
        select = create_string_select(
            [StringSelectOption(str(entity.id), entity.name) for entity in entities],
            select_custom_id_enabled,
            placeholder = f'Select a {entity_type_name}',
        )
    else:
        select = create_string_select(
            [StringSelectOption('_', 'No result', default = True)],
            select_custom_id_disabled,
            placeholder = 'No result',
        )
    
    return InteractionResponse(embed = embed, components = select)


OJ_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    name = 'oj',
    description = '100% Orange juice',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)


def render_character_embeds(character):
    url = character.url
    
    return [
        Embed(
            character.name,
            character.description,
            url = url,
        ).add_field(
            'Attack',
            (
                f'```\n'
                f'{character.attack}\n'
                f'```'
            ),
            inline = True,
        ).add_field(
            'Defense',
            (
                f'```\n'
                f'{character.defense}\n'
                f'```'
            ),
            inline = True,
        ).add_field(
            'Evasion',
            (
                f'```\n'
                f'{character.evasion}\n'
                f'```'
            ),
            inline = True,
        ).add_field(
            'HP',
            (
                f'```\n'
                f'{character.hp}\n'
                f'```'
            ),
            inline = True,
        ).add_field(
            'Recovery',
            (
                f'```\n'
                f'{character.recovery}\n'
                f'```'
            ),
            inline = True,
        ).add_footer(
            f'Origin: {character.origin.name}',
        ).add_image(
            RELATIONS[character.card_name],
        ),
        *(
            Embed(
                url = url
            ).add_image(
                RELATIONS[card.card_name]
            )
            for card in character.hyper_cards
        )
    ]

@OJ_COMMANDS.interactions
async def character(
    name: (str, 'The character\'s name.'),
):
    try:
        character = CHARACTERS_BY_NAME[name]
    except KeyError:
        abort(f'There is no character named like: {name}.')
    else:
        return render_character_embeds(character)



@character.autocomplete('name')
async def autocomplete_character_name(value):
    return get_auto_complete_results(value, CHARACTERS)


CUSTOM_ID_SELECT_CHARACTER = 'hpoj.character.select'
CUSTOM_ID_SELECT_CHARACTER_DISABLED = 'hpoj.character.select.disabled'

@OJ_COMMANDS.interactions
async def filter_characters(
    attack: ('int', 'attack') = None,
    defense: ('int', 'defense') = None,
    evasion: ('int', 'evasion') = None,
    recovery : ('int', 'recovery') = None,
    hp: ('int', 'hp') = None,
):
    return filter_entities_by(
        get_character_filter_keys(attack, defense, evasion, recovery, hp),
        CHARACTERS,
        CUSTOM_ID_SELECT_CHARACTER,
        CUSTOM_ID_SELECT_CHARACTER_DISABLED,
        'character',
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_SELECT_CHARACTER)
async def select_character(event):
    if event.message.interaction.user_id != event.user_id:
        return
    
    selected_character_ids = event.values
    if (selected_character_ids is None):
        return
    
    try:
        selected_character_id = int(selected_character_ids[0])
    except ValueError:
        return
    
    try:
        character = CHARACTERS[selected_character_id]
    except KeyError:
        return
    
    return InteractionResponse(
        embed = render_character_embeds(character),
        components = None,
    )


ATTACK_VALUES, DEFENSE_VALUES, EVASION_VALUES, RECOVERY_VALUES, HP_VALUES = create_character_filter_options()

@filter_characters.autocomplete('attack')
async def autocomplete_character_attack(value):
    return get_simple_autocomplete_results(value, ATTACK_VALUES)

@filter_characters.autocomplete('defense')
async def autocomplete_character_defense(value):
    return get_simple_autocomplete_results(value, DEFENSE_VALUES)

@filter_characters.autocomplete('evasion')
async def autocomplete_character_evasion(value):
    return get_simple_autocomplete_results(value, EVASION_VALUES)

@filter_characters.autocomplete('recovery')
async def autocomplete_character_recovery(value):
    return get_simple_autocomplete_results(value, RECOVERY_VALUES)

@filter_characters.autocomplete('hp')
async def autocomplete_character_hp(value):
    return get_simple_autocomplete_results(value, HP_VALUES)

def render_card_embed(card):
    embed = Embed(
        card.name,
        (
            f'{card.description}\n'
            f'\n'
            f'*{card.quote}*'
        ),
        url = card.url,
    ).add_field(
        'level',
        (
            f'```\n'
            f'{card.level}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'cost',
        (
            f'```\n'
            f'{card.cost.string}\n'
            f'```'
        ),
        inline = True,
    )
    
    limit = card.limit
    if limit != -1:
        embed.add_field(
            'limit',
            (
                f'```\n'
                f'{card.limit}\n'
                f'```'
            ),
            inline = True,
        )
    
    embed.add_field(
        'type',
        (
            f'```\n'
            f'{card.type_string}\n'
            f'```'
        ),
    ).add_image(
        RELATIONS[card.card_name],
    )
    
    pack = card.pack
    if (pack is not None):
        embed.add_field(
            'pack',
            (
                f'```\n'
                f'{pack.name}\n'
                f'```'
            ),
            inline = True,
        )
    
    rarity = card.rarity
    if rarity != CARD_RARITY_NONE:
        rarity_string = CARD_RARITY_VALUE_TO_NAME[rarity]
        
        embed.add_field(
            'rarity',
            (
                f'```\n'
                f'{rarity_string}\n'
                f'```'
            ),
            inline = True,
        )
    
    events = card.events
    if (events is not None):
        embed.add_field(
            'events',
            (
                f'```\n'
                f'{" & ".join(event.name for event in events)}\n'
                f'```'
            ),
            inline = True,
        )
    
    return embed

@OJ_COMMANDS.interactions
async def card(
    name: (str, 'The card\'s name.'),
):
    try:
        card = CARDS_BY_NAME[name]
    except KeyError:
        abort(f'There is no card named like: {name}.')
    else:
        return render_card_embed(card)


@card.autocomplete('name')
async def autocomplete_card_name(value):
    return get_auto_complete_results(value, CARDS)

CUSTOM_ID_SELECT_CARD = 'hpoj.card.select'
CUSTOM_ID_SELECT_CARD_DISABLED = 'hpoj.card.select.disabled'

@OJ_COMMANDS.interactions
async def filter_cards(
    level: ('int', 'The card\'s level.') = None,
    cost: ('str', 'The card\'s cost.') = None,
    limit: ('int', 'The card\'s limit per deck.') = None,
    type_: ('str', 'The card\'s type.') = None,
    pack: ('str', 'The card\'s pack.') = None,
    rarity: ('str', 'The card\'s rarity.') = None,
):
    return filter_entities_by(
        get_card_filter_keys(level, cost, limit, type_, pack, rarity),
        CARDS,
        CUSTOM_ID_SELECT_CARD,
        CUSTOM_ID_SELECT_CARD_DISABLED,
        'card',
    )

@filter_cards.autocomplete('level')
async def autocomplete_card_level(value):
    return get_simple_autocomplete_results(value, CARD_LEVEL_FILTERABLE_STRINGS)

@filter_cards.autocomplete('cost')
async def autocomplete_card_cost(value):
    return get_simple_autocomplete_results(value, CARD_COSTS_NAMES_SORTED)

@filter_cards.autocomplete('limit')
async def autocomplete_card_limit(value):
    return get_simple_autocomplete_results(value, CARD_LIMIT_FILTERABLE_STRINGS)

@filter_cards.autocomplete('type_')
async def autocomplete_card_type(value):
    if (value is not None):
        value = value.upper()
    
    return get_simple_autocomplete_results(value, CARD_TYPE_FILTERABLE_NAMES)

@filter_cards.autocomplete('pack')
async def autocomplete_card_pack(value):
    return get_simple_autocomplete_results(value, CARD_PACK_NAMES_SORTED_BY_COST)

@filter_cards.autocomplete('rarity')
async def autocomplete_card_rarity(value):
    return get_simple_autocomplete_results(value, CARD_RARITY_FILTERABLE_NAMES)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_SELECT_CARD)
async def select_card(event):
    if event.message.interaction.user_id != event.user_id:
        return
    
    selected_card_ids = event.values
    if (selected_card_ids is None):
        return
    
    try:
        selected_card_id = int(selected_card_ids[0])
    except ValueError:
        return
    
    try:
        card = CARDS[selected_card_id]
    except KeyError:
        return
    
    return InteractionResponse(
        embed = render_card_embed(card),
        components = None,
    )


@FEATURE_CLIENTS.interactions(
    custom_id = [
        CUSTOM_ID_SELECT_CHARACTER_DISABLED,
        CUSTOM_ID_SELECT_CARD_DISABLED,
    ]
)
async def handle_disabled_components():
    pass
