__all__ = ()

from hata import BUILTIN_EMOJIS

from ..item_modifier_core import (
    MODIFIER_ID__BUTCHERING, MODIFIER_ID__ENERGY, MODIFIER_ID__FISHING, MODIFIER_ID__FORAGING, MODIFIER_ID__GARDENING,
    MODIFIER_ID__HEALTH, MODIFIER_ID__HUNTING,
    MODIFIER_ID__INVENTORY, MODIFIER_ID__MOVEMENT, MODIFIER_ID__STAT_BEDROOM, MODIFIER_ID__STAT_CHARM,
    MODIFIER_ID__STAT_CUTENESS, MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT,
    MODIFIER_KIND__PERCENT, Modifier, construct_modifier_type
)

from .constants import ITEMS
from .flags import ITEM_FLAG_COSTUME, ITEM_FLAG_EDIBLE, ITEM_FLAG_HEAD, ITEM_FLAG_NPC, ITEM_FLAG_WEAPON
from .item import Item
from .item_ids import (
    ITEM_ID_ALICE, ITEM_ID_ANGELROOT, ITEM_ID_BAMBOO_SHOOT, ITEM_ID_BIG_BRAIDS_OF_THE_HELL_CAT, ITEM_ID_BISHOPHAT,
    ITEM_ID_BLUEBERRY, ITEM_ID_BLUEFRANKISH,
    ITEM_ID_BUNNY_SUIT,
    ITEM_ID_CARROT, ITEM_ID_ROGUISH_DRESS_OF_THE_CORPSE_VOYAGER, ITEM_ID_ELEGANT_DRESS_OF_THE_CHIEF_MAID,
    ITEM_ID_CHIRUNO, ITEM_ID_DAI, ITEM_ID_DEVILCART_OYSTER,
    ITEM_ID_ELECTROSTATIC_DISCHARGE_PROTECTIVE_COAT, ITEM_ID_FIERY_CHARIOT_OF_THE_RED_EYED_KASHA, ITEM_ID_FISHING_ROD,
    ITEM_ID_FLYKILLER_AMANITA, ITEM_ID_FROG, ITEM_ID_GARLIC, ITEM_ID_JUNKO, ITEM_ID_KINGS_NEW_CLOTHES, ITEM_ID_KOISHI,
    ITEM_ID_KOKORO, ITEM_ID_MAID_DRESS, ITEM_ID_MARISA, ITEM_ID_MYSTIA, ITEM_ID_ORIN, ITEM_ID_PEACH,
    ITEM_ID_RIBBON_BOW, ITEM_ID_RULER,
    ITEM_ID_SAKUYA, ITEM_ID_SCARLET_ONION, ITEM_ID_SCISSORS, ITEM_ID_STRAW_HAT, ITEM_ID_STRAWBERRY,
    ITEM_ID_PLUSHIE_BEAR, ITEM_ID_TORN_OUT_WING_OF_THE_UNKNOWN_OVEN, ITEM_ID_TEWI, ITEM_ID_YUKARI, ITEM_ID_YUUKA
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
    16, # value (hearts)
    18, # weight (grams)
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
    40, # value (hearts)
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
    4, # value (hearts)
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
        
        Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__PERCENT), -20),
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
    36, # value (hearts)
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
    33, # value (hearts)
    60, # weight (grams)
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
    23, # value (hearts)
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
        'A hand operated shearing tool.\n'
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
        'specialized in jumping. '
        'They have a carnivorous diet which mainly consist of insects. '
        'They look defenseless, but they are admissible in camouflage, and can flee dexterously by leaping with their '
        'strong back legs. '
        'The skin of many frogs contains mild toxin, the ones with more potent ones usually advertise it with bright '
        'colours. '
        'Frogs usually spawn their eggs in water bodies. These eggs hatch into fully aquatic tadpoles which have '
        'tails and internal grills.'
        'Their life cycle is completed when they metamorphose into their semiaquatic adult form.\n'
        '\n'
        'They can be most commonly found around wetlands, like the **Misty Lake**.'
    ),
    ITEM_FLAG_EDIBLE,
    69, # value (hearts)
    48, # weight (grams)
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


ITEM_DAI = ITEMS[ITEM_ID_DAI] = Item(
    ITEM_ID_DAI,
    'Dai',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
)


ITEM_ANGELROOT = ITEMS[ITEM_ID_ANGELROOT] = Item(
    ITEM_ID_ANGELROOT,
    'Angelroot',
    BUILTIN_EMOJIS['herb'],
    (
        'An aromatic herb with hollow stems and large round clusters of white or greenish flowers. '
        'Its roots and seeds are prized for their sweet, musky scent and bittersweet flavor. '
        'Its a biennial, sometimes perennial plant. '
        'Used to spice liqueurs, foods, and due to its pleasant odor perfumes as well. '
        'As medicine it is used to treat numerous medical issues, '
        'viewed to be suitable to treat any gynecological complaint.'
        '\n'
        'It prefers moist and shady environments, preferably near water bodies, like the **Misty Lake**.'
    ),
    ITEM_FLAG_EDIBLE,
    160, # value (hearts)
    130, # weight (grams)
    None,
)


