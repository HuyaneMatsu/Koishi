__all__ = ()

from ..item_core import (
    ITEM_ID_ALICE, ITEM_ID_BLUEBERRY, ITEM_ID_BLUEFRANKISH, ITEM_ID_CARROT, ITEM_ID_CHIRUNO, ITEM_ID_DEVILCART_OYSTER,
    ITEM_ID_FISHING_ROD, ITEM_ID_FLYKILLER_AMANITA, ITEM_ID_FROG, ITEM_ID_GARLIC, ITEM_ID_MARISA, ITEM_ID_MYSTIA,
    ITEM_ID_PEACH, ITEM_ID_SAKUYA, ITEM_ID_SCARLET_ONION, ITEM_ID_STRAWBERRY
)

from .amount_types import AMOUNT_TYPE_COUNT, AMOUNT_TYPE_WEIGHT
from .constants import DAY_IN_SECONDS, HOUR_IN_SECONDS, QUEST_TEMPLATES
from .quest_template import QuestTemplate
from .quest_template_ids import (
    QUEST_TEMPLATE_ID_ALICE_FLYKILLER_AMANITA, QUEST_TEMPLATE_ID_CHIRUNO_FROG,
    QUEST_TEMPLATE_ID_MARISA_FLYKILLER_AMANITA, QUEST_TEMPLATE_ID_MYSTIA_CARROT,
    QUEST_TEMPLATE_ID_MYSTIA_DEVILCART_OYSTER, QUEST_TEMPLATE_ID_MYSTIA_GARLIC, QUEST_TEMPLATE_ID_MYSTIA_PEACH,
    QUEST_TEMPLATE_ID_MYSTIA_SCARLET_ONION, QUEST_TEMPLATE_ID_SAKUYA_BLUEBERRY, QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH,
    QUEST_TEMPLATE_ID_SAKUYA_DEVILCART_OYSTER, QUEST_TEMPLATE_ID_SAKUYA_FISHING_ROD,
    QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
)
from .quest_types import QUEST_TYPE_ITEM_SUBMISSION


# - Sakuya +1 level
# - non-village collection +1 level
# Reward is around 2.5x of the value
QUEST_SAKUYA_STRAWBERRY = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY] = QuestTemplate(
    QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
    (
        'The favourite snack of my mistress is Tudor Strawberry Tart.\n'
        '\n'
        'I would like to surprise them with it, for this I would like to request its main ingredient, Strawberries.'
    ),
    QUEST_TYPE_ITEM_SUBMISSION,
    2,
    ITEM_ID_STRAWBERRY,
    ITEM_ID_SAKUYA,
    1000,
    50,
    75,
    150,
    AMOUNT_TYPE_WEIGHT,
    DAY_IN_SECONDS * 3,
    HOUR_IN_SECONDS,
    70,
    120,
    3,
    2500,
    100,
    80,
    120,
)


# - non-village collection +1 level
# Reward is around 2.0x of the value
QUEST_TEMPLATE_MYSTIA_PEACH = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_PEACH] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_PEACH,
    (
        'I am running low to serve some fruits used in sweets and as compote served next to main dishes.\n'
        '\n'
        'Requesting a basketful of Peaches.'
    ),
    QUEST_TYPE_ITEM_SUBMISSION,
    1,
    ITEM_ID_PEACH,
    ITEM_ID_MYSTIA,
    20,
    1,
    75,
    150,
    AMOUNT_TYPE_COUNT,
    DAY_IN_SECONDS * 3,
    HOUR_IN_SECONDS,
    70,
    100,
    2,
    600,
    50,
    80,
    120,
)


# - Sakuya +1 level
# - non-village collection +1 level
# Reward is around 2.5x of the value
QUEST_TEMPLATE_SAKUYA_BLUEBERRY = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_SAKUYA_BLUEBERRY] = QuestTemplate(
    QUEST_TEMPLATE_ID_SAKUYA_BLUEBERRY,
    (
        'As tradition, serving wild meat in the mansion every weekend. This time with berry dressing.\n'
        '\n'
        'I would like to request enough blueberries for a single occasion.'
    ),
    QUEST_TYPE_ITEM_SUBMISSION,
    2,
    ITEM_ID_BLUEBERRY,
    ITEM_ID_SAKUYA,
    400,
    20,
    75,
    125,
    AMOUNT_TYPE_WEIGHT,
    DAY_IN_SECONDS * 6,
    HOUR_IN_SECONDS,
    70,
    120,
    3,
    800,
    50,
    90,
    120,
)


