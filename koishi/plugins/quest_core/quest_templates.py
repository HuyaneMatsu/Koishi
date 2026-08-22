__all__ = ()

from ..item_core import (
    ITEM_GROUP_ID_BLOOD_SAUSAGE_MEAT, ITEM_GROUP_ID_BOILED_SAUSAGE, ITEM_GROUP_ID_FIREWOOD,
    ITEM_GROUP_ID_HUMAN_CORPSE_FULL, ITEM_GROUP_ID_KNIFE, ITEM_GROUP_ID_LIVER_SAUSAGE_MEAT,
    ITEM_GROUP_ID_MEAT_SAUSAGE_MEAT, ITEM_GROUP_ID_SWEETS, ITEM_ID_ALICE, ITEM_ID_ANGELROOT, ITEM_ID_AYA,
    ITEM_ID_BAMBOO_SHOOT, ITEM_ID_BISHOPHAT, ITEM_ID_BLOOD_SAUSAGE, ITEM_ID_BLUEBERRY, ITEM_ID_BLUEFRANKISH,
    ITEM_ID_CARROT, ITEM_ID_CHIRUNO, ITEM_ID_DAI, ITEM_ID_DANGO, ITEM_ID_DEVILCART_OYSTER, ITEM_ID_EIRIN,
    ITEM_ID_FISHING_ROD, ITEM_ID_FLANDRE, ITEM_ID_FLYKILLER_AMANITA, ITEM_ID_FROG, ITEM_ID_GARLIC, ITEM_ID_HUMAN_BLOOD,
    ITEM_ID_HUMAN_BODY_PART_SKULL, ITEM_ID_HUMAN_BODY_SHARD_CHEWED, ITEM_ID_HUMAN_BONE, ITEM_ID_HUMAN_BRAIN,
    ITEM_ID_HUMAN_EAR, ITEM_ID_HUMAN_EYE, ITEM_ID_HUMAN_FAT, ITEM_ID_HUMAN_INTESTINES, ITEM_ID_HUMAN_LIVER,
    ITEM_ID_HUMAN_LUNG, ITEM_ID_HUMAN_MUSCLE, ITEM_ID_HUMAN_SKIN, ITEM_ID_JUNKO, ITEM_ID_KOISHI, ITEM_ID_KOKORO,
    ITEM_ID_LIVER_SAUSAGE, ITEM_ID_MARISA, ITEM_ID_MEAT_SAUSAGE, ITEM_ID_MYSTIA, ITEM_ID_NINA, ITEM_ID_NITORI,
    ITEM_ID_ORIN, ITEM_ID_PARSEE, ITEM_ID_PATCHOULI, ITEM_ID_PEACH, ITEM_ID_PEN, ITEM_ID_PLUSHIE_BEAR, ITEM_ID_PUDDING,
    ITEM_ID_RAMEN, ITEM_ID_REIMU, ITEM_ID_REMILIA, ITEM_ID_RIBBON_BOW, ITEM_ID_RICE, ITEM_ID_RULER, ITEM_ID_RUMIA,
    ITEM_ID_SAKE, ITEM_ID_SAKUYA, ITEM_ID_SATORI, ITEM_ID_SCARLET_ONION, ITEM_ID_SCISSORS, ITEM_ID_STRAWBERRY,
    ITEM_ID_STRAW_HAT, ITEM_ID_SUIKA, ITEM_ID_TEA_LEAVES, ITEM_ID_TEWI, ITEM_ID_UNKNOWN_OVEN_S_TORN_OUT_WING,
    ITEM_ID_YOUMU, ITEM_ID_YUKARI, ITEM_ID_YUUKA,
)

