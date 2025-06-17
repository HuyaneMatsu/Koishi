__all__ = ('Chapter',)

from scarletio import RichAttributeErrorBaseType, include

from ..chapter_styles import CHAPTER_STYLE_DEFAULT
from ..constants import CHAPTER_STYLES, CHAPTERS, SKILLS, STAGES
from ..skills import SKILL_DEFAULT

from .constants import (
    JSON_KEY_CHAPTER_DISPLAY_NAME, JSON_KEY_CHAPTER_FIRST_STAGE_ID, JSON_KEY_CHAPTER_ID,
    JSON_KEY_CHAPTER_NEXT_CHAPTER_ID, JSON_KEY_CHAPTER_PREVIOUS_CHAPTER_ID, JSON_KEY_CHAPTER_RULE_ID,
    JSON_KEY_CHAPTER_SKILL_ID, JSON_KEY_CHAPTER_STYLE_ID, JSON_KEY_CHAPTER_STAGES,
    JSON_KEY_CHAPTER_UNLOCK_PREREQUISITE_STAGE_ID
)
from .stage import Stage


CHAPTER_DEFAULT = include('CHAPTER_DEFAULT')
STAGE_DEFAULT = include('STAGE_DEFAULT')


class Chapter(RichAttributeErrorBaseType):
    """
    A chapter storing exact data about it's stages, skills and buttons.
    
    Attributes
    ----------
    display_name : `str`
        The chapter's display name.
    
    file_name : `None | str`
        The file's name where the chapter is loaded from.
    
    first_stage_id : `int`
        The first stage's identifier of the chapter.
    
    id : `int`
        The chapter's identifier.
    
    next_chapter_id : `int`
        The next chapter's identifier.
    
    previous_chapter_id : `int`
        The previous chapter's identifier.
    
    rule_id : `int`
        The chapter's rule's identifier.
    
    skill_id : `int`
        The chapter's skill identifier.
    
    stages : ``list<Stage>``
        The stages of the chapter.
    
    style_id : `int`
        The chapter's style's identifier.
    
    unlock_prerequisite_stage_id : `int`
        The prerequisite stage identifier to unlock this chapter.
    """
    __slots__ = (
        'display_name', 'file_name', 'first_stage_id', 'id', 'next_chapter_id', 'previous_chapter_id', 'rule_id',
        'skill_id', 'stages', 'style_id','unlock_prerequisite_stage_id'
    )
    
    def __new__(
        cls,
        
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
    ):
        """
        Creates a chapter from the given fields.
        
        Parameters
        ----------
        file_name : `None | str`
            The file's name where the chapter is loaded from.
        
        chapter_id : `int`
            The chapter's identifier.
        
        
        first_stage_id : `int`
            The first stage's identifier of the chapter.
        
        next_chapter_id : `int`
            The next chapter's identifier.
        
        previous_chapter_id : `int`
            The previous chapter's identifier.
        
        unlock_prerequisite_stage_id : `int`
            The prerequisite stage identifier to unlock this chapter.
        
        
        display_name : `str`
            The chapter's display name.
        
        rule_id : `int`
            The chapter's rule's identifier.
        
        skill_id : `int`
            The chapter's skill identifier.
        
        stages : ``list<Stage>``
            The stages of the chapter.
        
        style_id : `int`
            The chapter's style's identifier.
        """
        self = object.__new__(cls)
        
        self.file_name = file_name
        self.id = chapter_id
        
        self.first_stage_id = first_stage_id
        self.next_chapter_id = next_chapter_id
        self.previous_chapter_id = previous_chapter_id
        self.unlock_prerequisite_stage_id = unlock_prerequisite_stage_id
        
        self.display_name = display_name
        self.rule_id = rule_id
        self.skill_id = skill_id
        self.stages = stages
        self.style_id = style_id
        
        return self
    
    
    @classmethod
    def from_data(cls, file_name, chapter_data):
        """
        Creates a chapter from the given data.
        
        Parameters
        ----------
        file_name : `None | str`
            The file's name.
        
        chapter_data : `dict<str, object>`
            Chapter data.
        
        Returns
        -------
        self : `instance<cls>`
        """
        chapter_id = chapter_data[JSON_KEY_CHAPTER_ID]
        stages = [
            Stage.from_data(chapter_id, stage_data) for stage_data
            in chapter_data[JSON_KEY_CHAPTER_STAGES]
        ]
        
        self = object.__new__(cls)
        self.display_name = chapter_data[JSON_KEY_CHAPTER_DISPLAY_NAME]
        self.file_name = file_name
        self.first_stage_id = chapter_data[JSON_KEY_CHAPTER_FIRST_STAGE_ID]
        self.id = chapter_id
        self.next_chapter_id = chapter_data[JSON_KEY_CHAPTER_NEXT_CHAPTER_ID]
        self.previous_chapter_id = chapter_data[JSON_KEY_CHAPTER_PREVIOUS_CHAPTER_ID]
        self.rule_id = chapter_data[JSON_KEY_CHAPTER_RULE_ID]
        self.skill_id = chapter_data[JSON_KEY_CHAPTER_SKILL_ID]
        self.stages = stages
        self.style_id = chapter_data[JSON_KEY_CHAPTER_STYLE_ID]
        self.unlock_prerequisite_stage_id = chapter_data[JSON_KEY_CHAPTER_UNLOCK_PREREQUISITE_STAGE_ID]
        
        return self
    
    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # id
        repr_parts.append(' id = ')
        repr_parts.append(repr(self.id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def get_first_stage(self):
        """
        Returns the chapter's first stage.
        
        Returns
        -------
        stage : ``Stage``
        """
        return STAGES.get(self.first_stage_id, STAGE_DEFAULT)
    
    
    def get_unlock_prerequisite_stage(self):
        """
        Returns which stage is a prerequisite to unlock this chapter.
        
        Returns
        -------
        stage : ``None | Stage``
        """
        unlock_prerequisite_stage_id = self.unlock_prerequisite_stage_id
        if unlock_prerequisite_stage_id:
            return STAGES.get(unlock_prerequisite_stage_id, STAGE_DEFAULT)
    
    
    def get_previous_chapter(self):
        """
        Returns the previous chapter.
        
        Returns
        -------
        chapter : ``None | Chapter``
        """
        previous_chapter_id = self.previous_chapter_id
        if previous_chapter_id:
            return CHAPTERS.get(previous_chapter_id, CHAPTER_DEFAULT)
    
    
    def get_next_chapter(self):
        """
        Returns the next chapter.
        
        Returns
        -------
        chapter : ``None | Chapter``
        """
        next_chapter_id = self.next_chapter_id
        if next_chapter_id:
            return CHAPTERS.get(next_chapter_id, CHAPTER_DEFAULT)
    
    
    def get_skill(self):
        """
        Returns the skill of the chapter.
        
        Returns
        -------
        skill : ``Skill``
        """
        return SKILLS.get(self.skill_id, SKILL_DEFAULT)

    
    def get_style(self):
        """
        Returns the style of the chapter.
        
        Returns
        -------
        style : ``ChapterStyle``
        """
        return CHAPTER_STYLES.get(self.style_id, CHAPTER_STYLE_DEFAULT)
