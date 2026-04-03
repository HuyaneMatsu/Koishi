import vampytest

from ...chapter_styles import CHAPTER_STYLE_DEFAULT, ChapterStyle
from ...constants import CHAPTER_STYLES, CHAPTERS, SKILLS, STAGES
from ...skills import SKILL_DEFAULT, Skill

from ..chapters import CHAPTER_DEFAULT, STAGE_DEFAULT
from ..chapter import Chapter
from ..constants import (
    JSON_KEY_CHAPTER_DISPLAY_NAME, JSON_KEY_CHAPTER_FIRST_STAGE_ID, JSON_KEY_CHAPTER_ID,
    JSON_KEY_CHAPTER_NEXT_CHAPTER_ID, JSON_KEY_CHAPTER_PREVIOUS_CHAPTER_ID, JSON_KEY_CHAPTER_RULE_ID,
    JSON_KEY_CHAPTER_SKILL_ID, JSON_KEY_CHAPTER_STYLE_ID, JSON_KEY_CHAPTER_STAGES,
    JSON_KEY_CHAPTER_UNLOCK_PREREQUISITE_STAGE_ID
)
from ..stage import Stage


def _assert_fields_set(chapter):
    """
    Asserts whether the chapter has all of its fields set.
    
    Parameters
    ----------
    chapter : ``Chapter``
        The chapter to test.
    """
    vampytest.assert_instance(chapter, Chapter)
    vampytest.assert_instance(chapter.display_name, str)
    vampytest.assert_instance(chapter.file_name, str, nullable = True)
    vampytest.assert_instance(chapter.first_stage_id, int)
    vampytest.assert_instance(chapter.id, int)
    vampytest.assert_instance(chapter.next_chapter_id, int)
    vampytest.assert_instance(chapter.previous_chapter_id, int)
    vampytest.assert_instance(chapter.rule_id, int)
    vampytest.assert_instance(chapter.skill_id, int)
    vampytest.assert_instance(chapter.stages, list)
    vampytest.assert_instance(chapter.style_id, int)
    vampytest.assert_instance(chapter.unlock_prerequisite_stage_id, int)


def test__Chapter__new():
    """
    Tests whether ``Chapter.__new__`` works as intended.
    """
    file_name = 'orin.json'
    chapter_id = 899
    
    first_stage_id = 898
    next_chapter_id = 897
    previous_chapter_id = 896
    unlock_prerequisite_stage_id = 895
    
    display_name = 'Orin'
    rule_id = 894
    skill_id = 893
    stages = []
    style_id = 892
    
    chapter = Chapter(
        file_name,
        chapter_id,
        
        first_stage_id,
        next_chapter_id,
        previous_chapter_id,
        unlock_prerequisite_stage_id,
        
        display_name,
        rule_id,
        skill_id,
        stages,
        style_id,
    )
    _assert_fields_set(chapter)
    
    vampytest.assert_eq(chapter.display_name, display_name)
    vampytest.assert_eq(chapter.id, chapter_id)
    
    vampytest.assert_eq(chapter.first_stage_id, first_stage_id)
    vampytest.assert_eq(chapter.next_chapter_id, next_chapter_id)
    vampytest.assert_eq(chapter.previous_chapter_id, previous_chapter_id)
    vampytest.assert_eq(chapter.unlock_prerequisite_stage_id, unlock_prerequisite_stage_id)
    
    vampytest.assert_eq(chapter.display_name, display_name)
    vampytest.assert_eq(chapter.rule_id, rule_id)
    vampytest.assert_eq(chapter.skill_id, skill_id)
    vampytest.assert_eq(chapter.stages, stages)
    vampytest.assert_eq(chapter.style_id, style_id)


