__all__ = ()

from hata import BUILTIN_EMOJIS

from ..item_modifier_core import (
    MODIFIER_ID__FISHING, MODIFIER_ID__STAT_BEDROOM, MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_ID__STAT_LOYALTY,
    MODIFIER_KIND__FLAT, Modifier, construct_modifier_type
)

from .constants import ITEMS
from .flags import ITEM_FLAG_EDIBLE, ITEM_FLAG_WEAPON
from .item import Item
from .item_ids import (
    ITEM_ID_BLUEBERRY, ITEM_ID_BLUEFRANKISH, ITEM_ID_CARROT, ITEM_ID_DEVILCART_OYSTER, ITEM_ID_FISHING_ROD,
    ITEM_ID_FLYKILLER_AMANATA, ITEM_ID_GARLIC, ITEM_ID_PEACH, ITEM_ID_SCARLETIO_ONION, ITEM_ID_STRAWBERRY
)


ITEM_STRAWBERRY = ITEMS[ITEM_ID_STRAWBERRY] = Item(
    ITEM_ID_STRAWBERRY,
    'Strawberry',
    BUILTIN_EMOJIS['strawberry'],
    (
        'Strawberries are loved worldwide for their aroma, bright red colour, juiciness, texture, and sweetness.\n'
        '\n'
        'Although they are not native to Gensoukyou, they can be found around the **Ruins**.'
    ),
    ITEM_FLAG_EDIBLE,
    28, # value (hearts)
    32, # weight (grams)
    None,
)


ITEM_PEACH = ITEMS[ITEM_ID_PEACH] = Item(
    ITEM_ID_PEACH,
    'Peach',
    BUILTIN_EMOJIS['peach'],
    (
        'One of the most popular temperate fruits. Has yellow flesh and beautiful yellow to orange skin with a cute '
        'red blush towards the sun.\n'
        '\n'
        'Can be found at the gardens of **Hakugyokurou**. '
        'Not sure if they were planted intentionally, or someone just mistake their pink blossom to cherry trees\''
    ),
    ITEM_FLAG_EDIBLE,
    21, # value (hearts)
    216, # weight (grams)
    None,
)


ITEM_BLUEBERRY = ITEMS[ITEM_ID_BLUEBERRY] = Item(
    ITEM_ID_BLUEBERRY,
    'Blueberries',
    BUILTIN_EMOJIS['blueberries'],
    (
        'Blue to black round berries that are popular for their taste. '
        'They are essential when preparing wild meat for their spiciness, served as dressing or jam.\n'
        '\n'
        'They can be found on the barren hillsides of the **Moriya Shrine**.'
    ),
    ITEM_FLAG_EDIBLE,
    3, # value (hearts)
    3, # weight (grams)
    None,
)


ITEM_DEVILCART_OYSTER = ITEMS[ITEM_ID_DEVILCART_OYSTER] = Item(
    ITEM_ID_DEVILCART_OYSTER,
    'Devilcart oyster',
    BUILTIN_EMOJIS['brown_mushroom'],
    (
        'An edible mushroom, the largest one in its genus. It has a thick, meaty white stem and a small tan cap. '
        'Tasteless raw, but has rich umami flavor when cooked.\n'
        '\n'
        'Can be found in any forest.'
    ),
    ITEM_FLAG_EDIBLE,
    83, # value (hearts)
    148, # weight (grams)
    None,
)


ITEM_FLYKILLER_AMANATA = ITEMS[ITEM_ID_FLYKILLER_AMANATA] = Item(
    ITEM_ID_FLYKILLER_AMANATA,
    'Flykiller amanata',
    BUILTIN_EMOJIS['mushroom'],
    (
        'A toxic mushroom mainly noted for its hallucinogenic properties. '
        'It is easily distinguishable for its red hat with white spots, although it also has several subspecies.\n'
        '\n'
        'Can be found in any forest.'
    ),
    ITEM_FLAG_EDIBLE,
    239, # value (hearts) # Note: in irl markets it can be 100x - 400x more
    456, # weight (grams)
    None,
)


