from random import random
from datetime import datetime

from hata import Client, Embed, Emoji
from hata.ext.slash import abort, InteractionResponse
from sqlalchemy.sql import select

from bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE

from bot_utils.constants import ROLE__SUPPORT__ELEVATED, ROLE__SUPPORT__BOOSTER, GUILD__SUPPORT, \
    EMOJI__HEART_CURRENCY, ROLE__SUPPORT__HEART_BOOST, IN_GAME_IDS, COLOR__GAMBLING
from bot_utils.daily import VOTE_BASE, calculate_daily_new_only, DAILY_PER_DAY_BONUS_W_B, DAILY_LIMIT_BONUS_W_E, \
    DAILY_BASE_BONUS_W_HE, DAILY_LIMIT_BONUS_W_HE, DAILY_LIMIT_BONUS_W_B, DAILY_BASE, VOTE_PER_DAY, \
    DAILY_LIMIT, DAILY_PER_DAY, VOTE_BASE_BONUS_WEEKEND, VOTE_PER_DAY_BONUS_WEEKEND

SLASH_CLIENT: Client

ESCAPED_AT_SIGN = '@\u200b'

EMOJI_DAILY_STREAK = Emoji.precreate(856244196129243146)
EMOJI_COUNT_DAILY_FOR_WAIFU = Emoji.precreate(853998726333726721)
EMOJI_COUNT_DAILY_BY_WAIFU = Emoji.precreate(854009984916127755)
EMOJI_COUNT_DAILY_SELF = Emoji.precreate(741004530212274234)
EMOJI_COUNT_TOP_GG_VOTE = Emoji.precreate(745286745460965466)

EMOJI_HEART_CURRENCY_EASTER_EGG = Emoji.precreate(853152420304912404)
EMOJI_DAILY_STREAK_EASTER_EGG = Emoji.precreate(690550888187822150)
EMOJI_COUNT_DAILY_FOR_WAIFU_EASTER_EGG = Emoji.precreate(853509920477413386)
EMOJI_COUNT_DAILY_BY_WAIFU_EASTER_EGG = Emoji.precreate(852857884478930964)
EMOJI_COUNT_DAILY_SELF_EASTER_EGG = Emoji.precreate(772356182206840833)
EMOJI_COUNT_TOP_GG_VOTE_EASTER_EGG = Emoji.precreate(772495100840247306)


def create_hearts_short_embed(event, target_user, total_love, daily_streak, ready_to_claim):
    is_own = (event.user is target_user)
    
    if is_own:
        title_prefix = 'You have'
    else:
        title_prefix = target_user.full_name+' has'
    
    title = f'{title_prefix} {total_love} {EMOJI__HEART_CURRENCY:e}'
    
    if total_love == 0 and daily_streak == 0:
        if is_own:
            description = 'Awww, you seem so lonely..'
        else:
            description = 'Awww, they seem so lonely..'
    elif daily_streak:
        if is_own:
            if ready_to_claim:
                description_postfix = 'and you are ready to claim your daily'
            else:
                description_postfix = 'keep up the good work'
            description = f'You are on a {daily_streak} day streak, {description_postfix}!'
        
        else:
            description = f'They are on a {daily_streak} day streak, hope they will keep up their good work.'
    else:
        description = None
    
    return Embed(title, description, color=COLOR__GAMBLING)


async def get_generic_fields(target_user):
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.daily_streak,
                    user_common_model.daily_next,
                    user_common_model.total_allocated,
                ]
            ).where(
                user_common_model.user_id == target_user.id,
            )
        )
        
        results = await response.fetchall()
    
        if results:
            entry_id, total_love, daily_streak, daily_next, total_allocated = results[0]
            
            now = datetime.utcnow()
            if daily_next > now:
                ready_to_claim = False
            else:
                ready_to_claim = True
                
                daily_streak = calculate_daily_new_only(daily_streak, daily_next, now)
        
            if total_allocated and (target_user.id not in IN_GAME_IDS):
                await connector.execute(
                    USER_COMMON_TABLE.update(
                        user_common_model.id == entry_id,
                    ).values(
                        total_allocated = 0,
                    )
                )
        
        else:
            total_love = 0
            daily_streak = 0
            ready_to_claim = True
    
    return total_love, daily_streak, ready_to_claim

async def render_hearts_short(client, event, target_user):
    total_love, daily_streak, ready_to_claim = await get_generic_fields(target_user)
    return create_hearts_short_embed(event, target_user, total_love, daily_streak, ready_to_claim)
    


