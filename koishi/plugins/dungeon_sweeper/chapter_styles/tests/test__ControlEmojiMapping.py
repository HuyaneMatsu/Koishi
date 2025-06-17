import vampytest
from hata import EMOJIS, Emoji

from ..control_emoji_mapping import ControlEmojiMapping


def _assert_fields_set(control_emoji_mapping):
    """
    Checks whether the given control emoji mapping has all of its fields set.
    
    Parameters
    ----------
    control_emoji_mapping : ``ControlEmojiMapping``
        The instance to test.
    """
    vampytest.assert_instance(control_emoji_mapping, ControlEmojiMapping)
    
    vampytest.assert_instance(control_emoji_mapping.end_screen_next_stage, Emoji)
    vampytest.assert_instance(control_emoji_mapping.end_screen_return_to_menu, Emoji)
    vampytest.assert_instance(control_emoji_mapping.end_screen_restart_stage, Emoji)
    
    vampytest.assert_instance(control_emoji_mapping.in_game_back, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_game_east, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_game_north, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_game_north_east, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_game_north_west, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_game_restart, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_game_return_to_menu, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_game_south, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_game_south_east, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_game_south_west, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_game_west, Emoji)
    
    vampytest.assert_instance(control_emoji_mapping.in_menu_chapter_next, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_menu_chapter_previous, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_menu_close, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_menu_select_stage, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_menu_stage_next, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_menu_stage_next_multi, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_menu_stage_previous, Emoji)
    vampytest.assert_instance(control_emoji_mapping.in_menu_stage_previous_multi, Emoji)
    
    vampytest.assert_instance(control_emoji_mapping.nothing, Emoji)


def test__control_emoji_mapping__new():
    """
    Tests whether ``ControlEmojiMapping.__new__`` works as intended.
    """
    end_screen_next_stage = EMOJIS[1]
    end_screen_return_to_menu = EMOJIS[2]
    end_screen_restart_stage = EMOJIS[3]
    
    in_game_back = EMOJIS[3]
    in_game_east = EMOJIS[4]
    in_game_north = EMOJIS[5]
    in_game_north_east = EMOJIS[6]
    in_game_north_west = EMOJIS[7]
    in_game_restart = EMOJIS[8]
    in_game_return_to_menu = EMOJIS[9]
    in_game_south = EMOJIS[10]
    in_game_south_east = EMOJIS[11]
    in_game_south_west = EMOJIS[12]
    in_game_west = EMOJIS[13]
    
    in_menu_chapter_next = EMOJIS[14]
    in_menu_chapter_previous = EMOJIS[15]
    in_menu_close = EMOJIS[16]
    in_menu_select_stage = EMOJIS[17]
    in_menu_stage_next = EMOJIS[18]
    in_menu_stage_next_multi = EMOJIS[19]
    in_menu_stage_previous = EMOJIS[20]
    in_menu_stage_previous_multi = EMOJIS[21]
    
    nothing = EMOJIS[22]
    
    control_emoji_mapping = ControlEmojiMapping(
        end_screen_next_stage = end_screen_next_stage,
        end_screen_return_to_menu = end_screen_return_to_menu,
        end_screen_restart_stage = end_screen_restart_stage,
        
        in_game_back = in_game_back,
        in_game_east = in_game_east,
        in_game_north = in_game_north,
        in_game_north_east = in_game_north_east,
        in_game_north_west = in_game_north_west,
        in_game_restart = in_game_restart,
        in_game_return_to_menu = in_game_return_to_menu,
        in_game_south = in_game_south,
        in_game_south_east = in_game_south_east,
        in_game_south_west = in_game_south_west,
        in_game_west = in_game_west,
        
        in_menu_chapter_next = in_menu_chapter_next,
        in_menu_chapter_previous = in_menu_chapter_previous,
        in_menu_close = in_menu_close,
        in_menu_select_stage = in_menu_select_stage,
        in_menu_stage_next = in_menu_stage_next,
        in_menu_stage_next_multi = in_menu_stage_next_multi,
        in_menu_stage_previous = in_menu_stage_previous,
        in_menu_stage_previous_multi = in_menu_stage_previous_multi,
        
        nothing = nothing,
    )
    _assert_fields_set(control_emoji_mapping)

    vampytest.assert_is(control_emoji_mapping.end_screen_next_stage, end_screen_next_stage)
    vampytest.assert_is(control_emoji_mapping.end_screen_return_to_menu, end_screen_return_to_menu)
    vampytest.assert_is(control_emoji_mapping.end_screen_restart_stage, end_screen_restart_stage)
    
    vampytest.assert_is(control_emoji_mapping.in_game_back, in_game_back)
    vampytest.assert_is(control_emoji_mapping.in_game_east, in_game_east)
    vampytest.assert_is(control_emoji_mapping.in_game_north, in_game_north)
    vampytest.assert_is(control_emoji_mapping.in_game_north_east, in_game_north_east)
    vampytest.assert_is(control_emoji_mapping.in_game_north_west, in_game_north_west)
    vampytest.assert_is(control_emoji_mapping.in_game_restart, in_game_restart)
    vampytest.assert_is(control_emoji_mapping.in_game_return_to_menu, in_game_return_to_menu)
    vampytest.assert_is(control_emoji_mapping.in_game_south, in_game_south)
    vampytest.assert_is(control_emoji_mapping.in_game_south_east, in_game_south_east)
    vampytest.assert_is(control_emoji_mapping.in_game_south_west, in_game_south_west)
    vampytest.assert_is(control_emoji_mapping.in_game_west, in_game_west)
    
    vampytest.assert_is(control_emoji_mapping.in_menu_chapter_next, in_menu_chapter_next)
    vampytest.assert_is(control_emoji_mapping.in_menu_chapter_previous, in_menu_chapter_previous)
    vampytest.assert_is(control_emoji_mapping.in_menu_close, in_menu_close)
    vampytest.assert_is(control_emoji_mapping.in_menu_select_stage, in_menu_select_stage)
    vampytest.assert_is(control_emoji_mapping.in_menu_stage_next, in_menu_stage_next)
    vampytest.assert_is(control_emoji_mapping.in_menu_stage_next_multi, in_menu_stage_next_multi)
    vampytest.assert_is(control_emoji_mapping.in_menu_stage_previous, in_menu_stage_previous)
    vampytest.assert_is(control_emoji_mapping.in_menu_stage_previous_multi, in_menu_stage_previous_multi)
    
    vampytest.assert_is(control_emoji_mapping.nothing, nothing)


