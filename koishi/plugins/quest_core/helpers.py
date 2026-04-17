__all__ = ('get_quest_template_nullable',)

from .constants import QUEST_TEMPLATES


def get_quest_template_nullable(quest_template_id):
    """
    Returns the quest template with the given identifier.
    
    Parameters
    ----------
    quest_template_id : `int`
        The quest template's identifier.
    
    Returns
    -------
    quest_template : ``None | QuestTemplate``
    """
    return QUEST_TEMPLATES.get(quest_template_id, None)
