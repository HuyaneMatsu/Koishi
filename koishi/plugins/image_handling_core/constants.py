__all__ = ('SAFE_TAGS_BANNED', 'NSFW_TAGS_BANNED', 'SOLO_REQUIRED_TAGS', 'TOUHOU_TAGS_BANNED',)


SHARED_TAGS_BANNED = (
    'huge_filesize',
    'ai-generated',
    'smoking',
)

SAFE_TAGS_BANNED = frozenset((
    *SHARED_TAGS_BANNED,
    'bdsm',
    'underwear',
    'sideboob',
    'pov_feet',
    'underboob',
    'upskirt',
    'sexually_suggestive',
    'ass',
    'bikini',
    'clothed_female_nude_male',
    'no_panties',
    'artificial_vagina',
    'covering_breasts',
    'huge_breasts',
    'blood',
    'penetration_gesture',
    'no_bra',
    'nude',
    'butt_crack',
    'naked_apron',
    'pantyshot',
    'open_shirt',
    'clothes_lift',
    'slingshot_swimsuit',
    'bikini',
    'middle_finger',
))


TOUHOU_TAGS_BANNED = frozenset((
    *SAFE_TAGS_BANNED,
    'comic',
    'greyscale',
    'ronald_mcdonald',
    'pokemon',
))


NSFW_TAGS_BANNED = frozenset((
    *SHARED_TAGS_BANNED,
    'loli',
    'lolicon',
    'shota',
    'shotacon',
))


SOLO_REQUIRED_TAGS = frozenset((
    'solo',
))

BLACKLISTED_TAGS = {
    # ai
    'pigsir13152',
    'dobostorte',
    'oekakizuki',
    'rikatan',
    'ai-generated',
}


PAGE_SIZE = 100
RETRIES_MAX = 5
AUTOCOMPLETE_PAGE_SIZE = 25