async def render_hearts_daily_extended(client, event, target_user):
    total_love, daily_streak, ready_to_claim = await get_generic_fields(target_user)
    embed = create_hearts_short_embed(event, target_user, total_love, daily_streak, ready_to_claim)
    
    if event.guild_id == GUILD__SUPPORT.id:
        can_mention_roles = True
    else:
        can_mention_roles = False
    
    field_value_parts = [
        '**Base:**\n'
        'Daily base: ', repr(DAILY_BASE), '\n'
        'Daily bonus: ', repr(DAILY_PER_DAY), '\n'
        'Daily bonus limit: ', repr(DAILY_LIMIT),
    ]
    
    daily_base = DAILY_BASE
    daily_per_day = DAILY_PER_DAY
    daily_limit = DAILY_LIMIT
    has_extra_role = False
    
    if target_user.has_role(ROLE__SUPPORT__ELEVATED):
        has_extra_role = True
        
        field_value_parts.append('\n\n**')
        if can_mention_roles:
            field_value_parts.append(ROLE__SUPPORT__ELEVATED.mention)
        else:
            field_value_parts.append(ESCAPED_AT_SIGN)
            field_value_parts.append(ROLE__SUPPORT__ELEVATED.name)
        
        field_value_parts.append(':**\n')
        
        field_value_parts.append('+ ')
        field_value_parts.append(repr(DAILY_LIMIT_BONUS_W_E))
        field_value_parts.append(' daily bonus limit')
        
        daily_limit += DAILY_LIMIT_BONUS_W_E
    
    if target_user.has_role(ROLE__SUPPORT__BOOSTER):
        has_extra_role = True
        
        field_value_parts.append('\n\n**')
        if can_mention_roles:
            field_value_parts.append(ROLE__SUPPORT__BOOSTER.mention)
        else:
            field_value_parts.append(ESCAPED_AT_SIGN)
            field_value_parts.append(ROLE__SUPPORT__BOOSTER.name)
        
        field_value_parts.append(':**\n')
        
        field_value_parts.append('+ ')
        field_value_parts.append(repr(DAILY_PER_DAY_BONUS_W_B))
        field_value_parts.append(' daily bonus\n')
        
        field_value_parts.append('+ ')
        field_value_parts.append(repr(DAILY_LIMIT_BONUS_W_B))
        field_value_parts.append(' daily bonus limit')
        
        daily_per_day += DAILY_PER_DAY_BONUS_W_B
        daily_limit += DAILY_LIMIT_BONUS_W_B
    
    if target_user.has_role(ROLE__SUPPORT__HEART_BOOST):
        has_extra_role = True
        
        field_value_parts.append('\n\n**')
        if can_mention_roles:
            field_value_parts.append(ROLE__SUPPORT__HEART_BOOST.mention)
        else:
            field_value_parts.append(ESCAPED_AT_SIGN)
            field_value_parts.append(ROLE__SUPPORT__HEART_BOOST.name)
        
        field_value_parts.append(':**\n')
        
        field_value_parts.append('+ ')
        field_value_parts.append(repr(DAILY_BASE_BONUS_W_HE))
        field_value_parts.append(' daily base\n')
        
        field_value_parts.append('+ ')
        field_value_parts.append(repr(DAILY_LIMIT_BONUS_W_HE))
        field_value_parts.append(' daily bonus limit')
        
        daily_base += DAILY_BASE_BONUS_W_HE
        daily_limit += DAILY_LIMIT_BONUS_W_HE
    
    field_value_parts.append('\n**\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**')
    
    if has_extra_role:
        field_value_parts.append('\n\n**Total:**\nDaily base: ')
        field_value_parts.append(repr(daily_base))
        field_value_parts.append('\nDaily bonus: ')
        field_value_parts.append(repr(daily_per_day))
        field_value_parts.append('\nDaily bonus limit: ')
        field_value_parts.append(repr(daily_limit))
    
    field_value_parts.append(
        '\n\n'
        '**Formula:**\n'
        'daily base + min(daily bonus limit, daily bonus * daily streak) + daily streak\n'
    )
    
    field_value_parts.append(repr(daily_base))
    field_value_parts.append(' + min(')
    field_value_parts.append(repr(daily_limit))
    field_value_parts.append(', ')
    field_value_parts.append(repr(daily_per_day))
    field_value_parts.append(' \* ')
    field_value_parts.append(repr(daily_streak))
    field_value_parts.append(') + ')
    field_value_parts.append(repr(daily_streak))
    field_value_parts.append(' = ')
    field_value_parts.append(repr(daily_base + min(daily_limit, daily_per_day * daily_streak) + daily_streak))
    
    field_value = ''.join(field_value_parts)
    
    embed.add_field('Daily reward calculation:', field_value)
    
    return InteractionResponse(embed=embed, allowed_mentions=None)