def test__control_emoji_mapping__repr():
    """
    Tests whether ``ControlEmojiMapping.__repr__`` works as intended.
    """
    end_screen_next_stage = EMOJIS[1]
    end_screen_return_to_menu = EMOJIS[2]
    end_screen_restart_stage = EMOJIS[3]
    
    in_game_back = EMOJIS[3]
    in_game_east = EMOJIS[4]
    in_game_north = EMOJIS[5]
    in_game_north_east = EMOJIS[6]
    in_game_north_west = EMOJIS[7]
    in_game_restart = EMOJIS[8]
    in_game_return_to_menu = EMOJIS[9]
    in_game_south = EMOJIS[10]
    in_game_south_east = EMOJIS[11]
    in_game_south_west = EMOJIS[12]
    in_game_west = EMOJIS[13]
    
    in_menu_chapter_next = EMOJIS[14]
    in_menu_chapter_previous = EMOJIS[15]
    in_menu_close = EMOJIS[16]
    in_menu_select_stage = EMOJIS[17]
    in_menu_stage_next = EMOJIS[18]
    in_menu_stage_next_multi = EMOJIS[19]
    in_menu_stage_previous = EMOJIS[20]
    in_menu_stage_previous_multi = EMOJIS[21]
    
    nothing = EMOJIS[22]
    
    control_emoji_mapping = ControlEmojiMapping(
        end_screen_next_stage = end_screen_next_stage,
        end_screen_return_to_menu = end_screen_return_to_menu,
        end_screen_restart_stage = end_screen_restart_stage,
        
        in_game_back = in_game_back,
        in_game_east = in_game_east,
        in_game_north = in_game_north,
        in_game_north_east = in_game_north_east,
        in_game_north_west = in_game_north_west,
        in_game_restart = in_game_restart,
        in_game_return_to_menu = in_game_return_to_menu,
        in_game_south = in_game_south,
        in_game_south_east = in_game_south_east,
        in_game_south_west = in_game_south_west,
        in_game_west = in_game_west,
        
        in_menu_chapter_next = in_menu_chapter_next,
        in_menu_chapter_previous = in_menu_chapter_previous,
        in_menu_close = in_menu_close,
        in_menu_select_stage = in_menu_select_stage,
        in_menu_stage_next = in_menu_stage_next,
        in_menu_stage_next_multi = in_menu_stage_next_multi,
        in_menu_stage_previous = in_menu_stage_previous,
        in_menu_stage_previous_multi = in_menu_stage_previous_multi,
        
        nothing = nothing,
    )
    
    output = repr(control_emoji_mapping)
    vampytest.assert_instance(output, str)
