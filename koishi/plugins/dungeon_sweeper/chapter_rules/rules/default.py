__all__ = ('CHAPTER_RULE_DEFAULT',)

from hata import BUILTIN_EMOJIS, create_text_display

from ...constants import CHAPTER_RULES

from ..chapter_rule import ChapterRule
from ..constants import CHAPTER_RULE_ID_DEFAULT


EMOJI_SIGN_TARGET = BUILTIN_EMOJIS["x"]


def build_component(chapter, style):
    """
    Builds the default rules component.
    
    Parameters
    ----------
    chapter : ``Chapter``
        The chapter to build rule component for.
    
    style : ``ChapterStyle``
        Chapter style to build the rule as.
    
    Returns
    -------
    component : ``Component``
    """
    chapter_emoji = style.emoji
    control_emoji_mapping = style.control_emoji_mapping
    tile_emoji_mapping = style.tile_emoji_mapping
    
    return create_text_display(
        f'### Rules of Dungeon sweeper\n'
        f'\n'
        f'Your quest is to help our cute Touhou characters to put their stuffs on places, where they supposed be. '
        f'These places are marked with an {EMOJI_SIGN_TARGET} on the floor. Because our characters are lazy, the '
        f'less steps required to sort their stuffs, makes them give you a better rating.\n'
        f'\n'
        f'You can move with the buttons under the embed, to activate your characters\' skill, or go back, reset the '
        f'map or cancel the game:\n'
        f'{control_emoji_mapping.in_game_north_west}{control_emoji_mapping.in_game_north}{control_emoji_mapping.in_game_north_east}{control_emoji_mapping.in_game_back}\n'
        f'{control_emoji_mapping.in_game_west}{chapter_emoji}{control_emoji_mapping.in_game_east}{control_emoji_mapping.in_game_restart}\n'
        f'{control_emoji_mapping.in_game_south_west}{control_emoji_mapping.in_game_south}{control_emoji_mapping.in_game_south_east}{control_emoji_mapping.in_game_return_to_menu}\n'
        f'\n'
        f'You can push boxes by moving towards them, but you cannot push more at the same time or push into the '
        f'wall:\n'
        f'{tile_emoji_mapping.character_east_on_floor}{tile_emoji_mapping.other_box_on_floor}{tile_emoji_mapping.other_floor}'
        f'{control_emoji_mapping.in_game_east}'
        f'{tile_emoji_mapping.other_floor}{tile_emoji_mapping.character_east_on_floor}{tile_emoji_mapping.other_box_on_floor}\n'
        f'\n'
        f'You can push the boxes into the holes to pass them, but be careful, you might lose too much boxes to finish'
        f'the stages!\n'
        f'{tile_emoji_mapping.character_east_on_floor}{tile_emoji_mapping.other_box_on_floor}{tile_emoji_mapping.other_hole}'
        f'{control_emoji_mapping.in_game_east}{tile_emoji_mapping.other_floor}{tile_emoji_mapping.character_east_on_floor}'
        f'{tile_emoji_mapping.other_box_on_hole_filled}{control_emoji_mapping.in_game_east}{tile_emoji_mapping.other_floor}{tile_emoji_mapping.other_floor}'
        f'{tile_emoji_mapping.character_east_on_hole_filled}\n'
        f'{tile_emoji_mapping.character_east_on_floor}{tile_emoji_mapping.other_box_on_floor}{tile_emoji_mapping.other_box_on_hole_filled}'
        f'{control_emoji_mapping.in_game_east}{tile_emoji_mapping.other_floor}{tile_emoji_mapping.character_east_on_floor}'
        f'{tile_emoji_mapping.other_hole_filled}\n'
        f'\n'
        f'If you get a box on the it\'s desired place it\'s color will change:\n'
        f'{tile_emoji_mapping.character_east_on_floor}{tile_emoji_mapping.other_box_on_floor}{tile_emoji_mapping.other_target_on_floor}'
        f'{control_emoji_mapping.in_game_east}{tile_emoji_mapping.other_floor}{tile_emoji_mapping.character_east_on_floor}'
        f'{tile_emoji_mapping.other_box_on_target}\n'
        f'\n'
        f'The game has 3 chapters. (*There might be more added.*) Each chapter introduces a different character to '
        f'play with.\n'
        f'\n'
        f'-# Game based on Sweeper of Suika.'
    )


CHAPTER_RULE_DEFAULT = CHAPTER_RULES[CHAPTER_RULE_ID_DEFAULT] = ChapterRule(
    CHAPTER_RULE_ID_DEFAULT,
    build_component,
)
