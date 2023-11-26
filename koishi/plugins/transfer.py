__all__ = ()

from datetime import datetime

from hata import Embed, DiscordException, ERROR_CODES, User, Permission
from hata.ext.slash import abort
from sqlalchemy.sql import select
from sqlalchemy.dialects.postgresql import insert

from ..bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE, get_create_common_user_expression, \
    WAIFU_LIST_TABLE, waifu_list_model, waifu_proposal_model, WAIFU_PROPOSAL_TABLE, item_model, ITEM_TABLE, \
    emoji_counter_model, EMOJI_COUNTER_TABLE, sticker_counter_model, STICKER_COUNTER_TABLE, ds_v2_model, DS_V2_TABLE, \
    ds_v2_result_model, DS_V2_RESULT_TABLE
from ..bot_utils.constants import GUILD__SUPPORT, ROLE__SUPPORT__ADMIN, IN_GAME_IDS,  COLOR__GAMBLING
from ..bot_utils.daily import calculate_daily_new_only
from ..bots import MAIN_CLIENT

WAIFU_STATE_NONE = 0
WAIFU_STATE_KEEP = 1
WAIFU_STATE_DIVORCE = 2

PROPOSAL_CANCEL_REASON_TRANSFERRED = 1
PROPOSAL_CANCEL_REASON_OVER_LIMIT = 2


def assert_required_permission(event):
    if not event.user_permissions.can_administrator:
        abort('You must have administrator permission to invoke this command.')


TRANSFER = MAIN_CLIENT.interactions(
    None,
    name = 'transfer',
    description = 'Transfers all of someone\'s hearts to an other person.',
    guild = GUILD__SUPPORT,
    required_permissions = Permission().update_by_keys(administrator = True),
)

@TRANSFER.interactions
async def user_(client, event,
    source_user: ('user', 'Who\'s hearst do you want to transfer?'),
    target_user: ('user', 'To who do you want transfer the taken heart?'),
    message: ('str', 'Optional message to send with the transfer.') = None,
):
    """Transfer with user parameters."""
    assert_required_permission(event)
    return do_transfer(client, event, source_user, target_user, message)

@TRANSFER.interactions
async def user_id(client, event,
    source_user_id: (int, 'Who\'s hearst do you want to transfer?'),
    target_user_id: (int, 'To who do you want transfer the taken heart?'),
    message: ('str', 'Optional message to send with the transfer.') = None,
):
    """Transfer with user_id parameters | Use this for deleted users."""
    assert_required_permission(event)
    yield
    
    try:
        source_user = await client.user_get(source_user_id)
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_user:
            source_user = User.precreate(source_user_id, name = 'Deleted User')
        else:
            raise
    
    try:
        target_user = await client.user_get(target_user_id)
    except DiscordException as err:
        if err.code == ERROR_CODES.unknown_user:
            target_user = User.precreate(target_user_id, name = 'Deleted User')
        else:
            raise
    
    yield do_transfer(client, event, source_user, target_user, message)


