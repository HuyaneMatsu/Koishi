__all__ = ()

from hata import Embed

from .constants import SUB_ENTRY_PER_PAGE
from .keys import KEY_CHARACTER
from .parsers_description import parse_description_character, parse_character_media_connections_description
from .parsers_name import parse_character_name
from .parsers_url import parse_image_url_character, parse_url_character


TEXT_RELATED_MEDIAS_TOP_N = f'Related medias (up to {SUB_ENTRY_PER_PAGE})'


def build_embed_character(data):
    """
    Builds character embed.
    
    Parameters
    ----------
    data : `None | dict<str, object>`
        Character query response data.
    
    Returns
    -------
    embed : ``Embed``
    """
    if data is None:
        return Embed(description = 'No result.')
    
    character_data = data['data'][KEY_CHARACTER]
    
    embed = Embed(
        parse_character_name(character_data),
        parse_description_character(character_data),
        url = parse_url_character(character_data),
    )
    
    image_url = parse_image_url_character(character_data)
    if (image_url is not None):
        embed.add_thumbnail(image_url)
    
    media_connections_description = parse_character_media_connections_description(character_data)
    if (media_connections_description is not None):
        embed.add_field(TEXT_RELATED_MEDIAS_TOP_N, media_connections_description)
    
    return embed
