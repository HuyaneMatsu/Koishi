import vampytest
from hata import Component, ComponentType

from ..chapters import CHAPTER_DEFAULT
from ..component_building import build_component_in_menu_description
from ..constants import CHAPTERS, DIFFICULTY_NAMES, DIFFICULTY_NAME_DEFAULT, STAGES


def test__build_component_in_menu_description__none():
    """
    Tests whether ``build_component_in_menu_description`` works as intended.
    
    Case: none
    """
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT and chapter.unlock_prerequisite_stage_id != 0:
            break
    
    else:
        raise RuntimeError('Could not detect sufficient chapter.')
    
    selectable_stages = None
    stage = chapter.get_first_stage()
    assert stage is not None
    unlock_prerequisite_stage = chapter.get_unlock_prerequisite_stage()
    assert unlock_prerequisite_stage is not None
    unlock_chapter = unlock_prerequisite_stage.get_chapter()
    
    output = build_component_in_menu_description(chapter, selectable_stages)
    vampytest.assert_instance(output, Component)
    vampytest.assert_is(output.type, ComponentType.text_display)
    
    vampytest.assert_eq(
        output.content,
        f'**You must finish chapter {unlock_chapter.display_name} '
        f'{DIFFICULTY_NAMES.get(unlock_prerequisite_stage.difficulty_id, DIFFICULTY_NAME_DEFAULT)} '
        f'{unlock_prerequisite_stage.in_difficulty_index + 1} first.**'
    )


def test__build_component_in_menu_description():
    """
    Tests whether ``build_component_in_menu_description`` works as intended.
    """
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT:
            break
    
    else:
        raise RuntimeError('Could not detect sufficient chapter.')
    
    stage_0 = STAGES[chapter.first_stage_id]
    stage_1 = STAGES[stage_0.next_stage_id]
    stage_2 = STAGES[stage_1.next_stage_id]
    stage_3 = STAGES[stage_2.next_stage_id]
    stage_4 = STAGES[stage_3.next_stage_id]
    stage_5 = STAGES[stage_4.next_stage_id]
    stage_6 = STAGES[stage_5.next_stage_id]
    stage_7 = STAGES[stage_6.next_stage_id]
    
    selectable_stages = [
        (stage_7, -1, False),
        (stage_6, 56, False),
        (stage_5, 55, False),
        (stage_4, 54, True),
        (stage_3, 53, False),
        (stage_2, 52, False),
        (stage_1, 51, False),
    ]
    
    output = build_component_in_menu_description(chapter, selectable_stages)
    vampytest.assert_instance(output, Component)
    vampytest.assert_is(output.type, ComponentType.text_display)
    
    vampytest.assert_eq(
        output.content,
        (
            f'**Easy level 5**\n'
            f'No results recorded yet!\n'
            f'\n'
            f'**Easy level 4**\n'
            f'rating : E; steps : 56\n'
            f'\n'
            f'**Easy level 3**\n'
            f'rating : E; steps : 55\n'
            f'\n'
            f'\\> **Easy level 2** \\<\n'
            f'\\> rating : E; steps : 54 \\<\n'
            f'\n'
            f'**Easy level 1**\n'
            f'rating : E; steps : 53\n'
            f'\n'
            f'**Tutorial level 3**\n'
            f'rating : E; steps : 52\n'
            f'\n'
            f'**Tutorial level 2**\n'
            f'rating : E; steps : 51'
        ),
    )
