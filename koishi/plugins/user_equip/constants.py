__all__ = ('ITEM_SLOTS',)

from ..item_core import ITEM_FLAG_HEAD, ITEM_FLAG_COSTUME, ITEM_FLAG_WEAPON


ITEM_SLOTS = {
    'Costume' : ITEM_FLAG_COSTUME,
    'Head accessory' : ITEM_FLAG_HEAD,
    'Weapon' : ITEM_FLAG_WEAPON,
}

ITEM_FLAGS_ALLOWED = (
    ITEM_FLAG_COSTUME,
    ITEM_FLAG_HEAD,
    ITEM_FLAG_WEAPON,
)

ITEM_SLOT_NAMES = {
    ITEM_FLAG_COSTUME : 'costume',
    ITEM_FLAG_HEAD : 'head accessory',
    ITEM_FLAG_WEAPON : 'weapon',
}
ITEM_SLOT_NAME_UNKNOWN = 'unknown'
