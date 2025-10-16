__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import elapsed_time

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from ..item_core import ITEM_NAME_DEFAULT, get_item_name, get_item_nullable
from ..quest_core import (
    AMOUNT_TYPE_COUNT, AMOUNT_TYPE_NAME_DEFAULT, AMOUNT_TYPE_VALUE, AMOUNT_TYPE_WEIGHT,
    LINKED_QUEST_COMPLETION_STATE_ACTIVE, QUEST_TYPE_ITEM_SUBMISSION, QUEST_TYPE_MONSTER_SUBJUGATION_LOCATED,
    QUEST_TYPE_MONSTER_SUBJUGATION_SELECTED, calculate_received_reward_credibility, get_adventurer_level_name,
    get_quest_board_resets_at
)

from .constants import BROKEN_QUEST_DESCRIPTION


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


def _produce_amount_completion_kg(amount_required, amount_submitted):
    """
    Produces the given amount of grams in a kilogram format.
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
        yield from _produce_amount_kg(amount_submitted)
        yield ' / '
    
    yield from _produce_amount_kg(amount_required)
    yield ' kg'


def _produce_quest_summary_line(quest_template, amount_required, amount_submitted):
    """
    Produces a quest's summary line.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    quest_template : ``QuestTemplate``
        The quest's template.
    
    amount_required : `int`
        The required amount of items to submit.
    
    amount_submitted : `int`
        The already submitted amount.
        If the quest is not accepted yet, pass it as `-1`.
    
    Yields
    ------
    part : `str`
    """
    quest_type = quest_template.type
    if quest_type == QUEST_TYPE_ITEM_SUBMISSION:
        yield 'Submit '
        
        amount_type = quest_template.amount_type
        if amount_type == AMOUNT_TYPE_COUNT:
            yield from _produce_amount_completion(amount_required, amount_submitted)
        
        elif amount_type == AMOUNT_TYPE_WEIGHT:
            yield from _produce_amount_completion_kg(amount_required, amount_submitted)
        
        elif amount_type == AMOUNT_TYPE_VALUE:
            yield from _produce_amount_completion(amount_required, amount_submitted)
            yield ' '
            yield EMOJI__HEART_CURRENCY.as_emoji
            yield ' wort of'
        
        else:
            yield from _produce_amount_completion(amount_required, amount_submitted)
            yield ' '
            yield AMOUNT_TYPE_NAME_DEFAULT
        
        yield ' '
        yield from _produce_nullable_item_parts(get_item_nullable(quest_template.item_id))
        
        yield ' to '
        yield get_item_name(quest_template.requester_id)
        yield '.'
    
    elif quest_type == QUEST_TYPE_MONSTER_SUBJUGATION_SELECTED:
        yield 'Subjugate '
        yield from _produce_amount_completion(amount_required, amount_submitted)
        yield ' '
        
        yield from _produce_nullable_item_parts(get_item_nullable(quest_template.item_id))
        yield '.'
    
    elif quest_type == QUEST_TYPE_MONSTER_SUBJUGATION_LOCATED:
        yield 'Subjugate '
        yield from _produce_amount_completion(amount_required, amount_submitted)
        yield 'monsters at '
        
        yield from _produce_nullable_item_parts(get_item_nullable(quest_template.item_id))
        yield '.'
    
    else:
        yield from _produce_amount_completion(amount_required, amount_submitted)
        yield ' '
        yield from _produce_nullable_item_parts(get_item_nullable(quest_template.item_id))
        yield '.'


def produce_quest_short_description(linked_quest, quest_template, amount_required):
    """
    Produces a linked quest's short description for listing it.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    linked_quest : ``None | LinkedQuest``
        The user's linked quest for this entry.
    
    quest_template : ``QuestTemplate``
        The quest's template.
    
    amount_required : `int`
        The required amount of items to submit.
    
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
    
    yield '\n'
    yield from _produce_quest_summary_line(quest_template, amount_required, -1)


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
        if linked_quest.expires_at <= now:
            yield 'Expired'
        
        else:
            yield 'Time left: '
            yield elapsed_time(RelativeDelta(linked_quest.expires_at, now))
        
        amount_submitted = linked_quest.amount_submitted
    
    else:
        repeat_count = quest_template.repeat_count
        completion_count = linked_quest.completion_count
        
        yield 'Completed: '
        yield str(completion_count)
        
        if repeat_count:
            yield ' / '
            yield str(repeat_count)
        
        yield ' times, '
        
        if (not repeat_count) or (repeat_count > completion_count):
            yield 're-acceptable for '
            yield elapsed_time(RelativeDelta(get_quest_board_resets_at(), now))
        
        else:
            yield 'cannot be re-accepted anymore'
        
        amount_submitted = -1
    
    yield '\n'
    yield from _produce_quest_summary_line(quest_template, linked_quest.amount_required, amount_submitted)


