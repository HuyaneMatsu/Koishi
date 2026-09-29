__all__ = ()

from hata import BUILTIN_EMOJIS

from ..item_modifier_core import (
    MODIFIER_ID__BUTCHERING, MODIFIER_ID__ENERGY, MODIFIER_ID__FISHING, MODIFIER_ID__FORAGING, MODIFIER_ID__GARDENING,
    MODIFIER_ID__HEALTH, MODIFIER_ID__HUNTING, MODIFIER_ID__INVENTORY, MODIFIER_ID__MOVEMENT, MODIFIER_ID__STAT_BEDROOM,
    MODIFIER_ID__STAT_CHARM, MODIFIER_ID__STAT_CUTENESS, MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_ID__STAT_LOYALTY,
    MODIFIER_KIND__FLAT, MODIFIER_KIND__PERCENT, Modifier, construct_modifier_type
)

from .constants import ITEMS
from .flags import (
    ITEM_FLAG_BUTCHERABLE, ITEM_FLAG_COSTUME, ITEM_FLAG_EDIBLE, ITEM_FLAG_HEAD, ITEM_FLAG_NPC, ITEM_FLAG_WEAPON
)
from .item import Item
from .item_ids import (
    ITEM_ID_ACHING_AFFECTION_S_HEART_PIERCER, ITEM_ID_ALICE, ITEM_ID_ANGELROOT, ITEM_ID_AYA, ITEM_ID_BAMBOO,
    ITEM_ID_BAMBOO_SHOOT, ITEM_ID_BISHOPHAT, ITEM_ID_BLOOD_SAUSAGE, ITEM_ID_BLUEBERRY, ITEM_ID_BLUEFRANKISH,
    ITEM_ID_BOUGH, ITEM_ID_BROOM, ITEM_ID_BUNNY_SUIT, ITEM_ID_CARROT, ITEM_ID_CHIEF_MAID_S_ELEGANT_DRESS,
    ITEM_ID_CHIRUNO, ITEM_ID_CORPSE_VOYAGER_S_ROGUISH_DRESS, ITEM_ID_CUT_WOOD, ITEM_ID_DAI, ITEM_ID_DANGO,
    ITEM_ID_DEVILCART_OYSTER, ITEM_ID_EIRIN, ITEM_ID_ELECTROSTATIC_DISCHARGE_PROTECTIVE_COAT, ITEM_ID_FISHING_ROD,
    ITEM_ID_FLANDRE, ITEM_ID_FLYKILLER_AMANITA, ITEM_ID_FROG, ITEM_ID_GARLIC, ITEM_ID_GOTHIC_ATTIRE, ITEM_ID_HAND_FAN,
    ITEM_ID_HELL_CAT_S_BIG_BRAIDS, ITEM_ID_HIKING_SET, ITEM_ID_HUMAN_BLOOD, ITEM_ID_HUMAN_BODY,
    ITEM_ID_HUMAN_BODY_PART_ARM, ITEM_ID_HUMAN_BODY_PART_DIGESTIVE_ORGANS, ITEM_ID_HUMAN_BODY_PART_FOOT,
    ITEM_ID_HUMAN_BODY_PART_HAND, ITEM_ID_HUMAN_BODY_PART_HEAD, ITEM_ID_HUMAN_BODY_PART_INTERNALS,
    ITEM_ID_HUMAN_BODY_PART_LEG, ITEM_ID_HUMAN_BODY_PART_SKULL, ITEM_ID_HUMAN_BODY_PART_TORSO,
    ITEM_ID_HUMAN_BODY_SHARD_BOTTOM_HALF, ITEM_ID_HUMAN_BODY_SHARD_CHEWED, ITEM_ID_HUMAN_BODY_SHARD_TOP_HALF,
    ITEM_ID_HUMAN_BONE, ITEM_ID_HUMAN_BRAIN, ITEM_ID_HUMAN_CARTILAGE, ITEM_ID_HUMAN_EAR, ITEM_ID_HUMAN_EYE,
    ITEM_ID_HUMAN_FAT, ITEM_ID_HUMAN_HAIR, ITEM_ID_HUMAN_HEART, ITEM_ID_HUMAN_INTESTINES, ITEM_ID_HUMAN_KIDNEY,
    ITEM_ID_HUMAN_LIVER, ITEM_ID_HUMAN_LUNG, ITEM_ID_HUMAN_MUSCLE, ITEM_ID_HUMAN_NAIL, ITEM_ID_HUMAN_NERVOUS_TISSUE,
    ITEM_ID_HUMAN_PANCREAS, ITEM_ID_HUMAN_SKIN, ITEM_ID_HUMAN_SPLEEN, ITEM_ID_HUMAN_TONGUE, ITEM_ID_HUMAN_TOOTH,
    ITEM_ID_HUMAN_TRIPE, ITEM_ID_JUNKO, ITEM_ID_KAGEROU, ITEM_ID_KIMONO, ITEM_ID_KINGS_NEW_CLOTHES,
    ITEM_ID_KITCHEN_KNIFE, ITEM_ID_KOISHI, ITEM_ID_KOKORO, ITEM_ID_LIVER_SAUSAGE, ITEM_ID_LOG, ITEM_ID_MAID_DRESS,
    ITEM_ID_MARISA, ITEM_ID_MEAT_SAUSAGE, ITEM_ID_MYSTIA, ITEM_ID_NINA, ITEM_ID_NITORI, ITEM_ID_ORIN, ITEM_ID_PARASOL,
    ITEM_ID_PARSEE, ITEM_ID_PATCHOULI, ITEM_ID_PEACH, ITEM_ID_PEN, ITEM_ID_PLUSHIE_BEAR, ITEM_ID_POKING_KNIFE,
    ITEM_ID_PUDDING, ITEM_ID_RAMEN, ITEM_ID_RED_EYED_KASHA_S_FIERY_CHARIOT, ITEM_ID_REIMU, ITEM_ID_REMILIA,
    ITEM_ID_RIBBON_BOW, ITEM_ID_RICE, ITEM_ID_RULER, ITEM_ID_RUMIA, ITEM_ID_SAKE, ITEM_ID_SAKUYA, ITEM_ID_SATORI,
    ITEM_ID_SCARLET_ONION, ITEM_ID_SCISSORS, ITEM_ID_SEIRAN, ITEM_ID_SEKIBANKI, ITEM_ID_STRAWBERRY, ITEM_ID_STRAW_HAT,
    ITEM_ID_SUIKA, ITEM_ID_SUNFLOWER, ITEM_ID_TEA_LEAVES, ITEM_ID_TEWI, ITEM_ID_TWIGS,
    ITEM_ID_UNKNOWN_OVEN_S_TORN_OUT_WING, ITEM_ID_YOUMU, ITEM_ID_YUKARI, ITEM_ID_YUUKA
)
from .option_butcher import OptionButcher


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
        'Not sure if they were planted intentionally, or someone just mistake their pink blossom to cherry trees\'.'
    ),
    ITEM_FLAG_EDIBLE,
    40, # value (hearts)
    216, # weight (grams)
    None,
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
    None,
)


ITEM_DEVILCART_OYSTER = ITEMS[ITEM_ID_DEVILCART_OYSTER] = Item(
    ITEM_ID_DEVILCART_OYSTER,
    'Devilcart oyster',
    BUILTIN_EMOJIS['brown_mushroom'],
    (
        'An edible mushroom, the largest one in its genus. It has a thick, meaty white stem and a small tan cap. '
        'Tasteless raw, but has rich umami flavour when cooked.\n'
        '\n'
        'Can be found in any forest.'
    ),
    ITEM_FLAG_EDIBLE,
    83, # value (hearts)
    148, # weight (grams)
    None,
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
    None,
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
    None,
)


ITEM_FROG = ITEMS[ITEM_ID_FROG] = Item(
    ITEM_ID_FROG,
    'Frog',
    BUILTIN_EMOJIS['frog'],
    (
        'Tailless amphibians with flattened bodies, protruding eyes, with weak front, but long muscular back legs '
        'specialized in jumping. '
        'They have a carnivorous diet which mainly consists of insects. '
        'They look defenseless, but they are adept in camouflage, and can flee dexterously by leaping with their '
        'strong back legs. '
        'The skin of many frogs contains mild toxins, the species with more potent ones usually advertise it with '
        'bright colours. '
        'Frogs usually spawn their eggs in water bodies. These eggs hatch into fully aquatic tadpoles which have '
        'tails and internal gills. '
        'Their life cycle is completed when they metamorphose into their semiaquatic adult form.\n'
        '\n'
        'They can be most commonly found around wetlands, like the **Misty Lake**.'
    ),
    0,
    69, # value (hearts)
    48, # weight (grams)
    None,
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
    None,
)


