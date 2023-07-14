import vampytest
from hata import Embed

from ..constants import URL_BASE_MANGA
from ..embed_building_media import build_embed_manga
from ..keys import (
    KEY_FUZZY_DATE_DAY, KEY_FUZZY_DATE_MONTH, KEY_FUZZY_DATE_YEAR, KEY_MEDIA, KEY_MEDIA_AVERAGE_SCORE,
    KEY_MEDIA_CHAPTER_COUNT, KEY_MEDIA_DESCRIPTION, KEY_MEDIA_FORMAT, KEY_MEDIA_ID, KEY_MEDIA_IMAGE,
    KEY_MEDIA_IMAGE_LARGE, KEY_MEDIA_NAME, KEY_MEDIA_NAME_ROMAJI, KEY_MEDIA_START_DATE, KEY_MEDIA_STATUS,
    KEY_MEDIA_VOLUME_COUNT
)
from ..parsers_media import MEDIA_FORMAT_DEFAULT, MEDIA_STATUS_DEFAULT
from ..parsers_name import NAME_DEFAULT


def _iter_options():
    yield (
        None,
        Embed(description = 'No result.'),
    )
    yield (
        {
            'data': {
                KEY_MEDIA: {}
            }
        },
        Embed(
            NAME_DEFAULT,
        ).add_field(
            'Status', MEDIA_STATUS_DEFAULT, inline = True,
        ).add_field(
            'Format', MEDIA_FORMAT_DEFAULT, inline = True,
        ),
    )
    
    yield (
        {
            'data': {
                KEY_MEDIA: {
                    KEY_MEDIA_NAME: {
                        KEY_MEDIA_NAME_ROMAJI: 'satori',
                    },
                    KEY_MEDIA_DESCRIPTION: 'love koishi',
                    KEY_MEDIA_ID: 12,
                    KEY_MEDIA_IMAGE: {
                        KEY_MEDIA_IMAGE_LARGE: 'https://orindance.party/'
                    },
                    KEY_MEDIA_VOLUME_COUNT: 2,
                    KEY_MEDIA_CHAPTER_COUNT: 3,
                    KEY_MEDIA_FORMAT: 'ova',
                    KEY_MEDIA_STATUS: 'FINISHED',
                    KEY_MEDIA_START_DATE: {
                        KEY_FUZZY_DATE_YEAR: 12,
                        KEY_FUZZY_DATE_MONTH: 10,
                        KEY_FUZZY_DATE_DAY: 8,
                    },
                    KEY_MEDIA_AVERAGE_SCORE: 69,
                },
            }
        },
        Embed(
            'satori',
            'love koishi',
            url = f'{URL_BASE_MANGA}{12}',
        ).add_thumbnail(
            'https://orindance.party/',
        ).add_field(
            'Volumes', '2', inline = True,
        ).add_field(
            'Chapters', '3', inline = True,
        ).add_field(
            'Status', 'finished', inline = True,
        ).add_field(
            'Format', 'ova', inline = True,
        ).add_field(
            'Started', '12-10-8', inline = True,
        ).add_field(
            'Average score', f'{69} / 100', inline = True,
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_embed_manga(data):
    """
    Tests whether ``build_embed_manga`` works as intended.
    
    Parameters
    ----------
    data : `None | dict<str, object>`
        Query response data.
    
    Returns
    -------
    embed : ``Embed``
    """
    return build_embed_manga(data)
