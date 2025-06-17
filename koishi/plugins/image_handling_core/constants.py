__all__ = ('SAFE_BOORU_ENDPOINT', 'SAFE_BOORU_PROVIDER', 'SOLO_REQUIRED_TAGS', 'TOUHOU_TAGS_BANNED',)


SAFE_TAGS_BANNED = frozenset((
    'bdsm',
    'huge_filesize',
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
    'ai-generated'
    'middle_finger',
    'smoking',
))


TOUHOU_TAGS_BANNED = frozenset((
    *SAFE_TAGS_BANNED,
    'comic',
    'greyscale',
    'ronald_mcdonald',
    'pokemon',
))


NSFW_TAGS_BANNED = frozenset((
    'loli',
    'lolicon',
    'shota',
    'shotacon',
    'huge_filesize',
    'ai-generated',
    'smoking',
))


SOLO_REQUIRED_TAGS = frozenset((
    'solo',
))


SAFE_BOORU_ENDPOINT = 'https://safebooru.org'
SAFE_BOORU_PROVIDER = 'safebooru'
SAFE_BOORU_AUTOCOMPLETE_ENDPOINT = f'{SAFE_BOORU_ENDPOINT}/autocomplete.php'
SAFE_BOORU_AUTOCOMPLETE_PARAMETERS = {}
SAFE_BOORU_AUTOCOMPLETE_QUERY_KEY = 'q'

NSFW_BOORU_ENDPOINT = 'https://gelbooru.com'
NSFW_BOORU_PROVIDER = 'gelbooru'
NSFW_BOORU_AUTOCOMPLETE_ENDPOINT = f'{NSFW_BOORU_ENDPOINT}/index.php'
NSFW_BOORU_AUTOCOMPLETE_PARAMETERS = {'page': 'autocomplete2', 'type': 'tag_query', 'limit': '10'}
NSFW_BOORU_AUTOCOMPLETE_QUERY_KEY = 'term'