def test__Chapter__from_data():
    """
    Tests whether ``Chapter.from_data`` works as intended.
    """
    file_name = 'orin.json'
    chapter_id = 899
    
    first_stage_id = 898
    next_chapter_id = 897
    previous_chapter_id = 896
    unlock_prerequisite_stage_id = 895
    
    display_name = 'Orin'
    rule_id = 894
    skill_id = 893
    stages = []
    style_id = 892
    
    data = {
        JSON_KEY_CHAPTER_ID : chapter_id,
        
        JSON_KEY_CHAPTER_FIRST_STAGE_ID : first_stage_id,
        JSON_KEY_CHAPTER_NEXT_CHAPTER_ID : next_chapter_id,
        JSON_KEY_CHAPTER_PREVIOUS_CHAPTER_ID : previous_chapter_id,
        JSON_KEY_CHAPTER_UNLOCK_PREREQUISITE_STAGE_ID : unlock_prerequisite_stage_id,
        
        JSON_KEY_CHAPTER_DISPLAY_NAME : display_name,
        JSON_KEY_CHAPTER_RULE_ID : rule_id,
        JSON_KEY_CHAPTER_SKILL_ID : skill_id,
        JSON_KEY_CHAPTER_STAGES : [],
        JSON_KEY_CHAPTER_STYLE_ID : style_id,
    }
    
    chapter = Chapter.from_data(
        file_name,
        data,
    )
    _assert_fields_set(chapter)
    
    vampytest.assert_eq(chapter.display_name, display_name)
    vampytest.assert_eq(chapter.id, chapter_id)
    
    vampytest.assert_eq(chapter.first_stage_id, first_stage_id)
    vampytest.assert_eq(chapter.next_chapter_id, next_chapter_id)
    vampytest.assert_eq(chapter.previous_chapter_id, previous_chapter_id)
    vampytest.assert_eq(chapter.unlock_prerequisite_stage_id, unlock_prerequisite_stage_id)
    
    vampytest.assert_eq(chapter.display_name, display_name)
    vampytest.assert_eq(chapter.rule_id, rule_id)
    vampytest.assert_eq(chapter.skill_id, skill_id)
    vampytest.assert_eq(chapter.stages, stages)
    vampytest.assert_eq(chapter.style_id, style_id)



def _iter_options__get_first_stage():
    for stage in STAGES.values():
        if stage is not STAGE_DEFAULT:
            break
    
    else:
        raise RuntimeError('Could not find non-default stage.')
    
    yield stage.id, stage
    yield 997, STAGE_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__get_first_stage()).returning_last())
def test__Chapter__get_first_stage(first_stage_id):
    """
    Tests whether ``Chapter.get_first_stage`` works as intended.
    
    Parameters
    ----------
    first_stage_id : `int`
        Stage identifier.
    
    Returns
    -------
    output : ``Stage``
    """
    file_name = 'orin.json'
    chapter_id = 899
    
    next_chapter_id = 897
    previous_chapter_id = 896
    unlock_prerequisite_stage_id = 895
    
    display_name = 'Orin'
    rule_id = 894
    skill_id = 893
    stages = []
    style_id = 892
    
    chapter = Chapter(
        file_name,
        chapter_id,
        
        first_stage_id,
        next_chapter_id,
        previous_chapter_id,
        unlock_prerequisite_stage_id,
        
        display_name,
        rule_id,
        skill_id,
        stages,
        style_id,
    )
    
    output = chapter.get_first_stage()
    vampytest.assert_instance(output, Stage)
    return output


def _iter_options__get_unlock_prerequisite_stage():
    for stage in STAGES.values():
        if stage is not STAGE_DEFAULT:
            break
    
    else:
        raise RuntimeError('Could not find non-default stage.')
    
    yield stage.id, stage
    yield 997, STAGE_DEFAULT
    yield 0, None


@vampytest._(vampytest.call_from(_iter_options__get_unlock_prerequisite_stage()).returning_last())
def test__Chapter__get_unlock_prerequisite_stage(unlock_prerequisite_stage_id):
    """
    Tests whether ``Chapter.get_unlock_prerequisite_stage`` works as intended.
    
    Parameters
    ----------
    unlock_prerequisite_stage_id : `int`
        Stage identifier.
    
    Returns
    -------
    output : ``Stage``
    """
    file_name = 'orin.json'
    chapter_id = 899
    
    first_stage_id = 898
    next_chapter_id = 897
    previous_chapter_id = 896
    
    display_name = 'Orin'
    rule_id = 894
    skill_id = 893
    stages = []
    style_id = 892
    
    chapter = Chapter(
        file_name,
        chapter_id,
        
        first_stage_id,
        next_chapter_id,
        previous_chapter_id,
        unlock_prerequisite_stage_id,
        
        display_name,
        rule_id,
        skill_id,
        stages,
        style_id,
    )
    
    output = chapter.get_unlock_prerequisite_stage()
    vampytest.assert_instance(output, Stage, nullable = True)
    return output


def _iter_options__get_previous_chapter():
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT:
            break
    
    else:
        raise RuntimeError('Could not find non-default chapter.')
    
    yield chapter.id, chapter
    yield 896, CHAPTER_DEFAULT
    yield 0, None