ITEM_FISHING_ROD = ITEMS[ITEM_ID_FISHING_ROD] = Item(
    ITEM_ID_FISHING_ROD,
    'Fishing rod',
    BUILTIN_EMOJIS['fishing_pole_and_fish'],
    (
        'A long thin rod with a cord used to catch fishe by having a hook attached to end of its cord. '
        'Far less effective than using nets or traps and usually only used to play around.\n'
        '\n'
        'Sakuya would surely save you from going fishing alone.'
    ),
    ITEM_FLAG_WEAPON,
    3000, # value (hearts) # Budget fishing rod, probably Mokou made it from bamboo.
    1018, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_BEDROOM, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__FLAT), -2),
    ),
)

ITEM_BLUEFRANKISH = ITEMS[ITEM_ID_BLUEFRANKISH] = Item(
    ITEM_ID_BLUEFRANKISH,
    'Bluefrankish',
    BUILTIN_EMOJIS['grapes'],
    (
        'A dark-skinned grape growing in medium sized clusters. '
        'Ripes late and rich of tannin, giving it spicy character. '
        'Used for red wine. '
        'Its plant is easily capable of producing high yields, but is susceptible to early spring frost, '
        'so it tends to be planted on warmer areas.\n'
        '\n'
        'Was brought to Gensoukyou before the Great Hakurei barrier was erected. '
        'Can be found in the **Human Village**.'
    ),
    ITEM_FLAG_EDIBLE,
    19, # value (hearts) # Its a whine grape, so costs barely anything. Although grape is made of water and sugar. heh
    180, # weight (grams)
    None,
)


ITEM_CARROT = ITEMS[ITEM_ID_CARROT] = Item(
    ITEM_ID_CARROT,
    'Carrot',
    BUILTIN_EMOJIS['carrot'],
    (
        'A root vegetable cultivated in many colors from yellow through red till purple. '
        'It is sweet and a significant source of vitamins. '
        'Its a biennial plant, first year it stores its energy in its taproot enabling itself to flower in the second.\n'
        '\n'
        'They can be found in the **Human Village** and at the outskirts of the **Eientei** mansion.'
    ),
    ITEM_FLAG_EDIBLE,
    18, # value (hearts)
    240, # weight (grams)
    None,
)


ITEM_GARLIC = ITEMS[ITEM_ID_GARLIC] = Item(
    ITEM_ID_GARLIC,
    'Garlic',
    BUILTIN_EMOJIS['garlic'],
    (
        'A bulbous plant used as seasoning and as medical remedy. '
        'It has virus, bacterium and fungi killing effect, rich of minerals and vitamins. '
        'Used as meat seasoning and marinade. '
        'Because of its medical properties and strong odor it is considered to repel and dispel evil spirits.\n'
        '\n'
        'Can be found in the **Human Village**.'
    ),
    ITEM_FLAG_EDIBLE,
    47, # value (hearts)
    85, # weight (grams)
    None,
)


SCARLET_ONION = ITEMS[ITEM_ID_SCARLETIO_ONION] = Item(
    ITEM_ID_SCARLETIO_ONION,
    'Scarlet onion',
    BUILTIN_EMOJIS['onion'],
    (
        'An bulbous plant used as seasoning since the ancients. '
        'Its one of the most important and widespread vegetable. '
        'Depending on its kind it is either biennial or perennial. Its inflorescence is fascinating, sphere shaped.\n'
        '\n'
        'Can be found in the **Human Village**.'
    ),
    ITEM_FLAG_EDIBLE,
    9, # value (hearts)
    170, # weight (grams)
    None,
)


# Some ideas:
"""
Big braids of the hell cat

A pair of fiery red braids with the length of a tail.
They appear irresistible not only to the men, but the women and children too
Experts state that they are the key to eternal happiness.

Charm +2
Cuteness skills +2
Cuteness + 10%
Loyalty +2

Fiery chariot

A burning cart that kashas travel the world with.
They are borrowing corpses that were not yet buried, or of who have lived a sinful live.
Carrying their soul to hell.

Housewife +2
Bedroom skills +2
Inventory +5300
Inventory +200%

"""
