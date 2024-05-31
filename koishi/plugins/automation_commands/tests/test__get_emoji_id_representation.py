import vampytest

from hata import BUILTIN_EMOJIS, Emoji

from ..constants import ENTITY_REPRESENTATION_DEFAULT
from ..representation_getters import get_emoji_id_representation


def _iter_options():
    emoji_id = 0
    yield emoji_id, [], ENTITY_REPRESENTATION_DEFAULT
    
    emoji_id = 202405300114
    yield emoji_id, [], f'<{emoji_id!s}>'
    
    emoji_id = 202405300115
    emoji = Emoji.precreate(emoji_id, name = 'pudding')
    yield emoji_id, [emoji], emoji.as_emoji

    emoji = BUILTIN_EMOJIS['heart']
    emoji_id = emoji.id
    yield emoji_id, [emoji], emoji.as_emoji


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_emoji_id_representation(emoji_id, extra):
    """
    Tests whether ``get_emoji_id_representation`` works as intended.
    
    Parameters
    ----------
    emoji_id : `int`
        Value to get representation for.
    extra : `list<object>`
        Entities to keep in the cache.
    
    Returns
    -------
    output : `str`
    """
    output = get_emoji_id_representation(emoji_id)
    vampytest.assert_instance(output, str)
    return output
