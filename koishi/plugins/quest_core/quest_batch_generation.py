__all__ = ('create_quest_batch',)

from random import Random
from math import floor

from .constants import QUEST_TEMPLATES
from .helpers import get_quest_template_nullable
from .quest import Quest
from .quest_batch import QuestBatch
from .quest_reward_types import QUEST_REWARD_TYPE_CREDIBILITY


def create_quest_from_template(random_number_generator, quest_template):
    """
    Creates a quest from the template.
    
    Parameters
    ----------
    random_number_generator : `random.Random`
        Random value generator.
    
    quest_template : ``QuestTemplate``
        Quest template to use.
    
    Returns
    -------
    quest : ``Quest``
    """
    accumulated_diversion = 1.0
    
    # Generate requirements
    requirement_generators = quest_template.requirements
    if (requirement_generators is None):
        requirement_instantiables = None
    else:
        requirement_instantiables = []
        
        for requirement_generator in requirement_generators:
            requirement_instantiable, diversion = requirement_generator.generate(
                random_number_generator
            )
            requirement_instantiables.append(requirement_instantiable)
            accumulated_diversion *= diversion
        
        requirement_instantiables = tuple(requirement_instantiables)
    
    
    # Generate rewards
    reward_generators = quest_template.rewards
    if (reward_generators is None):
        reward_instantiables = None
    else:
        reward_instantiables = []
        
        for reward_generator in reward_generators:
            reward_instantiable, diversion = reward_generator.generate_with_diversion(
                random_number_generator, accumulated_diversion
            )
            reward_instantiables.append(reward_instantiable)
            accumulated_diversion *= diversion
        
        reward_instantiables = tuple(reward_instantiables)
    
    # Construct
    return Quest(
        quest_template.id,
        requirement_instantiables,
        reward_instantiables,
    )


def select_random_quest_template(random_number_generator, quest_templates):
    """
    Selects a random quest template.
    
    Parameters
    ----------
    quest_templates : ``list<QuestTemplate>``
        Quest templates to select from.
    
    Return
    ------
    quest_template : ``QuestTemplate``
        The selected quest template.
    """
    return quest_templates[floor(random_number_generator.random() * len(quest_templates))]


def _exclude_from_quest_template_pool(quest_template_pool, quest_template):
    """
    Excludes from the quest template pool.
    
    Parameters
    ----------
    quest_template_pool : `dict<str, QuestTemplate``
        Quest template pool.
    
    quest_template : ``QuestTemplate``
        Quest template and its mutually exclude quests to exclude.
    """
    try:
        del quest_template_pool[quest_template.id]
    except KeyError:
        pass
    
    mutually_exclusive_with_ids = quest_template.mutually_exclusive_with_ids
    if (mutually_exclusive_with_ids is not None):
        for quest_template_id in mutually_exclusive_with_ids:
            try:
                del quest_template_pool[quest_template_id]
            except KeyError:
                pass


def _quest_sort_key_getter(quest):
    """
    Gets query sort key for the given quest.
    
    Parameters
    ----------
    quest : ``Quest``
        Quest to get sort key of.
    
    Returns
    -------
    sort_key : `(int, int, int)`
    """
    quest_template = get_quest_template_nullable(quest.template_id)
    if quest_template is None:
        return (-1, quest.reward_credibility, -1)
    
    reward_credibility = 0
    rewards = quest.rewards
    if (rewards is not None):
        for reward in rewards:
            if reward.TYPE == QUEST_REWARD_TYPE_CREDIBILITY:
                reward_credibility = reward.credibility
                break
    
    return (quest_template.level, reward_credibility, quest_template.id)


def create_quest_batch(guild_id, batch_id, level_limit, amount):
    """
    Generates a quest batch.
    
    Parameters
    ----------
    guild_id : `int`
        The respective guild' identifier.
    
    batch_id : `int`
        The identifier of the current batch.
    
    level_limit : `int`
        Level threshold to for selection.
    
    amount : `int`
        Amount of quests to generate.
    
    Returns
    -------
    quest_batch : ``QuestBatch``
    """
    random_number_generator = Random(guild_id ^ batch_id)
    
    # Collect available templates.
    quest_template_pool = {}
    
    for quest_template in QUEST_TEMPLATES.values():
        chance_in = quest_template.chance_in
        chance_out = quest_template.chance_out
        
        quest_template_level = quest_template.level
        if quest_template_level > level_limit:
            level_difference = quest_template_level - level_limit
            chance_out <<= level_difference
        
        if (chance_in != chance_out) and (random_number_generator.random() * chance_out >= chance_in):
            continue
        
        quest_template_pool[quest_template.id] = quest_template
        continue
    
    quests = []
    
    level = 0
    while (level <= level_limit) and (len(quests) < amount):
        quest_templates = [
            quest_template for quest_template in quest_template_pool.values() if quest_template.level == level
        ]
        level += 1
        if not quest_templates:
            continue
        
        quest_template = select_random_quest_template(random_number_generator, quest_templates)
        _exclude_from_quest_template_pool(quest_template_pool, quest_template)
        quests.append(create_quest_from_template(random_number_generator, quest_template))
    
    
    while quest_template_pool and (len(quests) < amount):
        quest_templates = [quest_template for quest_template in quest_template_pool.values()]
        quest_template = select_random_quest_template(random_number_generator, quest_templates)
        _exclude_from_quest_template_pool(quest_template_pool, quest_template)
        quests.append(create_quest_from_template(random_number_generator, quest_template))
    
    
    quests.sort(key = _quest_sort_key_getter)
    return QuestBatch(batch_id, tuple(quests))
