import vampytest
from hata import EMOJIS, Emoji
 
from ..chapter_style import ChapterStyle
from ..control_emoji_mapping import ControlEmojiMapping
from ..styles import CONTROL_EMOJI_MAPPING_DEFAULT, TILE_EMOJI_MAPPING_DEFAULT
from ..tile_emoji_mapping import TileEmojiMapping


def _assert_fields_set(chapter_style):
    """
    Asserts whether the given chapter style has all of its fields set.
    
    Parameters
    ----------
    chapter_style : ``ChapterStyle``
        The instance to check.
    """
    vampytest.assert_instance(chapter_style, ChapterStyle)
    vampytest.assert_instance(chapter_style.control_emoji_mapping, ControlEmojiMapping)
    vampytest.assert_instance(chapter_style.emoji, Emoji)
    vampytest.assert_instance(chapter_style.id, int)
    vampytest.assert_instance(chapter_style.tile_emoji_mapping, TileEmojiMapping)
    vampytest.assert_instance(chapter_style.tile_resolution_table, dict)


def test__ChapterStyle__new():
    """
    Tests whether ``ChapterStyle.__new__`` works as intended.
    """
    style_id = 9999
    emoji = EMOJIS[1]
    control_emoji_mapping = CONTROL_EMOJI_MAPPING_DEFAULT
    tile_emoji_mapping = TILE_EMOJI_MAPPING_DEFAULT
    
    chapter_style = ChapterStyle(
        style_id,
        emoji,
        control_emoji_mapping,
        tile_emoji_mapping
    )
    _assert_fields_set(chapter_style)
    
    vampytest.assert_eq(chapter_style.control_emoji_mapping, control_emoji_mapping)
    vampytest.assert_is(chapter_style.emoji, emoji)
    vampytest.assert_eq(chapter_style.id, style_id)
    vampytest.assert_eq(chapter_style.tile_emoji_mapping, tile_emoji_mapping)


def test__ChapterStyle__repr():
    """
    Tests whether ``ChapterStyle.__repr__`` works as intended.
    """
    style_id = 9999
    emoji = EMOJIS[1]
    control_emoji_mapping = CONTROL_EMOJI_MAPPING_DEFAULT
    tile_emoji_mapping = TILE_EMOJI_MAPPING_DEFAULT
    
    chapter_style = ChapterStyle(
        style_id,
        emoji,
        control_emoji_mapping,
        tile_emoji_mapping
    )
    
    output = repr(chapter_style)
    vampytest.assert_instance(output, str)
