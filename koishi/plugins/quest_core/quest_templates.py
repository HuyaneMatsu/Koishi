__all__ = ()

from ..item_core import (
    ITEM_GROUP_ID_FIREWOOD, ITEM_GROUP_ID_KNIFE, ITEM_ID_ALICE, ITEM_ID_ANGELROOT, ITEM_ID_BAMBOO_SHOOT,
    ITEM_ID_BISHOPHAT, ITEM_ID_BLUEBERRY, ITEM_ID_BLUEFRANKISH, ITEM_ID_CARROT, ITEM_ID_CHIRUNO, ITEM_ID_DAI,
    ITEM_ID_DEVILCART_OYSTER, ITEM_ID_EIRIN, ITEM_ID_FISHING_ROD, ITEM_ID_FLYKILLER_AMANITA, ITEM_ID_FROG,
    ITEM_ID_GARLIC, ITEM_ID_JUNKO, ITEM_ID_KOISHI, ITEM_ID_KOKORO, ITEM_ID_MARISA, ITEM_ID_MYSTIA, ITEM_ID_NINA,
    ITEM_ID_PEACH, ITEM_ID_REIMU, ITEM_ID_RULER, ITEM_ID_SAKE, ITEM_ID_SAKUYA, ITEM_ID_SCARLET_ONION, ITEM_ID_SCISSORS,
    ITEM_ID_STRAWBERRY, ITEM_ID_STRAW_HAT, ITEM_ID_SUIKA, ITEM_ID_TEWI, ITEM_ID_YUKARI, ITEM_ID_YUUKA
)

from .amount_types import AMOUNT_TYPE_COUNT, AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT
from .constants import DAY_IN_SECONDS, HOUR_IN_SECONDS, QUEST_TEMPLATES
from .quest_requirement_generators import (
    QuestRequirementGeneratorChoice, QuestRequirementGeneratorChoiceOption, QuestRequirementGeneratorDuration,
    QuestRequirementGeneratorItemExact, QuestRequirementGeneratorItemGroup
)
from .quest_reward_generators import (
    QuestRewardGeneratorBalance, QuestRewardGeneratorCredibility, QuestRewardGeneratorCredibilityFix,
    QuestRewardGeneratorItemExactFix
)
from .quest_template import QuestTemplate
from .quest_template_ids import (
    QUEST_TEMPLATE_ID_ALICE_ANGELROOT, QUEST_TEMPLATE_ID_ALICE_FLYKILLER_AMANITA, QUEST_TEMPLATE_ID_CHIRUNO_FROG,
    QUEST_TEMPLATE_ID_DAI_FROG, QUEST_TEMPLATE_ID_EIRIN_ANGELROOT_AND_BISHOPHAT, QUEST_TEMPLATE_ID_JUNKO_ANGELROOT,
    QUEST_TEMPLATE_ID_KOISHI_ANGELROOT, QUEST_TEMPLATE_ID_KOISHI_BISHOPHAT, QUEST_TEMPLATE_ID_KOISHI_GARLIC,
    QUEST_TEMPLATE_ID_KOISHI_KNIFE, QUEST_TEMPLATE_ID_KOISHI_RULER, QUEST_TEMPLATE_ID_KOKORO_SCISSORS,
    QUEST_TEMPLATE_ID_MARISA_FLYKILLER_AMANITA, QUEST_TEMPLATE_ID_MYSTIA_BAMBOO_SHOOT, QUEST_TEMPLATE_ID_MYSTIA_CARROT,
    QUEST_TEMPLATE_ID_MYSTIA_DEVILCART_OYSTER, QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD, QUEST_TEMPLATE_ID_MYSTIA_GARLIC,
    QUEST_TEMPLATE_ID_MYSTIA_PEACH, QUEST_TEMPLATE_ID_MYSTIA_SCARLET_ONION, QUEST_TEMPLATE_ID_NINA_STRAWBERRY,
    QUEST_TEMPLATE_ID_REIMU_BANQUET, QUEST_TEMPLATE_ID_SAKUYA_BLUEBERRY, QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH,
    QUEST_TEMPLATE_ID_SAKUYA_DEVILCART_OYSTER, QUEST_TEMPLATE_ID_SAKUYA_FISHING_ROD,
    QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, QUEST_TEMPLATE_ID_SUIKA_SAKE, QUEST_TEMPLATE_ID_TEWI_BISHOPHAT,
    QUEST_TEMPLATE_ID_YUKARI_RULER, QUEST_TEMPLATE_ID_YUUKA_STRAW_HAT
)