ITEM_ANGELROOT = ITEMS[ITEM_ID_ANGELROOT] = Item(
    ITEM_ID_ANGELROOT,
    'Angelroot',
    BUILTIN_EMOJIS['herb'],
    (
        'An aromatic herb with hollow stems and large round clusters of white or greenish flowers. '
        'Its roots and seeds are prized for their sweet, musky scent and bittersweet flavour. '
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
    None,
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
    None,
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
    None,
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
    88, # value (hearts)
    525, # weight (grams)
    None,
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
    None,
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
    None,
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
    None,
)


ITEM_CHIEF_MAID_S_ELEGANT_DRESS = ITEMS[ITEM_ID_CHIEF_MAID_S_ELEGANT_DRESS] = Item(
    ITEM_ID_CHIEF_MAID_S_ELEGANT_DRESS,
    'Chief maid\'s Elegant dress',
    BUILTIN_EMOJIS['stopwatch'],
    (
        'Perfect fit for a mansion\'s senior maid who directly reports to her mistress. '
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
    None,
)


ITEM_UNKNOWN_OVEN_S_TORN_OUT_WING = ITEMS[ITEM_ID_UNKNOWN_OVEN_S_TORN_OUT_WING] = Item(
    ITEM_ID_UNKNOWN_OVEN_S_TORN_OUT_WING,
    'Unknown Owen\'s Torn out wing',
    BUILTIN_EMOJIS['fishing_pole_and_fish'],
    (
        'A single wing, appearing to made out of some kind of metal, with 8 prims attached to it along. '
        'Its shape may be interpreted as a fishing rod, only a cord and a hook is missing.'
    ),
    ITEM_FLAG_WEAPON,
    138000, # value (hearts)
    3650, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__PERCENT), +4),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__PERCENT), +9),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__PERCENT), +5),
        
        Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__PERCENT), -40),
    ),
    None,
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
    None,
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
    None,
)


ITEM_HELL_CAT_S_BIG_BRAIDS = ITEMS[ITEM_ID_HELL_CAT_S_BIG_BRAIDS] = Item(
    ITEM_ID_HELL_CAT_S_BIG_BRAIDS,
    'Hell cat\'s Big braids',
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
    None,
)


ITEM_RED_EYED_KASHA_S_FIERY_CHARIOT = ITEMS[ITEM_ID_RED_EYED_KASHA_S_FIERY_CHARIOT] = Item(
    ITEM_ID_RED_EYED_KASHA_S_FIERY_CHARIOT,
    'Red eyed kasha\'s Fiery chariot',
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
    None,
)


ITEM_CORPSE_VOYAGER_S_ROGUISH_DRESS = ITEMS[ITEM_ID_CORPSE_VOYAGER_S_ROGUISH_DRESS] = Item(
    ITEM_ID_CORPSE_VOYAGER_S_ROGUISH_DRESS,
    'Corpse voyager\'s Roguish dress',
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
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__PERCENT), +10),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__PERCENT), +20),
        
        Modifier(construct_modifier_type(MODIFIER_ID__MOVEMENT, MODIFIER_KIND__FLAT), +20),
        Modifier(construct_modifier_type(MODIFIER_ID__MOVEMENT, MODIFIER_KIND__PERCENT), +6),
        Modifier(construct_modifier_type(MODIFIER_ID__HEALTH, MODIFIER_KIND__PERCENT), +10),
        Modifier(construct_modifier_type(MODIFIER_ID__ENERGY, MODIFIER_KIND__PERCENT), +10),
    ),
    None,
)



ITEM_KITCHEN_KNIFE = ITEMS[ITEM_ID_KITCHEN_KNIFE] = Item(
    ITEM_ID_KITCHEN_KNIFE,
    'Kitchen knife',
    BUILTIN_EMOJIS['knife'],
    (
        'A tool for every day use, It may have 2 main usa cases, both to cut and to poke.'
        'It consists out of 2 parts, the blade and the handle.\n'
        'The blade is made out of steel in almost every case. '
        'Its flat edge is curved, but its tip for stabbing is imprecise.'
        'The tall blade allows the equipping hand to not hit the cutting board while using it.'
        'For every day usage it has one of the best shape and great durability.\n'
        'The handle may be made of various materials. '
        'Most common are: any metal, varnished wood, antler or bone, hide, rubber or plastic.'
    ),
    ITEM_FLAG_WEAPON,
    8400, # value (hearts)
    410, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +5),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT), +1),
        
        Modifier(construct_modifier_type(MODIFIER_ID__BUTCHERING, MODIFIER_KIND__PERCENT), +15),
    ),
    None,
)


ITEM_POKING_KNIFE = ITEMS[ITEM_ID_POKING_KNIFE] = Item(
    ITEM_ID_POKING_KNIFE,
    'Poking knife',
    BUILTIN_EMOJIS['knife'],
    (
        'A tool for every day use, It may have 2 main usa cases, both to cut and to stab.'
        'It consists out of 2 parts, the blade and the handle.\n'
        'The blade is made out of steel in almost every case. '
        'Its spine is stiff, so it can have flat edge on both sides. It is better for fighting than for work.'
        'Its tip is located on its longitudinal axis, making it perfect for stabbing. '
        'Compared to single edge cutting knifes, it has either lower durability or dulls faster, '
        'For every day usage it has one of the best shape and it has great durability.\n'
        'The handle may be made of various materials. '
        'Most common are: any metal, varnished wood, antler or bone, hide, rubber or plastic.'
    ),
    ITEM_FLAG_WEAPON,
    4800, # value (hearts)
    280, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT), +4),
        
        Modifier(construct_modifier_type(MODIFIER_ID__BUTCHERING, MODIFIER_KIND__PERCENT), +15),
        Modifier(construct_modifier_type(MODIFIER_ID__HUNTING, MODIFIER_KIND__FLAT), 4),
        Modifier(construct_modifier_type(MODIFIER_ID__HUNTING, MODIFIER_KIND__PERCENT), +10),
    ),
    None,
)


ITEM_ACHING_AFFECTION_S_HEART_PIERCER = ITEMS[ITEM_ID_ACHING_AFFECTION_S_HEART_PIERCER] = Item(
    ITEM_ID_ACHING_AFFECTION_S_HEART_PIERCER,
    'Aching affection\'s Heart-piercer',
    BUILTIN_EMOJIS['knife'],
    (
        'A silver colored kitchen knife that can cut everything in the right hands. '
        'The spine of its back is curving forward, making it less top heavy, reducing its height. '
        'This allows it to better piercing compared to its regular counterparts.'
    ),
    ITEM_FLAG_WEAPON,
    82000, # value (hearts)
    380, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +5),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT), +4),
        
        Modifier(construct_modifier_type(MODIFIER_ID__BUTCHERING, MODIFIER_KIND__FLAT), 2),
        Modifier(construct_modifier_type(MODIFIER_ID__BUTCHERING, MODIFIER_KIND__PERCENT), +15),
        Modifier(construct_modifier_type(MODIFIER_ID__HUNTING, MODIFIER_KIND__PERCENT), +10),
    ),
    None,
)


ITEM_NINA = ITEMS[ITEM_ID_NINA] = Item(
    ITEM_ID_NINA,
    'Nina',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


ITEM_BROOM = ITEMS[ITEM_ID_BROOM] = Item(
    ITEM_ID_BROOM,
    'Broom',
    BUILTIN_EMOJIS['broom'],
    (
        'A popular housekeeping cleaning tool. Its common form a bundle which is attached to a long shaft. '
        'The bundle is usually made out from sorghum, perhaps twigs, from plastic bristles, or feathers.\n'
        'Dust or trash is collected with its help; typically used with a dustpan. '
        'For different cleaning jobs, different brooms are optimal.'
    ),
    ITEM_FLAG_WEAPON,
    900, # value (hearts)
    1428, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +5),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_BEDROOM, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT), +4),
    ),
    None,
)


ITEM_HAND_FAN = ITEMS[ITEM_ID_HAND_FAN] = Item(
    ITEM_ID_HAND_FAN,
    'Hand fan',
    BUILTIN_EMOJIS['folding_hand_fan'],
    (
        'A popular tool since the ancient times, which can be fanned to produce airflow. '
        'The tool is broad with a flat surface, usually made out of thin materials like skin, feathers, paper or wood. '
        'General purpose fans are usually folding, and have the shape of a circle segment when opened.\n'
        'The generated airflow can be used for cooling, to rouse fire, to chase flies and other bugs away, '
        'or simply as a protective tool from the sun rays.'
    ),
    ITEM_FLAG_WEAPON,
    1000, # value (hearts)
    136, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +3),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_BEDROOM, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +4),
        
        Modifier(construct_modifier_type(MODIFIER_ID__HUNTING, MODIFIER_KIND__PERCENT), +20),
    ),
    None,
)


