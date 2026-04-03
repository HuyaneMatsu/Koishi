import vampytest
from hata import Embed

from ..embed_building_media import add_media_shared_fields
from ..keys import (
    KEY_FUZZY_DATE_DAY, KEY_FUZZY_DATE_MONTH, KEY_FUZZY_DATE_YEAR, KEY_MEDIA_AVERAGE_SCORE, KEY_MEDIA_FORMAT,
    KEY_MEDIA_START_DATE, KEY_MEDIA_STATUS
)
from ..parsers_media import MEDIA_FORMAT_DEFAULT, MEDIA_STATUS_DEFAULT


def _iter_options():
    yield (
        {},
        Embed().add_field(
            'Status', MEDIA_STATUS_DEFAULT, inline = True,
        ).add_field(
            'Format', MEDIA_FORMAT_DEFAULT, inline = True,
        ),
    )
    yield (
        {
            KEY_MEDIA_FORMAT: 'ova',
            KEY_MEDIA_STATUS: 'FINISHED',
            KEY_MEDIA_START_DATE: {
                KEY_FUZZY_DATE_YEAR: 12,
                KEY_FUZZY_DATE_MONTH: 10,
                KEY_FUZZY_DATE_DAY: 8,
            },
            KEY_MEDIA_AVERAGE_SCORE: 69,
        },
        Embed().add_field(
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
def test__add_media_shared_fields(media_data):
    """
    Tests whether ``add_media_shared_fields`` works as intended.
    
    Parameters
    ----------
    media_data : `dict<str, object>`
        Media data.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed()
    add_media_shared_fields(embed, media_data)
    return embed