from .amount_types import AMOUNT_TYPE_COUNT, AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT
from .constants import DAY_IN_SECONDS, HOUR_IN_SECONDS, QUEST_TEMPLATES
from .quest_requirement_generators import (
    QuestRequirementGeneratorChoice, QuestRequirementGeneratorChoiceOption, QuestRequirementGeneratorDuration,
    QuestRequirementGeneratorItemExact, QuestRequirementGeneratorItemGroup
)
from .quest_reward_generators import (
    QuestRewardGeneratorBalance, QuestRewardGeneratorCredibility, QuestRewardGeneratorCredibilityFix,
    QuestRewardGeneratorItemExact, QuestRewardGeneratorItemExactFix
)
from .quest_template import QuestTemplate
from .quest_template_ids import (
    QUEST_TEMPLATE_ID_ALICE_ANGELROOT, QUEST_TEMPLATE_ID_ALICE_FLYKILLER_AMANITA, QUEST_TEMPLATE_ID_ALICE_SKIN,
    QUEST_TEMPLATE_ID_AYA_HUMAN_CORPSE, QUEST_TEMPLATE_ID_CHIRUNO_FROG, QUEST_TEMPLATE_ID_DAI_FROG,
    QUEST_TEMPLATE_ID_EIRIN_ANGELROOT_AND_BISHOPHAT, QUEST_TEMPLATE_ID_FLANDRE_RIBBON_BOW,
    QUEST_TEMPLATE_ID_FLANDRE_PLUSHIE_BEAR,
    QUEST_TEMPLATE_ID_JUNKO_ANGELROOT, QUEST_TEMPLATE_ID_KOISHI_ANGELROOT, QUEST_TEMPLATE_ID_KOISHI_BISHOPHAT,
    QUEST_TEMPLATE_ID_KOISHI_BRAIN, QUEST_TEMPLATE_ID_KOISHI_GARLIC, QUEST_TEMPLATE_ID_KOISHI_KNIFE,
    QUEST_TEMPLATE_ID_KOISHI_PEN, QUEST_TEMPLATE_ID_KOISHI_PUDDING, QUEST_TEMPLATE_ID_KOISHI_RULER,
    QUEST_TEMPLATE_ID_KOKORO_SCISSORS, QUEST_TEMPLATE_ID_MARISA_FLYKILLER_AMANITA, QUEST_TEMPLATE_ID_MARISA_RAMEN,
    QUEST_TEMPLATE_ID_MYSTIA_BAMBOO_SHOOT, QUEST_TEMPLATE_ID_MYSTIA_CARROT, QUEST_TEMPLATE_ID_MYSTIA_DEVILCART_OYSTER,
    QUEST_TEMPLATE_ID_MYSTIA_FAT, QUEST_TEMPLATE_ID_MYSTIA_FIREWOOD, QUEST_TEMPLATE_ID_MYSTIA_GARLIC,
    QUEST_TEMPLATE_ID_MYSTIA_MEAT, QUEST_TEMPLATE_ID_MYSTIA_HUMAN_BONE, QUEST_TEMPLATE_ID_MYSTIA_PEACH,
    QUEST_TEMPLATE_ID_MYSTIA_RICE,
    QUEST_TEMPLATE_ID_MYSTIA_SCARLET_ONION, QUEST_TEMPLATE_ID_NINA_SKULL, QUEST_TEMPLATE_ID_NINA_STRAWBERRY,
    QUEST_TEMPLATE_ID_NITORI_HUMAN_BONE, QUEST_TEMPLATE_ID_ORIN_FISHING_ROD, QUEST_TEMPLATE_ID_PARSEE_RIBBON_BOW,
    QUEST_TEMPLATE_ID_PATCHOULI_EYE, QUEST_TEMPLATE_ID_REIMU_BANQUET, QUEST_TEMPLATE_ID_REIMU_EAR,
    QUEST_TEMPLATE_ID_REMILIA_FLANDRE_WING, QUEST_TEMPLATE_ID_REMILIA_RIBBON_BOW, QUEST_TEMPLATE_ID_RUMIA_BLOOD_SAUSAGE,
    QUEST_TEMPLATE_ID_RUMIA_LIVER_SAUSAGE, QUEST_TEMPLATE_ID_RUMIA_MEAT_SAUSAGE, QUEST_TEMPLATE_ID_RUMIA_SWEETS,
    QUEST_TEMPLATE_ID_SAKUYA_BLUEBERRY, QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH, QUEST_TEMPLATE_ID_SAKUYA_BOILED_SAUSAGE,
    QUEST_TEMPLATE_ID_SAKUYA_DEVILCART_OYSTER, QUEST_TEMPLATE_ID_SAKUYA_FISHING_ROD,
    QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, QUEST_TEMPLATE_ID_SATORI_PUDDING, QUEST_TEMPLATE_ID_SUIKA_SAKE,
    QUEST_TEMPLATE_ID_TEWI_BISHOPHAT, QUEST_TEMPLATE_ID_TEWI_RICE, QUEST_TEMPLATE_ID_YOUMU_DANGO_TEA,
    QUEST_TEMPLATE_ID_YOUMU_RAMEN, QUEST_TEMPLATE_ID_YUKARI_RULER, QUEST_TEMPLATE_ID_YUUKA_STRAW_HAT
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


# - Mystia +0 level
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


# - Mystia +0 level
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


# - Mystia +0 level
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


# - Mystia +0 level
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


# - Mystia +0 level
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


# - Mystia +0 level
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
# - Misty lake +2 level
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
# - Misty lake +2 level
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
# - Rare drop +3 level
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
# - Rare drop +3 level
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
# - Rare drop +3 level
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
# - Rare drop +3 level
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


# - Mystia +0 level
# - Magic forest +1 level
# - Balance +1 level
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
        QuestRequirementGeneratorItemGroup(ITEM_GROUP_ID_FIREWOOD, AMOUNT_TYPE_VALUE, 1000, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(1000, 1, 100, 100),
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


# - Flandre +4
# - Ruins +1 level
# - Rare drop +3 level
QUEST_TEMPLATE_FLANDRE_RIBBON_BOW = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_FLANDRE_RIBBON_BOW] = QuestTemplate(
    QUEST_TEMPLATE_ID_FLANDRE_RIBBON_BOW,
    (
        QUEST_TEMPLATE_ID_REMILIA_RIBBON_BOW,
        QUEST_TEMPLATE_ID_REMILIA_FLANDRE_WING,
        QUEST_TEMPLATE_ID_FLANDRE_PLUSHIE_BEAR,
    ),
    4, # Target: 1
    34,
    (
        'I played outside lots today!!! But when I came back home, my onee-sama asked me where my ribbon went? '
        'I said "I don\'t know!!!"\n'
        'The ribbon is a gift from my onee-sama, I don\'t want to make her sad by losing it... I should find it...\n'
        'Oh I know! How about YOU find it? I will offer you a reward most fitting of the '
        'little sister of the Scarlet Devil herself!'
    ),
    8,
    1,
    ITEM_ID_FLANDRE,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 16, DAY_IN_SECONDS, 90, 110),
        QuestRequirementGeneratorItemExact(ITEM_ID_RIBBON_BOW, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorItemExactFix(ITEM_ID_PUDDING, 1),
        QuestRewardGeneratorCredibilityFix(240),
    ),
)


