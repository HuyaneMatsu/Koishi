__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from hata import DiscordException, ERROR_CODES, Embed, Sticker
from hata.ext.slash import Button, InteractionResponse, Row, abort
from sqlalchemy.sql import select

from .marriage_slot import EMOJI_NO, EMOJI_YES, buy_waifu_slot_invoke

from ..bot_utils.constants import (
    EMOJI__HEART_CURRENCY, GUILD__SUPPORT, ROLE__SUPPORT__ELEVATED, ROLE__SUPPORT__HEART_BOOST,
    ROLE__SUPPORT__NSFW_ACCESS
)
from ..bot_utils.daily import calculate_daily_new
from ..bot_utils.models import DB_ENGINE, USER_COMMON_TABLE, user_common_model
from ..bots import FEATURE_CLIENTS, MAIN_CLIENT


NSFW_ACCESS_COST = 8000
ELEVATED_COST = 12000
HEART_BOOST_COST = 100000


HEART_SHOP = FEATURE_CLIENTS.interactions(
    None,
    name = 'heart-shop',
    description = 'Trade your love!',
    is_global = True,
)


@HEART_SHOP.interactions
async def buy_waifu_slot(event):
    return await buy_waifu_slot_invoke(event)

def get_divorce_reduction_cost(user_id, divorce_count):
    return user_id % (10000 * divorce_count)


CUSTOM_ID_REDUCE_DIVORCE_PAPER_YES = 'heart_shop.reduce_divorce.1'
CUSTOM_ID_REDUCE_DIVORCE_PAPER_NO = 'heart_shop.reduce_divorce.0'

BUTTON_REDUCE_DIVORCE_YES = Button(
    'Take My money!',
    EMOJI_YES,
    custom_id = CUSTOM_ID_REDUCE_DIVORCE_PAPER_YES,
)

BUTTON_REDUCE_DIVORCE_NO = Button(
    'Never mind...',
    EMOJI_NO,
    custom_id = CUSTOM_ID_REDUCE_DIVORCE_PAPER_NO,
)

COMPONENTS_REDUCE_DIVORCE = Row(
    BUTTON_REDUCE_DIVORCE_YES,
    BUTTON_REDUCE_DIVORCE_NO,
)

STICKER_REDUCE_DIVORCE_SUCCESS = Sticker.precreate(947189211671429220)


@HEART_SHOP.interactions
async def burn_divorce_papers(client, event):
    user_id = event.user.id
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.total_love,
                    user_common_model.total_allocated,
                    user_common_model.waifu_divorces,
                ]
            ).where(
                user_common_model.user_id == user_id
            )
        )
        
        result = await response.fetchone()
        if result is None:
            total_love = 0
            total_allocated = 0
            waifu_divorces = 0
        else:
            total_love, total_allocated, waifu_divorces = result
    
    if waifu_divorces <= 0:
        return Embed(None, 'You do not have divorces')
    
    available_love = total_love-total_allocated
    cost = get_divorce_reduction_cost(user_id, waifu_divorces)
    
    if available_love < cost:
        return Embed(
            None,
            (
                f'To locate and burn one of your divorce papers is worth {cost} {EMOJI__HEART_CURRENCY}\n'
                f'\n'
                f'You have only {available_love} {EMOJI__HEART_CURRENCY} available.'
            ),
        )
    
    return InteractionResponse(
        embed = Embed(
            None,
            f'To locate and burn one of your divorce papers is worth {cost} {EMOJI__HEART_CURRENCY}',
        ),
        components = COMPONENTS_REDUCE_DIVORCE,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_REDUCE_DIVORCE_PAPER_YES)
