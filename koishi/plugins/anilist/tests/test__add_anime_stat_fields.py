import vampytest
from hata import Embed

from ..embed_building_media import add_anime_stat_fields
from ..keys import KEY_MEDIA_EPISODE_COUNT, KEY_MEDIA_EPISODE_LENGTH


def _iter_options():
    yield (
        {},
        Embed(),
    )
    yield (
        {
            KEY_MEDIA_EPISODE_COUNT: None,
        },
        Embed(),
    )
    yield (
        {
            KEY_MEDIA_EPISODE_COUNT: 1,
        },
        Embed(),
    )
    yield (
        {
            KEY_MEDIA_EPISODE_COUNT: 2,
        },
        Embed().add_field('Episodes', '2', inline = True),
    )
    yield (
        {
            KEY_MEDIA_EPISODE_LENGTH: 12,
        },
        Embed().add_field('Length', '12 minute', inline = True),
    )
    yield (
        {
            KEY_MEDIA_EPISODE_COUNT: 1,
            KEY_MEDIA_EPISODE_LENGTH: 12,
        },
        Embed().add_field('Length', '12 minute', inline = True),
    )
    yield (
        {
            KEY_MEDIA_EPISODE_COUNT: 2,
            KEY_MEDIA_EPISODE_LENGTH: 12,
        },
        Embed().add_field(
            'Episodes', '2', inline = True,
        ).add_field(
            'Episode length', '12 minute', inline = True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__add_anime_stat_fields(anime_data):
    """
    Tests whether ``add_anime_stat_fields`` works as intended.
    
    Parameters
    ----------
    anime_data : `dict<str, object>`
        Anime data.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed()
    add_anime_stat_fields(embed, anime_data)
    return embed