# - Sakuya +2 level
# - Ruins +1 level
# Reward is around 2.5x of the value
QUEST_SAKUYA_STRAWBERRY = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY] = QuestTemplate(
    QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
    (
        # If the mistress is requesting some creamy mushroom soup (yummy), you probably would not surprise them with
        # an other food.
        QUEST_TEMPLATE_ID_SAKUYA_DEVILCART_OYSTER,
    ),
    4, # Target: 1
    7,
    (
        'The favourite snack of my mistress is Tudor Strawberry Tart.\n'
        '\n'
        'I would like to surprise them with it, for this I would like to request its main ingredient, Strawberries.'
    ),
    3,
    1,
    ITEM_ID_SAKUYA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 3, HOUR_IN_SECONDS, 70, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000, 50, 75, 150),
    ),
    (
        QuestRewardGeneratorBalance(2300, 100, 80, 120),
        QuestRewardGeneratorCredibility(10),
    ),
)


# - Balancing +1 level
# - Hakugyokurou mansion +2 level
# Reward is around 2.0x of the value
QUEST_TEMPLATE_MYSTIA_PEACH = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_PEACH] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_PEACH,
    None,
    1,
    1,
    (
        'I am running low to serve some fruits used in sweets and as compote served next to main dishes.\n'
        '\n'
        'Requesting a basketful of Peaches.'
    ),
    3,
    3,
    ITEM_ID_MYSTIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 3, HOUR_IN_SECONDS, 70, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, 30, 5, 75, 150),
    ),
    (
        QuestRewardGeneratorBalance(2400, 50, 80, 120),
        QuestRewardGeneratorCredibility(10),
    ),
)


# - Sakuya +2 level
# - Moriya shrine +2 level
# Reward is around 2.5x of the value
QUEST_TEMPLATE_SAKUYA_BLUEBERRY = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_SAKUYA_BLUEBERRY] = QuestTemplate(
    QUEST_TEMPLATE_ID_SAKUYA_BLUEBERRY,
    None,
    4, # Target: 1
    7,
    (
        'As tradition, serving wild meat in the mansion every weekend. This time with berry dressing.\n'
        '\n'
        'I would like to request enough blueberries for a single occasion.'
    ),
    4,
    1,
    ITEM_ID_SAKUYA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 6, HOUR_IN_SECONDS, 70, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_BLUEBERRY, AMOUNT_TYPE_WEIGHT, 400, 20, 75, 125),
    ),
    (
        QuestRewardGeneratorBalance(1350, 50, 90, 120),
        QuestRewardGeneratorCredibility(20),
    ),
)


# - non-village collection +1 level
# Reward is around 2.0x of the value
QUEST_TEMPLATE_MYSTIA_DEVILCART_OYSTER = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_DEVILCART_OYSTER] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_DEVILCART_OYSTER,
    None,
    1,
    2,
    (
        'I am running low on mushroom to be prepared as part of foods.\n'
        '\n'
        'Requesting a basketful of Devilcart oysters.'
    ),
    1,
    3,
    ITEM_ID_MYSTIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 3, HOUR_IN_SECONDS, 70, 140),
        QuestRequirementGeneratorItemExact(ITEM_ID_DEVILCART_OYSTER, AMOUNT_TYPE_WEIGHT, 2000, 100, 75, 215),
    ),
    (
        QuestRewardGeneratorBalance(2300, 100, 90, 110),
        QuestRewardGeneratorCredibility(10),
    ),
)


# - non-village collection +1 level
# Reward is around 2.5x of the value
#
# This is a +1 version of the mystia one. Here the duration is lower, making it harder.
QUEST_TEMPLATE_SAKUYA_DEVILCART_OYSTER = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_SAKUYA_DEVILCART_OYSTER] = QuestTemplate(
    QUEST_TEMPLATE_ID_SAKUYA_DEVILCART_OYSTER,
    (
        # Exclude other sweet foods.
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
    ),
    4, # Target: 1
    7,
    (
        'My mistress, the mistress of the Scarlet Devil Mansion is greatly thrilled to have some splendid '
        'cream mushroom soup.\n'
        '\n'
        'I am making a request to retrieve a handful of Devilcart oysters in haste.'
    ),
    2,
    1,
    ITEM_ID_SAKUYA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 2, HOUR_IN_SECONDS, 67, 133),
        QuestRequirementGeneratorItemExact(ITEM_ID_DEVILCART_OYSTER, AMOUNT_TYPE_WEIGHT, 1400, 50, 75, 215),
    ),
    (
        QuestRewardGeneratorBalance(2000, 100, 80, 110),
        QuestRewardGeneratorCredibility(10),
    ),
)