async def reduce_divorce_yes(event):
    user = event.user
    if event.message.interaction.user_id != user.id:
        return
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.total_allocated,
                    user_common_model.waifu_divorces,
                ]
            ).where(
                user_common_model.user_id == user.id
            )
        )
        
        result = await response.fetchone()
        if result is None:
            entry_id = 0
            total_love = 0
            total_allocated = 0
            waifu_divorces = 0
        else:
            entry_id, total_love, total_allocated, waifu_divorces = result
        
        while True:
            if waifu_divorces <= 0:
                text = (
                    'Task failed successfully\n'
                    '\n'
                    'Sufficient amount of divorces.'
                )
                thumbnail_image_url = None
                break
            
            available_love = total_love-total_allocated
            cost = get_divorce_reduction_cost(user.id, waifu_divorces)
            
            if available_love < cost:
                text = (
                    f'Heart amount changed - sufficient amount of hearts\n'
                    f'\n'
                    f'Required: {cost} {EMOJI__HEART_CURRENCY}\n'
                    f'Available {available_love} {EMOJI__HEART_CURRENCY} .'
                )
                thumbnail_image_url = None
                break
            
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == entry_id,
                ).values(
                    total_love = user_common_model.total_love - cost,
                    waifu_divorces = user_common_model.waifu_divorces - 1,
                )
            )
            
            text = (
                'Divorce papers located and burned successfully!\n'
                '\n'
                '*they will never find the bodies*'
            )
            thumbnail_image_url = STICKER_REDUCE_DIVORCE_SUCCESS.url
            break
    
    embed = Embed(None, text)
    
    if (thumbnail_image_url is not None):
        embed.add_thumbnail(thumbnail_image_url)
    
    return InteractionResponse(embed = embed, components = None)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_REDUCE_DIVORCE_PAPER_NO)
async def reduce_divorce_yes(event):
    user = event.user
    if event.message.interaction.user_id != user.id:
        return
    
    return InteractionResponse(embed = Embed(None, 'Divorce paper exploration cancelled'), components = None)


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


@HEART_SHOP.interactions
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
    if (user.get_guild_profile_for(GUILD__SUPPORT) is None):
        abort(f'You must be in {GUILD__SUPPORT.name} to buy any role.')
    
    if user.has_role(role):
        abort(f'You already have {role.name} role.')
    
    user_id = user.id
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.total_love,
                    user_common_model.total_allocated,
                ]
            ).where(
                user_common_model.user_id == user_id,
            )
        )
        results = await response.fetchall()
        
        if results:
            total_love, total_allocated = results[0]
            available_love = total_love - total_allocated
        else:
            total_love = 0
            available_love = 0
        
        if available_love >= cost:
            can_buy = True
        else:
            can_buy = False
        
        
        if can_buy:
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
            
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.user_id == user_id,
                ).values(
                    total_love = user_common_model.total_love - cost,
                )
            )
    
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
                    f'{total_love} -> {total_love - cost}\n'
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
                f'{total_love}\n'
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



@HEART_SHOP.interactions
async def sell_daily(client, event,
    amount: ('number', 'How much?'),
):
    """Sell excess daily streak for extra hearts."""
    if amount < 1:
        abort('`amount` must be non-negative!')
    
    user_id = event.user.id
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.daily_streak,
                    user_common_model.daily_next,
                ]
            ).where(
                user_common_model.user_id == user_id,
            )
        )
        
        results = await response.fetchall()
        if results:
            entry_id, total_love, daily_streak, daily_next = results[0]
            daily_next = daily_next.replace(tzinfo = TimeZone.utc)
            
            now = DateTime.now(TimeZone.utc)
            if daily_next < now:
                daily_streak, daily_next = calculate_daily_new(daily_streak, daily_next, now)
                daily_next = daily_next.replace(tzinfo = TimeZone.utc)
        
        else:
            entry_id = -1
            total_love = 0
            daily_streak = 0
        
        if amount <= daily_streak:
            sell_price = calculate_sell_price(daily_streak, amount)
            
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == entry_id
                ).values(
                    total_love = user_common_model.total_love + sell_price,
                    daily_next = daily_next,
                    daily_streak = daily_streak - amount,
                )
            )
            
            sold = True
        else:
            sold = False
    
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
                f'{daily_streak} -> {daily_streak - amount}\n'
                f'```'
            ),
        )
        embed.add_field(
            f'Your {EMOJI__HEART_CURRENCY}',
            (
                f'```\n'
                f'{total_love} -> {total_love + sell_price}\n'
                f'```'
            ),
        )
    else:
        embed.description = 'You have insufficient amount of daily streak.'
        embed.add_field(
            f'Daily streak',
            (
                f'```\n'
                f'{daily_streak}\n'
                f'```'
            ),
        )
    
    return embed