@vampytest._(vampytest.call_from(_iter_options__get_previous_chapter()).returning_last())
def test__Chapter__get_previous_chapter(previous_chapter_id):
    """
    Tests whether ``Chapter.get_previous_chapter`` works as intended.
    
    Parameters
    ----------
    previous_chapter_id : `int`
        Chapter identifier.
    
    Returns
    -------
    output : ``None | Chapter``
    """
    file_name = 'orin.json'
    chapter_id = 899
    
    first_stage_id = 898
    next_chapter_id = 897
    unlock_prerequisite_stage_id = 895
    
    display_name = 'Orin'
    rule_id = 894
    skill_id = 893
    stages = []
    style_id = 892
    
    chapter = Chapter(
        file_name,
        chapter_id,
        
        first_stage_id,
        next_chapter_id,
        previous_chapter_id,
        unlock_prerequisite_stage_id,
        
        display_name,
        rule_id,
        skill_id,
        stages,
        style_id,
    )
    
    output = chapter.get_previous_chapter()
    vampytest.assert_instance(output, Chapter, nullable = True)
    return output


def _iter_options__get_next_chapter():
    for chapter in CHAPTERS.values():
        if chapter is not CHAPTER_DEFAULT:
            break
    
    else:
        raise RuntimeError('Could not find non-default chapter.')
    
    yield chapter.id, chapter
    yield 895, CHAPTER_DEFAULT
    yield 0, None


@vampytest._(vampytest.call_from(_iter_options__get_next_chapter()).returning_last())
def test__Chapter__get_next_chapter(next_chapter_id):
    """
    Tests whether ``Chapter.get_next_chapter`` works as intended.
    
    Parameters
    ----------
    next_chapter_id : `int`
        Chapter identifier.
    
    Returns
    -------
    output : ``None | Chapter``
    """
    file_name = 'orin.json'
    chapter_id = 899
    
    first_stage_id = 898
    previous_chapter_id = 896
    unlock_prerequisite_stage_id = 895
    
    display_name = 'Orin'
    rule_id = 894
    skill_id = 893
    stages = []
    style_id = 892
    
    chapter = Chapter(
        file_name,
        chapter_id,
        
        first_stage_id,
        next_chapter_id,
        previous_chapter_id,
        unlock_prerequisite_stage_id,
        
        display_name,
        rule_id,
        skill_id,
        stages,
        style_id,
    )
    
    output = chapter.get_next_chapter()
    vampytest.assert_instance(output, Chapter, nullable = True)
    return output


def _iter_options__get_skill():
    for skill in SKILLS.values():
        if skill is not SKILL_DEFAULT:
            break
    
    else:
        raise RuntimeError('Could not find non-default skill.')
    
    yield skill.id, skill
    yield 893, SKILL_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__get_skill()).returning_last())
def test__Chapter__get_skill(skill_id):
    """
    Tests whether ``Chapter.get_skill`` works as intended.
    
    Parameters
    ----------
    skill_id : `int`
        Skill identifier.
    
    Returns
    -------
    output : ``Skill``
    """
    file_name = 'orin.json'
    chapter_id = 899
    
    first_stage_id = 898
    next_chapter_id = 895
    previous_chapter_id = 896
    unlock_prerequisite_stage_id = 895
    
    display_name = 'Orin'
    rule_id = 894
    stages = []
    style_id = 892
    
    chapter = Chapter(
        file_name,
        chapter_id,
        
        first_stage_id,
        next_chapter_id,
        previous_chapter_id,
        unlock_prerequisite_stage_id,
        
        display_name,
        rule_id,
        skill_id,
        stages,
        style_id,
    )
    
    output = chapter.get_skill()
    vampytest.assert_instance(output, Skill)
    return output


def _iter_options__get_style():
    for style in CHAPTER_STYLES.values():
        if style is not SKILL_DEFAULT:
            break
    
    else:
        raise RuntimeError('Could not find non-default skill.')
    
    yield style.id, style
    yield 895, CHAPTER_STYLE_DEFAULT


@vampytest._(vampytest.call_from(_iter_options__get_style()).returning_last())
def test__Chapter__get_style(style_id):
    """
    Tests whether ``Chapter.get_style`` works as intended.
    
    Parameters
    ----------
    style_id : `int`
        Style identifier.
    
    Returns
    -------
    output : ``ChapterStyle``
    """
    file_name = 'orin.json'
    chapter_id = 899
    
    first_stage_id = 898
    next_chapter_id = 895
    previous_chapter_id = 896
    unlock_prerequisite_stage_id = 895
    
    display_name = 'Orin'
    rule_id = 894
    skill_id = 893
    stages = []
    
    chapter = Chapter(
        file_name,
        chapter_id,
        
        first_stage_id,
        next_chapter_id,
        previous_chapter_id,
        unlock_prerequisite_stage_id,
        
        display_name,
        rule_id,
        skill_id,
        stages,
        style_id,
    )
    
    output = chapter.get_style()
    vampytest.assert_instance(output, ChapterStyle)
    return output