# - Marisa +2 level
# - Magic forest +1 level
# Reward is around 1.5x of the value
QUEST_TEMPLATE_MARISA_FLYKILLER_AMANITA = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MARISA_FLYKILLER_AMANITA] = QuestTemplate(
    QUEST_TEMPLATE_ID_MARISA_FLYKILLER_AMANITA,
    None,
    4, # Target: 1
    14,
    (
        'I have great plans to cook some magic potions ze. For it I need a great batch of wonderful mushrooms.\n'
        '\n'
        'Please bring me a great batch of Flykiller amanita.'
    ),
    3,
    0,
    ITEM_ID_MARISA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 7, HOUR_IN_SECONDS, 100, 130),
        QuestRequirementGeneratorItemExact(ITEM_ID_FLYKILLER_AMANITA, AMOUNT_TYPE_WEIGHT, 8000, 500, 85, 125),
    ),
    (
        QuestRewardGeneratorBalance(6300, 100, 90, 110),
        QuestRewardGeneratorCredibility(30),
    ),
)


# - Sakuya +2 level
# Reward is around 1.5x of the value
#
# This quest requires a lot of grapes, making it great. 
# Compared to the delivery it is not worth much tho.
# A big advantage is that this quest can scale pretty well upwards.
QUEST_TEMPLATE_SAKUYA_BLUEFRANKISH = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH] = QuestTemplate(
    QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH,
    None,
    4, # Target: 1
    10,
    (
        'We are running low on wine in the mansion.\n'
        '\n'
        'I would like to request a great amount of grapes.'
    ),
    2,
    0,
    ITEM_ID_SAKUYA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 10, DAY_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_BLUEFRANKISH, AMOUNT_TYPE_WEIGHT, 100000, 1000, 100, 250),
    ),
    (
        QuestRewardGeneratorBalance(16000, 1000, 100, 120),
        QuestRewardGeneratorCredibility(50),
    ),
)


# Reward is around 2.0x of the value
#
# This is a pretty easy quest. Since carrots have low value this quest is not worth much.
QUEST_TEMPLATE_MYSTIA_CARROT = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_CARROT] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_CARROT,
    None,
    1,
    1,
    (
        'I am running low on some vegetables for soups.\n'
        '\n'
        'Requesting a basketful of Carrot.'
    ),
    0,
    3,
    ITEM_ID_MYSTIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 6, HOUR_IN_SECONDS, 90, 110),
        QuestRequirementGeneratorItemExact(ITEM_ID_CARROT, AMOUNT_TYPE_WEIGHT, 9000, 1000, 50, 120),
    ),
    (
        QuestRewardGeneratorBalance(2700, 50, 90, 110),
        QuestRewardGeneratorCredibility(10),
    ),
)


# Reward is around 2.0x of the value
QUEST_TEMPLATE_MYSTIA_GARLIC = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_GARLIC] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_GARLIC,
    None,
    1,
    1,
    (
        'I am running low on a few seasonings for meats.\n'
        '\n'
        'Requesting a few Garlic.'
    ),
    0,
    1,
    ITEM_ID_MYSTIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 2, HOUR_IN_SECONDS, 100, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_GARLIC, AMOUNT_TYPE_WEIGHT, 1000, 100, 75, 125),
    ),
    (
        QuestRewardGeneratorBalance(1050, 100, 90, 110),
        QuestRewardGeneratorCredibility(10),
    ),
)


# Reward is around 2.0x of the value
QUEST_TEMPLATE_MYSTIA_SCARLET_ONION = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_SCARLET_ONION] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_SCARLET_ONION,
    None,
    1,
    1,
    (
        'I am running severely low on regular onions.\n'
        '\n'
        'Requesting a basketful of Scarlet onions.'
    ),
    0,
    3,
    ITEM_ID_MYSTIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 2, HOUR_IN_SECONDS, 100, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_SCARLET_ONION, AMOUNT_TYPE_COUNT, 40, 1, 75, 125),
    ),
    (
        QuestRewardGeneratorBalance(1800, 100, 90, 110),
        QuestRewardGeneratorCredibility(10),
    ),
)


