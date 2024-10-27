import vampytest
from hata import Emoji

from ..field_renderers import render_emoji_field_into


def _iter_options():
    emoji_id = 202410160001
    name = 'koishi'
    emoji = Emoji.precreate(emoji_id, name = name)
    
    yield False, None, False, 'Emoji', ('Emoji: null', True)
    yield True, None, False, 'Emoji', ('\nEmoji: null', True)
    
    yield (
        False, emoji, False, 'Emoji',
        (f'Emoji: {name!s} ({emoji_id!s})', True),
    )
    yield (
        True, emoji, False, 'Emoji',
        (f'\nEmoji: {name!s} ({emoji_id!s})', True),
    )
    yield False, None, True, 'Emoji', ('', False)
    yield True, None, True, 'Emoji', ('', True)
    yield (
        False, emoji, True, 'Emoji',
        (f'Emoji: {name!s} ({emoji_id!s})', True),
    )
    yield (
        True, emoji, True, 'Emoji',
        (f'\nEmoji: {name!s} ({emoji_id!s})', True),
    )
    
    # title
    yield (
        False, emoji, True, 'Mister',
        (f'Mister: {name!s} ({emoji_id!s})', True),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_emoji_field_into(field_added, emoji, optional, title):
    """
    Tests whether ``render_emoji_field_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether a field was already added.
    
    emoji : `None | Emoji`
        The emoji to render.
    
    title : `str`
        The title to use.
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    into, field_added = render_emoji_field_into(
        [], field_added, emoji, optional = optional, title = title
    ) 
    
    for element in into:
        vampytest.assert_instance(element, str)
    
    return ''.join(into), field_added
