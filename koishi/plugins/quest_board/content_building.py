__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import DATETIME_FORMAT_CODE, elapsed_time

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from ..item_core import ITEM_NAME_DEFAULT, get_item_group_name, get_item, produce_item_flags_names
from ..quest_core import (
    AMOUNT_TYPE_COUNT, AMOUNT_TYPE_NAME_DEFAULT, AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT,
    LINKED_QUEST_COMPLETION_STATE_ACTIVE, QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY, QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
    QUEST_REQUIREMENT_TYPE_ITEM_GROUP, QUEST_REWARD_TYPE_BALANCE, QUEST_REWARD_TYPE_CREDIBILITY,
    QUEST_REWARD_TYPE_ITEM_EXACT, get_adventurer_level_name, get_current_batch_id, get_quest_board_resets_at
)

from .constants import BROKEN_QUEST_DESCRIPTION
from .helpers import (
    get_linked_quest_duration_delta, get_linked_quest_expiration, get_linked_quest_rewards_normalised,
    get_linked_quest_submission_requirements_normalised, get_quest_duration_delta, get_quest_expiration,
    get_quest_rewards_normalised, get_quest_submission_requirements_normalised
)

from config import ORIN_ID


def produce_quest_board_header_description(guild, adventurer_info, quest_count):
    """
    Produces a guild's quest board's header component's content.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    guild : ``Guild``
        The respective guild the quest board is bound to.
    
    adventurer_info : ``AdventurerRankInfo``
        Information about the guild's adventurer rank.
    
    quest_count : `int`
        The amount of quests the guild currently has.
    
    Yields
    ------
    part : `str`
    """
    yield '# '
    yield guild.name
    yield '\'s quest board\n\nGuild rank: '
    yield get_adventurer_level_name(adventurer_info.level)
    yield '\nQuest count: '
    
    quest_limit = adventurer_info.quest_limit
    if quest_count != quest_limit:
        yield str(quest_count)
        yield ' / '
    
    yield str(quest_limit)


def produce_linked_quest_header_description(user, guild_id, adventurer_info, quest_count):
    """
    Produces a user's linked quest listing's header component's content.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    
    guild_id : `int`
        The respective guild's identifier the command is used.
    
    adventurer_info : ``AdventurerRankInfo``
        Information about the guild's adventurer rank.
    
    quest_count : `int`
        The amount of quests the user currently has.
    
    Yields
    ------
    part : `str`
    """
    yield '# '
    yield user.name_at(guild_id)
    yield '\'s quests\n\nUser rank: '
    yield get_adventurer_level_name(adventurer_info.level)
    yield '\nActive quest count: '
    
    yield str(quest_count)
    yield ' / '
    yield str(adventurer_info.quest_limit)


def _produce_nullable_item_parts(item):
    """
    Produces a nullable item's part.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item : ``None | Item``
        The item to produce its part of.
    
    Yields
    ------
    part : `str`
    """
    if item is None:
        yield ITEM_NAME_DEFAULT
    
    else:
        emoji = item.emoji
        if (emoji is not None):
            yield emoji.as_emoji
            yield ' '
        
        yield item.name


def _produce_amount_kg(amount):
    """
    Produces amount of grams in kilogram.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    amount : `int`
        The amount to produce.
    
    Yields
    ------
    part : `str`
    """
    amount_string = str(amount)
    amount_string_length = len(amount_string)
    if amount_string_length > 3:
        yield amount_string[:-3]
        if not amount_string.endswith('000'):
            yield '.'
            yield amount_string[-3:].rstrip('0')
    
    else:
        yield '0.'
        if amount_string_length < 3:
            yield '0' * (3 - amount_string_length)
        
        yield amount_string.rstrip('0')


def _produce_amount_completion(amount_required, amount_submitted):
    """
    Produces the given amount.
    If submitted is not `-1` given it will produce it in a `submitted / required` format.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    amount_required : `int`
        The required amount.
    
    amount_submitted : `int`
        The already submitted amount.
        If the quest is not accepted yet, pass it as `-1`.
    
    Yields
    ------
    part : `str`
    """
    if amount_submitted != -1:
        yield str(amount_submitted)
        yield ' / '
    
    yield str(amount_required)