ITEM_BISHOPHAT = ITEMS[ITEM_ID_BISHOPHAT] = Item(
    ITEM_ID_BISHOPHAT,
    'Bishophat',
    BUILTIN_EMOJIS['seedling'],
    (
        'A perennial herb with delicate, heart-shaped leaves '
        'and small flowers that come in shades of yellow and white. '
        'Its leaves are harvested and dried for use as medicine or tonic. '
        'Called either as bishop\'s hat due to its flower\'s shape, '
        'or as horny goat weed due to goats being observed unusually frisky after consuming it. '
        'Used as a dietary supplement for improving blood flow and men\'s vigor. '
        'It prefers to grow in shaded areas.\n'
        '\n'
        'Can be found in any forest.'
    ),
    0,
    63, # value (hearts)
    22, # weight (grams)
    None,
)


ITEM_JUNKO = ITEMS[ITEM_ID_JUNKO] = Item(
    ITEM_ID_JUNKO,
    'Junko',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
)


ITEM_TEWI = ITEMS[ITEM_ID_TEWI] = Item(
    ITEM_ID_TEWI,
    'Tewi',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
)


ITEM_KOKORO = ITEMS[ITEM_ID_KOKORO] = Item(
    ITEM_ID_KOKORO,
    'Kokoro',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
)


ITEM_RIBBON_BOW = ITEMS[ITEM_ID_RIBBON_BOW] = Item(
    ITEM_ID_RIBBON_BOW,
    'Ribbon bow',
    BUILTIN_EMOJIS['ribbon'],
    (
        'An accessory made out of a ribbon. '
        'The ribbon may be from various materials, like textile, plastic or metal.\n'
        'Can be used to tie ponytail, braids or just used it as a general accessory anywhere.'
    ),
    ITEM_FLAG_HEAD,
    50, # value (hearts)
    10, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +5),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_BEDROOM, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +3),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT), +1),
    ),
)


ITEM_STRAW_HAT = ITEMS[ITEM_ID_STRAW_HAT] = Item(
    ITEM_ID_STRAW_HAT,
    'Straw hat',
    BUILTIN_EMOJIS['womans_hat'],
    (
        'A wide brimmed spun hat made out of straw or reed.\n'
        'It is engineered to protect head from the heat of the sun.'
    ),
    ITEM_FLAG_HEAD,
    700, # value (hearts)
    135, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_BEDROOM, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +2),
        
        Modifier(construct_modifier_type(MODIFIER_ID__GARDENING, MODIFIER_KIND__PERCENT), +25),
        Modifier(construct_modifier_type(MODIFIER_ID__FORAGING, MODIFIER_KIND__PERCENT), +10),
    ),
)

ITEM_RULER = ITEMS[ITEM_ID_RULER] = Item(
    ITEM_ID_RULER,
    'Ruler',
    BUILTIN_EMOJIS['straight_ruler'],
    (
        'A tool used to draw straight lines, furthermore to measure length. '
        'In the past they were made out of wood, but nowadays mostly from translucent plastic, or from metal. '
        'It usually contains millimeter scale, its length is variable, most commonly is between 20 and 50 cm-s.'
    ),
    ITEM_FLAG_WEAPON,
    300, # value (hearts)
    60, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_BEDROOM, MODIFIER_KIND__FLAT), +3),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +1),
        
        Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__PERCENT), +10),
        Modifier(construct_modifier_type(MODIFIER_ID__GARDENING, MODIFIER_KIND__PERCENT), +5),
        Modifier(construct_modifier_type(MODIFIER_ID__FORAGING, MODIFIER_KIND__PERCENT), +25),
    ),
)


ITEM_YUKARI = ITEMS[ITEM_ID_YUKARI] = Item(
    ITEM_ID_YUKARI,
    'Yukari',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
)


ITEM_YUUKA = ITEMS[ITEM_ID_YUUKA] = Item(
    ITEM_ID_YUUKA,
    'Yuuka',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
)


ITEM_BAMBOO_SHOOT = ITEMS[ITEM_ID_BAMBOO_SHOOT] = Item(
    ITEM_ID_BAMBOO_SHOOT,
    'Bamboo shoot',
    BUILTIN_EMOJIS['bamboo'],
    (
        'Bamboo shoots are the young sprouts of bamboo coming out from the ground. '
        'At the case of many species they are edible and they are used to make various dishes and broth. '
        'Raw bamboo shoots contain natural toxin, cyanogenic-glycosides, '
        'therefore they have to be heat treated for a long duration with frequent water change.\n'
        '\n'
        'Can be found in the **Bamboo forest**.'
    ),
    ITEM_FLAG_EDIBLE,
    107, # value (hearts)
    640, # weight (grams)
    None,
)