# - Alice +2 level
# - Magic forest +1 level
# - Short duration +1 level
# Reward is around 2.5x of the value
QUEST_TEMPLATE_ALICE_FLYKILLER_AMANITA = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_ALICE_FLYKILLER_AMANITA] = QuestTemplate(
    QUEST_TEMPLATE_ID_ALICE_FLYKILLER_AMANITA,
    None,
    4, # Target: 1
    10,
    (
        'I want to go to wonderland. For this all I need are spotty red mushrooms.\n'
        '\n'
        'Please bring me some Flykiller amanita.'
    ),
    4,
    1,
    ITEM_ID_ALICE,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS, HOUR_IN_SECONDS, 100, 130),
        QuestRequirementGeneratorItemExact(ITEM_ID_FLYKILLER_AMANITA, AMOUNT_TYPE_COUNT, 3, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(1300, 50, 90, 110),
        QuestRewardGeneratorCredibility(10),
    ),
)


# - Sakuya +2 level
# - misty lake +2 level
# - equipment +1 level
# Reward is around 2.0x of the value
QUEST_TEMPLATE_SAKUYA_FISHING_ROD = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_SAKUYA_FISHING_ROD] = QuestTemplate(
    QUEST_TEMPLATE_ID_SAKUYA_FISHING_ROD,
    None,
    4, # Target: 1
    14,
    (
        'Recently I was accompanying Koishi for a fishing trip to the Misty lake. '
        'I thought I packed everything up, but when I got home I noticed my fishing rod is nowhere.\n'
        '\n'
        'Could you please find me my missing fishing rod?'
    ),
    5,
    1,
    ITEM_ID_SAKUYA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 14, DAY_IN_SECONDS, 100, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_FISHING_ROD, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(6000, 1000, 100, 120),
        QuestRewardGeneratorCredibilityFix(45),
    ),
)


# - Chiruno +1 level
# - Misty lake +2 level
# Reward is around 2.5x of the value
QUEST_TEMPLATE_CHIRUNO_FROG = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_CHIRUNO_FROG] = QuestTemplate(
    QUEST_TEMPLATE_ID_CHIRUNO_FROG,
    (
        # Do not supply the same side of a war at a single day (2ve)
        QUEST_TEMPLATE_ID_DAI_FROG,
    ),
    3, # Target: 1
    5,
    (
        'The cowardly frogs are hiding from me. '
        'How could I maintain my superiority image like this, '
        'if I cannot show them how inferior they are in front of my chilling powers?\n'
        '\n'
        'If you do not bring me some, you will be the one I state order through!'
    ),
    3,
    3,
    ITEM_ID_CHIRUNO,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 2, HOUR_IN_SECONDS, 100, 140),
        QuestRequirementGeneratorItemExact(ITEM_ID_FROG, AMOUNT_TYPE_COUNT, 20, 1, 100, 150),
    ),
    (
        QuestRewardGeneratorBalance(3400, 50, 80, 120),
        QuestRewardGeneratorCredibility(10),
    ),
)


# - Dai +3 level
# - misty lake +2 level
# Reward is around 2.0x of the value
QUEST_TEMPLATE_DAI_FROG = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_DAI_FROG] = QuestTemplate(
    QUEST_TEMPLATE_ID_DAI_FROG,
    (
        # Do not supply the same side of a war at a single day (2ve)
        QUEST_TEMPLATE_ID_CHIRUNO_FROG,
    ),
    3, # Target: 1
    5,
    (
        'That stupid ice fairy is freezing the frogs. '
        'Even tho they are hiding frozen in fear, quite literally, '
        'Chiruno is still getting her hands on them due to requests. '
        'Please don\'t accept her quest.\n'
        '\n'
        'What are you waiting for? Help save the frogs!'
    ),
    5,
    0,
    ITEM_ID_DAI,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 7, HOUR_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_FROG, AMOUNT_TYPE_COUNT, 50, 10, 100, 200),
    ),
    (
        QuestRewardGeneratorBalance(6900, 100, 80, 120),
        QuestRewardGeneratorCredibility(20),
    ),
)