async def render_hearts_vote_extended(client, event, target_user):
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.daily_streak,
                    user_common_model.daily_next,
                    user_common_model.total_allocated,
                ]
            ).where(
                user_common_model.user_id == target_user.id,
            )
        )
        
        results = await response.fetchall()
        
        if results:
            entry_id, total_love, daily_streak, daily_next, total_allocated = results[0]
            
            now = datetime.utcnow()
            if daily_next > now:
                daily_streak = calculate_daily_new_only(daily_streak, daily_next, now)
        
            if total_allocated and (target_user.id not in IN_GAME_IDS):
                await connector.execute(
                    USER_COMMON_TABLE.update(
                        user_common_model.id == entry_id,
                    ).values(
                        total_allocated = 0,
                    )
                )
        
        else:
            daily_streak = 0
            total_love = 0
    
    is_own = (event.user is target_user)
    
    if is_own:
        title_prefix = 'You have'
    else:
        title_prefix = target_user.full_name+' has'
    
    title = f'{title_prefix} {total_love} {EMOJI__HEART_CURRENCY}'
    
    if total_love == 0 and daily_streak == 0:
        if is_own:
            description = 'Awww, you seem so lonely..'
        else:
            description = 'Awww, they seem so lonely..'
    elif daily_streak:
        if is_own:
            voted = await client.top_gg.get_user_vote(target_user.id)
            if voted:
                description_postfix = 'keep up the good work'
            else:
                description_postfix = 'and you are ready to vote'
            
            description = f'You are on a {daily_streak} day streak, {description_postfix}!'
        
        else:
            description = f'They are on a {daily_streak} day streak, hope they will keep up their good work.'
    else:
        description = None
    
    embed = Embed(title, description, color=COLOR__GAMBLING)
    

    field_value_parts = [
        '**Base:**\n'
        'Vote base: ', repr(VOTE_BASE), '\n'
        'Daily bonus: ', repr(VOTE_PER_DAY)
    ]
    
    vote_base = VOTE_BASE
    vote_per_day = VOTE_PER_DAY
    
    is_weekend = (datetime.utcnow().weekday() > 4)
    
    if is_weekend:
        field_value_parts.append('\n\n**Weekend bonus:**\n')
        
        field_value_parts.append('+ ')
        field_value_parts.append(repr(VOTE_BASE_BONUS_WEEKEND))
        field_value_parts.append(' vote base\n')
        
        field_value_parts.append('+ ')
        field_value_parts.append(repr(VOTE_PER_DAY_BONUS_WEEKEND))
        field_value_parts.append(' daily bonus')
        
        vote_base += VOTE_BASE_BONUS_WEEKEND
        vote_per_day += VOTE_PER_DAY_BONUS_WEEKEND
    
    field_value_parts.append('\n**\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**')
    
    if is_weekend:
        field_value_parts.append('\n\n**Total:**\nDaily base: ')
        field_value_parts.append(repr(vote_base))
        field_value_parts.append('\nDaily bonus: ')
        field_value_parts.append(repr(vote_per_day))
    
    field_value_parts.append(
        '\n\n'
        '**Formula:**\n'
        'vote base + daily bonus * daily streak\n'
    )
    
    field_value_parts.append(repr(vote_base))
    field_value_parts.append(' + ')
    field_value_parts.append(repr(vote_per_day))
    field_value_parts.append(' \* ')
    field_value_parts.append(repr(daily_streak))
    field_value_parts.append(' = ')
    field_value_parts.append(repr(vote_base + vote_per_day * daily_streak))
    
    field_value = ''.join(field_value_parts)
    
    embed.add_field('Vote calculation:', field_value)
    
    return embed


