import vampytest

from ..constants import DESCRIPTION_LENGTH_MAX
from ..parsers_description import parse_description_media
from ..keys import KEY_MEDIA_DESCRIPTION, KEY_MEDIA_GENRES


def _iter_options():
    yield (
        {},
        None,
    )
    yield (
        {
            KEY_MEDIA_DESCRIPTION: 'She likes Koishi',
            KEY_MEDIA_GENRES: ['satori', 'orin'],
        },
        (
            '**Genres:** satori, orin\n'
            '\n'
            'She likes Koishi'
        ),
    )
    yield (
        {
            KEY_MEDIA_DESCRIPTION: 'a' * (DESCRIPTION_LENGTH_MAX + 1),
        },
        'a' * (DESCRIPTION_LENGTH_MAX - 4) + ' ...',
    )

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_description_media(media_data):
    """
    Tests whether ``parse_description_media`` works as intended.
    
    Parameters
    ----------
    media_data : `dict<str, object>`
        Media data to pass to the function.
    
    Returns
    -------
    description : `str`
        The parsed description.
    """
    return parse_description_media(media_data)
