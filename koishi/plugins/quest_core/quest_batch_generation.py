__all__ = ('create_quest_batch',)

from random import Random
from math import floor

from .constants import QUEST_TEMPLATES
from .quest_batch import QuestBatch
from .quest import Quest
from .utils import get_quest_template


def round_value(value, require_multiple_of):
    """
    Rounds the given value to the closest multiple.
    
    Parameters
    ----------
    value : `int`
        Value to round.
    
    require_multiple_of : `int`
        Value to require the output to be multiple of.
    
    Returns
    -------
    value : `int`
    """
    if require_multiple_of != 1:
        fraction = value % require_multiple_of
        value -= fraction
        if fraction > require_multiple_of >> 1:
            value += require_multiple_of
    return value


def get_random_value_and_diversity_with_variance(
    random_number_generator,
    base,
    require_multiple_of,
    variance_percentage_lower_threshold,
    variance_percentage_upper_threshold,
):
    """
    Returns a random value for the given variance.
    
    Parameters
    ----------
    random_number_generator : `random.Random`
        Random value generator.
    
    base : `int`
        Base value.
    
    variance_percentage_lower_threshold : `int`
        Lower variance percentage threshold.
    
    variance_percentage_upper_threshold : `int`
        Upper variance percentage threshold.
    
    Returns
    -------
    value_with_diversity : `(int, float)`
    """
    variance_percentage = (
        variance_percentage_lower_threshold +
        floor(
            random_number_generator.random() *
            (variance_percentage_upper_threshold - variance_percentage_lower_threshold + 1)
        )
    )
    
    value = floor(base * variance_percentage / 100)
    value = round_value(value, require_multiple_of)
    value = max(value, require_multiple_of)
    diversion = value / base
    return value, diversion


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
    amount, amount_diversion = get_random_value_and_diversity_with_variance(
        random_number_generator,
        quest_template.amount_base,
        quest_template.amount_require_multiple_of,
        quest_template.amount_variance_percentage_lower_threshold,
        quest_template.amount_variance_percentage_upper_threshold,
    )
    duration, duration_diversion = get_random_value_and_diversity_with_variance(
        random_number_generator,
        quest_template.duration_base,
        quest_template.duration_require_multiple_of,
        quest_template.duration_variance_percentage_lower_threshold,
        quest_template.duration_variance_percentage_upper_threshold,
    )
    
    total_diversion = amount_diversion / duration_diversion
    reward_balance, reward_balance_diversion = get_random_value_and_diversity_with_variance(
        random_number_generator,
        floor(quest_template.reward_balance_base * total_diversion),
        quest_template.reward_balance_require_multiple_of,
        quest_template.reward_balance_variance_percentage_lower_threshold,
        quest_template.reward_balance_variance_percentage_upper_threshold,
    )
    # Give higher credibility if the reward balance diversion is lower
    total_diversion /= reward_balance_diversion
    base_reward_credibility = quest_template.reward_credibility
    reward_credibility = max(floor(base_reward_credibility * total_diversion), base_reward_credibility)
    
    return Quest(
        quest_template.id,
        amount,
        duration,
        reward_credibility,
        reward_balance,
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
    quest_template = get_quest_template(quest.template_id)
    if quest_template is None:
        return (-1, quest.reward_credibility, -1)
    
    return (quest_template.level, quest.reward_credibility, quest_template.id)


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
        if quest_template.level > level_limit:
            continue
        
        chance_in = quest_template.chance_in
        chance_out = quest_template.chance_out
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