# - non-village collection +1 level
# Reward is around 2.0x of the value
QUEST_TEMPLATE_MYSTIA_DEVILCART_OYSTER = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_DEVILCART_OYSTER] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_DEVILCART_OYSTER,
    (
        'I am running low on mushroom to be prepared as part of foods.\n'
        '\n'
        'Requesting a basketful of Devilcart oysters.'
    ),
    QUEST_TYPE_ITEM_SUBMISSION,
    1,
    ITEM_ID_DEVILCART_OYSTER,
    ITEM_ID_MYSTIA,
    2000,
    100,
    75,
    215,
    AMOUNT_TYPE_WEIGHT,
    DAY_IN_SECONDS * 3,
    HOUR_IN_SECONDS,
    70,
    140,
    2,
    4600,
    100,
    90,
    110,
)


# - non-village collection +1 level
# Reward is around 2.5x of the value
#
# This is a +1 version of the mystia one. Here the duration is lower, making it harder.
QUEST_TEMPLATE_SAKUYA_DEVILCART_OYSTER = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_SAKUYA_DEVILCART_OYSTER] = QuestTemplate(
    QUEST_TEMPLATE_ID_SAKUYA_DEVILCART_OYSTER,
    (
        'My mistress, the mistress of the Scarlet Devil Mansion is greatly thrilled to have some splendid '
        'cream mushroom soup.\n'
        '\n'
        'I am making a request to retrieve a handful of Devilcart oysters in haste.'
    ),
    QUEST_TYPE_ITEM_SUBMISSION,
    2,
    ITEM_ID_DEVILCART_OYSTER,
    ITEM_ID_SAKUYA,
    1400,
    50,
    75,
    215,
    AMOUNT_TYPE_WEIGHT,
    DAY_IN_SECONDS * 2,
    HOUR_IN_SECONDS,
    50,
    100,
    3,
    4000,
    100,
    80,
    110,
)


# - Marisa +2 level
# - non-village collection +1 level
# Reward is around 1.5x of the value
QUEST_TEMPLATE_MARISA_FLYKILLER_AMANITA = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MARISA_FLYKILLER_AMANITA] = QuestTemplate(
    QUEST_TEMPLATE_ID_MARISA_FLYKILLER_AMANITA,
    (
        'I have great plans to cook some magic potions ze. For it I need a great batch of wonderful mushrooms.\n'
        '\n'
        'Please bring me a great batch of Flykiller amanita.'
    ),
    QUEST_TYPE_ITEM_SUBMISSION,
    3,
    ITEM_ID_FLYKILLER_AMANITA,
    ITEM_ID_MARISA,
    8000,
    500,
    85,
    125,
    AMOUNT_TYPE_WEIGHT,
    DAY_IN_SECONDS * 7,
    HOUR_IN_SECONDS,
    100,
    130,
    5,
    6300,
    100,
    90,
    110,
)


# - Sakuya +1 level
# - long term quest +1 level
# Reward is around 1.0x of the value
#
# This quest requires a lot of grapes, making it great. 
# Compared to the delivery it is not worth much tho.
# A big advantage is that this quest can scale pretty well upwards.
QUEST_TEMPLATE_SAKUYA_BLUEFRANKISH = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH] = QuestTemplate(
    QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH,
    (
        'We are running low on wine in the mansion.\n'
        '\n'
        'I would like to request a great amount of grapes.'
    ),
    QUEST_TYPE_ITEM_SUBMISSION,
    2,
    ITEM_ID_BLUEFRANKISH,
    ITEM_ID_SAKUYA,
    100000,
    1000,
    100,
    400,
    AMOUNT_TYPE_WEIGHT,
    DAY_IN_SECONDS * 6,
    HOUR_IN_SECONDS,
    90,
    110,
    3,
    10000,
    100,
    100,
    120,
)


# Reward is around 2.0x of the value
#
# This is a pretty easy quest. Since carrots have low value this quest is not worth much.
QUEST_TEMPLATE_MYSTIA_CARROT = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_CARROT] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_CARROT,
    (
        'I am running low on some vegetables for soups.\n'
        '\n'
        'Requesting a basketful of Carrot.'
    ),
    QUEST_TYPE_ITEM_SUBMISSION,
    0,
    ITEM_ID_CARROT,
    ITEM_ID_MYSTIA,
    9000,
    1000,
    50,
    120,
    AMOUNT_TYPE_WEIGHT,
    DAY_IN_SECONDS * 6,
    HOUR_IN_SECONDS,
    90,
    110,
    1,
    600,
    50,
    90,
    110,
)


