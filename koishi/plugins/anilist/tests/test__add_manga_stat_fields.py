import vampytest
from hata import Embed

from ..embed_building_media import add_manga_stat_fields
from ..keys import KEY_MEDIA_CHAPTER_COUNT, KEY_MEDIA_VOLUME_COUNT


def _iter_options():
    yield (
        {},
        Embed(),
    )
    yield (
        {
            KEY_MEDIA_VOLUME_COUNT: None,
        },
        Embed(),
    )
    yield (
        {
            KEY_MEDIA_VOLUME_COUNT: 1,
        },
        Embed().add_field('Volumes', 1, inline = True),
    )
    yield (
        {
            KEY_MEDIA_CHAPTER_COUNT: None,
        },
        Embed(),
    )
    yield (
        {
            KEY_MEDIA_CHAPTER_COUNT: 1,
        },
        Embed().add_field('Chapters', 1, inline = True),
    )
    yield (
        {
            KEY_MEDIA_VOLUME_COUNT: 2,
            KEY_MEDIA_CHAPTER_COUNT: 3,
        },
        Embed().add_field(
            'Volumes', '2', inline = True,
        ).add_field(
            'Chapters', '3', inline = True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__add_manga_stat_fields(manga_data):
    """
    Tests whether ``add_manga_stat_fields`` works as intended.
    
    Parameters
    ----------
    manga_data : `dict<str, object>`
        Manga data.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed()
    add_manga_stat_fields(embed, manga_data)
    return embed
