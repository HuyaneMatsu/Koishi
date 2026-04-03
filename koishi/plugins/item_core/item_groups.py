__all__ = ()

from hata import BUILTIN_EMOJIS

from .constants import ITEM_GROUPS
from .item_group import ItemGroup
from .item_group_ids import ITEM_GROUP_ID_FIREWOOD, ITEM_GROUP_ID_KNIFE
from .item_ids import (
    ITEM_ID_ACHING_AFFECTION_S_HEART_PIERCER, ITEM_ID_BAMBOO, ITEM_ID_BOUGH, ITEM_ID_CUT_WOOD, ITEM_ID_KITCHEN_KNIFE,
    ITEM_ID_LOG, ITEM_ID_POKING_KNIFE, ITEM_ID_TWIGS
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
