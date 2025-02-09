__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from hata import ClientUserBase, DiscordException, ERROR_CODES, Embed
from hata.ext.slash import P, abort

from ..bot_utils.constants import (
    EMOJI__HEART_CURRENCY, ROLE__SUPPORT__ELEVATED, ROLE__SUPPORT__HEART_BOOST, ROLE__SUPPORT__NSFW_ACCESS
)
from ..bot_utils.daily import calculate_daily_new
from ..bots import FEATURE_CLIENTS, MAIN_CLIENT

from .relationship_divorces_interactions import (
    relationship_divorces_decrement_invoke_other_question, relationship_divorces_decrement_invoke_self_question
)
from .relationship_slots_interactions import (
    relationship_slot_increment_invoke_other_question, relationship_slot_increment_invoke_self_question
)
from .relationships_core import (
    autocomplete_relationship_extended_user_name, get_extender_relationship_and_relationship_and_user_like_at
)
from .user_balance import get_user_balance


SHOP = FEATURE_CLIENTS.interactions(
    None,
    name = 'shop',
    description = 'Trade your hearts!',
    is_global = True,
)


@SHOP.interactions
async def buy_relationship_slot(
    event,
    target_related_name : P(
        str,
        'Buy relationship slot for someone related',
        'related',
        autocomplete = autocomplete_relationship_extended_user_name,
    ) = None,
    target_user : (
        ClientUserBase,
        'Buy waifu slot for someone else?',
        'someone-else',
    ) = None,
):
    if (target_user is None) and (target_related_name is not None):
        extender_relationship, relationship, target_user = (
            await get_extender_relationship_and_relationship_and_user_like_at(
                event.user_id, target_related_name, event.guild_id
            )
        )
    
    if target_user is None:
        coroutine = relationship_slot_increment_invoke_self_question(event)
    else:
        coroutine = relationship_slot_increment_invoke_other_question(event, target_user)
    
    return await coroutine


@SHOP.interactions
async def burn_divorce_papers(
    event,
    target_related_name : P(
        str,
        'Hire ninjas to burn and locate divorce papers for someone related',
        'related',
        autocomplete = autocomplete_relationship_extended_user_name,
    ) = None,
    target_user : (
        ClientUserBase,
        'Hire ninjas to burn an locate divorce papers for someone else?',
        'someone-else',
    ) = None,
):
    if (target_user is None) and (target_related_name is not None):
        extender_relationship, relationship, target_user = (
            await get_extender_relationship_and_relationship_and_user_like_at(
                event.user_id, target_related_name, event.guild_id
            )
        )
    
    if target_user is None:
        coroutine = relationship_divorces_decrement_invoke_self_question(event)
    else:
        coroutine = relationship_divorces_decrement_invoke_other_question(event, target_user)
    
    return await coroutine


NSFW_ACCESS_COST = 8000
ELEVATED_COST = 12000
HEART_BOOST_COST = 100000


NSFW_ACCESS_IDENTIFIER = '0'
ELEVATED_IDENTIFIER = '1'
HEART_BOOST_IDENTIFIER = '2'

BUYABLE_ROLES = {
    NSFW_ACCESS_IDENTIFIER: (ROLE__SUPPORT__NSFW_ACCESS, NSFW_ACCESS_COST),
    ELEVATED_IDENTIFIER: (ROLE__SUPPORT__ELEVATED, ELEVATED_COST),
    HEART_BOOST_IDENTIFIER: (ROLE__SUPPORT__HEART_BOOST, HEART_BOOST_COST),
}

ROLE_CHOICES = [
    (f'Horny ({NSFW_ACCESS_COST})', NSFW_ACCESS_IDENTIFIER),
    (f'Orin\'s Workcarrier ({ELEVATED_COST})', ELEVATED_IDENTIFIER),
    (f'Koishi enjoyer ({HEART_BOOST_COST})', HEART_BOOST_IDENTIFIER),
]