ITEM_PARASOL = ITEMS[ITEM_ID_PARASOL] = Item(
    ITEM_ID_PARASOL,
    'Parasol',
    BUILTIN_EMOJIS['closed_umbrella'],
    (
        'A shading tool used to keep the sun rays (either the light and/or the heat) away. '
        'It can be used to protect not only people, but also buildings, areas and vehicles as well.\n'
        'Its main parts being: the shaft, which is made out of bamboo, wood, or from metal nowadays; canopy, '
        'which is made out of linen, cotton or silk; ribs, that were made out from fish bones, although nowadays '
        'they are made out of really thin steel beams; stretchers which are also made out of thin steel beams, '
        'they connect the ribs with either the shaft or the runner which can be slid on the shaft to open or '
        'close the canopy.'
    ),
    ITEM_FLAG_WEAPON,
    1200, # value (hearts)
    1800, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +3),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +4),
        
        Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__PERCENT), +20),
    ),
    None,
)


ITEM_GOTHIC_ATTIRE = ITEMS[ITEM_ID_GOTHIC_ATTIRE] = Item(
    ITEM_ID_GOTHIC_ATTIRE,
    'Gothic attire',
    BUILTIN_EMOJIS['womans_clothes'],
    (
        'The outfit consists of a dress and vest with a frilled shirt underneath, '
        'ruffle socks and red sandals as well as a mob cap. '
    ),
    ITEM_FLAG_COSTUME,
    12000, # value (hearts)
    3840, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +8),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +5),
    ),
    None,
)


ITEM_HIKING_SET = ITEMS[ITEM_ID_HIKING_SET] = Item(
    ITEM_ID_HIKING_SET,
    'Hiking set',
    BUILTIN_EMOJIS['school_satchel'],
    (
        'Long stretch pants and a long sleeved t-shirt that provides excellent protection against vegetation and bugs '
        'while letting the body breath. Boots which hold the feet securely in place, keeping the user\'s heels '
        'planted. A backpack that can hold everything for the trip and a little more.\n'
        'For colder days, a jacket and a beanie is also worn.'
    ),
    ITEM_FLAG_COSTUME,
    7300, # value (hearts)
    2300, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_BEDROOM, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_LOYALTY, MODIFIER_KIND__FLAT), +2),
        
        Modifier(construct_modifier_type(MODIFIER_ID__INVENTORY, MODIFIER_KIND__FLAT), +10000),
        Modifier(construct_modifier_type(MODIFIER_ID__HEALTH, MODIFIER_KIND__PERCENT), +6),
        
        Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__FORAGING, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__HUNTING, MODIFIER_KIND__FLAT), +2),
    ),
    None,
)


ITEM_KIMONO = ITEMS[ITEM_ID_KIMONO] = Item(
    ITEM_ID_KIMONO,
    'Kimono',
    BUILTIN_EMOJIS['kimono'],
    (
        'The kimono\'s original meaning was wearable clothes, later on, it would become limited to only a few pieces.\n'
        'It\'s tailored to a T shape. Unlike most clothes, it doesn\'t follow the body\'s shape in '
        'favour of an angular appearance when worn.\n'
        'Traditionally, the left end of the kimono is folded over the right one.'
    ),
    ITEM_FLAG_COSTUME,
    1800, # value (hearts)
    1400, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +3),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__FLAT), +2),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CUTENESS, MODIFIER_KIND__PERCENT), +20),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_BEDROOM, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +2),
    ),
    None,
)


ITEM_TWIGS = ITEMS[ITEM_ID_TWIGS] = Item(
    ITEM_ID_TWIGS,
    'Twigs',
    BUILTIN_EMOJIS['chopsticks'],
    (
        'Twigs are thin branches of trees or bushes. '
        'Due to their high surface to volume ratio, they catch on fire fast and burn on high temperature, '
        'making them really good for starting fires.'
    ),
    0,
    5, # value (hearts)
    134, # weight (grams)
    None,
    None,
)


ITEM_BOUGH = ITEMS[ITEM_ID_BOUGH] = Item(
    ITEM_ID_BOUGH,
    'Bough',
    BUILTIN_EMOJIS['chopsticks'],
    (
        'Thick branches of trees or bushes, usually 3 or more years old. '
        'They are thick enough to saw, but not thick enough to cut to fire wood.'
    ),
    0,
    50, # value (hearts)
    1206, # weight (grams)
    None,
    None,
)


ITEM_LOG = ITEMS[ITEM_ID_LOG] = Item(
    ITEM_ID_LOG,
    'Log',
    BUILTIN_EMOJIS['wood'],
    (
        'A slice of a trunk or of a really thick bough. '
        'They can be cut to firewood to use as a fuel and to make charcoal as well.'
    ),
    0,
    250, # value (hearts)
    5427, # weight (grams)
    None,
    None,
)


ITEM_BAMBOO = ITEMS[ITEM_ID_BAMBOO] = Item(
    ITEM_ID_BAMBOO,
    'Bamboo',
    BUILTIN_EMOJIS['tanabata_tree'],
    (
        'Bamboos belong to the family of Poaceae, but unlike its other members, '
        'bamboos\'s leaves are connected to its stem with petioles. '
        'Some bamboos develop to tress, their height is between 3 and 10 meters, '
        'and their stem width between 3 and 5 cm-s.\n'
        'Due to its hollow build, low weight and flexible stem, it can be used in most areas of life.'
    ),
    0,
    200, # value (hearts)
    5360, # weight (grams)
    None,
    None,
)


ITEM_CUT_WOOD = ITEMS[ITEM_ID_CUT_WOOD] = Item(
    ITEM_ID_CUT_WOOD,
    'Cut wood',
    BUILTIN_EMOJIS['wood'],
    (
        'A split log or sliced up bough, just the right width to fuel a fire.'
    ),
    0,
    250, # value (hearts)
    4824, # weight (grams)
    None,
    None,
)