# - Remilia +3
# - Ruins +1 level
# - Rare drop +3 level
QUEST_TEMPLATE_REMILIA_RIBBON_BOW = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_REMILIA_RIBBON_BOW] = QuestTemplate(
    QUEST_TEMPLATE_ID_REMILIA_RIBBON_BOW,
    (
        QUEST_TEMPLATE_ID_FLANDRE_RIBBON_BOW,
    ),
    4, # Target: 1
    44,
    (
        'I like to go on long walks when the day is pleasant, but when I returned to my mansion and looked at myself '
        'in the mirror today; my beautiful ribbon was nowhere to be seen!\n'
        'Since I prefer to wear my ribbon a little loose (for comfort, of course), '
        'it may have come off on the way back...\n'
        'I am already feeling a little weak from my walk outside, therefore I request that whoever finds my beautiful '
        'ribbon shall return it at once! Naturally, I would reward that person with a reward most fitting of the '
        'Scarlet Devil herself~'
    ),
    7,
    1,
    ITEM_ID_REMILIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 32, DAY_IN_SECONDS, 90, 110),
        QuestRequirementGeneratorItemExact(ITEM_ID_RIBBON_BOW, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(1000, 100, 70, 130),
        QuestRewardGeneratorItemExactFix(ITEM_ID_PUDDING, 4),
        QuestRewardGeneratorCredibilityFix(160),
    ),
)


# - Koishi +1
# - Requires reward of rare drop quest +4 level
# - Gives unique items +2 level
QUEST_TEMPLATE_KOISHI_PUDDING = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_KOISHI_PUDDING] = QuestTemplate(
    QUEST_TEMPLATE_ID_KOISHI_PUDDING,
    (
        QUEST_TEMPLATE_ID_SATORI_PUDDING,
        QUEST_TEMPLATE_ID_REMILIA_FLANDRE_WING,
    ),
    4, # Target: 1
    56,
    (
        'Hello!\n'
        'I\'m just wanted to open tea party at Palace of the Earth Spirits with my sister. '
        'But, my sister said "If doing the tea party, then need some sweets." '
        'I think Scarlet Devil Mansion\'s sweets is good for tea party, you can give it for me?'
    ),
    7,
    1,
    ITEM_ID_KOISHI,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 38, DAY_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_PUDDING, AMOUNT_TYPE_COUNT, 2, 2, 100, 100),
    ),
    (
        QuestRewardGeneratorItemExactFix(ITEM_ID_UNKNOWN_OVEN_S_TORN_OUT_WING, 1),
        QuestRewardGeneratorCredibility(10),
    ),
)

# - Satori +2
# - Requires reward of rare drop quest +4 level
# - Balance +1 level
QUEST_TEMPLATE_SATORI_PUDDING = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_SATORI_PUDDING] = QuestTemplate(
    QUEST_TEMPLATE_ID_SATORI_PUDDING,
    (
        QUEST_TEMPLATE_ID_KOISHI_PUDDING,
    ),
    4, # Target: 1
    28,
    (
        'Dear Reader, I am Komeiji Satori, the master of the Palace of the Earth Spirits.\n'
        '\n'
        'Recently my little sister, Koishi was pleading for some sweets. '
        'Since she joined the Scarlet Devil mansion\'s tea party recently, '
        'she says, that her friends, Flandre likes pudding and cake.\n'
        '\n'
        'Please bring some Scarlet Devil Mansion\'s sweets for me. It would make my little sister really happy.'
    ),
    7,
    1,
    ITEM_ID_SATORI,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 16, DAY_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_PUDDING, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
        QuestRequirementGeneratorItemGroup(ITEM_GROUP_ID_SWEETS, AMOUNT_TYPE_WEIGHT, 200, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorItemExact(ITEM_ID_TEA_LEAVES, 16, 1, 80, 120),
        QuestRewardGeneratorCredibility(20),
    ),
)


# - Remilia +3
# - Requires reward of unique drop quest +5 level
QUEST_TEMPLATE_REMILIA_FLANDRE_WING = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_REMILIA_FLANDRE_WING] = QuestTemplate(
    QUEST_TEMPLATE_ID_REMILIA_FLANDRE_WING,
    (
        QUEST_TEMPLATE_ID_REMILIA_RIBBON_BOW,
        QUEST_TEMPLATE_ID_KOISHI_PUDDING,
        QUEST_TEMPLATE_ID_FLANDRE_PLUSHIE_BEAR,
    ),
    4, # Target: 1
    48,
    (
        'Today when my little sister Flandre came to greet me, I saw that she was missing a wing! '
        'She doesn\'t even seem to notice that it\'s gone...\n'
        'But this is a very troubling matter! I demand that her wing is returned at once before she realises '
        '~~wreaking havoc on Gensoukyou~~ and goes looking for it herself!!'
    ),
    8,
    1,
    ITEM_ID_REMILIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 8, 1, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_UNKNOWN_OVEN_S_TORN_OUT_WING, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(138000, 100, 90, 110),
        QuestRewardGeneratorCredibilityFix(200),
    ),
)