# - Tewi +3 level
# - Bamboo forest +0 level
# Reward is around 1.5x of the value
QUEST_TEMPLATE_TEWI_BISHOPHAT = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_TEWI_BISHOPHAT] = QuestTemplate(
    QUEST_TEMPLATE_ID_TEWI_BISHOPHAT,
    None,
    4, # Target: 1:ha
    10,
    (
        'In our establishment, at the tower of eternity, we wish for all of our customers good fortune. '
        'Unfortunately some of our customers are not blessed with such, but as there is no too deep hole to dig, '
        'there is neither anybody that cannot be granted good fortune.\n'
        '\n'
        'Please bring us a delivery of bishophats, not to be confused with the pesky horny goat weed.'
    ),
    3,
    9,
    ITEM_ID_TEWI,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 21, DAY_IN_SECONDS, 70, 150),
        QuestRequirementGeneratorItemExact(ITEM_ID_BISHOPHAT, AMOUNT_TYPE_WEIGHT, 1000, 100, 70, 120),
    ),
    (
        QuestRewardGeneratorBalance(4300, 100, 80, 130),
        QuestRewardGeneratorCredibility(20),
    ),
)


# - Junko +3 level
# - Misty lake +2 level
# Reward is around 2.5x of the value
QUEST_TEMPLATE_JUNKO_ANGELROOT = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_JUNKO_ANGELROOT] = QuestTemplate(
    QUEST_TEMPLATE_ID_JUNKO_ANGELROOT,
    None,
    4, # Target: 1
    7,
    (
        '\-No details included\-\n'
        '\n'
        'Please deliver angelroots.'
    ),
    5,
    1,
    ITEM_ID_JUNKO,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 2 + HOUR_IN_SECONDS * 12, HOUR_IN_SECONDS, 70, 130),
        QuestRequirementGeneratorItemExact(ITEM_ID_ANGELROOT, AMOUNT_TYPE_WEIGHT, 1000, 1000, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(3050, 50, 90, 110),
        QuestRewardGeneratorCredibility(10),
    ),
)

# - Koishi +1 level
# - Misty lake +2 level
# Reward is around 2.0x of the value
QUEST_TEMPLATE_KOISHI_ANGELROOT = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_KOISHI_ANGELROOT] = QuestTemplate(
    QUEST_TEMPLATE_ID_KOISHI_ANGELROOT,
    None,
    4, # Target: 1
    7,
    (
        'Hey!!\n'
        'I wanna surprise my gf with a child, so I am keep holding her hand, although nothing happened yet... '
        'They are still not preggy. I do not know what I am doing wrong, perhaps they have some gynecological issues.\n'
        '\n'
        'I heard angelroot is good for treating it, would you please bring me some?'
    ),
    3,
    1,
    ITEM_ID_KOISHI,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 5, HOUR_IN_SECONDS, 70, 130),
        QuestRequirementGeneratorItemExact(ITEM_ID_ANGELROOT, AMOUNT_TYPE_WEIGHT, 600, 100, 70, 120),
    ),
    (
        QuestRewardGeneratorBalance(1200, 50, 80, 110),
        QuestRewardGeneratorCredibility(10),
    ),
)

# - Kokoro +2 level
# - Rare drop +3 level
# Reward is around 2x of the value
QUEST_TEMPLATE_KOKORO_SCISSORS = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_KOKORO_SCISSORS] = QuestTemplate(
    QUEST_TEMPLATE_ID_KOKORO_SCISSORS,
    None,
    4, # Target: 1
    28,
    (
        'Someone is going around being real busy with their mushroom. '
        'I would like to fix this situation with some snipping action, if you know what I mean.\n'
        '\n'
        'Please deliver me a single scissors.'
    ),
    5,
    1,
    ITEM_ID_KOKORO,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 28, DAY_IN_SECONDS, 70, 130),
        QuestRequirementGeneratorItemExact(ITEM_ID_SCISSORS, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(16000, 50, 90, 110),
        QuestRewardGeneratorCredibilityFix(270),
    ),
)

# - Koishi +1 level
# - Bamboo forest +0 level
# Reward is around 2.5x of the value
QUEST_TEMPLATE_KOISHI_BISHOPHAT = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_KOISHI_BISHOPHAT] = QuestTemplate(
    QUEST_TEMPLATE_ID_KOISHI_BISHOPHAT,
    None,
    2, # Target: 1
    4,
    (
        'Hello Hello!!\n'
        'My sister is always so gloomy and tired, I wish I could fix it somehow and make them a little more active. '
        'I asked around how I could help her, and Tewi as a guardian angel came to my save.\n'
        '\n'
        'They recommended to try brewing for Satori some bishophat tea to increase their blood-flow, '
        'could you please bring some of it?'
    ),
    1,
    3,
    ITEM_ID_KOISHI,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 7, HOUR_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_BISHOPHAT, AMOUNT_TYPE_WEIGHT, 200, 10, 70, 130),
    ),
    (
        QuestRewardGeneratorBalance(1400, 50, 80, 120),
        QuestRewardGeneratorCredibility(10),
    ),
)


