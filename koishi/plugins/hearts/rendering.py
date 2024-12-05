__all__ = ()

from .constants import ESCAPED_AT_SIGN

from ...bot_utils.constants import EMOJI__HEART_CURRENCY
from ...bot_utils.daily import ConditionRole, ConditionWeekend, ConditionName, RewardAccumulator


def render_condition_head_none_into(into, condition, interaction_event):
    """
    Renders a condition head (no condition).
    
    Parameters
    ----------
    into : `list<str>`
        Container to render into.
    
    condition : `None`
        Condition to render.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append('**Base:**\n')
    return into
    

def render_condition_head_role_into(into, condition, interaction_event):
    """
    Renders a condition head (condition role).
    
    Parameters
    ----------
    into : `list<str>`
        Container to render into.
    
    condition : ``ConditionRole``
        Condition to render.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append('**Has role ')
    role = condition.role
    if role.guild_id == interaction_event.guild_id:
        into.append(role.mention)
    else:
        into.append(ESCAPED_AT_SIGN)
        into.append(role.name)
    into.append(':**\n')
    
    return into


def render_condition_head_weekend_into(into, condition, interaction_event):
    """
    Renders a condition head (condition weekend).
    
    Parameters
    ----------
    into : `list<str>`
        Container to render into.
    
    condition : ``ConditionWeekend``
        Condition to render.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append('**Its weekend:**\n')
    return into


def render_condition_head_name_into(into, condition, interaction_event):
    """
    Renders a condition head (condition name).
    
    Parameters
    ----------
    into : `list<str>`
        Container to render into.
    
    condition : ``ConditionName``
        Condition to render.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append('**Called as `')
    into.append(condition.name)
    into.append('`:**\n')
    return into


def render_condition_head_unknown_into(into, condition, interaction_event):
    """
    Renders a condition head (condition unknown).
    
    Parameters
    ----------
    into : `list<str>`
        Container to render into.
    
    condition : ``ConditionBase``
        Condition to render.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    into : `list<str>`
    """
    into.append('**Unknown:**\n')
    return into


CONDITION_HEAD_RENDERERS = {
    type(None): render_condition_head_none_into,
    ConditionRole: render_condition_head_role_into,
    ConditionWeekend: render_condition_head_weekend_into,
    ConditionName: render_condition_head_name_into,
}


def render_reward_fields_into(into, prefix, base, extra_limit, extra_per_streak):
    """
    Renders the given reward fields.
    
    Parameters
    ----------
    into : `list<str>`
        Container to render into.
    
    prefix : `None | str`
        Prefix to use if any.
    
    base : `int`
        Reward base.
    
    extra_limit : `int`
        Reward extra limit.
    
    extra_per_streak : `int`
        Reward extra per streak.
    
    Returns
    -------
    into : `list<str>`
    """
    for name, value in zip(
        ('Base', 'Extra limit', 'Extra per streak'),
        (base, extra_limit, extra_per_streak),
    ):
        if not value:
            continue
        
        if (prefix is not None):
            into.append(prefix)
            into.append(' ')
        
        into.append(name)
        into.append(': ')
        into.append(repr(value))
        into.append('\n')
    
    return into


def render_reward_into(into, interaction_event, reward):
    """
    Renders the given reward.
    
    Parameters
    ----------
    into : `list<str>`
        Container to render into.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    reward : ``Reward``
        Reward to render.
    
    Returns
    -------
    into : `list<str>`
    """
    condition = reward.condition
    into = CONDITION_HEAD_RENDERERS.get(type(condition), render_condition_head_unknown_into)(
        into, condition, interaction_event
    )
    into = render_reward_fields_into(
        into,
        (None if reward.condition is None else '+'),
        reward.base,
        reward.extra_limit,
        reward.extra_per_streak,
    )
    return into


def render_hearts_short_title(interaction_event, target_user, total):
    """
    Renders a shot hearts title.
    
    Returns
    -------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    total : `int`
        The user's total hearts.
    
    Returns
    -------
    title : `str`
    """
    into = []
    
    if interaction_event.user is target_user:
        into.append('You have')
    else:
        into.append(target_user.name_at(interaction_event.guild))
        into.append(' has')
    
    into.append(' ')
    into.append(str(total))
    into.append(' ')
    into.append(EMOJI__HEART_CURRENCY.as_emoji)
    
    return ''.join(into)


def render_hearts_short_description(
    interaction_event, target_user, total, streak, ready_to_claim, ready_to_claim_string
):
    """
    Renders a short hearts description.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        The targeted user.
    
    total : `int`
        The user's total hearts.
    
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
    if (not streak) and total:
        return
    
    own = target_user is interaction_event.user
    into = []
    
    if streak or total:
        into.append('You' if own else 'They')
        into.append(' are on a ')
        into.append(str(streak))
        into.append(' day streak, ')
        
        if own:
            if ready_to_claim:
                into.append('and you are ready to ')
                into.append(ready_to_claim_string)
            else:
                into.append('keep up the good work')
            
            into.append('!')
        else:
            into.append('hope they will keep up their good work.')
    
    else:
        into.append('Awww, ')
        into.append('you' if own else 'they')
        into.append(' seem so lonely..')
    
    return ''.join(into)


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
    into = []
    
    reward_accumulator = RewardAccumulator()
    
    added_count = 0
    
    for reward in rewards:
        if not reward_accumulator.add_reward(reward, target_user):
            continue
        
        if added_count:
            into.append('\n')
        
        into = render_reward_into(into, interaction_event, reward)
        added_count += 1
        continue
    
    if added_count > 1:
        into.append('**\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_\\_**\n\n**Total**\n')
        into = render_reward_fields_into(
            into, None, reward_accumulator.base, reward_accumulator.extra_limit, reward_accumulator.extra_per_streak
        )
    
    into.append('\n**Formula:**\nbase + min(extra\\_limit, extra\\_per\\_streak * streak) + streak\n')
    into.append(str(reward_accumulator.base))
    into.append(' + min(')
    into.append(str(reward_accumulator.extra_limit))
    into.append(', ')
    into.append(str(reward_accumulator.extra_per_streak))
    into.append(' * ')
    into.append(str(streak))
    into.append(') + ')
    into.append(str(streak))
    into.append(' = ')
    into.append(str(reward_accumulator.sum_rewards(streak)))
    return ''.join(into)


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