# - Rumia +2
# - Requires meat +3
QUEST_TEMPLATE_RUMIA_LIVER_SAUSAGE = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_RUMIA_LIVER_SAUSAGE] = QuestTemplate(
    QUEST_TEMPLATE_ID_RUMIA_LIVER_SAUSAGE,
    (
        QUEST_TEMPLATE_ID_RUMIA_BLOOD_SAUSAGE,
        QUEST_TEMPLATE_ID_RUMIA_MEAT_SAUSAGE,
    ),
    2, # Target: 1
    14,
    (
        'I am feeling like making some homemade flavours; are you interested perhaps?\n'
        '\n'
        'I will want to make some liver flavoured boiled sausage. '
        'If you bring me the ingredients, I will also tell you the wonderful boiled sausage\'s recipe.'
    ),
    5,
    1,
    ITEM_ID_RUMIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 7, DAY_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_LUNG, AMOUNT_TYPE_WEIGHT, 2000, 2000, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_LIVER, AMOUNT_TYPE_WEIGHT, 1000, 1000, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_FAT, AMOUNT_TYPE_WEIGHT, 1000, 1000, 100, 100),
        QuestRequirementGeneratorItemGroup(ITEM_GROUP_ID_LIVER_SAUSAGE_MEAT, AMOUNT_TYPE_WEIGHT, 1000, 1000, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_MUSCLE, AMOUNT_TYPE_WEIGHT, 1000, 1000, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_INTESTINES, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_RICE, AMOUNT_TYPE_WEIGHT, 2000, 2000, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_SCARLET_ONION, AMOUNT_TYPE_WEIGHT, 2000, 2000, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(5000, 100, 90, 110),
        QuestRewardGeneratorItemExactFix(ITEM_ID_LIVER_SAUSAGE, 2),
        QuestRewardGeneratorCredibility(20),
    ),
)


# - Rumia +2
# - Requires meat +3
QUEST_TEMPLATE_RUMIA_BLOOD_SAUSAGE = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_RUMIA_BLOOD_SAUSAGE] = QuestTemplate(
    QUEST_TEMPLATE_ID_RUMIA_BLOOD_SAUSAGE,
    (
        QUEST_TEMPLATE_ID_RUMIA_LIVER_SAUSAGE,
        QUEST_TEMPLATE_ID_RUMIA_MEAT_SAUSAGE,
    ),
    2, # Target: 1
    14,
    (
        'I am feeling like making some homemade flavours; are you interested perhaps?\n'
        '\n'
        'I will want to make some blood flavoured boiled sausage. '
        'If you bring me the ingredients, I will also tell you the wonderful boiled sausage\'s recipe.'
    ),
    5,
    1,
    ITEM_ID_RUMIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 7, DAY_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_LUNG, AMOUNT_TYPE_WEIGHT, 2000, 2000, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_BLOOD, AMOUNT_TYPE_WEIGHT, 2000, 2000, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_FAT, AMOUNT_TYPE_WEIGHT, 1000, 1000, 100, 100),
        QuestRequirementGeneratorItemGroup(ITEM_GROUP_ID_BLOOD_SAUSAGE_MEAT, AMOUNT_TYPE_WEIGHT, 1400, 1000, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_MUSCLE, AMOUNT_TYPE_WEIGHT, 2000, 1000, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_INTESTINES, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_RICE, AMOUNT_TYPE_WEIGHT, 2000, 2000, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_SCARLET_ONION, AMOUNT_TYPE_WEIGHT, 1000, 2000, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_GARLIC, AMOUNT_TYPE_WEIGHT, 400, 400, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(5000, 100, 90, 110),
        QuestRewardGeneratorItemExactFix(ITEM_ID_BLOOD_SAUSAGE, 2),
        QuestRewardGeneratorCredibility(20),
    ),
)


# - Rumia +2
# - Requires meat +3
QUEST_TEMPLATE_RUMIA_MEAT_SAUSAGE = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_RUMIA_MEAT_SAUSAGE] = QuestTemplate(
    QUEST_TEMPLATE_ID_RUMIA_MEAT_SAUSAGE,
    (
        QUEST_TEMPLATE_ID_RUMIA_LIVER_SAUSAGE,
        QUEST_TEMPLATE_ID_RUMIA_BLOOD_SAUSAGE,
    ),
    2, # Target: 1
    14,
    (
        'I am feeling like making some homemade flavours; are you interested perhaps?\n'
        '\n'
        'I will want to make some meat flavoured boiled sausage. '
        'If you bring me the ingredients, I will also tell you the wonderful boiled sausage\'s recipe.'
    ),
    5,
    1,
    ITEM_ID_RUMIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 7, DAY_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_FAT, AMOUNT_TYPE_WEIGHT, 1000, 1000, 100, 100),
        QuestRequirementGeneratorItemGroup(ITEM_GROUP_ID_MEAT_SAUSAGE_MEAT, AMOUNT_TYPE_WEIGHT, 2000, 1000, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_MUSCLE, AMOUNT_TYPE_WEIGHT, 4000, 1000, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_INTESTINES, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_RICE, AMOUNT_TYPE_WEIGHT, 2000, 2000, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_SCARLET_ONION, AMOUNT_TYPE_WEIGHT, 1000, 2000, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(5000, 100, 90, 110),
        QuestRewardGeneratorItemExactFix(ITEM_ID_MEAT_SAUSAGE, 2),
        QuestRewardGeneratorCredibility(20),
    ),
)