# Reward is around 2.0x of the value
QUEST_TEMPLATE_MYSTIA_GARLIC = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_GARLIC] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_GARLIC,
    (
        'I am running low on a few seasonings for meats.\n'
        '\n'
        'Requesting a few Garlic.'
    ),
    QUEST_TYPE_ITEM_SUBMISSION,
    0,
    ITEM_ID_GARLIC,
    ITEM_ID_MYSTIA,
    10,
    1,
    75,
    125,
    AMOUNT_TYPE_COUNT,
    DAY_IN_SECONDS * 2,
    HOUR_IN_SECONDS,
    100,
    120,
    1,
    900,
    100,
    90,
    110,
)


# Reward is around 2.0x of the value
QUEST_TEMPLATE_MYSTIA_SCARLET_ONION = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_SCARLET_ONION] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_SCARLET_ONION,
    (
        'I am running severely low on regular onions.\n'
        '\n'
        'Requesting a basketful of Scarlet onions.'
    ),
    QUEST_TYPE_ITEM_SUBMISSION,
    0,
    ITEM_ID_SCARLET_ONION,
    ITEM_ID_MYSTIA,
    40,
    1,
    75,
    125,
    AMOUNT_TYPE_COUNT,
    DAY_IN_SECONDS * 2,
    HOUR_IN_SECONDS,
    100,
    120,
    1,
    1300,
    100,
    90,
    110,
)


# - Alice +3 level
# - non-village collection +1 level
# Reward is around 2.5x of the value
QUEST_TEMPLATE_ALICE_FLYKILLER_AMANITA = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_ALICE_FLYKILLER_AMANITA] = QuestTemplate(
    QUEST_TEMPLATE_ID_ALICE_FLYKILLER_AMANITA,
    (
        'I want to go to wonderland. For this all I need are spotty red mushrooms.\n'
        '\n'
        'Please bring me some Flykiller amanita.'
    ),
    QUEST_TYPE_ITEM_SUBMISSION,
    4,
    ITEM_ID_FLYKILLER_AMANITA,
    ITEM_ID_ALICE,
    700,
    50,
    70,
    120,
    AMOUNT_TYPE_WEIGHT,
    DAY_IN_SECONDS,
    HOUR_IN_SECONDS,
    100,
    130,
    5,
    1000,
    50,
    90,
    110,
)


# - Sakuya +1 level
# - misty lake +2 level
# - equipment + 1 level
# Reward is around 2.0x of the value
QUEST_TEMPLATE_SAKUYA_FISHING_ROD = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_SAKUYA_FISHING_ROD] = QuestTemplate(
    QUEST_TEMPLATE_ID_SAKUYA_FISHING_ROD,
    (
        'Recently I was accompanying Koishi for a fishing trip to the Misty lake. '
        'I though I packed everything up, but when I got home I noticed my fishing rod is nowhere.\n'
        '\n'
        'Could you please find me my missing fishing rod?'
    ),
    QUEST_TYPE_ITEM_SUBMISSION,
    4,
    ITEM_ID_FISHING_ROD,
    ITEM_ID_SAKUYA,
    1,
    1,
    100,
    100,
    AMOUNT_TYPE_COUNT,
    DAY_IN_SECONDS * 7,
    DAY_IN_SECONDS,
    100,
    120,
    5,
    6000,
    1000,
    100,
    120,
)


# - Chiruno +1 level
# - misty lake +2 level
# Reward is around 2.5x of the value
QUEST_TEMPLATE_CHIRUNO_FROG = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_CHIRUNO_FROG] = QuestTemplate(
    QUEST_TEMPLATE_ID_CHIRUNO_FROG,
    (
        'The coward frogs are hiding from me. '
        'How could I maintain my superiority image like this, '
        'if I cannot show them how inferior they are in front of my chilling powers?\n'
        '\n'
        'If you do not bring me some, you will be the one I state order through!'
    ),
    QUEST_TYPE_ITEM_SUBMISSION,
    3,
    ITEM_ID_FROG,
    ITEM_ID_CHIRUNO,
    10,
    1,
    100,
    200,
    AMOUNT_TYPE_COUNT,
    DAY_IN_SECONDS * 2,
    HOUR_IN_SECONDS,
    100,
    140,
    4,
    1150,
    50,
    80,
    120,
)