# - Koishi +1 level
# - Magic forest + 1 level
# - rare drop +3 level
# Reward is around 2.5x of the value
QUEST_TEMPLATE_KOISHI_RULER = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_KOISHI_RULER] = QuestTemplate(
    QUEST_TEMPLATE_ID_KOISHI_RULER,
    (
        QUEST_TEMPLATE_ID_KOISHI_KNIFE,
    ),
    4, # Target: 1
    28,
    (
        'Its me, your imaginary friend!!\n'
        'I was on my way to measure my mushroom, but then I forgot where I put it last time!!!\n'
        '\n'
        'Could you please find the ruler I have lost?'
    ),
    5,
    1,
    ITEM_ID_KOISHI,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 28, DAY_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_RULER, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(750, 100, 80, 120),
        QuestRewardGeneratorCredibility(250),
    ),
)


# - Yukari +3 level
# - rare drop +3 level
# Reward is around 3x of the value
QUEST_TEMPLATE_YUKARI_RULER = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_YUKARI_RULER] = QuestTemplate(
    QUEST_TEMPLATE_ID_YUKARI_RULER,
    None,
    4, # Target: 1
    28,
    (
        'Dear adventurer, good afternoon, how do you do?\n'
        '\n'
        'Today I have woke up from my nap and I was like: '
        '"How long did I sleep?"\n'
        'Then a voice in my mind: '
        '"I would keep a ruler under my pillow, how else would I know how how long have I slept-"\n'
        'Genius!!\n'
        '\n'
        'Please bring me a ruler in utter priority!\n'
        '\n'
        'Respectfully yours,\n'
        'Sage Yakumo Yukari'
    ),
    6,
    1,
    ITEM_ID_YUKARI,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 14, DAY_IN_SECONDS, 90, 130),
        QuestRequirementGeneratorItemExact(ITEM_ID_RULER, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(900, 100, 80, 120),
        QuestRewardGeneratorCredibilityFix(250),
    ),
)

# - Yuuka +2 level
# - rare drop +3 level
# Reward is around 2x of the value
QUEST_TEMPLATE_YUUKA_STRAW_HAT = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_YUUKA_STRAW_HAT] = QuestTemplate(
    QUEST_TEMPLATE_ID_YUUKA_STRAW_HAT,
    None,
    4, # Target: 1
    28,
    (
        'Could you please bring me a new straw hat, my current one is torn. '
        'Those with a flower on them look like a lot of fun.'
    ),
    5,
    1,
    ITEM_ID_YUUKA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 28, DAY_IN_SECONDS, 70, 130),
        QuestRequirementGeneratorItemExact(ITEM_ID_STRAW_HAT, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(1400, 100, 80, 120),
        QuestRewardGeneratorCredibilityFix(240),
    ),
)

# - Koishi +1 level
# - human village outskirts +0 level
# - large quantity with short time +1
# Reward is around 1.5x of the value
QUEST_TEMPLATE_KOISHI_GARLIC = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_KOISHI_GARLIC] = QuestTemplate(
    QUEST_TEMPLATE_ID_KOISHI_GARLIC,
    None,
    4, # Target: 1
    10,
    (
        'Hiya!!\n'
        '\n'
        'Flan told me Remi needs a lot of garlic!\n'
        '\n'
        'You may ask: "Eh? why do the SDM residents need garlic?"\n'
        '\n'
        'Did you know that Garlic helps fluidify your blood? '
        'It actually makes it easier for vampires to sukk your blood, so they actually gaslighted the whole world '
        'into thinking that it helps repel them, while it just seasons them and make them bleed easier!'
    ),
    2,
    1,
    ITEM_ID_KOISHI,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 3 + HOUR_IN_SECONDS * 12, HOUR_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_GARLIC, AMOUNT_TYPE_WEIGHT, 8000, 500, 80, 130),
    ),
    (
        QuestRewardGeneratorBalance(6500, 500, 80, 120),
        QuestRewardGeneratorCredibility(40),
    ),
)