# - Orin +1 level
# - Misty lake +2 level
# - equipment +1 level
# Reward is around 3x of the value
QUEST_TEMPLATE_ORIN_FISHING_ROD = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_ORIN_FISHING_ROD] = QuestTemplate(
    QUEST_TEMPLATE_ID_ORIN_FISHING_ROD,
    None,
    4, # Target: 1
    14,
    (
        'hey, Its me, your favourite catgirl!!!!\n'
        '\n'
        'Please bring me a fishing rod; '
        'I think the goblin shamans burt mine while I was in the mines looking for some nice corpses!'
    ),
    4,
    1,
    ITEM_ID_ORIN,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 28, DAY_IN_SECONDS, 100, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_FISHING_ROD, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(9000, 1000, 100, 120),
        QuestRewardGeneratorCredibilityFix(25),
    ),
)


# - Sakuya +2 level
# - Requires meat +3 level
# Reward around 2.5x the value in Sake
QUEST_TEMPLATE_SAKUYA_BOILED_SAUSAGE = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_SAKUYA_BOILED_SAUSAGE] = QuestTemplate(
    QUEST_TEMPLATE_ID_SAKUYA_BOILED_SAUSAGE,
    None,
    2, # Target: 1
    7,
    (
        'My mistress is wishing to consume some all famous boiled sausage of the Rumia butchery.\n'
        '\n'
        'Please bring us a feastful.'
    ),
    5,
    1,
    ITEM_ID_SAKUYA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 12, HOUR_IN_SECONDS, 70, 120),
        QuestRequirementGeneratorItemGroup(ITEM_GROUP_ID_BOILED_SAUSAGE, AMOUNT_TYPE_WEIGHT, 2000, 2000, 65, 135),
    ),
    (
        QuestRewardGeneratorBalance(2500, 100, 80, 120),
        QuestRewardGeneratorCredibility(20),
    ),
)


# - Alice +2 level
# - Requires meat +3 level
# Reward around 2x the value in Sake
QUEST_TEMPLATE_ALICE_SKIN = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_ALICE_SKIN] = QuestTemplate(
    QUEST_TEMPLATE_ID_ALICE_SKIN,
    None,
    2, # Target: 1
    10,
    (
        'I am running low on some supplies for my dolls. I would like to restock on some skin for them.\n'
        '\n'
        'Could you please bring me some?'
    ),
    5,
    1,
    ITEM_ID_ALICE,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 6, HOUR_IN_SECONDS, 70, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_SKIN, AMOUNT_TYPE_COUNT, 16, 2, 50, 150),
    ),
    (
        QuestRewardGeneratorBalance(800, 100, 80, 120),
        QuestRewardGeneratorCredibility(10),
    ),
)


# - Mystia +0 level
# - Requires meat +3 level
# Reward around 2x the value in Sake
QUEST_TEMPLATE_MYSTIA_MEAT = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_MEAT] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_MEAT,
    None,
    1,
    3,
    (
        'I am running severely low on meat.\n'
        '\n'
        'Any regular meat is fine, could you please bring me some?'
    ),
    5,
    3,
    ITEM_ID_MYSTIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 4, HOUR_IN_SECONDS, 70, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_MUSCLE, AMOUNT_TYPE_WEIGHT, 8000, 1000, 80, 120),
    ),
    (
        QuestRewardGeneratorBalance(8000, 1000, 80, 120),
        QuestRewardGeneratorCredibility(10),
    ),
)


# - Mystia +0 level
# - Requires meat +3 level
QUEST_TEMPLATE_MYSTIA_FAT = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_FAT] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_FAT,
    None,
    1,
    4,
    (
        'I am running severely low on fat.\n'
        '\n'
        'One can\'t cook without fat, please bring me some as soon as possible.'
    ),
    3,
    1,
    ITEM_ID_MYSTIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 2 + HOUR_IN_SECONDS * 6, HOUR_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_FAT, AMOUNT_TYPE_WEIGHT, 2000, 100, 80, 120),
    ),
    (
        QuestRewardGeneratorBalance(1150, 50, 80, 120),
        QuestRewardGeneratorCredibility(20),
    ),
)


# - Patchouli +2 level
# - Requires meat +3 level
# Reward around 3x the value
QUEST_TEMPLATE_PATCHOULI_EYE = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_PATCHOULI_EYE] = QuestTemplate(
    QUEST_TEMPLATE_ID_PATCHOULI_EYE,
    None,
    4, # Target: 1
    28,
    (
        'We would like to perform some eye research in the Scarlet Devil Mansion.\n'
        '\n'
        'Please bring me a few eyes.'
    ),
    5,
    1,
    ITEM_ID_PATCHOULI,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 32, DAY_IN_SECONDS, 90, 110),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_EYE, AMOUNT_TYPE_COUNT, 6, 6, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(100, 1, 100, 100),
        QuestRewardGeneratorCredibility(30),
    ),
)