async def do_transfer(client, event, source_user, target_user, message):
    if not event.user.has_role(ROLE__SUPPORT__ADMIN):
        abort(f'{ROLE__SUPPORT__ADMIN.mention} only!', allowed_mentions = None)
    
    if source_user.id in IN_GAME_IDS:
        abort(f'{source_user:m} is in a game, cannot transfer now.')
    
    if (message is not None) and len(message) > 1000:
        message = message[:1000]+'...'
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.user_id,
                    
                    user_common_model.total_love,
                    user_common_model.total_allocated,
                    
                    user_common_model.daily_next,
                    user_common_model.daily_streak,
                    
                    user_common_model.count_daily_self,
                    user_common_model.count_daily_by_waifu,
                    user_common_model.count_daily_for_waifu,
                    user_common_model.count_top_gg_vote,
                    
                    user_common_model.waifu_cost,
                    user_common_model.waifu_divorces,
                    user_common_model.waifu_slots,
                ]
            ).where(
                user_common_model.user_id.in_(
                    [
                        source_user.id,
                        target_user.id,
                    ]
                )
            )
        )
        
        results = await response.fetchall()
        result_count = len(results)
        
        if result_count == 0:
            source_user_result = None
            target_user_result = None
        else:
            if result_count == 1:
                source_user_result = results[0]
                target_user_result = None
            else:
                source_user_result, target_user_result = results
            
            if source_user_result[1] != source_user.id:
                target_user_result, source_user_result = source_user_result, target_user_result
        
        
        now = datetime.utcnow()
        
        if (source_user_result is None):
            source_user_entry_id = -1
            
            source_user_total_love = 0
            source_user_total_allocated = 0
            
            source_user_daily_next = now
            source_user_daily_streak = 0
            
            source_user_count_daily_self = 0
            source_user_count_daily_by_waifu = 0
            source_user_count_daily_for_waifu = 0
            source_user_count_top_gg_vote = 0
            
            source_user_waifu_cost = 0
            source_user_waifu_divorces = 0
            source_user_waifu_slots = 14
        
        else:
            source_user_entry_id, \
            _, \
            \
            source_user_total_love, \
            \
            source_user_daily_next, \
            source_user_daily_streak, \
            \
            source_user_count_daily_self, \
            source_user_count_daily_by_waifu, \
            source_user_count_daily_for_waifu, \
            source_user_count_top_gg_vote, \
            \
            source_user_waifu_cost, \
            source_user_waifu_divorces, \
            source_user_waifu_slots, \
                = source_user_result
            
            if source_user_daily_next > now:
                source_user_daily_streak = calculate_daily_new_only(
                source_user_daily_streak,
                source_user_daily_next,
                now,
            )
        

        if (target_user_result is None):
            target_user_entry_id = -1
            
            target_user_total_love = 0
            target_user_total_allocated = 0
            
            target_user_daily_next = now
            target_user_daily_streak = 0
            
            target_user_count_daily_self = 0
            target_user_count_daily_by_waifu = 0
            target_user_count_daily_for_waifu = 0
            target_user_count_top_gg_vote = 0
            
            target_user_waifu_cost = 0
            target_user_waifu_divorces = 0
            target_user_waifu_slots = 1
        
        else:
            target_user_entry_id, \
            _, \
            \
            target_user_total_love, \
            target_user_total_allocated, \
            \
            target_user_daily_next, \
            target_user_daily_streak, \
            \
            target_user_count_daily_self, \
            target_user_count_daily_by_waifu, \
            target_user_count_daily_for_waifu, \
            target_user_count_top_gg_vote, \
            \
            target_user_waifu_cost, \
            target_user_waifu_divorces, \
            target_user_waifu_slots, \
                = target_user_result
            
            now = datetime.utcnow()
            if target_user_daily_next > now:
                target_user_daily_streak = calculate_daily_new_only(
                target_user_daily_streak,
                target_user_daily_next,
                now,
            )
            
            if target_user.id not in IN_GAME_IDS:
                target_user_total_allocated = 0
        
        new_entry_id = target_user_entry_id

        new_total_love = source_user_total_love + target_user_total_love
        target_user_total_allocated = target_user_total_allocated
        
        if (target_user_daily_next > source_user_daily_next):
            new_daily_next = target_user_daily_next
        else:
            new_daily_next = source_user_daily_next
        
        new_daily_streak = source_user_daily_streak + target_user_daily_streak
        
        new_count_daily_self = source_user_count_daily_self + target_user_count_daily_self
        new_count_daily_by_waifu = source_user_count_daily_by_waifu + target_user_count_daily_by_waifu
        new_count_daily_for_waifu = source_user_count_daily_for_waifu + target_user_count_daily_for_waifu
        new_count_top_gg_vote = source_user_count_top_gg_vote + target_user_count_top_gg_vote
        
        if target_user_waifu_cost >= source_user_waifu_cost:
            new_waifu_cost = target_user_waifu_cost
        else:
            new_waifu_cost = source_user_waifu_cost
        
        
        new_waifu_divorces = source_user_waifu_divorces + target_user_waifu_divorces
        
        if source_user_waifu_slots > target_user_waifu_slots:
            new_waifu_slots = source_user_waifu_slots
        else:
            new_waifu_slots = target_user_waifu_slots
        
        # transfer waifus
        
        await connector.execute(
            WAIFU_LIST_TABLE.update(
                waifu_list_model.user_id == source_user.id,
            ).values(
                user_id = target_user.id,
            )
        )
        
        await connector.execute(
            WAIFU_LIST_TABLE.update(
                waifu_list_model.waifu_id == source_user.id,
            ).values(
                waifu_id = target_user.id,
            )
        )
        
        # remove proposals
        
        await connector.execute(
            WAIFU_PROPOSAL_TABLE.delete().where(
                waifu_proposal_model.source_id.in_(
                    [
                        source_user.id,
                        target_user.id,
                    ],
                ),
            ).returning(
                waifu_proposal_model.investment,
            )
        )
        
        # Update tables
        
        if (source_user_entry_id != -1):
            await connector.execute(
                USER_COMMON_TABLE.delete().where(
                    user_common_model.id == source_user_entry_id,
                )
            )
        
        if (target_user_entry_id != -1):
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == target_user_entry_id,
                ).values(
                    total_love = new_total_love,
                    daily_next = new_daily_next,
                    daily_streak = new_daily_streak,
                    total_allocated = target_user_total_allocated,
                    waifu_cost = new_waifu_cost,
                    waifu_divorces = new_waifu_divorces,
                    waifu_slots = new_waifu_slots,
                    count_daily_self = new_count_daily_self,
                    count_daily_by_waifu = new_count_daily_by_waifu,
                    count_daily_for_waifu = new_count_daily_for_waifu,
                    count_top_gg_vote = new_count_top_gg_vote,
                )
            )
        
        else:
            await connector.execute(
                get_create_common_user_expression(
                    target_user.id,
                    total_love = new_total_love,
                    daily_next = new_daily_next,
                    daily_streak = new_daily_streak,
                    total_allocated = target_user_total_allocated,
                    waifu_cost = new_waifu_cost,
                    waifu_divorces = new_waifu_divorces,
                    waifu_slots = new_waifu_slots,
                    count_daily_self = new_count_daily_self,
                    count_daily_by_waifu = new_count_daily_by_waifu,
                    count_daily_for_waifu = new_count_daily_for_waifu,
                    count_top_gg_vote = new_count_top_gg_vote,
                )
            )
        
        # Transfer ownership
        await connector.execute(
            WAIFU_LIST_TABLE.update(
                waifu_list_model.waifu_id == source_user.id,
            ).values(
                waifu_id = target_user.id,
            )
        )
        
        # Transfer items
        
        # hah, witchcraft is not released yet!
        
        # Transfer counted emojis
        
        await connector.execute(
            EMOJI_COUNTER_TABLE.update(
                emoji_counter_model.user_id == source_user.id,
            ).values(
                user_id = target_user.id,
            )
        )
        
        # Transfer stickers
    
        await connector.execute(
            STICKER_COUNTER_TABLE.update(
                sticker_counter_model.user_id == source_user.id,
            ).values(
                user_id = target_user.id,
            )
        )
        
        # Transfer ds
        
        response = await connector.execute(
            select(
                [
                    ds_v2_model.id,
                    ds_v2_model.user_id,
                ]
            ).where(
                ds_v2_model.user_id.in_(
                    [
                        source_user.id,
                        target_user.id,
                    ]
                )
            )
        )

        results = await response.fetchall()
        result_count = len(results)
        
        if result_count == 0:
            source_user_ds_result = None
            target_user_ds_result = None
        else:
            if result_count == 1:
                source_user_ds_result = results[0]
                target_user_ds_result = None
            else:
                source_user_ds_result, target_user_ds_result = results
            
            if source_user_ds_result[1] != source_user.id:
                target_user_ds_result, source_user_ds_result = source_user_ds_result, target_user_ds_result
        
        if (source_user_ds_result is None):
            source_user_ds_entry_id = -1
        else:
            source_user_ds_entry_id = source_user_ds_result[0]
        
        if (target_user_ds_result is None):
            target_user_ds_entry_id = -1
        else:
            target_user_ds_entry_id = target_user_ds_result[0]
        
        if (source_user_ds_entry_id != -1):
            await connector.execute(
                DS_V2_TABLE.delete().where(
                    ds_v2_model.id == source_user_ds_entry_id,
                )
            )
            
            if (target_user_ds_entry_id == -1):
                response = await connector.execute(
                    DS_V2_TABLE.insert().values(
                        user_id = target_user.id,
                        game_state = None,
                        selected_stage_id = 0,
                    ).returning(
                        ds_v2_model.id,
                    )
                )
                result = await response.fetchone()
                target_user_ds_entry_id = result[0]
                
                await connector.execute(
                    DS_V2_RESULT_TABLE.update(
                        ds_v2_result_model.user_id == source_user.id,
                    ).values(
                        user_id = target_user.id,
                    )
                )
                
            else:
                response = await connector.execute(
                    DS_V2_RESULT_TABLE.delete().where(
                        ds_v2_result_model.user_id.in_(
                            [
                                target_user.id,
                                source_user.id,
                            ]
                        ),
                    ).returning(
                        ds_v2_result_model.stage_id,
                        ds_v2_result_model.best,
                    )
                )
                
                
                results = await response.fetchall()
                
                ds_result_relations = {}
                for stage_id, best in results:
                    try:
                        old_best = ds_result_relations[stage_id]
                    except KeyError:
                        pass
                    else:
                        if best <= old_best:
                            continue
                    
                    ds_result_relations[stage_id] = best
                
                data = [
                    {
                        'user_id': target_user.id,
                        'stage_id': stage_id,
                        'best': best,
                    } for stage_id, best in ds_result_relations.items()
                ]
                
                await connector.execute(insert(DS_V2_RESULT_TABLE, data))
                
    
    embed = Embed(
        f'You transferred {source_user.full_name}\'s data to {target_user.full_name}',
        color = COLOR__GAMBLING,
    )
    
    if (message is not None):
        embed.add_field('Message:', message)
    
    yield embed
    
    if target_user.bot:
        return
    
    try:
        target_user_channel = await client.channel_private_create(target_user)
    except ConnectionError:
        return
    
    embed = Embed(
        f'{source_user.full_name}\'s data has been transferred to you.',
        color = COLOR__GAMBLING,
    )
    
    if (message is not None):
        embed.add_field('Message:', message)
    
    try:
        await client.message_create(target_user_channel, embed = embed)
    except ConnectionError:
        return
    except DiscordException as err:
        if err.code == ERROR_CODES.cannot_message_user:
            return
        
        raise
