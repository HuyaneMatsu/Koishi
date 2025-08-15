__all__ = ()

from .constants import ESCAPED_AT_SIGN

from ...bot_utils.constants import EMOJI__HEART_CURRENCY
from ...bot_utils.daily import ConditionGuildBadge, ConditionRole, ConditionWeekend, ConditionName, RewardAccumulator


def produce_condition_head_none(condition, interaction_event):
    """
    produces a condition head (no condition).
    
    This function is an iterable generator.
    
    Parameters
    ----------
    condition : `None`
        Condition to produce.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    -------
    part : `str`
    """
    yield '**Base:**\n'


def produce_condition_head_guild_badge(condition, interaction_event):
    """
    Produces a condition head (condition guild badge).
    
    This function is an iterable generator.
    
    Parameters
    ----------
    condition : ``ConditionGuildBadge``
        Condition to produce.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    -------
    part : `str`
    """
    yield '**Has tag of '
    yield condition.guild.name
    yield ':**\n'


def produce_condition_head_role(condition, interaction_event):
    """
    Produces a condition head (condition role).
    
    This function is an iterable generator.
    
    Parameters
    ----------
    condition : ``ConditionRole``
        Condition to produce.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    -------
    part : `str`
    """
    yield '**Has role '
    role = condition.role
    if role.guild_id == interaction_event.guild_id:
        yield role.mention
    else:
        yield ESCAPED_AT_SIGN
        yield role.name
    yield ':**\n'


def produce_condition_head_weekend(condition, interaction_event):
    """
    Produces a condition head (condition weekend).
    
    This function is an iterable generator.
    
    Parameters
    ----------
    condition : ``ConditionWeekend``
        Condition to produce.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    -------
    part : `str`
    """
    yield '**Its weekend:**\n'


def produce_condition_head_name(condition, interaction_event):
    """
    Renders a condition head (condition name).
    
    This function is an iterable generator.
    
    Parameters
    ----------
    condition : ``ConditionName``
        Condition to produce.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    -------
    part : `str`
    """
    yield '**Called as `'
    yield condition.name
    yield '`:**\n'


def produce_condition_head_unknown(condition, interaction_event):
    """
    Renders a condition head (condition unknown).
    
    This function is an iterable generator.
    
    Parameters
    ----------
    condition : ``ConditionBase``
        Condition to produce.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    -------
    part : `str`
    """
    yield '**Unknown:**\n'


CONDITION_HEAD_PRODUCERS = {
    type(None): produce_condition_head_none,
    ConditionGuildBadge : produce_condition_head_guild_badge,
    ConditionRole: produce_condition_head_role,
    ConditionWeekend: produce_condition_head_weekend,
    ConditionName: produce_condition_head_name,
}


def produce_reward_fields(prefix, base, extra_limit, extra_per_streak):
    """
    Produces the given reward fields.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    prefix : `None | str`
        Prefix to use if any.
    
    base : `int`
        Reward base.
    
    extra_limit : `int`
        Reward extra limit.
    
    extra_per_streak : `int`
        Reward extra per streak.
    
    Yields
    -------
    part : `str`
    """
    for name, value in zip(
        ('Base', 'Extra limit', 'Extra per streak'),
        (base, extra_limit, extra_per_streak),
    ):
        if not value:
            continue
        
        if (prefix is not None):
            yield prefix
            yield ' '
        
        yield name
        yield ': '
        yield repr(value)
        yield '\n'


def produce_reward(interaction_event, reward):
    """
    Renders the given reward.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    reward : ``Reward``
        Reward to render.
    
    Yields
    -------
    part : `str`
    """
    condition = reward.condition
    condition_head_producer = CONDITION_HEAD_PRODUCERS.get(type(condition), produce_condition_head_unknown)
    
    yield from condition_head_producer(condition, interaction_event)
    yield from produce_reward_fields(
        (None if reward.condition is None else '+'),
        reward.base,
        reward.extra_limit,
        reward.extra_per_streak,
    )


def produce_hearts_short_title(interaction_event, target_user, balance):
    """
    Produces a shot hearts title.
    
    This function is an iterable generator.
    
    Returns
    -------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    balance : `int`
        The user's balance.
    
    Yields
    -------
    part : `str`
    """
    if interaction_event.user is target_user:
        yield 'You have'
    else:
        yield target_user.name_at(interaction_event.guild)
        yield ' has'
    
    yield ' '
    yield str(balance)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji


def render_hearts_short_title(interaction_event, target_user, balance):
    """
    Renders a shot hearts title.
    
    Returns
    -------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    balance : `int`
        The user's balance.
    
    Returns
    -------
    title : `str`
    """
    return ''.join([*produce_hearts_short_title(interaction_event, target_user, balance)])


def produce_hearts_short_description(
    interaction_event, target_user, balance, streak, ready_to_claim, ready_to_claim_string
):
    """
    Produces a short hearts description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    balance : `int`
        The user's balance.
    
    streak : `int`
        The user's streak
    
    ready_to_claim : `bool`
        Whether daily is ready to claim.
    
    ready_to_claim_string : `str`
        String to use when the user is ready to claim its reward.
    
    Yields
    -------
    part : `str`
    """
    own = target_user is interaction_event.user
    
    if not (streak or balance):
        yield 'Awww, '
        yield ('you' if own else 'they')
        yield ' seem so lonely..'
        return
    
    yield ('You' if own else 'They')
    yield ' are on a '
    yield str(streak)
    yield ' day streak, '
    
    if not own:
        yield 'hope they will keep up their good work.'
        return
    
    if ready_to_claim:
        yield 'and you are ready to '
        yield ready_to_claim_string
    else:
        yield 'keep up the good work'
    
    yield '!'
    return


def render_hearts_short_description(
    interaction_event, target_user, balance, streak, ready_to_claim, ready_to_claim_string
):
    """
    Renders a short hearts description.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    balance : `int`
        The user's balance.
    
    streak : `int`
        The user's streak
    
    ready_to_claim : `bool`
        Whether daily is ready to claim.
    
    ready_to_claim_string : `str`
        String to use when the user is ready to claim its reward.
    
    Returns
    -------
    description : `None | str`
    """
    if (not streak) and balance:
        return
    
    return ''.join([*produce_hearts_short_description(
        interaction_event, target_user, balance, streak, ready_to_claim, ready_to_claim_string
    )])


def produce_hearts_extended_description(interaction_event, target_user, rewards, streak):
    """
    Produces extended hearts description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        User to calculate the reward of.
    
    rewards : `tuple<Reward>`
        Rewards to render.
    
    streak : `int`
        The user's streak.
    
    Yields
    -------
    part : `str`
    """
    reward_accumulator = RewardAccumulator()
    
    added_count = 0
    
    for reward in rewards:
        if not reward_accumulator.add_reward(reward, target_user):
            continue
        
        if added_count:
            yield '\n'
        
        yield from produce_reward(interaction_event, reward)
        added_count += 1
        continue
    
    if added_count > 1:
        yield '**\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_**\n\n**Total**\n'
        yield from produce_reward_fields(
            None, reward_accumulator.base, reward_accumulator.extra_limit, reward_accumulator.extra_per_streak
        )
    
    yield '\n**Formula:**\nbase + min(extra\\_limit, extra\\_per\\_streak * streak) + streak\n'
    yield str(reward_accumulator.base)
    yield ' + min('
    yield str(reward_accumulator.extra_limit)
    yield ', '
    yield str(reward_accumulator.extra_per_streak)
    yield ' * '
    yield str(streak)
    yield ') + '
    yield str(streak)
    yield ' = '
    yield str(reward_accumulator.sum_rewards(streak))


def render_hearts_extended_description(interaction_event, target_user, rewards, streak):
    """
    Renders extended hearts description.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        User to calculate the reward of.
    
    rewards : `tuple<Reward>`
        Rewards to render.
    
    streak : `int`
        The user's streak.
    
    Returns
    -------
    description : `str`
    """
    return ''.join([*produce_hearts_extended_description(interaction_event, target_user, rewards, streak)])


def render_int_block(value):
    """
    Renders a code block that encapsulates an integer.
    
    Parameters
    ----------
    value : `int`
        The value to encapsulate.
    
    Returns
    -------
    block : `str`
    """
    return (
        f'```\n'
        f'{value}\n'
        f'```'
    )