# - Patchouli +1 level
# - Requires meat +3 level
# Reward around 1x the value
QUEST_TEMPLATE_ID_BRAIN = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_KOISHI_BRAIN] = QuestTemplate(
    QUEST_TEMPLATE_ID_KOISHI_BRAIN,
    None,
    4, # Target: 1
    56,
    (
        'Flan ask why I brain dead after woke up.\n'
        '\n'
        'She says it\'s because I need a a RAM upgrade\n'
        'But how can Ran upgrade me?'
    ),
    4,
    1,
    ITEM_ID_KOISHI,
    (
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_BRAIN, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(900, 1, 100, 100),
        QuestRewardGeneratorCredibility(10),
    ),
)


# - Nina +3 level
# - Requires meat +3 level
# - Requires large amount +1 level
# Reward is around 1.5x of the value
QUEST_NINA_SKULL = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_NINA_SKULL] = QuestTemplate(
    QUEST_TEMPLATE_ID_NINA_SKULL,
    None,
    2, # Target: 1
    72,
    (
        'HAAAA!!\n'
        'I heard Reimu Is working on touching up the Hakurei shrine!!\n'
        '\n'
        'I had a great idea today, a new altar could really spruce up the place, what about that?\n'
        'Since she is dealing with a lot of evil beings I thought of a skull rack would be a great choice!!! '
        'It would definitely help deter all crimes!!!!'
    ),
    7,
    1,
    ITEM_ID_NINA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 120, DAY_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_BODY_PART_SKULL, AMOUNT_TYPE_COUNT, 60, 1, 90, 110),
    ),
    (
        QuestRewardGeneratorBalance(15000, 100, 90, 110),
        QuestRewardGeneratorCredibility(90),
    ),
)


# - Reimu +1 level
# - Requires meat +3 level
# Reward is around 3x of the value
QUEST_REIMU_EAR = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_REIMU_EAR] = QuestTemplate(
    QUEST_TEMPLATE_ID_REIMU_EAR,
    None,
    4, # Target: 1
    16,
    (
        'As a good pet owner, I wish to praise, pamper and reward my cutie. '
        'I heard from Yukari that some people use dried ears as rewards, therefore I would like to request some to try.'
    ),
    4,
    1,
    ITEM_ID_REIMU,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 7, HOUR_IN_SECONDS * 12, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_EAR, AMOUNT_TYPE_COUNT, 10, 1, 80, 120),
    ),
    (
        QuestRewardGeneratorItemExactFix(ITEM_ID_DANGO, 1),
        QuestRewardGeneratorCredibility(20),
    ),
)


# - Mystia +0 level
# - Human village outskirts +0 level
# - Requires large amount.
# Reward is around 2.0x of the value
QUEST_TEMPLATE_MYSTIA_RICE = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_RICE] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_RICE,
    None,
    1,
    4,
    (
        'As the owner of the izakaya, I am always in need of rice to serve.\n'
        '\n'
        'Please resupply me.'
    ),
    1,
    2,
    ITEM_ID_MYSTIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 7, HOUR_IN_SECONDS * 12, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_RICE, AMOUNT_TYPE_WEIGHT, 10000, 100, 80, 120),
    ),
    (
        QuestRewardGeneratorBalance(11000, 100, 80, 120),
        QuestRewardGeneratorCredibility(30),
    ),
)


# - Tewi +3 level
# - Human village outskirts +0 level
# - Requires large amount.
# Reward is around 1.5x of the value
QUEST_TEMPLATE_TEWI_RICE = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_TEWI_RICE] = QuestTemplate(
    QUEST_TEMPLATE_ID_TEWI_RICE,
    None,
    4, # target 1
    28,
    (
        'It is that time of the month again.\n'
        '\n'
        'Exactly! We need a large amount of rice supply to make mochi. '
        'Unfortunately, the supply at this time is a little bit short. '
        'I hope to see someone who can supply the remaining.\n'
        '\n'
        'Please bring the rice at least a few days before the full moon.'
    ),
    4,
    1,
    ITEM_ID_TEWI,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 10, DAY_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_RICE, AMOUNT_TYPE_WEIGHT, 32000, 1000, 80, 120),
    ),
    (
        QuestRewardGeneratorBalance(26000, 1000, 80, 120),
        QuestRewardGeneratorItemExactFix(ITEM_ID_DANGO, 3),
        QuestRewardGeneratorCredibility(60),
    ),
)


# - Rumia +2
# - Requires quest reward +1
# Reward is around 2x of the value
QUEST_TEMPLATE_RUMIA_SWEETS = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_RUMIA_SWEETS] = QuestTemplate(
    QUEST_TEMPLATE_ID_RUMIA_SWEETS,
    None,
    2, # Target: 1
    14,
    (
        'I am in the mood for something sweet! I accidentally ate a vegetable, I do not like vegetables, '
        'I like CANDIES and CAKES and I want this horrible taste gone!! Please, could you bring me some sweets?'
    ),
    3,
    1,
    ITEM_ID_RUMIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 5, HOUR_IN_SECONDS * 6, 80, 120),
        QuestRequirementGeneratorItemGroup(ITEM_GROUP_ID_SWEETS, AMOUNT_TYPE_WEIGHT, 200, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(1200, 100, 90, 110),
        QuestRewardGeneratorCredibility(20),
    ),
)

