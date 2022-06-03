__all__ = ()


WAIFU_TYPE_WIFE = 0
WAIFU_TYPE_SISTER_LIL = 1
WAIFU_TYPE_SISTER_BIG = 2
WAIFU_TYPE_MAMA = 3
WAIFU_TYPE_MASTER = 4
WAIFU_TYPE_MAID = 5


WAIFU_TYPE_NAMES = {
    WAIFU_TYPE_WIFE: ('wife', 'wives'),
    WAIFU_TYPE_SISTER_LIL: ('little sister', 'little sisters'),
    WAIFU_TYPE_SISTER_BIG: ('big sister', 'big sisters'),
    WAIFU_TYPE_MAMA: ('mama', 'mamas'),
    WAIFU_TYPE_MASTER: ('master', 'masters'),
    WAIFU_TYPE_MAID: ('maid', 'maids'),
}

WAIFU_TYPE_NAMES_REVERTED = {
    WAIFU_TYPE_WIFE: ('wife', 'wives'),
    WAIFU_TYPE_SISTER_LIL: ('big sister', 'big sisters'),
    WAIFU_TYPE_SISTER_BIG: ('little sister', 'little sisters'),
    WAIFU_TYPE_MAMA: ('daughter', 'daughters'),
    WAIFU_TYPE_MASTER: ('maid', 'maids'),
    WAIFU_TYPE_MAID: ('master', 'masters'),
}

WAIFU_TYPE_NAME_UNKNOWN = ('pudding', 'puddings')


def get_relation_name(relation_type, reverted, plural):
    if reverted:
        collection = WAIFU_TYPE_NAMES_REVERTED
    else:
        collection = WAIFU_TYPE_NAMES
    
    return collection.get(relation_type, WAIFU_TYPE_NAME_UNKNOWN)[plural]