ITEM_PLUSHIE_BEAR = ITEMS[ITEM_ID_PLUSHIE_BEAR] = Item(
    ITEM_ID_PLUSHIE_BEAR,
    'Plushie bear',
    BUILTIN_EMOJIS['teddy_bear'],
    (
        'A stuffed toy made out of fabric, which embodies a friendly bear. '
        'It is an interesting duality that while plushie bears are a cute and popular creature, '
        'real bears are highly dangerous.'
    ),
    ITEM_FLAG_WEAPON,
    875, # value (hearts)
    125, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +5),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_BEDROOM, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT), +3),
    ),
)


ITEM_KINGS_NEW_CLOTHES = ITEMS[ITEM_ID_KINGS_NEW_CLOTHES] = Item(
    ITEM_ID_KINGS_NEW_CLOTHES,
    'King\'s new clothes',
    BUILTIN_EMOJIS['crown'],
    (
        'The new clothes of the kings, who is not willing to appear in front of his people twice in the same clothes. '
        'Made out of truth-seering fabric, that can be visible only by honest and blameless people. '
        'Stupid, liar or evil cannot see it.'
    ),
    ITEM_FLAG_COSTUME,
    400, # value (hearts)
    0, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_BEDROOM, MODIFIER_KIND__FLAT), +1),
        
        Modifier(construct_modifier_type(MODIFIER_ID__MOVEMENT, MODIFIER_KIND__PERCENT), +4),
    ),
)


ITEM_MAID_DRESS = ITEMS[ITEM_ID_MAID_DRESS] = Item(
    ITEM_ID_MAID_DRESS,
    'Maid dress',
    BUILTIN_EMOJIS['stopwatch'],
    (
        'A servants\'s dress, that may be either conservative or revealing depending on the purpose. '
        'It is usually a black dress with white trim and a skirt above knee length. Worn with an apron, '
        'dark stockings and black shoes.'
    ),
    ITEM_FLAG_COSTUME,
    3500, # value (hearts)
    2400, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__PERCENT), +7),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__PERCENT), +7),
        
        Modifier(construct_modifier_type(MODIFIER_ID__BUTCHERING, MODIFIER_KIND__PERCENT), +10),
    ),
)


ITEM_ELEGANT_DRESS_OF_THE_CHIEF_MAID = ITEMS[ITEM_ID_ELEGANT_DRESS_OF_THE_CHIEF_MAID] = Item(
    ITEM_ID_ELEGANT_DRESS_OF_THE_CHIEF_MAID,
    'Elegant dress of the Chief maid',
    BUILTIN_EMOJIS['stopwatch'],
    (
        'Perfect fit for a mansion\'s senior maid who directorly reports to her mistress. '
        'A blue dress with white trim and a laced skirt above knee length. Worn with an ruffled apron, '
        'dark stockings and black shoes. '
        'Always keeping knifes in reach within the garter ... who knows when they may be needed.'
    ),
    ITEM_FLAG_COSTUME,
    104000, # value (hearts)
    3200, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__PERCENT), +10),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__PERCENT), +10),
        
        Modifier(construct_modifier_type(MODIFIER_ID__INVENTORY, MODIFIER_KIND__FLAT), +800),
        Modifier(construct_modifier_type(MODIFIER_ID__MOVEMENT, MODIFIER_KIND__FLAT), +50),
        
        Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__PERCENT), +10),
        Modifier(construct_modifier_type(MODIFIER_ID__BUTCHERING, MODIFIER_KIND__PERCENT), +10),
        Modifier(construct_modifier_type(MODIFIER_ID__HUNTING, MODIFIER_KIND__PERCENT), +20),
    ),
)


ITEM_TORN_OUT_WING_OF_THE_UNKNOWN_OVEN = ITEMS[ITEM_ID_TORN_OUT_WING_OF_THE_UNKNOWN_OVEN] = Item(
    ITEM_ID_TORN_OUT_WING_OF_THE_UNKNOWN_OVEN,
    'Torn out wing of the Unknown oven',
    BUILTIN_EMOJIS['fishing_pole_and_fish'],
    (
        'A single wing, appearing to made out of some kind of metal, with 8 prims attached to it along. '
        'Its shape may be interpreted as a fishing rod, only a cord and a hook is missing.'
    ),
    ITEM_FLAG_WEAPON,
    1380000, # value (hearts)
    3650, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__PERCENT), +4),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__PERCENT), +9),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__PERCENT), +5),
        
        Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__PERCENT), -40),
    ),
)