# - Aya +0
# - Requires meat +3
# - Rare drop +3 level
# reward is 1.5x the requirement.
QUEST_TEMPLATE_AYA_HUMAN_CORPSE = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_AYA_HUMAN_CORPSE] = QuestTemplate(
    QUEST_TEMPLATE_ID_AYA_HUMAN_CORPSE,
    None,
    2, # Target: 1
    38,
    (
        'I\'d like to ask you about delivery of a dead human body.\n'
        'A story about the cause of its death would make for an excellent article at the Bunbunmaru Newspapers!'
    ),
    6,
    1,
    ITEM_ID_AYA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 72, DAY_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemGroup(ITEM_GROUP_ID_HUMAN_CORPSE_FULL, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(27000, 1000, 90, 110),
        QuestRewardGeneratorItemExactFix(ITEM_ID_PEN, 1),
        QuestRewardGeneratorCredibility(60),
    ),
)

# - Youmu +0
# - Requires quest reward + meat +4
# Reward is around 2.5x the value.
QUEST_TEMPLATE_YOUMU_RAMEN = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_YOUMU_RAMEN] = QuestTemplate(
    QUEST_TEMPLATE_ID_YOUMU_RAMEN,
    (
        QUEST_TEMPLATE_ID_YOUMU_DANGO_TEA,
    ),
    2, # Target: 1
    28,
    (
        'Pasta, ramen, soba... Yuyuko adores noodles!\n'
        'She is crawling for a good Ramen, please bring one, so I can feed her.'
    ),
    4,
    2,
    ITEM_ID_YOUMU,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 4, HOUR_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_RAMEN, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(930, 10, 80, 120),
        QuestRewardGeneratorCredibility(10),
    ),
)

# - Youmu +0
# - Requires item reward of quest level 7 +8
# Reward is around 33x the requirements.
QUEST_TEMPLATE_YOUMU_DANGO_TEA = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_YOUMU_DANGO_TEA] = QuestTemplate(
    QUEST_TEMPLATE_ID_YOUMU_DANGO_TEA,
    (
        QUEST_TEMPLATE_ID_YOUMU_RAMEN,
    ),
    2, # Target: 1
    28,
    (
        'Yuyuko wants dango and tea for tomorrow\'s dessert.\n'
        'I am busy with other errands today, so please deliver it for me.'
    ),
    8,
    2,
    ITEM_ID_YOUMU,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 2, 1, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_DANGO, AMOUNT_TYPE_COUNT, 3, 1, 100, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_TEA_LEAVES, AMOUNT_TYPE_COUNT, 4, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorItemExact(ITEM_ID_PEACH, 8, 1, 100, 100),
        QuestRewardGeneratorBalance(400, 10, 80, 120),
        QuestRewardGeneratorCredibility(30),
    ),
)


# - Koishi +1
# - Requires reward of rare drop quest + meat +7 level
# Reward is around 2x the value.
QUEST_TEMPLATE_KOISHI_PEN = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_KOISHI_PEN] = QuestTemplate(
    QUEST_TEMPLATE_ID_KOISHI_PEN,
    None,
    2, # Target: 1
    70,
    (
        'Satori is soon to die from sleep depri- uhh i forgor what Orin said.\n'
        'I want her last corporate work days to be memorable!! '
        'I would like to gift her a top quality pen, so she can do her last paper works with a smile!!'
    ),
    8,
    1,
    ITEM_ID_KOISHI,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 72, DAY_IN_SECONDS, 80, 100),
        QuestRequirementGeneratorItemExact(ITEM_ID_PEN, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(5000, 10, 80, 120),
        QuestRewardGeneratorCredibility(80),
    ),
)


# - Nitori +0
# - Requires meat +3
# Reward is around 1.7x the value.
QUEST_TEMPLATE_NITORI_HUMAN_BONE = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_NITORI_HUMAN_BONE] = QuestTemplate(
    QUEST_TEMPLATE_ID_NITORI_HUMAN_BONE,
    None,
    2, # Target: 1
    23,
    (
        'Hey!\n'
        '\n'
        'I am trying to cultivate cucumbers in the Genbu Ravine, but the the soil here lacks important nutrients, '
        'like calcium. Therefore I am thinking on sprinkling the soil with some bone meal.\n'
        '\n'
        'Could you please collect a bunch of bones for me?'
    ),
    3,
    0,
    ITEM_ID_NITORI,
    (
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_BONE, AMOUNT_TYPE_WEIGHT, 10000, 10000, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(2200, 1, 100, 100),
        QuestRewardGeneratorCredibilityFix(15),
    ),
)


# - Parsee +2
# - Ruins +1 level
# - Rare drop +3 level
QUEST_TEMPLATE_PARSEE_RIBBON_BOW = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_PARSEE_RIBBON_BOW] = QuestTemplate(
    QUEST_TEMPLATE_ID_PARSEE_RIBBON_BOW,
    (
        QUEST_TEMPLATE_ID_FLANDRE_RIBBON_BOW,
        QUEST_TEMPLATE_ID_REMILIA_RIBBON_BOW,
    ),
    2, # Target: 1
    71,
    (
        'Collecting Ribbons is the rage in Former Hell now!!\n'
        'I want one too, I want one NOW!!\n'
        'I need you to bring me one!!'
    ),
    6,
    1,
    ITEM_ID_PARSEE,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 32, DAY_IN_SECONDS, 90, 110),
        QuestRequirementGeneratorItemExact(ITEM_ID_RIBBON_BOW, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorCredibilityFix(240),
    ),
)