@SHOP.interactions
async def roles(
    event,
    role_choice: (ROLE_CHOICES, 'Choose a role to buy!', 'role'),
):
    """
    Buy roles to enhance your love!
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    role_choice : `str`
        The chosen role.
    
    Yields
    ------
    acknowledge / response : `None` / `Embed`
    """
    role, cost = BUYABLE_ROLES[role_choice]
    
    user = event.user
    role_guild = role.guild
    if (user.get_guild_profile_for(role_guild) is None):
        abort(f'You must be in {role_guild.name} to buy this role.')
    
    if user.has_role(role):
        abort(f'You already have {role.name} role.')
    
    user_id = user.id
    
    user_balance = await get_user_balance(user_id)
    balance = user_balance.balance
    can_buy = (balance - user_balance.allocated) >= cost
    
    if not can_buy:
        buying_success = False
    
    else:
        yield
        
        try:
            await MAIN_CLIENT.user_role_add(user, role)
        except DiscordException as err:
            if err.code in (
                ERROR_CODES.unknown_user,
                ERROR_CODES.unknown_member,
            ):
                buying_success = False
            
            else:
                raise
        
        else:
            buying_success = True
        
        user_balance.set('balance', balance - cost)
        await user_balance.save()

    embed = Embed(
        f'Buying {role.name} for {cost} {EMOJI__HEART_CURRENCY}'
    ).add_thumbnail(
        user.avatar_url_at(event.guild_id),
    )
    
    if can_buy:
        if buying_success:
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
            embed.description = 'Was unsuccessful; user not in guild.'
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


# ((d + 1) * d) >> 1 - (((d - a) + 1) * (d - a)) >> 1
# (((d + 1) * d) - (((d - a) + 1) * (d - a))) >> 1
# (d * d + d - (((d - a) + 1) * (d - a))) >> 1
# (d * d + d - ((d - a + 1) * (d - a))) >> 1
# (d * d + d - (d * d - d * a + d - d * a + a * a - a)) >> 1
# (d * d + d - (d * d - d * a + d - d * a + a * a - a)) >> 1
# (d * d + d + (-d * d + d * a - d + d * a - a * a + a)) >> 1
# (d * d + d - d * d + d * a - d + d * a - a * a + a) >> 1
# (d + d * a - d + d * a - a * a + a) >> 1
# (d * a + d * a - a * a + a) >> 1
# (d * a + d * a - a * a + a) >> 1
# (2 * d * a - a * a + a) >> 1
# (a * (2 * d - a + 1)) >> 1
# (a * ((d << 1) - a + 1)) >> 1
# (a * ((d << 1) - a + 1)) >> 1

DAILY_REFUND_MIN = 124

def calculate_sell_price(daily_count, daily_refund):
    under_price = DAILY_REFUND_MIN - daily_count + daily_refund
    if under_price < 0:
        under_price = 0
        over_price = daily_refund
    else:
        if under_price > daily_refund:
            under_price = daily_refund
            over_price = 0
        else:
            over_price = daily_refund - under_price
    
    price = 0
    
    if over_price:
        price += (over_price * ((daily_count << 1) - over_price + 1)) >> 1
    
    if under_price:
        price += (under_price * DAILY_REFUND_MIN)
    
    return price



@SHOP.interactions
async def sell_daily(
    client,
    event,
    amount: ('number', 'How much?'),
):
    """Sell excess daily streak for extra hearts."""
    if amount < 1:
        abort('`amount` must be non-negative!')
    
    user_id = event.user.id
    user_balance = await get_user_balance(user_id)
    balance = user_balance.balance
    streak = user_balance.streak
    daily_can_claim_at = user_balance.daily_can_claim_at
    now = DateTime.now(TimeZone.utc)
    streak, daily_can_claim_at = calculate_daily_new(streak, daily_can_claim_at, now)
    
    if amount > streak:
        sold = False
    
    else:
        sell_price = calculate_sell_price(streak, amount)
        
        user_balance.set('balance', balance + sell_price)
        user_balance.set('daily_can_claim_at', daily_can_claim_at)
        user_balance.set('streak', streak - amount)
        await user_balance.save()
        
        sold = True
    
    embed = Embed(
        f'Selling {amount} daily for {EMOJI__HEART_CURRENCY}'
    ).add_thumbnail(
        event.user.avatar_url,
    )
    
    if sold:
        embed.description = 'Great success!'
        embed.add_field(
            f'Your daily streak',
            (
                f'```\n'
                f'{streak} -> {streak - amount}\n'
                f'```'
            ),
        )
        embed.add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```\n'
                f'{balance} -> {balance + sell_price}\n'
                f'```'
            ),
        )
    else:
        embed.description = 'You have insufficient amount of daily streak.'
        embed.add_field(
            f'Daily streak',
            (
                f'```\n'
                f'{streak}\n'
                f'```'
            ),
        )
    
    return embed
