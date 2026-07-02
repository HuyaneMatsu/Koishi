__all__ = ()

from hata import BUILTIN_EMOJIS

from .constants import ITEM_GROUPS
from .item_group import ItemGroup
from .item_group_ids import (
    ITEM_GROUP_ID_BLOOD_SAUSAGE_MEAT, ITEM_GROUP_ID_BOILED_SAUSAGE, ITEM_GROUP_ID_FIREWOOD, ITEM_GROUP_ID_KNIFE,
    ITEM_GROUP_ID_LIVER_SAUSAGE_MEAT, ITEM_GROUP_ID_MEAT_SAUSAGE_MEAT, ITEM_GROUP_ID_SWEETS
)
from .item_ids import (
    ITEM_ID_ACHING_AFFECTION_S_HEART_PIERCER, ITEM_ID_BAMBOO, ITEM_ID_BLOOD_SAUSAGE, ITEM_ID_BOUGH, ITEM_ID_CUT_WOOD,
    ITEM_ID_DANGO, ITEM_ID_HUMAN_HEART, ITEM_ID_HUMAN_KIDNEY, ITEM_ID_HUMAN_LIVER, ITEM_ID_HUMAN_LUNG,
    ITEM_ID_HUMAN_SPLEEN, ITEM_ID_HUMAN_TONGUE, ITEM_ID_KITCHEN_KNIFE, ITEM_ID_LIVER_SAUSAGE, ITEM_ID_LOG,
    ITEM_ID_MEAT_SAUSAGE, ITEM_ID_POKING_KNIFE, ITEM_ID_PUDDING, ITEM_ID_TWIGS
)


ITEM_GROUP_KNIFE = ITEM_GROUPS[ITEM_GROUP_ID_KNIFE] = ItemGroup(
    ITEM_GROUP_ID_KNIFE,
    'knife',
    BUILTIN_EMOJIS['knife'],
    (
        'Knifes are tools for every day use. They have 2 possible use cases: slicing and stabbing.'
    ),
    (
        ITEM_ID_ACHING_AFFECTION_S_HEART_PIERCER,
        ITEM_ID_KITCHEN_KNIFE,
        ITEM_ID_POKING_KNIFE,
    ),
)


ITEM_GROUP_FIREWOOD = ITEM_GROUPS[ITEM_GROUP_ID_FIREWOOD] = ItemGroup(
    ITEM_GROUP_ID_KNIFE,
    'firewood',
    BUILTIN_EMOJIS['wood'],
    (
        'Firewood is a form of wood based fuels. Wood can be used for firing in many forms, commonly known forms are: '
        'charcoal, briquette, pellets, chops or sawdust. '
        'Although firewood means the usage of wood which is not overly processed.'
    ),
    (
        ITEM_ID_TWIGS,
        ITEM_ID_BOUGH,
        ITEM_ID_LOG,
        ITEM_ID_BAMBOO,
        ITEM_ID_CUT_WOOD,
    ),
)


ITEM_GROUP_SWEETS = ITEM_GROUPS[ITEM_GROUP_ID_SWEETS] = ItemGroup(
    ITEM_GROUP_ID_SWEETS,
    'Sweets',
    BUILTIN_EMOJIS['cake'],
    (
        'Sweets are such a food category, which usually has high sugar content. '
        'They are commonly used as desserts, cakes, ice cream, chocolates and sweet pies.'
    ),
    (
        ITEM_ID_DANGO,
        ITEM_ID_PUDDING,
    ),
)


ITEM_GROUP_LIVER_SAUSAGE_MEAT = ITEM_GROUPS[ITEM_GROUP_ID_LIVER_SAUSAGE_MEAT] = ItemGroup(
    ITEM_GROUP_ID_LIVER_SAUSAGE_MEAT,
    'Liver sausage meat',
    BUILTIN_EMOJIS['cut_of_meat'],
    (
        'Various meats used additionally in liver sausages.'
    ),
    (
        ITEM_ID_HUMAN_HEART,
        ITEM_ID_HUMAN_TONGUE,
    ),
)


ITEM_GROUP_BLOOD_SAUSAGE_MEAT = ITEM_GROUPS[ITEM_GROUP_ID_BLOOD_SAUSAGE_MEAT] = ItemGroup(
    ITEM_GROUP_ID_BLOOD_SAUSAGE_MEAT,
    'Blood sausage meat',
    BUILTIN_EMOJIS['cut_of_meat'],
    (
        'Various meats used additionally in blood sausages.'
    ),
    (
        ITEM_ID_HUMAN_HEART,
        ITEM_ID_HUMAN_TONGUE,
        ITEM_ID_HUMAN_SPLEEN,
        ITEM_ID_HUMAN_KIDNEY,
        ITEM_ID_HUMAN_LUNG,
    ),
)


ITEM_GROUP_MEAT_SAUSAGE_MEAT = ITEM_GROUPS[ITEM_GROUP_ID_MEAT_SAUSAGE_MEAT] = ItemGroup(
    ITEM_GROUP_ID_MEAT_SAUSAGE_MEAT,
    'Blood sausage meat',
    BUILTIN_EMOJIS['cut_of_meat'],
    (
        'Various meats used additionally in meat sausages.'
    ),
    (
        ITEM_ID_HUMAN_HEART,
        ITEM_ID_HUMAN_TONGUE,
        ITEM_ID_HUMAN_SPLEEN,
        ITEM_ID_HUMAN_KIDNEY,
        ITEM_ID_HUMAN_LIVER,
        ITEM_ID_HUMAN_LUNG,
    ),
)


ITEM_GROUP_BOILED_SAUSAGE = ITEM_GROUPS[ITEM_GROUP_ID_BOILED_SAUSAGE] = ItemGroup(
    ITEM_GROUP_ID_BOILED_SAUSAGE,
    'Boiled sausage',
    BUILTIN_EMOJIS['worm'],
    (
        'Boiled sausage is a stuffed good which should be eaten after cooked or fried. '
        'It may be made out of meats or various organs of slaughter animals. '
        'It is made of of spiced filling stuffed into a natural or artificial cover.\n'
        'It has multiple popular versions, like blood, liver, rice and lung.'
    ),
    (
        ITEM_ID_LIVER_SAUSAGE,
        ITEM_ID_BLOOD_SAUSAGE,
        ITEM_ID_MEAT_SAUSAGE,
    ),
)
