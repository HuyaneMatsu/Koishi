__all__ = ()

from hata import BUILTIN_EMOJIS, create_text_display

from ...constants import CHAPTER_RULES

from ..chapter_rule import ChapterRule
from ..constants import CHAPTER_RULE_ID_REIMU


EMOJI_SIGN_TARGET = BUILTIN_EMOJIS["x"]


def build_component(chapter, style):
    """
    Builds the reimu rules component.
    
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
        f'Your character is Hakurei Reimu (博麗 霊夢), who needs some help at her basement to sort her *boxes* out.\n'
        f'Reimu can jump over a box or hole.\n'
        f'{tile_emoji_mapping.character_east_on_floor}{tile_emoji_mapping.other_box_on_floor}{tile_emoji_mapping.other_floor}'
        f'{control_emoji_mapping.in_game_east}{tile_emoji_mapping.other_floor}{tile_emoji_mapping.other_box_on_floor}'
        f'{tile_emoji_mapping.character_east_on_floor}\n'
        f'{tile_emoji_mapping.character_east_on_floor:}{tile_emoji_mapping.other_hole}{tile_emoji_mapping.other_floor}'
        f'{control_emoji_mapping.in_game_east}{tile_emoji_mapping.other_floor}{tile_emoji_mapping.other_hole}'
        f'{tile_emoji_mapping.character_east_on_floor}'
    )


CHAPTER_RULE_REIMU = CHAPTER_RULES[CHAPTER_RULE_ID_REIMU] = ChapterRule(
    CHAPTER_RULE_ID_REIMU,
    build_component,
)