# - non-village collection +1 level
# Reward is around 2.0x of the value
QUEST_TEMPLATE_MYSTIA_BAMBOO_SHOOT = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_BAMBOO_SHOOT] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_BAMBOO_SHOOT,
    None,
    1,
    1,
    (
        'I am running out of some local ingredients.\n'
        '\n'
        'Could you please bring some bamboo shoots?'
    ),
    1,
    3,
    ITEM_ID_MYSTIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 3, HOUR_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_BAMBOO_SHOOT, AMOUNT_TYPE_COUNT, 5, 1, 80, 120),
    ),
    (
        QuestRewardGeneratorBalance(900, 50, 90, 110),
        QuestRewardGeneratorCredibility(10),
    ),
)


# - Alice +2 level
# - Misty lake +2 level
# Reward is around 2.0x of the value
QUEST_TEMPLATE_ALICE_ANGELROOT = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_ALICE_ANGELROOT] = QuestTemplate(
    QUEST_TEMPLATE_ID_ALICE_ANGELROOT,
    None,
    4, # Target: 1
    10,
    (
        'Word of Angelroot has gotten around enough as it seems to be in demand lately, '
        'and really popular amongst couples.\n'
        'I keep asking Marisa about it, but she doesn\'t explain and just says not to worry, '
        'so I have decided to procure some on my own.\n'
        '\n'
        'Since I do not frequent the forests like Marisa does, '
        'I put up a quest so that the angelroots can be delivered to me.'
    ),
    4,
    1,
    ITEM_ID_ALICE,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 2, HOUR_IN_SECONDS, 100, 130),
        QuestRequirementGeneratorItemExact(ITEM_ID_ANGELROOT, AMOUNT_TYPE_COUNT, 8, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(2550, 50, 90, 110),
        QuestRewardGeneratorCredibility(10),
    ),
)

# - Nina +3 level
# - Ruins +1 level
# Reward is around 2.0x of the value
QUEST_NINA_STRAWBERRY = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_NINA_STRAWBERRY] = QuestTemplate(
    QUEST_TEMPLATE_ID_NINA_STRAWBERRY,
    None,
    8, # Target: 1
    28,
    (
        'What! Strawberry crisis??\n'
        'HEEEE\~\~... HEEEE\~\~...\n'
        '\n'
        'There is a strawberry crisis out there, when I see a strawberry for sale, I must buy it. '
        'Without them my days would be so boring... I want to request them.'
        
    ),
    4,
    1,
    ITEM_ID_NINA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 6, DAY_IN_SECONDS, 70, 130),
        QuestRequirementGeneratorItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 8000, 500, 75, 175),
    ),
    (
        QuestRewardGeneratorBalance(14000, 1000, 80, 120),
        QuestRewardGeneratorCredibility(30),
    ),
)

# - Koishi +1 level
# - Moriya shrine +2 level
# - rare drop +3 level
# Reward is around 2x of the value
QUEST_TEMPLATE_KOISHI_KNIFE = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_KOISHI_KNIFE] = QuestTemplate(
    QUEST_TEMPLATE_ID_KOISHI_KNIFE,
    (
        QUEST_TEMPLATE_ID_KOISHI_RULER,
    ),
    28, # Target: 1
    28,
    (
        'Help me! I was lost my knife! Probably I\'m dropped knife during Danmaku match with Reimu recently...\n'
        'Will you find my lost knife?'
    ),
    6,
    1,
    ITEM_ID_KOISHI,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 28, DAY_IN_SECONDS, 70, 130),
        QuestRequirementGeneratorItemGroup(ITEM_GROUP_ID_KNIFE, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(13000, 1000, 80, 120),
        QuestRewardGeneratorCredibilityFix(250),
    ),
)


# - Mystia +1 level
# - Uncommon drop + 1 level
# Reward is around 1.0x of the value
QUEST_TEMPLATE_MYSTIA_FIREWOOD = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD,
    (
        QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD,
    ),
    1,
    2,
    (
        'To run an izakaya, one is always in need of dry firewood in great quantities. '
        'Since I have to attend it, I do not have the opportunity to go out and collect any.\n'
        '\n'
        'I hope you would not mind helping me out, I will pay you fairly.'
    ),
    2,
    0,
    ITEM_ID_MYSTIA,
    (
        QuestRequirementGeneratorItemGroup(ITEM_GROUP_ID_FIREWOOD, AMOUNT_TYPE_VALUE, 1000, 1000, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(1000, 1000, 100, 100),
        QuestRewardGeneratorCredibilityFix(20),
    ),
)


