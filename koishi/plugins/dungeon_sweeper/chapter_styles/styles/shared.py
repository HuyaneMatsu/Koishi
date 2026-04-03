__all__ = ('CONTROL_EMOJI_MAPPING_DEFAULT',)

from hata import BUILTIN_EMOJIS, Emoji

from ..control_emoji_mapping import ControlEmojiMapping


EMOJI_NOTHING = Emoji.precreate(568838460434284574, name = '0Q')

EMOJI_WALL = EMOJI_NOTHING
EMOJI_WALL_EAST = Emoji.precreate(568838488464687169, name = '0P')
EMOJI_WALL_SOUTH =  Emoji.precreate(568838546853462035, name = '0N')
EMOJI_WALL_WEST = Emoji.precreate(568838580278132746, name = '0K')
EMOJI_WALL_NORTH_EAST_SOUTH_WEST = Emoji.precreate(578678249518006272, name = '0X')
EMOJI_WALL_EAST_SOUTH = Emoji.precreate(568838557318250499, name = '0M')
EMOJI_WALL_SOUTH_WEST = Emoji.precreate(568838569087598627, name = '0L')
EMOJI_WALL_NORTH_EAST = Emoji.precreate(574312331849498624, name = '01')
EMOJI_WALL_NORTH_WEST = Emoji.precreate(574312332453216256, name = '00')
EMOJI_WALL_NORTH_EAST_SOUTH = Emoji.precreate(578648597621506048, name = '0R')
EMOJI_WALL_NORTH_SOUTH_WEST = Emoji.precreate(578648597546139652, name = '0S')
EMOJI_WALL_NORTH_SOUTH = Emoji.precreate(578654051848421406, name = '0T')
EMOJI_WALL_EAST_WEST = Emoji.precreate(578674409968238613, name = '0U')
EMOJI_WALL_NORTH_EAST_WEST = Emoji.precreate(578676096829227027, name = '0V')
EMOJI_WALL_EAST_SOUTH_WEST = Emoji.precreate(578676650389274646, name = '0W')


CONTROL_EMOJI_MAPPING_DEFAULT = ControlEmojiMapping(
    end_screen_next_stage = BUILTIN_EMOJIS['arrow_right'],
    end_screen_return_to_menu = BUILTIN_EMOJIS['x'],
    end_screen_restart_stage = BUILTIN_EMOJIS['arrows_counterclockwise'],
    
    in_game_back = BUILTIN_EMOJIS['leftwards_arrow_with_hook'],
    in_game_east = BUILTIN_EMOJIS['arrow_right'],
    in_game_north = BUILTIN_EMOJIS['arrow_up'],
    in_game_north_east = BUILTIN_EMOJIS['arrow_upper_right'],
    in_game_north_west = BUILTIN_EMOJIS['arrow_upper_left'],
    in_game_restart = BUILTIN_EMOJIS['arrows_counterclockwise'],
    in_game_return_to_menu = BUILTIN_EMOJIS['x'],
    in_game_south = BUILTIN_EMOJIS['arrow_down'],
    in_game_south_east = BUILTIN_EMOJIS['arrow_lower_right'],
    in_game_south_west = BUILTIN_EMOJIS['arrow_lower_left'],
    in_game_west = BUILTIN_EMOJIS['arrow_left'],

    in_menu_chapter_next = BUILTIN_EMOJIS['arrow_forward'],
    in_menu_chapter_previous = BUILTIN_EMOJIS['arrow_backward'],
    in_menu_close = BUILTIN_EMOJIS['x'],
    in_menu_select_stage = BUILTIN_EMOJIS['ok'],
    in_menu_stage_next = BUILTIN_EMOJIS['arrow_up_small'],
    in_menu_stage_next_multi = BUILTIN_EMOJIS['arrow_double_up'],
    in_menu_stage_previous = BUILTIN_EMOJIS['arrow_down_small'],
    in_menu_stage_previous_multi = BUILTIN_EMOJIS['arrow_double_down'],
    
    nothing = EMOJI_NOTHING,
)