ITEM_BUNNY_SUIT = ITEMS[ITEM_ID_BUNNY_SUIT] = Item(
    ITEM_ID_BUNNY_SUIT,
    'Bunny suit',
    BUILTIN_EMOJIS['necktie'],
    (
        'A one piece swimsuit like tightly laced corsets cinching in the waist with its legs cut higher on the hips. '
        'Wearing stockings or fishnets on the legs connecting with the corset, '
        'and a white puff tail at the back as a cherry on the cake.'
    ),
    ITEM_FLAG_COSTUME,
    2500, # value (hearts)
    1600, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_BEDROOM, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +5),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT), -2),
    ),
)


ITEM_ELECTROSTATIC_DISCHARGE_PROTECTIVE_COAT = ITEMS[ITEM_ID_ELECTROSTATIC_DISCHARGE_PROTECTIVE_COAT] = Item(
    ITEM_ID_ELECTROSTATIC_DISCHARGE_PROTECTIVE_COAT,
    'Electrostatical discharge protective coat',
    BUILTIN_EMOJIS['lab_coat'],
    (
        'A white coat and a glove in which everyone can look like a scientist or as a math teacher. '
        'Made out of a fabric that does not allow static energy to be accumulated, '
        'preventing it to be discharged onto electrical components when contact is made.'
    ),
    ITEM_FLAG_COSTUME,
    3200, # value (hearts)
    400, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +3),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT), +3),
    ),
)


ITEM_BIG_BRAIDS_OF_THE_HELL_CAT = ITEMS[ITEM_ID_BIG_BRAIDS_OF_THE_HELL_CAT] = Item(
    ITEM_ID_BIG_BRAIDS_OF_THE_HELL_CAT,
    'Big braids of the Hell cat',
    BUILTIN_EMOJIS['black_cat'],
    (
        'A pair of fiery red braids with the length of a tail. '
        'Tied by black bows which fit perfectly with black cat ears. '
        'They appear irresistible for both humans and the youkais too. '
        'Some say they are the key for eternal happiness.'
    ),
    ITEM_FLAG_HEAD,
    187000, # value (hearts)
    4600, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__PERCENT), +20),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__PERCENT), +20),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT), +3),
    ),
)


ITEM_FIERY_CHARIOT_OF_THE_RED_EYED_KASHA = ITEMS[ITEM_ID_FIERY_CHARIOT_OF_THE_RED_EYED_KASHA] = Item(
    ITEM_ID_FIERY_CHARIOT_OF_THE_RED_EYED_KASHA,
    'Fiery chariot of the Red eyed kasha',
    BUILTIN_EMOJIS['shopping_cart'],
    (
        'A wheelbarrow with burning wheels that kashas travel the world with. '
        'They are borrowing corpses that were not yet buried, '
        'or even digging up the ones of who have lived a sinful live. '
        'Carrying their soul to hell, torturing the sinful bodies on the way.'
    ),
    ITEM_FLAG_WEAPON,
    124000, # value (hearts)
    28000, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +4),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_BEDROOM, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_BEDROOM, MODIFIER_KIND__PERCENT), +10),
        
        Modifier(construct_modifier_type(MODIFIER_ID__INVENTORY, MODIFIER_KIND__FLAT), +56000),
        Modifier(construct_modifier_type(MODIFIER_ID__INVENTORY, MODIFIER_KIND__PERCENT), +70),
    ),
)


ITEM_ROGUISH_DRESS_OF_THE_CORPSE_VOYAGER = ITEMS[ITEM_ID_ROGUISH_DRESS_OF_THE_CORPSE_VOYAGER] = Item(
    ITEM_ID_ROGUISH_DRESS_OF_THE_CORPSE_VOYAGER,
    'Roguish dress of the Corpse voyager',
    BUILTIN_EMOJIS['black_cat'],
    (
        'A dark dress with green frills, red ribbons tying it at the sleeve and at the neck. '
        'With an additional corset making sure that the body posture is correct in long travels. '
        'The overall composition is perfect to give the impression of a stormy night.'
    ),
    ITEM_FLAG_COSTUME,
    164000, # value (hearts)
    3200, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__PERCENT), +5),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__PERCENT), +10),
        
        Modifier(construct_modifier_type(MODIFIER_ID__MOVEMENT, MODIFIER_KIND__FLAT), +20),
        Modifier(construct_modifier_type(MODIFIER_ID__MOVEMENT, MODIFIER_KIND__PERCENT), +6),
        Modifier(construct_modifier_type(MODIFIER_ID__HEALTH, MODIFIER_KIND__PERCENT), +10),
        Modifier(construct_modifier_type(MODIFIER_ID__ENERGY, MODIFIER_KIND__PERCENT), +10),
    ),
)