def _produce_amount_completion_kg(amount_required, amount_submitted):
    """
    Produces the given amount of grams in a kilogram format.
    If submitted is not `-1` given it will produce it in a `submitted / required` format.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    amount_required : `int`
        The required amount.
    
    amount_submitted : `int`
        The already submitted amount.
        If the quest is not accepted yet, pass it as `-1`.
    
    Yields
    ------
    part : `str`
    """
    if amount_submitted != -1:
        yield from _produce_amount_kg(amount_submitted)
        yield ' / '
    
    yield from _produce_amount_kg(amount_required)
    yield ' kg'


def _produce_amount_completion_value(amount_required, amount_submitted):
    """
    Produces the given amount of balance in worth of format.
    If submitted is not `-1`given it will produce it in a `submitted / required` format.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    amount_required : `int`
        The required amount.
    
    amount_submitted : `int`
        The already submitted amount.
        If the quest is not accepted yet, pass it as `-1`.
    
    Yields
    ------
    part : `str`
    """
    if amount_submitted != -1:
        yield str(amount_submitted)
        yield ' / '
    
    yield str(amount_required)
    
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ' worth of'


def _produce_amount_completion_unknown(amount_required, amount_submitted):
    """
    Produces the given amount in an unknown format.
    If submitted is not `-1`given it will produce it in a `submitted / required` format.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    amount_required : `int`
        The required amount.
    
    amount_submitted : `int`
        The already submitted amount.
        If the quest is not accepted yet, pass it as `-1`.
    
    Yields
    ------
    part : `str`
    """
    if amount_submitted != -1:
        yield str(amount_submitted)
        yield ' / '
    
    yield str(amount_required)
    
    yield ' '
    yield AMOUNT_TYPE_NAME_DEFAULT


def _produce_item_exact_name(item_id):
    """
    Produces an item's name.
    
    Parameters
    ----------
    item_id : `int`
        Item's identifier.
    
    Yields
    ------
    part : `str`
    """
    item = get_item(item_id)
    
    emoji = item.emoji
    if (emoji is not None):
        yield emoji.as_emoji
        yield ' '
    
    yield item.name
    