# - Requires meat +3
# Reward is around 2x the requirements
QUEST_TEMPLATE_MYSTIA_HUMAN_BONE = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MYSTIA_HUMAN_BONE] = QuestTemplate(
    QUEST_TEMPLATE_ID_MYSTIA_HUMAN_BONE,
    None,
    1,
    4,
    (
        'I would like to request a key ingredient for my broth.\n'
        '\n'
        'Could you please bring me some bones?'
    ),
    3,
    1,
    ITEM_ID_MYSTIA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 3, HOUR_IN_SECONDS, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_HUMAN_BONE, AMOUNT_TYPE_WEIGHT, 2000, 100, 80, 120),
    ),
    (
        QuestRewardGeneratorItemExact(ITEM_ID_RAMEN, 1, 1, 100, 100),
        QuestRewardGeneratorBalance(150, 10, 100, 100),
        QuestRewardGeneratorCredibility(10),
    ),
)


# - Flandre +4
# - Ruins +1 level
# - Rare drop +3 level
QUEST_TEMPLATE_FLANDRE_PLUSHIE_BEAR = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_FLANDRE_PLUSHIE_BEAR] = QuestTemplate(
    QUEST_TEMPLATE_ID_FLANDRE_PLUSHIE_BEAR,
    (
        QUEST_TEMPLATE_FLANDRE_RIBBON_BOW,
        QUEST_TEMPLATE_ID_REMILIA_RIBBON_BOW,
        QUEST_TEMPLATE_ID_REMILIA_FLANDRE_WING,
    ),
    1,
    53,
    (
        'Today my sister came into my room and demanded me to go take a shower because '
        'I supposedly smell like dog\'s pile!! They want me to take a shower at least once every two months!!! '
        'What the HELL?!?!\n'
        '\n'
        'I bet it\'s because Sakuya keeps bringing me dirty bodies to play with!! '
        'They keep squirting their body fluids all over the room as I am indulging myself in the fun!!\n'
        'I would like to play with something clean instead, like a cute plushie!"'
    ),
    8,
    1,
    ITEM_ID_FLANDRE,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 72, DAY_IN_SECONDS, 90, 110),
        QuestRequirementGeneratorItemExact(ITEM_ID_PLUSHIE_BEAR, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorItemExactFix(ITEM_ID_HUMAN_BODY_SHARD_CHEWED, 1),
        QuestRewardGeneratorCredibilityFix(120),
    ),
)


# - Marisa +2 level
# - Requires quest reward + meat +4
# Reward is around 2x of the value
QUEST_TEMPLATE_MARISA_FLYKILLER_AMANITA = QUEST_TEMPLATES[QUEST_TEMPLATE_ID_MARISA_FLYKILLER_AMANITA] = QuestTemplate(
    QUEST_TEMPLATE_ID_MARISA_FLYKILLER_AMANITA,
    None,
    1,
    28,
    (
        'Hey there!!\n'
        'Once again, Reimu is unable to afford any food due to lack of donations to her shrine, '
        'yet she refuses to eat anything I make her! She is so greedy...'
        'Could you please just bring Reimu some Ramen? '
        'Maybe she will see it as a donation if someone else were to offer it.'
    ),
    6,
    1,
    ITEM_ID_MARISA,
    (
        QuestRequirementGeneratorDuration(DAY_IN_SECONDS * 7, HOUR_IN_SECONDS, 80, 130),
        QuestRequirementGeneratorItemExact(ITEM_ID_RAMEN, AMOUNT_TYPE_COUNT, 1, 1, 100, 100),
    ),
    (
        QuestRewardGeneratorBalance(700, 50, 80, 120),
        QuestRewardGeneratorCredibility(10),
    ),
)

# Idea:
# Yuyuko's stomach is crawling like she is starving to death habitually. Would you please feed a morsel to this beast?
# Maybe an XXX would do the job? I would reward you plentifully.

# Idea:
# Oh no!! When i got home I found out that Reimu drank all of my precious sake!
# Please bring me 3 bottles of Sake urgently!

# Idea:
# As you know, there is a critical shortage of XXX in XXX tight now. I will pay you well if you can bring me XXX.

# Idea:
# I am a collector of XXX. Please do not ask why I am collecting such things. 
# My XXX is already staring at me as Kokoro would if I would have one of her masks. I Promise, I don't!!!.
# Anyways, can you bring me XXX?

# Idea:
# I had a fortune recently, therefore I decided to treat myself with XXX.
# Could you please bring me one?

# Idea:
# I need XXX for some errand. If you can deliver me one within the deadline, would be great.

# Idea:
# As you probably know, I am living with the gluttonous Yuyuko. 
# Today I have seen something so obscure, that I did not even believe my eyes!! She was licking the wall!!! 
# I don't want her to eat my home!! Please bring me a large amount of supplies, so I can calm her hunger!



# Quest ideas:
# Bring satori food for pets
# Aya heard rumors that something is to do with insert item here, can you bring said item.
# Sakuya, bring remi tea & blood?
# Bring suwako a bunch of random things.
# Bring reimu a ramen, because they are fucking broke as shit.


