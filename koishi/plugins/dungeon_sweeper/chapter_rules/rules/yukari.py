__all__ = ()

from hata import BUILTIN_EMOJIS, create_text_display

from ...constants import CHAPTER_RULES

from ..chapter_rule import ChapterRule
from ..constants import CHAPTER_RULE_ID_YUKARI


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
    chapter_name = chapter.display_name
    chapter_emoji = style.emoji
    control_emoji_mapping = style.control_emoji_mapping
    tile_emoji_mapping = style.tile_emoji_mapping
    
    return create_text_display(
        f'### Chapter {chapter_name} {chapter_emoji}\n'
        f'\n'
        f'Your character is Yakumo Yukari (八雲 紫). Her beddings needs some replacing at her home.\n'
        f'Yukari can create gaps and travel trough them. She will open gap to the closest place straightforward, '
        f'which is separated by a bedding or with wall from her.\n'
        f'{tile_emoji_mapping.character_east_on_floor}{tile_emoji_mapping.wall_north}{tile_emoji_mapping.wall_north}'
        f'{tile_emoji_mapping.other_floor}{control_emoji_mapping.in_game_east}{tile_emoji_mapping.other_floor}{tile_emoji_mapping.wall_north}'
        f'{tile_emoji_mapping.wall_north}{tile_emoji_mapping.character_east_on_floor}\n'
        f'{tile_emoji_mapping.character_east_on_floor}{tile_emoji_mapping.other_box_on_floor}{tile_emoji_mapping.other_box_on_floor}'
        f'{tile_emoji_mapping.other_floor}{control_emoji_mapping.in_game_east}{tile_emoji_mapping.other_floor}{tile_emoji_mapping.other_box_on_floor}'
        f'{tile_emoji_mapping.other_box_on_floor}{tile_emoji_mapping.character_east_on_floor}'
    )


CHAPTER_RULE_YUKARI = CHAPTER_RULES[CHAPTER_RULE_ID_YUKARI] = ChapterRule(
    CHAPTER_RULE_ID_YUKARI,
    build_component,
)
