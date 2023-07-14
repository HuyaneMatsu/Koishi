__all__ = ()

from hata import Embed

from .keys import (
    KEY_MEDIA, KEY_MEDIA_AVERAGE_SCORE, KEY_MEDIA_CHAPTER_COUNT, KEY_MEDIA_EPISODE_COUNT, KEY_MEDIA_EPISODE_LENGTH,
    KEY_MEDIA_VOLUME_COUNT
)
from .parsers_date import parse_media_date_range
from .parsers_description import parse_description_media
from .parsers_media import parse_media_format, parse_media_status
from .parsers_name import parse_name_media
from .parsers_url import parse_url_anime, parse_url_manga, parse_image_url_media


def build_embed_media_based(media_data, url_parser):
    """
    Builds a base media embed.
    
    Parameters
    ----------
    media_data : `dict<str, object>`
        Media data.
    url_parser : `FunctionType`
        parser to parse url with.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        parse_name_media(media_data),
        parse_description_media(media_data),
        url = url_parser(media_data),
    )
    
    image_url = parse_image_url_media(media_data)
    if (image_url is not None):
        embed.add_thumbnail(
            image_url,
        )
    
    return embed

   
def add_anime_stat_fields(embed, anime_data):
    """
    Adds anime stat fields to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    anime_data : `dict<str, object>`
        Anime data.
    """
    episode_count = anime_data.get(KEY_MEDIA_EPISODE_COUNT, None)
    if (episode_count is not None) and (episode_count != 1):
        embed.add_field('Episodes', str(episode_count), inline = True)
    
    episode_length = anime_data.get(KEY_MEDIA_EPISODE_LENGTH, None)
    if (episode_length is not None):
        if (episode_count is None) or (episode_count == 1):
            field_name = 'Length'
        else:
            field_name = 'Episode length'
        
        embed.add_field(field_name, f'{episode_length} minute', inline = True)


def add_manga_stat_fields(embed, manga_data):
    """
    Adds manga stat fields to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    manga_data : `dict<str, object>`
        Manga data.
    """
    volume_count = manga_data.get(KEY_MEDIA_VOLUME_COUNT, None)
    if (volume_count is not None):
        embed.add_field('Volumes', str(volume_count), inline = True)
    
    chapter_count = manga_data.get(KEY_MEDIA_CHAPTER_COUNT, None)
    if (chapter_count is not None):
        embed.add_field('Chapters', chapter_count, inline = True)


def add_media_shared_fields(embed, media_data):
    """
    Adds shared media fields to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    media_data : `dict<str, object>`
        Media data.
    """
    embed.add_field('Status', parse_media_status(media_data), inline = True)
    embed.add_field('Format', parse_media_format(media_data), inline = True)
    
    date_range = parse_media_date_range(media_data)
    if (date_range is not None):
        embed.add_field(*date_range, inline = True)
    
    average_score = media_data.get(KEY_MEDIA_AVERAGE_SCORE, None)
    if (average_score is not None):
        embed.add_field('Average score', f'{average_score} / 100', inline = True)


def build_embed_anime(data):
    """
    Builds an anime embed.
    
    Parameters
    ----------
    data : `None | dict<str, object>`
        Anime query response data.
    
    Returns
    -------
    embed : ``Embed``
    """
    if data is None:
        return Embed(description = 'No result.')
    
    anime_data = data['data'][KEY_MEDIA]
    
    embed = build_embed_media_based(anime_data, parse_url_anime)
    add_anime_stat_fields(embed, anime_data)
    add_media_shared_fields(embed, anime_data)
    return embed


def build_embed_manga(data):
    """
    Builds a manga embed.
    
    Parameters
    ----------
    data : `None | dict<str, object>`
        Manga query response data.
    
    Returns
    -------
    embed : ``Embed``
    """
    if data is None:
        return Embed(description = 'No result.')
    
    manga_data = data['data'][KEY_MEDIA]
    
    embed = build_embed_media_based(manga_data, parse_url_manga)
    add_manga_stat_fields(embed, manga_data)
    add_media_shared_fields(embed, manga_data)
    return embed