def _produce_quest_details_base_section(
    quest_template, amount_required, amount_submitted, reward_balance, reward_credibility
):
    """
    Builds the base of a quest's details section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    quest_template : ``QuestTemplate``
        The quest's template.
    
    amount_required : `int`
        The required amount of items to submit.
    
    amount_submitted : `int`
        The already submitted amount.
    
    reward_balance : `int`
        Reward balance.
    
    reward_credibility : `int`
        Reward credibility.
    
    Yields
    ------
    part : `str`
    """
    yield '**Task: '
    yield from _produce_quest_summary_line(quest_template, amount_required, amount_submitted)
    yield '**'
    
    description = quest_template.description
    if (description is not None):
        yield '\n\n'
        yield description
    
    yield '\n\n'
    yield '**Reward:**\n- **'
    yield str(reward_balance)
    yield '** '
    yield EMOJI__HEART_CURRENCY.as_emoji
    
    reward_credibility = reward_credibility
    if reward_credibility:
        yield '\n- **'
        yield str(reward_credibility)
        yield '** credibility'


def _produce_time_available(duration):
    """
    Produces available time section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    duration : `RelativeDelta`
        The quest's duration in relative delta.
    
    Yields
    ------
    part : `str`
    """
    yield '**Time available:**\n- **'
    yield elapsed_time(duration)
    yield '**'


def _produce_time_left(expires_at):
    """
    Produces time left section.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    expires_at : `DateTime`
        When the quest expires.
    
    Yields
    ------
    part : `str`
    """
    yield '**Time left:**\n- **'
    now = DateTime.now(tz = TimeZone.utc)
    if expires_at > now:
        yield elapsed_time(RelativeDelta(expires_at, now))
    else:
        yield 'expired'
    yield '**'


def produce_quest_detailed_description(quest, quest_template, user_level):
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
    
    Yields
    ------
    part : `str`
    """
    if quest_template is None:
        yield BROKEN_QUEST_DESCRIPTION
        return
    
    reward_credibility = quest.reward_credibility
    if reward_credibility:
        reward_credibility = calculate_received_reward_credibility(
            reward_credibility, quest_template.level, user_level
        )
    
    yield from _produce_quest_details_base_section(
        quest_template,
        quest.amount,
        -1,
        quest.reward_balance,
        reward_credibility,
    )
    yield '\n'
    yield from _produce_time_available(RelativeDelta(seconds = quest.duration))


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
    
    reward_credibility = linked_quest.reward_credibility
    if reward_credibility:
        reward_credibility = calculate_received_reward_credibility(
            reward_credibility, quest_template.level, user_level
        )
    
    yield from _produce_quest_details_base_section(
        quest_template,
        linked_quest.amount_required,
        linked_quest.amount_submitted,
        linked_quest.reward_balance,
        reward_credibility,
    )
    yield '\n'
    yield from _produce_time_available(RelativeDelta(linked_quest.expires_at, linked_quest.taken_at))
    yield '\n'
    yield from _produce_time_left(linked_quest.expires_at)


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
        yield item.description


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


def _produce_you_have_submitted_section(item, amount_type, amount_used):
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


def produce_linked_quest_submit_success_n_left_description(
    item, amount_type, amount_submitted, amount_required, amount_used
):
    """
    Produces response parts when the user successfully submitted `n` amount of items.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item : ``None | Item``
        The submitted item.
    
    amount_type : `int`
        The amount's type.
    
    amount_submitted : `int`
        Already submitted amount.
    
    amount_required : `int`
        The amount of required items.
    
    amount_used : `int`
        The used up amount.
    
    Yields
    ------
    part : `str`
    """
    yield from _produce_you_have_submitted_section(item, amount_type, amount_used)
    yield '\n'
    yield from _produce_amount_typed_bold(amount_type, amount_required - amount_submitted - amount_used)
    yield ' more to submit.'


def produce_linked_quest_submit_success_completed_description(
    item,
    amount_type,
    amount_required,
    amount_used,
    reward_balance,
    reward_credibility,
    user_level_old,
    user_level_new,
):
    """
    Produces response parts when the user successfully submits all the remaining items.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    item : ``None | Item``
        The submitted item.
    
    amount_type : `int`
        The amount's type.
    
    amount_required : `int`
        The amount of required items.
    
    amount_used : `int`
        The used up amount.
    
    reward_balance : `int`
        The amount of balance the user receives.
    
    reward_credibility : `int`
        The amount of credibility the user receives.
    
    user_level_old : `int`
        The user's adventurer rank before completing the quest.
    
    user_level_new : `int`
        The user's adventurer rank after completing the quest.
    
    Yields
    ------
    part : `str`
    """
    yield from _produce_you_have_submitted_section(item, amount_type, amount_used)
    yield '\nFor a total of '
    yield from _produce_amount_typed_bold(amount_type, amount_required)
    yield ' and finished the quest.\n\n**You received:**\n- **'
    yield str(reward_balance)
    yield '** '
    yield EMOJI__HEART_CURRENCY.as_emoji
    
    if not reward_credibility:
        return
    
    yield '\n- **'
    yield str(reward_credibility)
    yield '** credibility'
    
    if user_level_old == user_level_new:
        return
    
    yield '\n\nBy completing this quest you have ranked up from **'
    yield get_adventurer_level_name(user_level_old)
    yield '** to **'
    yield get_adventurer_level_name(user_level_new)
    yield '** rank; congratulation.'