# - Eirin +2 level
# - Misty lake +2 level
# Reward is around 2.0x of the value
QUEST_TEMPLATE_EIRIN_ANGELROOT_AND_BISHOPHAT = \
QUEST_TEMPLATES[QUEST_TEMPLATE_ID_EIRIN_ANGELROOT_AND_BISHOPHAT] = QuestTemplate(
    QUEST_TEMPLATE_ID_EIRIN_ANGELROOT_AND_BISHOPHAT,
    None,
    4, # Target: 1
    14,
    (
        'The residents of Gensoukyou seem to be interested in angelroots and bishophats lately... '
        'As nice it is of them to look towards these items for medicinal properties, '
        'they don\'t realise their true potential if correctly combined.\n'
        '\n'
        'I would like to request some bishophats and angelroots to further my research on this new kind of medicine.'
    ),
    4,
    1,
    ITEM_ID_EIRIN,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 3 + HOUR_IN_SECONDS * 12, HOUR_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_ANGELROOT, AMOUNT_TYPE_WEIGHT, 1000, 50, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_BISHOPHAT, AMOUNT_TYPE_WEIGHT, 500, 10, 80, 120),
    ),
    (
        QuestRewardGeneratorBalance(5300, 100, 80, 120),
        QuestRewardGeneratorCredibility(15),
    ),
)


# - Reimu +1 level
# - Balance +1 level
# Reward around 2x the value in Sake
QUEST_TEMPLATE_REIMU_BANQUET = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_REIMU_BANQUET] = QuestTemplate(
    QUEST_TEMPLATE_ID_REIMU_BANQUET,
    None,
    4, # Target: 1
    10,
    (
        'As the shrine maiden of the Hakurei Shrine; '
        'I would like to hold a banquet inviting the most generous shrinegoers, '
        'where a delicious hot pot shall be served.\n'
        'Alas, the donations this month haven\'t been very kind to neither me nor the shrine itself for me to '
        'afford procuring the ingredients from the market, '
        'therefore I have put up this quest requesting for the ingredients required to prepare the hot pot.\n'
        '\n'
        'No need to question the reward, what this request lacks in monetary gain is made up for through the honour '
        'of having worked with the Hakurei Shrine Maiden herself.'
    ),
    2,
    1,
    ITEM_ID_REIMU,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 6, HOUR_IN_SECONDS * 12, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_DEVILCART_OYSTER, AMOUNT_TYPE_WEIGHT, 1800, 100, 65, 135),
        QuestRequirementGeneratorItemExact(ITEM_ID_CARROT, AMOUNT_TYPE_WEIGHT, 6000, 500, 65, 135),
        QuestRequirementGeneratorItemExact(ITEM_ID_BAMBOO_SHOOT, AMOUNT_TYPE_COUNT, 8, 1, 65, 135),
        QuestRequirementGeneratorChoice(
            (
                QuestRequirementGeneratorChoiceOption(
                    QuestRequirementGeneratorItemExact(ITEM_ID_GARLIC, AMOUNT_TYPE_WEIGHT, 600, 50, 65, 135),
                    1,
                ),
                QuestRequirementGeneratorChoiceOption(
                    QuestRequirementGeneratorItemExact(ITEM_ID_SCARLET_ONION, AMOUNT_TYPE_WEIGHT, 1600, 100, 65, 135),
                    1,
                ),
            ),
        ),
    ),
    (
        QuestRewardGeneratorItemExactFix(ITEM_ID_SAKE, 3),
        QuestRewardGeneratorCredibility(30),
    ),
)

# - Suika +2 level
# - Requires reward +1 level
# Reward around 2x the value
QUEST_TEMPLATE_SUIKA_SAKE = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_SUIKA_SAKE] = QuestTemplate(
    QUEST_TEMPLATE_ID_SUIKA_SAKE,
    None,
    4, # Target: 1
    21,
    (
        'Hey! I heard Alice will be joining the next feast. '
        'She\'s usually cold and unwilling to talk to non-humans. Does she wish to be a human? '
        'Or is she too cowardly to talk to people stronger than her?\n'
        'I\'d like to make her a little relaxed, so she can have fun. It\'s for her sake, I promise.\n'
        '\n'
        'For this, all I need is some Hakurei Sake, the three digits on the back...\n'
        'Sorry, Reimu keeps replaying this dumb video, it\'s so annoying, smh (shaking my horns).'
    ),
    3,
    1,
    ITEM_ID_SUIKA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 5 + HOUR_IN_SECONDS * 12, HOUR_IN_SECONDS * 12, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_SAKE, AMOUNT_TYPE_COUNT, 4, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(13600, 400, 80, 120),
        QuestRewardGeneratorCredibility(10),
    ),
)
