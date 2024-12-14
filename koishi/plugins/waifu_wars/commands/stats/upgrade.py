__all__ = ('command_upgrade',)

from hata import Embed
from hata.ext.slash import P, abort

from ...core.constants import (
    STAT_NAME_FULL_BEDROOM, STAT_NAME_FULL_CHARM, STAT_NAME_FULL_CUTENESS, STAT_NAME_FULL_HOUSEWIFE,
    STAT_NAME_FULL_LOYALTY, STAT_NAME_SHORT_BEDROOM, STAT_NAME_SHORT_CHARM, STAT_NAME_SHORT_CUTENESS,
    STAT_NAME_SHORT_HOUSEWIFE, STAT_NAME_SHORT_LOYALTY
)
from ...core.helpers import calculate_stat_upgrade_cost, get_user_chart_color

from .....bot_utils.bind_types import WaifuStats
from .....bot_utils.constants import EMOJI__HEART_CURRENCY, WAIFU_COST_DEFAULT

from ....user_balance import get_user_balance


STAT_NAMES_AND_SLOTS = (
    (STAT_NAME_FULL_HOUSEWIFE, WaifuStats.stat_housewife),
    (STAT_NAME_FULL_CUTENESS, WaifuStats.stat_cuteness),
    (STAT_NAME_FULL_BEDROOM, WaifuStats.stat_bedroom),
    (STAT_NAME_FULL_CHARM, WaifuStats.stat_charm),
    (STAT_NAME_FULL_LOYALTY, WaifuStats.stat_loyalty),
)


STAT_NAME_IDENTIFYING = (
    (STAT_NAME_SHORT_HOUSEWIFE.casefold(), STAT_NAME_FULL_HOUSEWIFE, WaifuStats.stat_housewife),
    (STAT_NAME_SHORT_CUTENESS.casefold(), STAT_NAME_FULL_CUTENESS, WaifuStats.stat_cuteness),
    (STAT_NAME_SHORT_BEDROOM.casefold(), STAT_NAME_FULL_BEDROOM, WaifuStats.stat_bedroom),
    (STAT_NAME_SHORT_CHARM.casefold(), STAT_NAME_FULL_CHARM, WaifuStats.stat_charm),
    (STAT_NAME_SHORT_LOYALTY.casefold(), STAT_NAME_FULL_LOYALTY, WaifuStats.stat_loyalty),
)


def try_identify_stat(value):
    """
    Tries to identify the stat by the given value.
    
    Parameters
    ----------
    value : `str`
        The received value.
    
    Returns
    -------
    stat_name_and_slot : `None`, `tuple` of (`str`, ``FieldDescriptor``)
    """
    value = value.casefold()
    
    for name_to_match, name_full, slot in STAT_NAME_IDENTIFYING:
        if value.startswith(name_to_match):
            return name_full, slot
    
    return None


def try_identify_stats(value):
    """
    tries to identify the stat by the given value.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    value : `str`
        The received value.
    
    Returns
    -------
    stat_name_and_slot : `None`, `tuple` of (`str`, ``FieldDescriptor``)
    """
    value = value.casefold()
    
    for name_to_match, name_full, slot in STAT_NAME_IDENTIFYING:
        if value.startswith(name_to_match):
            yield name_full, slot


async def try_upgrade_stat(waifu_stats, slot):
    """
    Gets how much hearts the user have.
    
    This function is a coroutine.
    
    Parameters
    ----------
    waifu_stats : ``WaifuStats``
        The user's waifu stats.
    
    slot : ``FieldDescriptor``
        The stat slot to upgrade.
    
    Returns
    -------
    success : `bool`
        Whether upgrading the stat was successful.
    old_hearts : `int`
        The user's old hearts.
    cost : `int`
        Upgrade cost.
    next_point : `int`
        The new amount the stat has been upgraded to.
    """
    user_balance = await get_user_balance(waifu_stats.user_id)
    balance = user_balance.balance

    total_points = (
        waifu_stats.stat_housewife +
        waifu_stats.stat_cuteness +
        waifu_stats.stat_bedroom +
        waifu_stats.stat_charm +
        waifu_stats.stat_loyalty
    )
    next_point = slot.__get__(waifu_stats, WaifuStats) + 1
    
    cost = calculate_stat_upgrade_cost(total_points, next_point)
    
    if (balance - user_balance.avaiilable) < cost:
        success = False
    
    else:
        success = True
        
        user_balance.set('balance', balance - cost)
        user_balance.set('waifu_cost', (user_balance.waifu_cost or WAIFU_COST_DEFAULT) + cost // 100)
        await user_balance.save()
        
        slot.__set__(waifu_stats, next_point)
        waifu_stats.save()


    return success, balance, cost, next_point


async def autocomplete_upgrade_stat(event, value):
    """
    Auto completes the stats parameter of the `upgrade` command.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    stat : `None`, `str`
        The received stat name.
    
    Returns
    -------
    choices : `list` of `str`
    """
    waifu_stats = await event.user.waifu_stats
    
    if value is None:
        iterator = iter(STAT_NAMES_AND_SLOTS)
    else:
        iterator = try_identify_stats(value)
    
    total_points = (
        waifu_stats.stat_housewife +
        waifu_stats.stat_cuteness +
        waifu_stats.stat_bedroom +
        waifu_stats.stat_charm +
        waifu_stats.stat_loyalty
    )
    
    choices = []
    
    for name, slot in iterator:
        next_point = slot.__get__(waifu_stats, WaifuStats) + 1
        cost = calculate_stat_upgrade_cost(total_points, next_point)
        choices.append( f'{name} -> {next_point} for {cost}')
    
    return choices


async def command_upgrade(event, stat: P(str, 'Select a stat', autocomplete = autocomplete_upgrade_stat)):
    """
    Upgrades the given stat.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    stat : `str`
        The received stat name.
    
    Yields
    ------
    response : `None`, ``Embed``
    """
    identified_stat = try_identify_stat(stat)
    if identified_stat is None:
        abort('Unknown stat given.')
        return
    
    yield
    
    stat_name, slot = identified_stat
    waifu_stats = await event.user.waifu_stats
    
    success, balance, cost, next_point = await try_upgrade_stat(waifu_stats, slot)
    
    embed = Embed(
        f'Upgrading {stat_name} -> {next_point} for {cost} {EMOJI__HEART_CURRENCY}',
        color = get_user_chart_color(
            event.user.id,
            waifu_stats.stat_housewife,
            waifu_stats.stat_cuteness,
            waifu_stats.stat_bedroom,
            waifu_stats.stat_charm,
            waifu_stats.stat_loyalty,
        )
    ).add_thumbnail(
        event.user.avatar_url,
    )
    
    if success:
        embed.description = 'Was successful.'
        embed.add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```\n'
                f'{balance} -> {balance - cost}\n'
                f'```'
            )
        )
    else:
        embed.description = 'You have insufficient amount of hearts.'
        embed.add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```\n'
                f'{balance}\n'
                f'```'
            ),
        )
    
    yield embed
