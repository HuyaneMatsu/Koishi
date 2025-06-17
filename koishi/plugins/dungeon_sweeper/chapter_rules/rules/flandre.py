__all__ = ()

from hata import BUILTIN_EMOJIS, create_text_display

from ...constants import CHAPTER_RULES

from ..chapter_rule import ChapterRule
from ..constants import CHAPTER_RULE_ID_FLANDRE


EMOJI_SIGN_TARGET = BUILTIN_EMOJIS["x"]


def build_component(chapter, style):
    """
    Builds the flandre rules component.
    
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
    chapter_name = chapter.display_name
    chapter_emoji = style.emoji
    control_emoji_mapping = style.control_emoji_mapping
    tile_emoji_mapping = style.tile_emoji_mapping
    
    return create_text_display(
        f'### Chapter {chapter_name} {chapter_emoji}\n'
        f'\n'
        f'Your character is Scarlet Flandre (スカーレット フランドール Sukaaretto Furandooru), who want to put her '
        f'*bookshelves* on their desired place.\n'
        f'Flandre can destroy absolutely anything and everything, and she will get rid of the pillars for you.\n'
        f'{tile_emoji_mapping.character_east_on_floor}{tile_emoji_mapping.other_obstacle}{control_emoji_mapping.in_game_east}'
        f'{tile_emoji_mapping.character_east_on_floor}{tile_emoji_mapping.other_obstacle_destroyed}{control_emoji_mapping.in_game_east}'
        f'{tile_emoji_mapping.other_floor}{tile_emoji_mapping.character_east_on_obstacle_destroyed}\n'
        f'{tile_emoji_mapping.character_east_on_floor}{tile_emoji_mapping.other_box_on_floor}{tile_emoji_mapping.other_obstacle_destroyed}'
        f'{control_emoji_mapping.in_game_east}{tile_emoji_mapping.other_floor}{tile_emoji_mapping.character_east_on_floor}'
        f'{tile_emoji_mapping.other_box_on_obstacle_destroyed}'
    )


CHAPTER_RULE_FLANDRE = CHAPTER_RULES[CHAPTER_RULE_ID_FLANDRE] = ChapterRule(
    CHAPTER_RULE_ID_FLANDRE,
    build_component,
)