async def render_hearts_stats(client, event, target_user):
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.daily_streak,
                    user_common_model.daily_next,
                    user_common_model.total_allocated,
                    
                    # Counts
                    user_common_model.count_daily_self,
                    user_common_model.count_daily_by_waifu,
                    user_common_model.count_daily_for_waifu,
                    user_common_model.count_top_gg_vote,
                ]
            ).where(
                user_common_model.user_id == target_user.id,
            )
        )
        
        results = await response.fetchall()
        
        if results:
            entry_id, total_love, daily_streak, daily_next, total_allocated, count_daily_self, \
                count_daily_by_waifu, count_daily_for_waifu, count_top_gg_vote = results[0]
            
            now = datetime.utcnow()
            if daily_next > now:
                daily_streak = calculate_daily_new_only(daily_streak, daily_next, now)
            
            if total_allocated and (target_user.id not in IN_GAME_IDS):
                await connector.execute(
                    USER_COMMON_TABLE.update(
                        user_common_model.id == entry_id,
                    ).values(
                        total_allocated = 0,
                    )
                )
        
        else:
            total_love = 0
            daily_streak = 0
            
            count_daily_self = 0
            count_daily_by_waifu = 0
            count_daily_for_waifu = 0
            count_top_gg_vote = 0
    
    
    if random() < 0.01:
        emoji_heart_currency = EMOJI_HEART_CURRENCY_EASTER_EGG
        emoji_daily_streak = EMOJI_DAILY_STREAK_EASTER_EGG
        emoji_count_daily_self = EMOJI_COUNT_DAILY_SELF_EASTER_EGG
        emoji_count_daily_for_waifu = EMOJI_COUNT_DAILY_FOR_WAIFU_EASTER_EGG
        emoji_count_daily_by_waifu = EMOJI_COUNT_DAILY_BY_WAIFU_EASTER_EGG
        emoji_count_top_gg_vote = EMOJI_COUNT_TOP_GG_VOTE_EASTER_EGG
    else:
        emoji_heart_currency = EMOJI__HEART_CURRENCY
        emoji_daily_streak = EMOJI_DAILY_STREAK
        emoji_count_daily_self = EMOJI_COUNT_DAILY_SELF
        emoji_count_daily_for_waifu = EMOJI_COUNT_DAILY_FOR_WAIFU
        emoji_count_daily_by_waifu = EMOJI_COUNT_DAILY_BY_WAIFU
        emoji_count_top_gg_vote = EMOJI_COUNT_TOP_GG_VOTE
    
    
    return Embed(
        color = COLOR__GAMBLING
    ).add_author(
        target_user.avatar_url,
        f'Heart stats for {target_user.full_name}',
    ).add_field(
        f'{emoji_heart_currency} Hearts',
        (
            f'```\n'
            f'{total_love}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        f'{emoji_daily_streak} Daily streak',
        (
            f'```\n'
            f'{daily_streak}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        f'{emoji_count_daily_self} Claimed dailies',
        (
            f'```\n'
            f'{count_daily_self}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        f'{emoji_count_daily_for_waifu} Claimed for waifus',
        (
            f'```\n'
            f'{count_daily_for_waifu}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        f'{emoji_count_daily_by_waifu} Claimed by waifu',
        (
            f'```\n'
            f'{count_daily_by_waifu}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        f'{emoji_count_top_gg_vote} Top.gg votes',
        (
            f'```\n'
            f'{count_top_gg_vote}\n'
            f'```'
        ),
        inline = True,
    )



HEARTS_FIELD_NAME_SHORT = 'short'
HEARTS_FIELD_NAME_DAILY_EXTENDED = 'daily-extended'
HEARTS_FIELD_NAME_VOTE_EXTENDED = 'vote-extended'
HEARTS_FIELD_NAME_STATS = 'stats'

HEARTS_FIELD_CHOICES = [
    HEARTS_FIELD_NAME_SHORT,
    HEARTS_FIELD_NAME_DAILY_EXTENDED,
    HEARTS_FIELD_NAME_VOTE_EXTENDED,
    HEARTS_FIELD_NAME_STATS,
]

HEARTS_FIELD_NAME_TO_RENDERER = {
    HEARTS_FIELD_NAME_SHORT: (False, render_hearts_short),
    HEARTS_FIELD_NAME_DAILY_EXTENDED: (False, render_hearts_daily_extended),
    HEARTS_FIELD_NAME_VOTE_EXTENDED: (True, render_hearts_vote_extended),
    HEARTS_FIELD_NAME_STATS: (False, render_hearts_stats),
}

@SLASH_CLIENT.interactions(is_global=True)
async def hearts(client, event,
    target_user: ('user', 'Do you wanna know some1 else\'s hearts?') = None,
    field: (HEARTS_FIELD_CHOICES, 'Choose a field!') = HEARTS_FIELD_NAME_SHORT,
):
    """How many hearts do you have?"""
    if target_user is None:
        target_user = event.user
    
    try:
        acknowledge_required, field_renderer = HEARTS_FIELD_NAME_TO_RENDERER[field]
    except KeyError:
        abort(f'Unknown field: {field!r}.')
    else:
        if acknowledge_required:
            await client.interaction_application_command_acknowledge(event)
        
        return await field_renderer(client, event, target_user)
