__all__ = ()

from .keys import KEY_MEDIA_FORMAT, KEY_MEDIA_STATUS


MEDIA_FORMAT_MAP = {
    'TV': 'tv',
    'TV_SHORT': 'tv short',
    'MOVIE': 'movie',
    'SPECIAL': 'special',
    'OVA': 'ova',
    'ONA': 'ona',
    'MUSIC': 'music',
    'MANGA': 'manga',
    'NOVEL': 'novel',
    'ONE_SHOT': 'one shot'
}

MEDIA_FORMAT_DEFAULT = 'unknown'


def parse_media_format(media_data):
    """
    Parses the media's format out from the given data.
    
    Parameters
    ----------
    media_data : `dict<str, object>`
        Media data.
    
    Returns
    -------
    media_format : `str`
    """
    media_format = media_data.get(KEY_MEDIA_FORMAT, None)
    if (media_format is None):
        return MEDIA_FORMAT_DEFAULT
    
    try:
        converted_media_format = MEDIA_FORMAT_MAP[media_format]
    except KeyError:
        converted_media_format = media_format.lower().replace('_', ' ')
        MEDIA_FORMAT_MAP[media_format] = converted_media_format
    
    return converted_media_format


MEDIA_STATUS_MAP = {
    'FINISHED': 'finished',
    'RELEASING': 'releasing',
    'NOT_YET_RELEASED': 'not yet released',
    'CANCELLED': 'cancelled',
    'HIATUS': 'hiatus',
}

MEDIA_STATUS_DEFAULT = 'unknown'


def parse_media_status(media_data):
    """
    Parses the media's status out from the given data.
    
    Parameters
    ----------
    media_data : `dict<str, object>`
        Media data.
    
    Returns
    -------
    media_status : `str`
    """
    media_status = media_data.get(KEY_MEDIA_STATUS, None)
    if (media_status is None):
        return MEDIA_STATUS_DEFAULT
    
    try:
        converted_media_status = MEDIA_STATUS_MAP[media_status]
    except KeyError:
        converted_media_status = media_status.lower().replace('_', ' ')
        MEDIA_STATUS_MAP[media_status] = converted_media_status
    
    return converted_media_status