ITEM_EIRIN = ITEMS[ITEM_ID_EIRIN] = Item(
    ITEM_ID_EIRIN,
    'Eirin',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


ITEM_REIMU = ITEMS[ITEM_ID_REIMU] = Item(
    ITEM_ID_REIMU,
    'Reimu',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


ITEM_SAKE = ITEMS[ITEM_ID_SAKE] = Item(
    ITEM_ID_SAKE,
    'Sake',
    BUILTIN_EMOJIS['sake'],
    (
        'Sake is an alcoholic drink made by fermenting rice.\n'
        'They add enzyme-producing fungus and yeast to the soaked and cooked rice. '
        'This makes the sugaring and the sugar\'s fermentation happen at the same time.\n'
        'Sake originally is a broad term for any alcoholic drink. '
        'What we specifically call sake has its own name, nihonsu.'
    ),
    ITEM_FLAG_EDIBLE,
    1715, # value (hearts)
    880, # weight (grams), including the bottle, ofc
    None,
    None,
)


ITEM_SUIKA = ITEMS[ITEM_ID_SUIKA] = Item(
    ITEM_ID_SUIKA,
    'Suika',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


ITEM_SEKIBANKI = ITEMS[ITEM_ID_SEKIBANKI] = Item(
    ITEM_ID_SEKIBANKI,
    'Sekibanki',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


ITEM_KAGEROU = ITEMS[ITEM_ID_KAGEROU] = Item(
    ITEM_ID_KAGEROU,
    'Kagerou',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


ITEM_SEIRAN = ITEMS[ITEM_ID_SEIRAN] = Item(
    ITEM_ID_SEIRAN,
    'Seiran',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


ITEM_DANGO = ITEMS[ITEM_ID_DANGO] = Item(
    ITEM_ID_DANGO,
    'Dango',
    BUILTIN_EMOJIS['dango'],
    (
        'Dango is an kind dumpling made out of rice flour. They are usually round and are served on skewers.\n'
        'They are commonly covered or flavoured with sugar, syrup, red bean paste, green tea or and other sweeteners. '
        'It is often served with Tea\n'
        'Dango falls under the general category of confectionery, but has many traditional varieties. '
        'One of these varieties is the pink, white and green coloured one, '
        'which one may identify as the flagship dango. '
        'This exact variety is traditionally made during cherry blossom viewing season.'
    ),
    ITEM_FLAG_EDIBLE,
    150, # value (hearts)
    46, # weight (grams), including the skewers, ofc
    None,
    None,
)


ITEM_FLANDRE = ITEMS[ITEM_ID_FLANDRE] = Item(
    ITEM_ID_FLANDRE,
    'Flandre',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


ITEM_REMILIA = ITEMS[ITEM_ID_REMILIA] = Item(
    ITEM_ID_REMILIA,
    'Remilia',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


ITEM_PUDDING = ITEMS[ITEM_ID_PUDDING] = Item(
    ITEM_ID_PUDDING,
    'Pudding',
    BUILTIN_EMOJIS['custard'],
    (
        'Pudding is mainly a sweet, although it has salty, meaty and doughy versions as well around the world.\n'
        'As a sweet, it usually describes something that has gelatinous, spongy or creamy consistency. '
        'Made from milk or fruit juice, with the usage of some kind of thickener, like starch, flour, rice, egg, etc.'
    ),
    ITEM_FLAG_EDIBLE,
    175, # value (hearts)
    190, # weight (grams), including the skewers, ofc
    None,
    None,
)


ITEM_TEA_LEAVES = ITEMS[ITEM_ID_TEA_LEAVES] = Item(
    ITEM_ID_TEA_LEAVES,
    'Tea leaves',
    BUILTIN_EMOJIS['leaves'],
    (
        'Tea leaves grow on Tea trees, which are usually raised to become shrubs. '
        'From the trees\' leaves or other parts an identically named cooked drink is made, tea.\n'
        'The tea bush is native to Asia, as the tea drink made from it. '
        'Cooking teas have plenty of physiological effect. '
        'Although different types may have different effects, so before drinking, '
        'it is recommended to read up their effects.'
    ),
    ITEM_FLAG_EDIBLE,
    90, # value (hearts)
    30, # weight (grams), including the skewers, ofc
    None,
    None,
)


ITEM_SATORI = ITEMS[ITEM_ID_SATORI] = Item(
    ITEM_ID_SATORI,
    'Satori',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


# 35 kg / human
ITEM_HUMAN_MUSCLE = ITEMS[ITEM_ID_HUMAN_MUSCLE] = Item(
    ITEM_ID_HUMAN_MUSCLE,
    'Human Muscle',
    BUILTIN_EMOJIS['cut_of_meat'],
    (
        'Muscles are organs made out of tissues which specialise for retraction. '
        'To retract, they are converting chemical energy to mechanical energy.'
    ),
    ITEM_FLAG_EDIBLE,
    50, # value (hearts)
    100, # weight (grams)
    None,
    None,
)


# 2 / human
ITEM_HUMAN_EYE = ITEMS[ITEM_ID_HUMAN_EYE] = Item(
    ITEM_ID_HUMAN_EYE,
    'Human Eye',
    BUILTIN_EMOJIS['eye'],
    (
        'An eye is a sensory organ which captures possible stimulus\' from electromagnetic radiation of the range '
        'of light.'
    ),
    ITEM_FLAG_EDIBLE,
    7, # value (hearts)
    57, # weight (grams)
    None,
    None,
)


# 1 / human
ITEM_HUMAN_BRAIN = ITEMS[ITEM_ID_HUMAN_BRAIN] = Item(
    ITEM_ID_HUMAN_BRAIN,
    'Human brain',
    BUILTIN_EMOJIS['brain'],
    (
        'The brain is an the central nervous system of vertebrates located in their cranial cavity. '
        'This organ is responsible for receiving information from other sensory organs, for processing these signals, '
        'for the cognitive functions and the coordination of motor control.' 
    ),
    ITEM_FLAG_EDIBLE,
    894, # value (hearts)
    1300, # weight (grams)
    None,
    None,
)


# 2 / human
ITEM_HUMAN_LUNG = ITEMS[ITEM_ID_HUMAN_LUNG] = Item(
    ITEM_ID_HUMAN_LUNG,
    'Human lung',
    BUILTIN_EMOJIS['lungs'],
    (
        'The lung is the most important part of the respiratory system of vertebrates. '
        'It is responsible for capturing oxygen from the atmosphere into the bloodstream, '
        'and to release carbon-dioxide into the atmosphere from the bloodstream through exhaling.'
    ),
    ITEM_FLAG_EDIBLE,
    160, # value (hearts)
    550, # weight (grams)
    None,
    None,
)


# 1 / human
ITEM_HUMAN_HEART = ITEMS[ITEM_ID_HUMAN_HEART] = Item(
    ITEM_ID_HUMAN_HEART,
    'Human heart',
    BUILTIN_EMOJIS['anatomical_heart'],
    (
        'The heart is the central organ of the blood circulatory system. '
        'For vertebrates it is a hollow, muscular-walled tube, which pumps blood with rhythmic contractions.'
    ),
    ITEM_FLAG_EDIBLE,
    125, # value (hearts)
    325, # weight (grams)
    None,
    None,
)


# 1 / human
ITEM_HUMAN_LIVER = ITEMS[ITEM_ID_HUMAN_LIVER] = Item(
    ITEM_ID_HUMAN_LIVER,
    'Human liver',
    BUILTIN_EMOJIS['cut_of_meat'],
    (
        'Liver has an important role in the metabolic processes, in detoxification and in production and '
        'storage of certain compounds.'
    ),
    ITEM_FLAG_EDIBLE,
    441, # value (hearts)
    1400, # weight (grams)
    None,
    None,
)


# 1 / human
ITEM_HUMAN_INTESTINES = ITEMS[ITEM_ID_HUMAN_INTESTINES] = Item(
    ITEM_ID_HUMAN_INTESTINES,
    'Human intestines',
    BUILTIN_EMOJIS['worm'],
    (
        'Animal organism use their intestines to capture necessary substances, '
        'to build, maintain themselves and to satisfy their energy demands.'
    ),
    ITEM_FLAG_EDIBLE,
    30, # value (hearts)
    200, # weight (grams)
    None,
    None,
)


# 1 / human
ITEM_HUMAN_TRIPE = ITEMS[ITEM_ID_HUMAN_TRIPE] = Item(
    ITEM_ID_HUMAN_TRIPE,
    'Human tripe',
    BUILTIN_EMOJIS['rock'],
    (
        'Tripe is a food product, mainly made out of cattle\'s pre-stomach used for ruminanting.'
    ),
    ITEM_FLAG_EDIBLE,
    465, # value (hearts)
    910, # weight (grams)
    None,
    None,
)


# 1 / human
ITEM_HUMAN_PANCREAS = ITEMS[ITEM_ID_HUMAN_PANCREAS] = Item(
    ITEM_ID_HUMAN_PANCREAS,
    'Human pancreas',
    BUILTIN_EMOJIS['dumpling'],
    (
        'Pancreas is both an exocrine and an endocrine glad of vertebrates.'
        'As as exocrine, it produces stomach saliva produced by the pancreas consist of many important digestive '
        'ensime. '
        'As endocrine, it produces highly important hormones, like insulin, glucagon and somatostatin.'
    ),
    ITEM_FLAG_EDIBLE,
    25, # value (hearts)
    100, # weight (grams)
    None,
    None,
)


# 1 / human
ITEM_HUMAN_SPLEEN = ITEMS[ITEM_ID_HUMAN_SPLEEN] = Item(
    ITEM_ID_HUMAN_SPLEEN,
    'Human spleen',
    BUILTIN_EMOJIS['potato'],
    (
        'The spleen is a sponge like lymphatic organ. '
        'Its function is to destruct aged red blood cells, to produce lymphocytes, immune substance, '
        'and store various other substances.'
    ),
    ITEM_FLAG_EDIBLE,
    42, # value (hearts)
    170, # weight (grams)
    None,
    None,
)


# 2 / human
ITEM_HUMAN_KIDNEY = ITEMS[ITEM_ID_HUMAN_KIDNEY] = Item(
    ITEM_ID_HUMAN_KIDNEY,
    'Human kidney',
    BUILTIN_EMOJIS['ballet_shoes'],
    (
        'The kidney is the excretory organ of the vertebrates. '
        'It is responsible for eliminating end-metabolism water-soluble products. '
        'Additionally it has elementary role in salt and water keeping and in homeostasis.'
    ),
    ITEM_FLAG_EDIBLE,
    45, # value (hearts)
    150, # weight (grams)
    None,
    None,
)


# 5 kg / human
ITEM_HUMAN_BLOOD = ITEMS[ITEM_ID_HUMAN_BLOOD] = Item(
    ITEM_ID_HUMAN_BLOOD,
    'Human blood',
    BUILTIN_EMOJIS['wine_glass'],
    (
        'Blood is mainly red coloured, the body liquid of secondary body cavity invertebrate and vertebrates. '
        'Its main purpose is to transport carbon-dioxide, nutrients, water and the dissolved metabolism products. '
        'Additionally it has an important role in immune responses, transferring hormones and in regulating body '
        'temperature.'
    ),
    ITEM_FLAG_EDIBLE,
    6, # value (hearts)
    100, # weight (grams)
    None,
    None,
)


# 1 kg / human
ITEM_HUMAN_CARTILAGE = ITEMS[ITEM_ID_HUMAN_CARTILAGE] = Item(
    ITEM_ID_HUMAN_CARTILAGE,
    'Human cartilage',
    BUILTIN_EMOJIS['fish_cake'],
    (
        'Cartilage is a medium solid, flexible supporting tissues. The cartilage of vertebrates slowly ossifies. '
        'It consists of cells and the base substance surrounding them. '
        'From the outside it is covered with membrane consisting of connective tissues, blood vessels and nervous '
        'tissue. '
        'Inside of the cartilage there are no blood vessels, therefore its metabolism is slow.'
    ),
    ITEM_FLAG_EDIBLE,
    1, # value (hearts)
    20, # weight (grams)
    None,
    None,
)


# 10.5 kg / human
ITEM_HUMAN_FAT = ITEMS[ITEM_ID_HUMAN_FAT] = Item(
    ITEM_ID_HUMAN_FAT,
    'Human fat',
    BUILTIN_EMOJIS['rock'],
    (
        'The fat tissue is a tissue of animals, mainly built out of fat cells. '
        'It\'s main purpose is to store energy, to protect the organism from physical effects and to '
        'pillow out specific organs. It has two types, yellow or white and brown. '
        'The brown one can be found in animals which hibernate, producing significant amount heat.'
    ),
    ITEM_FLAG_EDIBLE,
    28, # value (hearts)
    100, # weight (grams)
    None,
    None,
)


# 17 g / human
ITEM_HUMAN_HAIR = ITEMS[ITEM_ID_HUMAN_HAIR] = Item(
    ITEM_ID_HUMAN_HAIR,
    'Human hair',
    BUILTIN_EMOJIS['thread'],
    (
        'Hair is the fur located on the human head which is protecting the skull. '
        'Alongside this, it also a determining factor of their outlook.'
    ),
    0,
    1, # value (hearts)
    17, # weight (grams)
    None,
    None,
)


# 20 / human
ITEM_HUMAN_NAIL = ITEMS[ITEM_ID_HUMAN_NAIL] = Item(
    ITEM_ID_HUMAN_NAIL,
    'Human nail',
    BUILTIN_EMOJIS['nail_care_tone1'],
    (
        'Nail is protective plate found at the back side of the last digit of fingers. '
        'It is slightly is slightly convex in the middle.'
    ),
    0,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


# 180g / human (Could not find any info about it, so made it up)
ITEM_HUMAN_NERVOUS_TISSUE = ITEMS[ITEM_ID_HUMAN_NERVOUS_TISSUE] = Item(
    ITEM_ID_HUMAN_NERVOUS_TISSUE,
    'Human nervous tissue',
    BUILTIN_EMOJIS['knot'],
    (
        'Nervous tissue is a bundle of nerves in the peripheral nervous system. '
        'Nervous tissues are used as nervous fibers, transferring action potentials to peripheral organs; '
        'or at the case of receptor nerves, from the receptors to the central nervous system.'
    ),
    ITEM_FLAG_EDIBLE,
    1, # value (hearts)
    20, # weight (grams)
    None,
    None,
)


# 6 kg / human (Can be more)
ITEM_HUMAN_SKIN = ITEMS[ITEM_ID_HUMAN_SKIN] = Item(
    ITEM_ID_HUMAN_SKIN,
    'Human skin',
    BUILTIN_EMOJIS['full_moon'],
    (
        'Skin is the tissue covering the eumetazoas, it is their biggest organ. '
        'The most important function of skin is to protect the body from external impacts. '
        'It does not provide only physical protection, but it also has an active immunology function containing '
        'special immune cells, which recognise pathogen and in starting the immune response against them.'
    ),
    ITEM_FLAG_EDIBLE,
    25, # value (hearts)
    100, # weight (grams)
    None,
    None,
)


# 7 kg / human
ITEM_HUMAN_BONE = ITEMS[ITEM_ID_HUMAN_BONE] = Item(
    ITEM_ID_HUMAN_BONE,
    'Human bone',
    BUILTIN_EMOJIS['bone'],
    (
        'Bones are a hard organ found in vertebrates. Bones are made out of highly mineralized tissues. '
        'The skeleton gives the body\'s shape and is protecting it from external impacts.'
    ),
    0,
    13, # value (hearts)
    100, # weight (grams)
    None,
    None,
)


# 32 / human
ITEM_HUMAN_TOOTH = ITEMS[ITEM_ID_HUMAN_TOOTH] = Item(
    ITEM_ID_HUMAN_TOOTH,
    'Human tooth',
    BUILTIN_EMOJIS['tooth'],
    (
        'The tooth is a a hard organ consisting of a visible crown, and root being fixated into the jaw. '
        'Teeth were developed by vertebrates. '
        'The dentition\'s consisting of teeth, main function is for grabbing food, '
        'while for mammals also to easy the digestion by chewing the food into smaller pieces.'
    ),
    0,
    1, # value (hearts)
    1, # weight (grams)
    None,
    None,
)


# 2 / human
ITEM_HUMAN_EAR = ITEMS[ITEM_ID_HUMAN_EAR] = Item(
    ITEM_ID_HUMAN_EAR,
    'Human ear',
    BUILTIN_EMOJIS['ear_tone1'],
    (
        'The auricle part of the outer auditory sense organ. It surrounds the ear canal in a cone shape.'
    ),
    ITEM_FLAG_EDIBLE,
    5, # value (hearts)
    14, # weight (grams)
    None,
    None,
)


# 1 / human
ITEM_HUMAN_TONGUE = ITEMS[ITEM_ID_HUMAN_TONGUE] = Item(
    ITEM_ID_HUMAN_TONGUE,
    'Human tongue',
    BUILTIN_EMOJIS['tongue'],
    (
        'Tongue is located in the oral cavity. '
        'It is a muscle with a characteristic shape, covered with mucous membrane. '
        'It has a determinative function in chewing, morsel-creation, speak and in forming specific facial expressions.'
    ),
    ITEM_FLAG_EDIBLE,
    33, # value (hearts)
    65, # weight (grams)
    None,
    None,
)


ITEM_HUMAN_BODY_PART_HAND = ITEMS[ITEM_ID_HUMAN_BODY_PART_HAND] = Item(
    ITEM_ID_HUMAN_BODY_PART_HAND,
    'Human hand',
    BUILTIN_EMOJIS['palm_up_hand_tone1'],
    (
        'Hand is the holding organ of the upper limbs of primates. The thumb helps most primates to have a better grip. '
        'Other terrestrial animals\' corresponding organ is usually called front leg or paw.'
    ),
    ITEM_FLAG_BUTCHERABLE,
    89, # value (hearts)
    400, # weight (grams)
    None,
    (
        OptionButcher(True, 1, 2, 1, ITEM_ID_HUMAN_CARTILAGE, 8, 0, 4),
        OptionButcher(True, 7, 10, 1, ITEM_ID_HUMAN_BONE, 6, 0, 0),
        OptionButcher(True, 3, 6, 1, ITEM_ID_HUMAN_MUSCLE, 10, 0, 4),
        OptionButcher(True, 1, 2, 1, ITEM_ID_HUMAN_SKIN, 5, 0, 3),
        OptionButcher(True, 3, 4, 5, ITEM_ID_HUMAN_NAIL, 0, 1, 1),
    ),
)


ITEM_HUMAN_BODY_PART_ARM = ITEMS[ITEM_ID_HUMAN_BODY_PART_ARM] = Item(
    ITEM_ID_HUMAN_BODY_PART_ARM,
    'Human arm',
    BUILTIN_EMOJIS['muscle_tone1'],
    (
        'Arm is the upper limb of primates.'
    ),
    ITEM_FLAG_BUTCHERABLE,
    791, # value (hearts)
    3500, # weight (grams)
    None,
    (
        OptionButcher(True, 9, 8, 1, ITEM_ID_HUMAN_BODY_PART_HAND, 2, 0, 4),
        OptionButcher(True, 1, 2, 3, ITEM_ID_HUMAN_CARTILAGE, 0, 1, 4),
        OptionButcher(True, 2, 5, 1, ITEM_ID_HUMAN_NERVOUS_TISSUE, 5, 0, 0),
        OptionButcher(True, 7, 10, 6, ITEM_ID_HUMAN_BONE, 6, 0, 0),
        OptionButcher(True, 4, 5, 10, ITEM_ID_HUMAN_MUSCLE, 3, 0, 1),
        OptionButcher(False, 1, 4, 12, ITEM_ID_HUMAN_MUSCLE, 0, 1, 0),
        OptionButcher(True, 4, 5, 4, ITEM_ID_HUMAN_SKIN, 3, 0, 1),
        OptionButcher(False, 1, 4, 3, ITEM_ID_HUMAN_SKIN, 0, 1, 1),
        OptionButcher(True, 4, 5, 1, ITEM_ID_HUMAN_FAT, 4, 0, 0),
        OptionButcher(False, 1, 4, 10, ITEM_ID_HUMAN_FAT, 0, 2, 0),
    ),
)


ITEM_HUMAN_BODY_PART_FOOT = ITEMS[ITEM_ID_HUMAN_BODY_PART_FOOT] = Item(
    ITEM_ID_HUMAN_BODY_PART_FOOT,
    'Human foot',
    BUILTIN_EMOJIS['foot_tone1'],
    (
        'Foot is an anatomical structure of many vertebrates located at the end of their limbs, '
        'allowing them locomotion.'
    ),
    ITEM_FLAG_BUTCHERABLE,
    204, # value (hearts)
    1000, # weight (grams)
    None,
    (
        OptionButcher(True, 1, 2, 2, ITEM_ID_HUMAN_CARTILAGE, 8, 0, 4),
        OptionButcher(True, 7, 10, 4, ITEM_ID_HUMAN_BONE, 6, 0, 0),
        OptionButcher(True, 3, 6, 2, ITEM_ID_HUMAN_MUSCLE, 10, 0, 4),
        OptionButcher(True, 1, 2, 2, ITEM_ID_HUMAN_SKIN, 5, 0, 3),
        OptionButcher(True, 3, 4, 5, ITEM_ID_HUMAN_NAIL, 0, 1, 1),
    ),
)


ITEM_HUMAN_BODY_PART_LEG = ITEMS[ITEM_ID_HUMAN_BODY_PART_LEG] = Item(
    ITEM_ID_HUMAN_BODY_PART_LEG,
    'Human leg',
    BUILTIN_EMOJIS['leg_tone1'],
    (
        'Leg is a part of animals that allows them to change their position on solid floor. '
        'It is called motion organ or limb.'
    ),
    ITEM_FLAG_BUTCHERABLE,
    1645, # value (hearts)
    5000, # weight (grams)
    None,
    (
        OptionButcher(True, 9, 8, 1, ITEM_ID_HUMAN_BODY_PART_FOOT, 2, 0, 4),
        OptionButcher(True, 1, 2, 4, ITEM_ID_HUMAN_CARTILAGE, 0, 1, 4),
        OptionButcher(True, 2, 5, 1, ITEM_ID_HUMAN_NERVOUS_TISSUE, 5, 0, 0),
        OptionButcher(True, 7, 10, 7, ITEM_ID_HUMAN_BONE, 6, 0, 0),
        OptionButcher(True, 4, 5, 23, ITEM_ID_HUMAN_MUSCLE, 6, 0, 1),
        OptionButcher(False, 1, 4, 10, ITEM_ID_HUMAN_MUSCLE, 0, 1, 0),
        OptionButcher(True, 4, 5, 7, ITEM_ID_HUMAN_SKIN, 6, 0, 1),
        OptionButcher(False, 1, 4, 6, ITEM_ID_HUMAN_SKIN, 0, 1, 1),
        OptionButcher(True, 4, 5, 1, ITEM_ID_HUMAN_FAT, 4, 0, 0),
        OptionButcher(False, 1, 4, 20, ITEM_ID_HUMAN_FAT, 0, 2, 0),
    ),
)


ITEM_HUMAN_BODY_PART_SKULL = ITEMS[ITEM_ID_HUMAN_BODY_PART_SKULL] = Item(
    ITEM_ID_HUMAN_BODY_PART_SKULL,
    'Human skull',
    BUILTIN_EMOJIS['skull'],
    (
        'Skull a bony part of many animals which servers as the base of their head. '
        'The face skull creates the base of the face\'s structure, the brain skull servers to protect the brain.'
    ),
    ITEM_FLAG_BUTCHERABLE,
    168, # value (hearts)
    1200, # weight (grams)
    None,
    (
        OptionButcher(True, 4, 5, 12, ITEM_ID_HUMAN_BONE, 12, 0, 0),
        OptionButcher(True, 4, 5, 12, ITEM_ID_HUMAN_TOOTH, 0, 1, 2),
        OptionButcher(True, 3, 5, 8, ITEM_ID_HUMAN_TOOTH, 0, 1, 3),
        OptionButcher(True, 2, 5, 8, ITEM_ID_HUMAN_TOOTH, 0, 2, 6),
        OptionButcher(False, 1, 5, 4, ITEM_ID_HUMAN_TOOTH, 0, 3, 0),
    ),
)


ITEM_HUMAN_BODY_PART_HEAD = ITEMS[ITEM_ID_HUMAN_BODY_PART_HEAD] = Item(
    ITEM_ID_HUMAN_BODY_PART_HEAD,
    'Human head',
    BUILTIN_EMOJIS['adult_tone1'],
    (
        'The head of an animal is usually located at its rostral part. It usually holds eyes, ears, nose and mouth.'
    ),
    ITEM_FLAG_BUTCHERABLE,
    1670, # value (hearts)
    5200, # weight (grams)
    None,
    (
        OptionButcher(True, 9, 8, 1, ITEM_ID_HUMAN_BODY_PART_SKULL, 8, 0, 4),
        OptionButcher(True, 1, 2, 2, ITEM_ID_HUMAN_CARTILAGE, 0, 3, 4),
        OptionButcher(True, 3, 4, 1, ITEM_ID_HUMAN_BRAIN, 4, 0, 4),
        OptionButcher(True, 4, 5, 1, ITEM_ID_HUMAN_TONGUE, 3, 0, 4),
        OptionButcher(True, 9, 10, 1, ITEM_ID_HUMAN_EAR, 1, 0, 0),
        OptionButcher(True, 4, 5, 1, ITEM_ID_HUMAN_EYE, 2, 0, 4), 
        OptionButcher(True, 3, 5, 1, ITEM_ID_HUMAN_EYE, 2, 0, 4),
        OptionButcher(True, 9, 10, 1, ITEM_ID_HUMAN_HAIR, 2, 0, 2),
        OptionButcher(False, 1, 2, 1, ITEM_ID_HUMAN_HAIR, 0, 2, 0),
        OptionButcher(True, 4, 2, 1, ITEM_ID_HUMAN_BONE, 1, 0, 0),
        OptionButcher(True, 7, 10, 7, ITEM_ID_HUMAN_MUSCLE, 0, 1, 0),
        OptionButcher(True, 4, 5, 5, ITEM_ID_HUMAN_SKIN, 0, 2, 3), 
        OptionButcher(True, 4, 5, 3, ITEM_ID_HUMAN_FAT, 4, 0, 0),
    ),
)


ITEM_HUMAN_BODY_PART_DIGESTIVE_ORGANS = ITEMS[ITEM_ID_HUMAN_BODY_PART_DIGESTIVE_ORGANS] = Item(
    ITEM_ID_HUMAN_BODY_PART_DIGESTIVE_ORGANS,
    'Human digestive organs',
    BUILTIN_EMOJIS['worm'],
    (
        'At the case of animal bodies, it is responsible for capturing necessary substances, '
        'for building, maintaining themselves and for satisfying their energy demands.'
    ),
    ITEM_FLAG_BUTCHERABLE,
    790, # value (hearts)
    4700, # weight (grams)
    None,
    (
        OptionButcher(True, 3, 4, 10, ITEM_ID_HUMAN_INTESTINES, 0, 2, 3),
        OptionButcher(True, 3, 4, 1, ITEM_ID_HUMAN_TRIPE, 5, 0, 5),
        OptionButcher(True, 4, 5, 1, ITEM_ID_HUMAN_PANCREAS, 1, 0, 4),
        OptionButcher(False, 1, 2, 2, ITEM_ID_HUMAN_FAT, 0, 1, 0),
    ),
)


ITEM_HUMAN_BODY_PART_INTERNALS = ITEMS[ITEM_ID_HUMAN_BODY_PART_INTERNALS] = Item(
    ITEM_ID_HUMAN_BODY_PART_INTERNALS,
    'Human internals',
    BUILTIN_EMOJIS['ballet_shoes'],
    (
        'A collection of organs.'
    ),
    ITEM_FLAG_BUTCHERABLE,
    958, # value (hearts)
    3200, # weight (grams)
    None,
    (
        OptionButcher(True, 3, 4, 2, ITEM_ID_HUMAN_LUNG, 0, 1, 0),
        OptionButcher(True, 9, 10, 1, ITEM_ID_HUMAN_HEART, 0, 1, 2),
        OptionButcher(True, 9, 10, 1, ITEM_ID_HUMAN_LIVER, 0, 1, 0),
        OptionButcher(True, 9, 10, 1, ITEM_ID_HUMAN_SPLEEN, 0, 1, 0),
        OptionButcher(True, 4, 5, 2, ITEM_ID_HUMAN_KIDNEY, 0, 1, 0),
        OptionButcher(True, 3, 4, 2, ITEM_ID_HUMAN_MUSCLE, 0, 1, 0),
        OptionButcher(False, 1, 2, 3, ITEM_ID_HUMAN_MUSCLE, 0, 1, 0),
        OptionButcher(False, 1, 2, 3, ITEM_ID_HUMAN_FAT, 0, 1, 0),
    ),
)


ITEM_HUMAN_BODY_PART_TORSO = ITEMS[ITEM_ID_HUMAN_BODY_PART_TORSO] = Item(
    ITEM_ID_HUMAN_BODY_PART_TORSO,
    'Human torso',
    BUILTIN_EMOJIS['running_shirt_with_sash'],
    (
        'Torso is the central part of animals from which other parts; head, limbs, tail and other attachment grow out.'
    ),
    ITEM_FLAG_BUTCHERABLE,
    11822, # value (hearts)
    35000, # weight (grams)
    None,
    (
        OptionButcher(True, 7, 10, 34, ITEM_ID_HUMAN_BONE, 6, 0, 0),
        OptionButcher(True, 4, 5, 100, ITEM_ID_HUMAN_MUSCLE, 20, 0, 0),
        OptionButcher(True, 3, 5, 100, ITEM_ID_HUMAN_MUSCLE, 0, 1, 2),
        OptionButcher(False, 1, 2, 40, ITEM_ID_HUMAN_MUSCLE, 0, 1, 0),
        OptionButcher(True, 4, 5, 24, ITEM_ID_HUMAN_SKIN, 20, 0, 1),
        OptionButcher(False, 1, 2, 14, ITEM_ID_HUMAN_SKIN, 0, 1, 0),
        OptionButcher(True, 1, 2, 60, ITEM_ID_HUMAN_CARTILAGE, 20, 0, 2),
        OptionButcher(False, 1, 2, 18, ITEM_ID_HUMAN_CARTILAGE, 0, 1, 0),
        OptionButcher(True, 1, 2, 36, ITEM_ID_HUMAN_FAT, 20, 0, 1),
        OptionButcher(False, 1, 2, 20, ITEM_ID_HUMAN_FAT, 0, 1, 0),
    ),
)


ITEM_HUMAN_BODY = ITEMS[ITEM_ID_HUMAN_BODY] = Item(
    ITEM_ID_HUMAN_BODY,
    'Human body',
    BUILTIN_EMOJIS['person_doing_cartwheel_tone1'],
    (
        'The most abundant and widespread species of primates. '
        'They can be characterised by minimal body-hair, sweating, body structure allowing throwing '
        'and large complex brains.'
    ),
    ITEM_FLAG_BUTCHERABLE,
    20344, # value (hearts)
    68000, # weight (grams)
    None,
    (
        OptionButcher(True, 9, 10, 40, ITEM_ID_HUMAN_BLOOD, 6, 0, 0),
        OptionButcher(False, 1, 2, 10, ITEM_ID_HUMAN_BLOOD, 0, 1, 0),
        OptionButcher(True, 9, 10, 1, ITEM_ID_HUMAN_BODY_PART_HEAD, 6, 0, 0),
        OptionButcher(True, 9, 10, 1, ITEM_ID_HUMAN_BODY_PART_LEG, 6, 0, 0),
        OptionButcher(True, 4, 5, 1, ITEM_ID_HUMAN_BODY_PART_LEG, 6, 0, 0),
        OptionButcher(True, 9, 10, 1, ITEM_ID_HUMAN_BODY_PART_ARM, 4, 0, 0),
        OptionButcher(True, 4, 5, 1, ITEM_ID_HUMAN_BODY_PART_ARM, 4, 0, 0),
        OptionButcher(True, 9, 10, 1, ITEM_ID_HUMAN_BODY_PART_INTERNALS, 6, 0, 0),
        OptionButcher(True, 4, 5, 1, ITEM_ID_HUMAN_BODY_PART_DIGESTIVE_ORGANS, 6, 0, 30),
        OptionButcher(True, 9, 10, 1, ITEM_ID_HUMAN_BODY_PART_TORSO, 0, 0, 0),
    ),
)


ITEM_HUMAN_BODY_SHARD_BOTTOM_HALF = ITEMS[ITEM_ID_HUMAN_BODY_SHARD_BOTTOM_HALF] = Item(
    ITEM_ID_HUMAN_BODY_SHARD_BOTTOM_HALF,
    'Human body (bottom part)',
    BUILTIN_EMOJIS['person_kneeling_tone1'],
    (
        'A greatly damaged body of a human, where only the bottom parts are usable.'
    ),
    ITEM_FLAG_BUTCHERABLE,
    6399, # value (hearts)
    23000, # weight (grams)
    None,
    (
        OptionButcher(False, 1, 2, 10, ITEM_ID_HUMAN_BLOOD, 0, 1, 0),
        OptionButcher(True, 9, 10, 1, ITEM_ID_HUMAN_BODY_PART_LEG, 6, 0, 0),
        OptionButcher(True, 4, 5, 1, ITEM_ID_HUMAN_BODY_PART_LEG, 6, 0, 0),
            
        OptionButcher(True, 7, 10, 8, ITEM_ID_HUMAN_BONE, 6, 0, 0),
        OptionButcher(True, 4, 5, 50, ITEM_ID_HUMAN_MUSCLE, 0, 2, 1),
        OptionButcher(True, 4, 5, 7, ITEM_ID_HUMAN_SKIN, 0, 2, 3),
        OptionButcher(True, 1, 2, 10, ITEM_ID_HUMAN_CARTILAGE, 0, 2, 4),
        OptionButcher(True, 1, 2, 13, ITEM_ID_HUMAN_FAT, 0, 2, 1),
    ),
)


ITEM_HUMAN_BODY_SHARD_TOP_HALF = ITEMS[ITEM_ID_HUMAN_BODY_SHARD_TOP_HALF] = Item(
    ITEM_ID_HUMAN_BODY_SHARD_TOP_HALF,
    'Human body (top part)',
    BUILTIN_EMOJIS['person_kneeling_tone1'],
    (
        'A greatly damaged body of a human, where only the top parts are usable.'
    ),
    ITEM_FLAG_BUTCHERABLE,
    6361, # value (hearts)
    23000, # weight (grams)
    None,
    (
        OptionButcher(False, 1, 2, 10, ITEM_ID_HUMAN_BLOOD, 0, 1, 0),
        OptionButcher(True, 9, 10, 1, ITEM_ID_HUMAN_BODY_PART_HEAD, 6, 0, 0),
        OptionButcher(True, 9, 10, 1, ITEM_ID_HUMAN_BODY_PART_ARM, 6, 0, 0),
        OptionButcher(True, 4, 5, 1, ITEM_ID_HUMAN_BODY_PART_ARM, 6, 0, 0),
        
        OptionButcher(True, 7, 10, 8, ITEM_ID_HUMAN_BONE, 6, 0, 0),
        OptionButcher(True, 4, 5, 50, ITEM_ID_HUMAN_MUSCLE, 0, 2, 1),
        OptionButcher(True, 4, 5, 7, ITEM_ID_HUMAN_SKIN, 0, 2, 3),
        OptionButcher(True, 1, 2, 10, ITEM_ID_HUMAN_CARTILAGE, 0, 2, 4),
        OptionButcher(True, 1, 2, 13, ITEM_ID_HUMAN_FAT, 0, 2, 1),
    ),
)


ITEM_HUMAN_BODY_SHARD_CHEWED = ITEMS[ITEM_ID_HUMAN_BODY_SHARD_CHEWED] = Item(
    ITEM_ID_HUMAN_BODY_SHARD_CHEWED,
    'Human body chewed',
    BUILTIN_EMOJIS['dancer_tone1'],
    (
        'A medium damaged body of a human, where parts appear to be chewed on.'
    ),
    ITEM_FLAG_BUTCHERABLE,
    16179, # value (hearts)
    54400, # weight (grams)
    None,
    (
        OptionButcher(True, 4, 5, 20, ITEM_ID_HUMAN_BLOOD, 6, 0, 0),
        OptionButcher(False, 1, 2, 5, ITEM_ID_HUMAN_BLOOD, 0, 1, 0),
        OptionButcher(True, 2, 5, 1, ITEM_ID_HUMAN_BODY_PART_HEAD, 6, 0, 0),
        OptionButcher(True, 2, 5, 1, ITEM_ID_HUMAN_BODY_PART_LEG, 5, 0, 0),
        OptionButcher(False, 3, 5, 1, ITEM_ID_HUMAN_BODY_PART_LEG, 5, 0, 0),
        OptionButcher(True, 2, 5, 1, ITEM_ID_HUMAN_BODY_PART_ARM, 3, 0, 0),
        OptionButcher(False, 3, 5, 1, ITEM_ID_HUMAN_BODY_PART_ARM, 3, 0, 0),
        OptionButcher(True, 2, 5, 1, ITEM_ID_HUMAN_BODY_PART_INTERNALS, 6, 0, 0),
        OptionButcher(True, 2, 5, 1, ITEM_ID_HUMAN_BODY_PART_DIGESTIVE_ORGANS, 6, 0, 30),
        OptionButcher(True, 2, 5, 1, ITEM_ID_HUMAN_BODY_PART_TORSO, 0, 0, 0),
    ),
)


ITEM_RICE = ITEMS[ITEM_ID_RICE] = Item(
    ITEM_ID_RICE,
    'Rice',
    BUILTIN_EMOJIS['rice'],
    (
        'A domesticated cereal grain, it is the staple food of over half of humanity.\n'
        'The plant itself grows to over a meter tall. It takes around half a year for it to be sown.\n'
        '\n'
        'They can be found in the outskirts of **Human Village**.'
    ),
    ITEM_FLAG_EDIBLE,
    55, # value (hearts)
    100, # weight (grams)
    None,
    None,
)


ITEM_RUMIA = ITEMS[ITEM_ID_RUMIA] = Item(
    ITEM_ID_RUMIA,
    'Rumia',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


ITEM_LIVER_SAUSAGE = ITEMS[ITEM_ID_LIVER_SAUSAGE] = Item(
    ITEM_ID_LIVER_SAUSAGE,
    'Liver sausage',
    BUILTIN_EMOJIS['worm'],
    (
        'Boiled sausage is a stuffed good which should be eaten after cooked or fried. '
        'It may be made out of meats or various organs of slaughter animals. '
        'It is made of of spiced filling stuffed into a natural or artificial cover.\n'
        'It has multiple popular versions, like blood, liver, rice and lung.'
    ),
    ITEM_FLAG_EDIBLE,
    250, # value (hearts)
    500, # weight (grams)
    None,
    None,
)


ITEM_BLOOD_SAUSAGE = ITEMS[ITEM_ID_BLOOD_SAUSAGE] = Item(
    ITEM_ID_BLOOD_SAUSAGE,
    'Blood sausage',
    ITEM_LIVER_SAUSAGE.emoji,
    ITEM_LIVER_SAUSAGE.description,
    ITEM_LIVER_SAUSAGE.flags,
    ITEM_LIVER_SAUSAGE.value,
    ITEM_LIVER_SAUSAGE.weight,
    None,
    None
)


ITEM_MEAT_SAUSAGE = ITEMS[ITEM_ID_MEAT_SAUSAGE] = Item(
    ITEM_ID_MEAT_SAUSAGE,
    'Meat sausage',
    ITEM_LIVER_SAUSAGE.emoji,
    ITEM_LIVER_SAUSAGE.description,
    ITEM_LIVER_SAUSAGE.flags,
    ITEM_LIVER_SAUSAGE.value,
    ITEM_LIVER_SAUSAGE.weight,
    None,
    None
)


ITEM_PATCHOULI = ITEMS[ITEM_ID_PATCHOULI] = Item(
    ITEM_ID_PATCHOULI,
    'Patchouli',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


ITEM_AYA = ITEMS[ITEM_ID_AYA] = Item(
    ITEM_ID_AYA,
    'Aya',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


ITEM_RAMEN = ITEMS[ITEM_ID_RAMEN] = Item(
    ITEM_ID_RAMEN,
    'Ramen',
    BUILTIN_EMOJIS['ramen'],
    (
        'Ramen is a Japanese noodle soup. '
        'It is made out of chinese style wheat flour noodles, broth made out of meat (sometimes fish), '
        'which is commonly flavoured with soy sauce or miso. '
        'For topping mostly pork, dried seaweed, kamaboko and green onions are used.\n'
        'In Japan almost every region has its own variety.'
    ),
    ITEM_FLAG_EDIBLE,
    375, # value (hearts)
    400, # weight (grams)
    None,
    None,
)


ITEM_PEN = ITEMS[ITEM_ID_PEN] = Item(
    ITEM_ID_PEN,
    'Pen',
    BUILTIN_EMOJIS['pen_ballpoint'],
    (
        'The pen is a writing tool that in the process of writing or drawing to transport ink '
        'onto the writing surface (most commonly into paper). '
        'Through the history humans used writing tools made out of reed or bird feather; '
        'while writing they submerged the nib into the ink.\n.'
        'The kind of pens used nowadays are the ballpoint pen, the fountain pen, the felt pen and the rollerball pen.'
    ),
    ITEM_FLAG_WEAPON,
    2424, # value (hearts)
    30, # weight (grams)
    (
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_HOUSEWIFE, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_BEDROOM, MODIFIER_KIND__FLAT), +3),
        Modifier(construct_modifier_type(MODIFIER_ID__STAT_CHARM, MODIFIER_KIND__FLAT), +3),
        
        Modifier(construct_modifier_type(MODIFIER_ID__GARDENING, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__GARDENING, MODIFIER_KIND__PERCENT), +5),
        Modifier(construct_modifier_type(MODIFIER_ID__FORAGING, MODIFIER_KIND__FLAT), +1),
        Modifier(construct_modifier_type(MODIFIER_ID__FORAGING, MODIFIER_KIND__PERCENT), +10),
        Modifier(construct_modifier_type(MODIFIER_ID__FISHING, MODIFIER_KIND__FLAT), +1),
    ),
    None,
)


ITEM_YOUMU = ITEMS[ITEM_ID_YOUMU] = Item(
    ITEM_ID_YOUMU,
    'Youmu',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


ITEM_NITORI = ITEMS[ITEM_ID_NITORI] = Item(
    ITEM_ID_NITORI,
    'Nitori',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


ITEM_PARSEE = ITEMS[ITEM_ID_PARSEE] = Item(
    ITEM_ID_PARSEE,
    'Parsee',
    None,
    None,
    ITEM_FLAG_NPC,
    0, # value (hearts)
    0, # weight (grams)
    None,
    None,
)


ITEM_SUNFLOWER = ITEMS[ITEM_ID_SUNFLOWER] = Item(
    ITEM_ID_SUNFLOWER,
    'Sunflower',
    BUILTIN_EMOJIS['sunflower'],
    (
        'Sunflowers grow 1 - 3 meters tall, herbaceous plant. Its stem is sponge like. '
        'There are types which grow 2.5 - 3.2 meters tall and their stem splits, holding multiple plates; '
        'Although the farmed varieties are short 1 - 2 meters tall, without branching.\n'
        '\n'
        'Its roots are advanced, copious secondary roots are growing out of taproot, which  penetrates deep into the '
        'soil. '
        'Its leaves are big, heart shaped, which connect to the stem with their shaft. '
        'Its nest inflorescence is surrounded by its side with nest scales. '
        'At the side of its plate are tongued flowers which serve as a connecting point for insects. '
        'Moving towards the middle of the plate, it holds hermaphroditic flowers, which mature their stamen before '
        'their stigma.\n'
        '\n'
        'Sunflower is one of the arable crop plats. '
        'Since its oil has favourable life physiological benefits, it counts as a medical herb.'
    ),
    ITEM_FLAG_EDIBLE,
    40, # value (hearts)
    4160, # weight (grams)
    None,
    None,
)
