__all__ = ()

from hata import BUILTIN_EMOJIS

from ..item_modifier_core import (
    MODIFIER_ID__BUTCHERING, MODIFIER_ID__FISHING, MODIFIER_ID__FORAGING, MODIFIER_ID__GARDENING,
    MODIFIER_ID__STAT_BEDROOM, MODIFIER_ID__STAT_CHARM, MODIFIER_ID__STAT_CUTENESS, MODIFIER_ID__STAT_HOUSEWIFE,
    MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT, MODIFIER_KIND__PERCENT, Modifier, construct_modifier_type
)

from .constants import ITEMS
from .flags import ITEM_FLAG_EDIBLE, ITEM_FLAG_NPC, ITEM_FLAG_WEAPON
from .item import Item
from .item_ids import (
    ITEM_ID_ALICE, ITEM_ID_BLUEBERRY, ITEM_ID_BLUEFRANKISH, ITEM_ID_CARROT, ITEM_ID_CHIRUNO, ITEM_ID_DEVILCART_OYSTER,
    ITEM_ID_FISHING_ROD, ITEM_ID_FLYKILLER_AMANITA, ITEM_ID_FROG, ITEM_ID_GARLIC, ITEM_ID_KOISHI, ITEM_ID_MARISA,
    ITEM_ID_MYSTIA, ITEM_ID_ORIN, ITEM_ID_PEACH, ITEM_ID_SAKUYA, ITEM_ID_SCARLET_ONION, ITEM_ID_SCISSORS,
    ITEM_ID_STRAWBERRY
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
    21, # value (hearts)
    24, # weight (grams)
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
        'Can be found at the gardens of **Hakugyokurou mansion**. '
        'Not sure if they were planted intentionally, or someone just mistake their pink blossom to cherry trees\''
    ),
    ITEM_FLAG_EDIBLE,
    30, # value (hearts)
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


ITEM_FLYKILLER_AMANITA = ITEMS[ITEM_ID_FLYKILLER_AMANITA] = Item(
    ITEM_ID_FLYKILLER_AMANITA,
    'Flykiller amanita',
    BUILTIN_EMOJIS['mushroom'],
    (
        'A toxic mushroom mainly noted for its hallucinogenic properties. '
        'It is easily distinguishable for its red hat with white spots, although it also has several subspecies.\n'
        '\n'
        'Can be found in any forest.'
    ),
    ITEM_FLAG_EDIBLE,
    179, # value (hearts) # Note: in irl markets it can be 100x - 400x more
    342, # weight (grams)
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
        'A root vegetable cultivated in many colours from yellow through red till purple. '
        'It is sweet and a significant source of vitamins. '
        'Its a biennial plant, first year it stores its energy in its taproot enabling itself to flower in the second.\n'
        '\n'
        'They can be found in the outskirts of **Human Village** and around the **Eientei mansion**.'
    ),
    ITEM_FLAG_EDIBLE,
    27, # value (hearts)
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


ITEM_SCARLET_ONION = ITEMS[ITEM_ID_SCARLET_ONION] = Item(
    ITEM_ID_SCARLET_ONION,
    'Scarlet onion',
    BUILTIN_EMOJIS['onion'],
    (
        'A bulbous plant used as seasoning since the ancients. '
        'Its one of the most important and widespread vegetable. '
        'Depending on its kind it is either biennial or perennial. Its inflorescence is fascinating, sphere shaped.\n'
        '\n'
        'Can be found in the **Human Village**.'
    ),
    ITEM_FLAG_EDIBLE,
    14, # value (hearts)
    170, # weight (grams)
    None,
)


ITEM_MYSTIA = ITEMS[ITEM_ID_MYSTIA] = Item(
    ITEM_ID_MYSTIA,
    'Mystia',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
)


ITEM_SAKUYA = ITEMS[ITEM_ID_SAKUYA] = Item(
    ITEM_ID_SAKUYA,
    'Sakuya',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
)


ITEM_MARISA = ITEMS[ITEM_ID_MARISA] = Item(
    ITEM_ID_MARISA,
    'Marisa',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
)


ITEM_ALICE = ITEMS[ITEM_ID_ALICE] = Item(
    ITEM_ID_ALICE,
    'Alice',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
)


ITEM_KOISHI = ITEMS[ITEM_ID_KOISHI] = Item(
    ITEM_ID_KOISHI,
    'Koishi',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
)


ITEM_ORIN = ITEMS[ITEM_ID_ORIN] = Item(
    ITEM_ID_ORIN,
    'Orin',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
)


ITEM_SCISSORS = ITEMS[ITEM_ID_SCISSORS] = Item(
    ITEM_ID_SCISSORS,
    'Scissors',
    BUILTIN_EMOJIS['scissors'],
    (
        'A hand operation shearing tool.\n'
        'It has blades pivoted in a way that when the handles are pulled into each other, '
        'the sharpened edges on the other end of the tool slide into each other.\n'
        'They are meant to be used for cutting various thin materials. '
        'There are also many specialized ones as well, for example for cutting hair, metal, meat or branches.'
    ),
    ITEM_FLAG_WEAPON,
    8000, # value (hearts)
    70, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +3),
        
        Modifier(construct_modifier_type(MODIFIER_ID__BUTCHERING, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__GARDENING, MODIFIER_KIND__PERCENT), +10),
        Modifier(construct_modifier_type(MODIFIER_ID__FORAGING, MODIFIER_KIND__PERCENT), +20),
    ),
)


ITEM_FROG = ITEMS[ITEM_ID_FROG] = Item(
    ITEM_ID_FROG,
    'Frog',
    BUILTIN_EMOJIS['frog'],
    (
        'Tailless amphibians with flattened body, protruding eyes and with weak front, but long muscular back legs '
        'specialized in jumping.\n'
        'They have a carnivorous diet which mainly consist of insects. '
        'They look defenseless, but they are admissible in camouflage, and can flee dexterously by leaping with their '
        'strong back legs.'
        'The skin of many frogs contains mild toxin, the ones with more potent ones usually advertise it with bright '
        'colours.\n'
        'Frogs usually spawn their eggs in water bodies. These eggs hatch into fully aquatic tadpoles which have '
        'tails and internal grills.'
        'Their life cycle is completed when they metamorphose into their semiaquatic adult form.\n'
        '\n'
        'They can be most commonly found around wetlands, like the **Misty Lake**.'
    ),
    ITEM_FLAG_EDIBLE,
    46, # value (hearts)
    24, # weight (grams)
    None,
)


ITEM_CHIRUNO = ITEMS[ITEM_ID_CHIRUNO] = Item(
    ITEM_ID_CHIRUNO,
    'Chiruno',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
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
