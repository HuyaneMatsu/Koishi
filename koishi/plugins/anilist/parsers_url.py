__all__ = ()

from .constants import URL_BASE_ANIME, URL_BASE_CHARACTER, URL_BASE_MANGA
from .keys import (
    KEY_CHARACTER_ID, KEY_CHARACTER_IMAGE, KEY_CHARACTER_IMAGE_LARGE, KEY_MEDIA_ID, KEY_MEDIA_IMAGE,
    KEY_MEDIA_IMAGE_LARGE, KEY_MEDIA_TYPE, KEY_MEDIA_TYPE_ANIME, KEY_MEDIA_TYPE_MANGA
)


def parse_url_character(character_data):
    """
    Parses the character's url from its data.
    
    Parameters
    ----------
    character_data : `dict<str, object>`
        Character data.
    
    Returns
    -------
    character_url : `None | str`
    """
    character_id = character_data.get(KEY_CHARACTER_ID, None)
    if character_id is None:
        return
    
    return f'{URL_BASE_CHARACTER}{character_id}'


def parse_image_url_character(character_data):
    """
    Parsers the character's image's url.
    
    Parameters
    ----------
    character_data : `dict<str, object>`
        Character data.
    
    Returns
    -------
    character_image_url : `None | str`
    """
    image_datas = character_data.get(KEY_CHARACTER_IMAGE, None)
    if image_datas is None:
        return
    
    return image_datas.get(KEY_CHARACTER_IMAGE_LARGE, None)


def parse_url_media(media_data):
    """
    Parses the media's url out from the given media data.
    
    Parameters
    ----------
    media_data : `dict<str, object>`
        Media data.
    
    Returns
    -------
    media_url : `None | str`
    """
    media_type = media_data.get(KEY_MEDIA_TYPE, None)
    if media_type is None:
        return
    
    if media_type == KEY_MEDIA_TYPE_ANIME:
        url_base = URL_BASE_ANIME
    elif media_type == KEY_MEDIA_TYPE_MANGA:
        url_base = URL_BASE_MANGA
    else:
        return
    
    media_id = media_data.get(KEY_MEDIA_ID, None)
    if media_id is None:
        return
    
    return f'{url_base}{media_id}'


def parse_image_url_media(media_data):
    """
    Parsers the media's image's url.
    
    Parameters
    ----------
    media_data : `dict<str, object>`
        Media data.
    
    Returns
    -------
    media_image_url : `None | str`
    """
    image_datas = media_data.get(KEY_MEDIA_IMAGE, None)
    if image_datas is None:
        return
    
    return image_datas.get(KEY_MEDIA_IMAGE_LARGE, None)


def parse_url_anime(anime_data):
    """
    Parses the anime's url from its data.
    
    Parameters
    ----------
    anime_data : `dict<str, object>`
        Anime data.
    
    Returns
    -------
    anime_url : `None | str`
    """
    anime_id = anime_data.get(KEY_MEDIA_ID, None)
    if anime_id is None:
        return
    
    return f'{URL_BASE_ANIME}{anime_id}'


def parse_url_manga(manga_data):
    """
    Parses the manga's url from its data.
    
    Parameters
    ----------
    manga_data : `dict<str, object>`
        Manga data.
    
    Returns
    -------
    manga_url : `None | str`
    """
    manga_id = manga_data.get(KEY_MEDIA_ID, None)
    if manga_id is None:
        return
    
    return f'{URL_BASE_MANGA}{manga_id}'