def _produce_item_group_name(item_group_id):
    """
    Produces an item group's name.
    
    Parameters
    ----------
    item_group_id : `int`
        Item group's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield get_item_group_name(item_group_id)


def _produce_item_category_name(item_flags):
    """
    Produces an item category's name.
    
    Parameters
    ----------
    item_flags : `int`
        Item flags.
    
    Yields
    ------
    part : `str`
    """
    yield from produce_item_flags_names(item_flags, ' & ')


def _produce_item_unknown_name(identifier):
    """
    Produces an item category's name.
    
    Parameters
    ----------
    identifier : `int`
        Unknown identifier.
    
    Yields
    ------
    part : `str`
    """
    yield ITEM_NAME_DEFAULT


def _produce_submit_summary(submission_requirement_normalised):
    """
    Produces a single submit summary.
    
    Parameters
    ----------
    submission_requirement_normalised : `(int, int, int, int, int)`
        Submission requirement normalised.
    
    Yields
    ------
    part : `str`
    """
    (
        requirement_type,
        required_identifier,
        amount_type,
        amount_required,
        amount_submitted,
    ) = submission_requirement_normalised
    
    if amount_type == AMOUNT_TYPE_COUNT:
        amount_producer = _produce_amount_completion
    elif amount_type == AMOUNT_TYPE_WEIGHT:
        amount_producer = _produce_amount_completion_kg
    elif amount_type == AMOUNT_TYPE_VALUE:
        amount_producer = _produce_amount_completion_value
    else:
        amount_producer = _produce_amount_completion_unknown
    
    if requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_EXACT:
        name_producer = _produce_item_exact_name
    elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_GROUP:
        name_producer = _produce_item_group_name
    elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY:
        name_producer = _produce_item_category_name
    else:
        name_producer = _produce_item_unknown_name
    
    yield from amount_producer(amount_required, amount_submitted)
    yield ' '
    yield from name_producer(required_identifier)
    

def _produce_quest_summary_line(submission_requirements_normalised, requester_id):
    """
    Produces a quest's summary line.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    submission_requirements_normalised : `list<(int, int, int, int, int)>`
        The normalised submission requirements.
    
    requester_id : `int`
        The quest's requester.
    
    Yields
    ------
    part : `str`
    """
    yield 'Submit '
    
    last_index = len(submission_requirements_normalised) - 1
    
    for (index, submission_requirement_normalised) in enumerate(submission_requirements_normalised):
        if index:
            yield (' and ' if (index == last_index) else ', ')
        
        yield from _produce_submit_summary(submission_requirement_normalised)
        continue
    
    yield ' to '
    yield get_item(requester_id).name
    yield '.'


def produce_quest_short_description(linked_quest, quest, quest_template):
    """
    Produces a linked quest's short description for listing it.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    linked_quest : ``None | LinkedQuest``
        The user's linked quest for this entry.
    
    quest : ``Quest``
        The quest to produce description for.
    
    quest_template : ``QuestTemplate``
        The quest's template.
    
    Yields
    ------
    part : `str`
    """
    if quest_template is None:
        yield BROKEN_QUEST_DESCRIPTION
        return
    
    yield 'Required rank: '
    yield get_adventurer_level_name(quest_template.level)
    
    if (linked_quest is not None):
        yield '      Completed: '
        yield str(linked_quest.completion_count)
        
        repeat_count = quest_template.repeat_count
        if repeat_count:
            yield ' / '
            yield str(repeat_count)
        
        yield ' times'
    
    submission_requirements_normalised = get_quest_submission_requirements_normalised(quest)
    if (submission_requirements_normalised is not None):
        yield '\n'
        yield from _produce_quest_summary_line(submission_requirements_normalised, quest_template.requester_id)


def produce_linked_quest_short_description(linked_quest, quest_template):
    """
    Produces a linked quest's short description for listing it.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        The linked quest being rendered.
    
    quest_template : ``QuestTemplate``
        The quest's template.
    
    Yields
    ------
    part : `str`
    """
    if quest_template is None:
        yield BROKEN_QUEST_DESCRIPTION
        return
    
    now = DateTime.now(tz = TimeZone.utc)
    
    completion_state = linked_quest.completion_state
    if completion_state == LINKED_QUEST_COMPLETION_STATE_ACTIVE:
        expiration = get_linked_quest_expiration(linked_quest)
        yield 'Time left: '
        if (expiration is None):
            yield 'unlimited'
        elif expiration <= now:
            yield 'expired'
        else:
            yield elapsed_time(RelativeDelta(expiration, now))
    
    else:
        repeat_count = quest_template.repeat_count
        completion_count = linked_quest.completion_count
        
        yield 'Completed: '
        yield str(completion_count)
        yield ' / '
        yield (str(repeat_count) if repeat_count else 'unlimited')
        yield ' times, '
        
        if (not repeat_count) or (repeat_count > completion_count):
            yield 're-acceptable for '
            yield elapsed_time(RelativeDelta(get_quest_board_resets_at(), now))
        
        else:
            yield 'cannot be re-accepted anymore'
    
    submission_requirements_normalised = get_linked_quest_submission_requirements_normalised(linked_quest)
    if (submission_requirements_normalised is not None):
        yield '\n'
        yield from _produce_quest_summary_line(submission_requirements_normalised, quest_template.requester_id)


def _produce_quest_rewards_listing(title, rewards_normalised):
    """
    Produces a quest rewards listing.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    title : `str`
        Title to begin with.
    
    rewards_normalised : `None | list<(int, int, int)>`
        Rewards in a normalised form.
    
    Yields
    ------
    part : `str`
    """
    yield '**'
    yield title
    yield ':**'
    
    for reward_type, reward_identifier, amount_given in rewards_normalised:
        yield '\n- **'
        yield str(amount_given)
        yield '** '
        
        if reward_type == QUEST_REWARD_TYPE_BALANCE:
            yield EMOJI__HEART_CURRENCY.as_emoji
        
        elif reward_type == QUEST_REWARD_TYPE_CREDIBILITY:
            yield 'credibility'
        
        elif reward_type == QUEST_REWARD_TYPE_ITEM_EXACT:
            yield from _produce_item_exact_name(reward_identifier)
        
        else:
            yield ITEM_NAME_DEFAULT
    
    
def _produce_quest_details_base_section(linked_quest, quest, quest_template, user_level):
    """
    Builds the base of a quest's details section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    linked_quest : ``None | LinkedQuest``
        The linked quest to render.
    
    quest : ``None | Quest``
        The quest to render.
    
    quest_template : ``None | QuestTemplate``
        The quest's template.
    
    user_level : `int`
        The user's adventurer rank.
    
    Yields
    ------
    part : `str`
    
    Returns
    -------
    add_extra_line_break_after : `bool`
    """
    field_added = False
    
    if (linked_quest is not None):
        submission_requirements_normalised = get_linked_quest_submission_requirements_normalised(linked_quest)
    elif (quest is not None):
        submission_requirements_normalised = get_quest_submission_requirements_normalised(quest)
    else:
        submission_requirements_normalised = None
    
    if (submission_requirements_normalised is not None):
        field_added = True
        
        yield '**Task: '
        yield from _produce_quest_summary_line(submission_requirements_normalised, quest_template.requester_id)
        yield '**'
    
    description = quest_template.description
    if (description is not None):
        if field_added:
            yield '\n\n'
        else:
            field_added = True
        
        yield description
    
    if (linked_quest is not None):
        rewards_normalised = get_linked_quest_rewards_normalised(
            linked_quest, quest_template.level, user_level
        )
    elif (quest is not None):
        rewards_normalised = get_quest_rewards_normalised(
            quest, quest_template.level, user_level
        )
    else:
        rewards_normalised = None
    
    if (rewards_normalised is not None):
        if field_added:
            yield '\n\n'
        yield from _produce_quest_rewards_listing('Rewards', rewards_normalised)
        return False
    
    return True


def _produce_time_available(duration_delta, expiration):
    """
    Produces available time section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    duration_delta : `None | RelativeDelta`
        The quest's duration in relative delta.
    
    expiration : `None | DateTime`
        When the quest expires.
    
    Yields
    ------
    part : `str`
    """
    yield '**Time available:**\n- **'
    if (duration_delta is not None):
        yield elapsed_time(duration_delta)
    elif (expiration is not None):
        yield 'until '
        yield format(expiration, DATETIME_FORMAT_CODE)
        yield ' UTC'
    else:
        yield 'unlimited'
    
    yield '**'


def _produce_time_left(expiration):
    """
    Produces time left section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    expiration : `None | DateTime`
        When the quest expires.
    
    Yields
    ------
    part : `str`
    """
    yield '**Time left:**\n- **'
    if expiration is None:
        yield 'unlimited'
    else:
        now = DateTime.now(tz = TimeZone.utc)
        if expiration > now:
            yield elapsed_time(RelativeDelta(expiration, now))
        else:
            yield 'expired'
    yield '**'


def produce_quest_detailed_description(quest, quest_template, user_level, completion_count):
    """
    Produces a quest's detailed description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    quest : ``Quest``
        The quest in context.
    
    quest_template : ``None | QuestTemplate``
        The quest's template.
    
    user_level : `int`
        The user's adventurer rank.
    
    completion_count : `int`
        HHow much times was the quest already completed.
    
    Yields
    ------
    part : `str`
    """
    if quest_template is None:
        yield BROKEN_QUEST_DESCRIPTION
        return
    
    add_extra_line_break_after = yield from _produce_quest_details_base_section(
        None,
        quest,
        quest_template,
        user_level,
    )
    if add_extra_line_break_after:
        yield '\n'
    
    yield '\n'
    
    duration_delta = get_quest_duration_delta(quest)
    if (duration_delta is None):
        expiration = get_quest_expiration(quest)
    else:
        expiration = None
    
    yield from _produce_time_available(duration_delta, expiration)
    
    yield '\n**Completable:**\n- '
    repeat_count = quest_template.repeat_count
    if not repeat_count:
        yield '**unlimited** times'
    else:
        yield '**'
        yield str(repeat_count)
        yield '** times'
        
        if completion_count:
            yield ' ('
            yield str(max(repeat_count - completion_count, 0))
            yield ' left)'


def produce_linked_quest_detailed_description(linked_quest, quest_template, user_level):
    """
    Produces a linked quest's detailed description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        The linked quest in context.
    
    quest_template : ``None | QuestTemplate``
        The quest's template.
    
    user_level : `int`
        The user's adventurer rank.
    
    Yields
    ------
    part : `str`
    """
    if quest_template is None:
        yield BROKEN_QUEST_DESCRIPTION
        return
    
    add_extra_line_break_after = yield from _produce_quest_details_base_section(
        linked_quest,
        None,
        quest_template,
        user_level,
    )
    if add_extra_line_break_after:
        yield '\n'
    
    yield '\n'
    
    duration_delta = get_linked_quest_duration_delta(linked_quest)
    expiration = get_linked_quest_expiration(linked_quest)
    
    yield from _produce_time_available(duration_delta, expiration)
    yield '\n'
    yield from _produce_time_left(expiration)
    yield '\n'
    
    completion_count = linked_quest.completion_count
    repeat_count = quest_template.repeat_count
    yield '**Completed:**\n- **'
    yield str(completion_count)
    yield ' / '
    yield (str(repeat_count) if repeat_count else 'unlimited')
    yield '** times'
    
    if (not repeat_count) or (repeat_count - 1 > completion_count):
        yield ', '
        if (linked_quest.batch_id == get_current_batch_id()):
            yield 're-acceptable if completed within '
            yield elapsed_time(RelativeDelta(get_quest_board_resets_at(), DateTime.now(tz = TimeZone.utc)))
        
        else:
            yield 'cannot be re-accepted anymore'


def produce_nullable_item_description(item):
    """
    Produces a nullable item's description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item : ``None | Item``
        Item to produce its description of.
    
    Yields
    ------
    part : `str`
    """
    yield '**Item information: '
    yield from _produce_nullable_item_parts(item)
    yield '**\n\n'
    
    if item is None:
        description = None
    else:
        description = item.description
    if (description is None):
        yield '*no description*'
    else:
        yield description


def _produce_amount_typed_bold(amount_type, amount):
    """
    Produces typed amount appearing bold in markdown.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    amount_type : `int`
        The amount's type.
    
    amount : `int`
        The amount.
    
    Yields
    ------
    part : `str`
    """
    yield '**'
    
    if amount_type != AMOUNT_TYPE_WEIGHT:
        yield str(amount)
    
    else:
        yield from _produce_amount_kg(amount)
        yield ' kg'
    
    yield '**'
    
    if amount_type != AMOUNT_TYPE_COUNT and amount_type != AMOUNT_TYPE_WEIGHT:
        yield ' '
        if amount_type == AMOUNT_TYPE_VALUE:
            yield EMOJI__HEART_CURRENCY.as_emoji
            yield ' worth of'
        
        else:
            yield AMOUNT_TYPE_NAME_DEFAULT


def _produce_you_have_submitted_section_single(item, amount_type, amount_used):
    """
    Produces a section describing how much items the user submitted.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item : ``None | Item``
        The submitted item.
    
    amount_type : `int`
        The amount's type.
    
    amount_used : `int`
        The used up amount.
    
    Yields
    ------
    part : `str`
    """
    yield 'You have submitted '
    yield from _produce_amount_typed_bold(amount_type, amount_used)
    yield ' '
    yield from _produce_nullable_item_parts(item)
    yield '.'


def _produce_submit_success_n_left_single(item, amount_type, amount_used, amount_left):
    """
    Produces response parts when the user successfully submitted `n` amount of items.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item : ``None | Item``
        The submitted item.
    
    amount_type : `int`
        The amount's type.
    
    amount_used : `int`
        The used up amount.
    
    amount_left : `int`
        How much more to submit.
    
    Yields
    ------
    part : `str`
    """
    yield from _produce_you_have_submitted_section_single(item, amount_type, amount_used)
    yield '\n'
    yield from _produce_amount_typed_bold(amount_type, amount_left)
    yield ' more to submit.'


def _produce_submit_success_zero_left_single(item, amount_type, amount_required, amount_used):
    yield from _produce_you_have_submitted_section_single(item, amount_type, amount_used)
    yield '\nFor a total of '
    yield from _produce_amount_typed_bold(amount_type, amount_required)
    yield '.'


def produce_linked_quest_submit_success(submissions_normalised):
    """
    Produces response parts when the user successfully submitted `n` amount of items.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    submissions_normalised : ``list<(Item, int, int, int, int)>``
        The submitted amounts normalised.
    
    Yields
    ------
    part : `str`
    """
    field_added = False
    for item, amount_type, amount_required, amount_submitted, amount_used in submissions_normalised:
        if field_added:
            yield '\n'
        else:
            field_added = True
        
        amount_left = amount_required - amount_submitted - amount_used
        if amount_left > 0:
            yield from _produce_submit_success_n_left_single(item, amount_type, amount_used, amount_left)
        else:
            yield from _produce_submit_success_zero_left_single(item, amount_type, amount_required, amount_used)


def produce_linked_quest_submit_success_completed_description(
    client_id,
    submissions_normalised,
    rewards_normalised,
    user_level_old,
    user_level_new,
):
    """
    Produces response parts when the user successfully submits all the remaining items.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    client_id : `int`
        The client's identifier who is rendering this message.
    
    submissions_normalised : ``list<(Item, int, int, int, int)>``
        The submitted amounts normalised.
    
    rewards_normalised : `None | list<(int, int, int)>`
        The rewards given by the quest in a normalised form.
    
    user_level_old : `int`
        The user's adventurer rank before completing the quest.
    
    user_level_new : `int`
        The user's adventurer rank after completing the quest.
    
    Yields
    ------
    part : `str`
    """
    yield from produce_linked_quest_submit_success(submissions_normalised)
    yield '\nBy doing so, you finished the quest.'
    
    if (rewards_normalised is not None):
        yield '\n\n'
        yield from _produce_quest_rewards_listing('You received', rewards_normalised)
    
    if user_level_old == user_level_new:
        return
    
    yield '\n\nBy completing this quest you have ranked up from **'
    yield get_adventurer_level_name(user_level_old)
    yield '** to **'
    yield get_adventurer_level_name(user_level_new)
    yield '** rank.\n'
    
    if client_id == ORIN_ID:
        name = 'Maids'
        whos = 'my'
    else:
        name = 'Orin'
        whos = None
    
    yield name
    yield '! Bring '
    yield ('the' if whos is None else whos)
    yield ' buffet chariot! Let the party begin!'


def _produce_owned_amount_extra(amount_type, accumulated_weight, accumulated_value):
    """
    Produces owned amount extra postfix in case the requirement is not count.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    amount_type : `int`
        The type of the amount.
    
    accumulated_weight : `int`
        Accumulated weight in grams.
    
    accumulated_value : `int`
        Accumulated value in hearts.
    
    Yields
    ------
    part : `str`
    """
    if amount_type not in (AMOUNT_TYPE_WEIGHT, AMOUNT_TYPE_VALUE):
        return
    
    yield ' ('
    if amount_type == AMOUNT_TYPE_WEIGHT:
        yield from _produce_amount_kg(accumulated_weight)
        yield ' kg'
    else:
        yield str(accumulated_value)
        yield ' '
        yield EMOJI__HEART_CURRENCY.as_emoji
    
    yield ')'
    

def produce_linked_quest_submission_requirements_entry_description(
    submission_requirement_normalised, accumulated_amount, accumulated_weight, accumulated_value
):
    """
    Produces a submission requirements entry's description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    submission_requirement_normalised : `(int, int, int, int, int)`
        Normalised requirement to produce.
    
    accumulated_amount : `int`
        The amount of items the user has that satisfies the requirement.
    
    accumulated_weight : `int`
        The weight of items the user has that satisfies the requirement.
    
    accumulated_value : `int`
        The value of items the user has that satisfies the requirement.
    
    Yields
    ------
    part : `str`
    """
    yield from _produce_submit_summary(submission_requirement_normalised)
    yield ', '
    
    if not accumulated_amount:
        yield 'none on stock'
        return
    
    yield str(accumulated_amount)
    yield ' on stock'
    
    yield from _produce_owned_amount_extra(submission_requirement_normalised[2], accumulated_weight, accumulated_value)


def produce_linked_quest_submission_item_select_header(
    submission_requirement_normalised, accumulated_amount, accumulated_weight, accumulated_value
):
    """
    Produces linked quest submission item select header.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    submission_requirement_normalised : `None | (int, int, int, int, int)`
        Normalised requirement to produce.
    
    accumulated_amount : `int`
        The amount of items the user has that satisfies the requirement.
    
    accumulated_weight : `int`
        The weight of items the user has that satisfies the requirement.
    
    accumulated_value : `int`
        The value of items the user has that satisfies the requirement.
    
    Yields
    ------
    part : `str`
    """
    yield '### Select item to submit'
    
    if submission_requirement_normalised is None:
        return
    
    yield '\n\n'
    yield from produce_linked_quest_submission_requirements_entry_description(
        submission_requirement_normalised, accumulated_amount, accumulated_weight, accumulated_value
    )


def produce_linked_quest_submission_item_select_description(item_entry, amount_type):
    """
    Produces linked quest submission item select description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item_entry : ``ItemEntry``
        Item entry to build description for.
    
    amount_type : `int`
        The type of the amount.
    
    Yields
    ------
    part : `str`
    """
    amount = item_entry.amount
    yield str(amount)
    yield ' '
    
    item = item_entry.item
    
    emoji = item.emoji
    if (emoji is not None):
        yield emoji.as_emoji
        yield ' '
    
    yield item.name
    
    yield from _produce_owned_amount_extra(amount_type, amount * item.weight, amount * item.value)
