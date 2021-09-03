from math import floor

from hata import Client, Embed, mention_user_by_id, DiscordException, ERROR_CODES
from hata.ext.slash import InteractionResponse, abort

from bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE, get_create_common_user_expression, \
    waifu_list_model, WAIFU_LIST_TABLE, waifu_proposal_model, WAIFU_PROPOSAL_TABLE
from bot_utils.shared import EMOJI__HEART_CURRENCY, GUILD__NEKO_DUNGEON

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import func as alchemy_function, and_, distinct
from sqlalchemy.sql import select, desc

SLASH_CLIENT: Client

"""
y = 0
for x in range(0, 13):
    v = x*x*1000
    y += v
    print(y)
"""

WAIFU_COST_DEFAULT = 500

WAIFU_SLOT_COST_DEFAULT = 0

WAIFU_SLOT_2_COST = 5000
WAIFU_SLOT_3_COST = 14000
WAIFU_SLOT_4_COST = 30000
WAIFU_SLOT_5_COST = 55000
WAIFU_SLOT_6_COST = 91000
WAIFU_SLOT_7_COST = 140000
WAIFU_SLOT_8_COST = 204000
WAIFU_SLOT_9_COST = 285000
WAIFU_SLOT_10_COST = 385000
WAIFU_SLOT_11_COST = 506000
WAIFU_SLOT_12_COST = 650000


WAIFU_SLOT_NEXT_COSTS = {
    1: WAIFU_SLOT_2_COST,
    2: WAIFU_SLOT_3_COST,
    3: WAIFU_SLOT_4_COST,
    4: WAIFU_SLOT_5_COST,
    5: WAIFU_SLOT_6_COST,
    6: WAIFU_SLOT_7_COST,
    7: WAIFU_SLOT_8_COST,
    8: WAIFU_SLOT_9_COST,
    9: WAIFU_SLOT_10_COST,
    10: WAIFU_SLOT_11_COST,
    11: WAIFU_SLOT_12_COST,
}


GET_NUMBER_TH_ENDING = {
    1: 'st',
    2: 'nd',
    3: 'rd',
}

DEFAULT_TH_ENDING = 'th'

MAX_WAIFU_SLOTS = 12

def get_multiplier(user_id_1, user_id_2):
    return 2.1-(((user_id_1&0x1111111111111111111111)+(user_id_2&0x1111111111111111111111))%101*0.01)

@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def buy_waifu_slot(event):
    user_id = event.user.id
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.waifu_slots,
                    user_common_model.total_love,
                    user_common_model.total_allocated,
                ]
            ).where(
                user_common_model.user_id == user_id,
            )
        )
        
        results = await response.fetchall()
        if results:
            entry_id, waifu_slots, total_love, total_allocated = results[0]
            
            if waifu_slots >= MAX_WAIFU_SLOTS:
                return Embed(
                    None,
                    'You reached the maximal amount of waifu slots.',
                )
            
            available_love = total_love-total_allocated
            required_love = WAIFU_SLOT_NEXT_COSTS.get(waifu_slots, WAIFU_SLOT_COST_DEFAULT)
            
            if (required_love != WAIFU_SLOT_COST_DEFAULT) and (available_love > required_love):
                await connector.execute(
                    USER_COMMON_TABLE.update(
                        user_common_model.id == entry_id,
                    ).values(
                        total_love = user_common_model.total_love-required_love,
                        waifu_slots = user_common_model.waifu_slots+1,
                    )
                )
                
                return Embed(
                    'Great success!',
                    f'Your waifu slots have been increased to {waifu_slots+1} for '
                    f'{required_love} {EMOJI__HEART_CURRENCY.as_emoji}',
                )
        
        else:
            required_love = WAIFU_SLOT_2_COST
            waifu_slots = 1
    
    waifu_slots += 1
    return Embed(
        None,
        'You do not have enough available love to buy more waifu slots.\n'
        f'You need {required_love} {EMOJI__HEART_CURRENCY.as_emoji} to buy the {waifu_slots}'
        f'{GET_NUMBER_TH_ENDING.get(waifu_slots, DEFAULT_TH_ENDING)} slot.',
    )


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def waifu_info(event,
        user: ('user', 'The user to get') = None,
            ):
    
    if user is None:
        user = event.user
    
    user_id = user.id
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.waifu_owner_id,
                    user_common_model.waifu_cost,
                    user_common_model.waifu_divorces,
                    user_common_model.waifu_slots,
                ]
            ).where(
                user_common_model.user_id == user_id,
            )
        )
        
        results = await response.fetchall()
        if results:
            waifu_owner_id, waifu_cost, waifu_divorces, waifu_slots = results[0]
            
            response = await connector.execute(
                select(
                    [
                        waifu_list_model.waifu_id,
                    ]
                ).where(
                    waifu_list_model.user_id == user_id,
                )
            )
            
            results = await response.fetchall()
            if results:
                waifu_ids = sorted(result[0] for result in results)
            else:
                waifu_ids = None
        else:
            waifu_owner_id = 0
            waifu_cost = WAIFU_COST_DEFAULT
            waifu_divorces = 0
            waifu_slots = 1
            waifu_ids = None
    
    embed = Embed(
        f'{user.full_name}\'s waifu info'
    )
    
    if waifu_owner_id:
        field_value = mention_user_by_id(waifu_owner_id)
    else:
        field_value = '*none*'
    
    embed.add_field(
        f'Claimed by:',
        field_value,
        inline = True,
    )
    
    if not waifu_cost:
        waifu_cost = WAIFU_COST_DEFAULT
    
    embed.add_field(
        f'Cost:',
        str(waifu_cost),
        inline = True,
    )
    
    embed.add_field(
        'Divorces',
        str(waifu_divorces),
        inline = True,
    )
    
    embed.add_field(
        'Waifu slots',
        str(waifu_slots),
        inline = True,
    )
    
    if waifu_ids is None:
        field_value = '*none*'
    else:
        field_value = '\n'.join(mention_user_by_id(waifu_id) for waifu_id in waifu_ids)
    
    embed.add_field(
        'Waifus',
        field_value,
        inline = True,
    )
    
    return InteractionResponse(embed=embed, allowed_mentions=None)


# Work in progress

@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def propose(client, event,
        user: ('user', 'The user to propose to.'),
        amount: ('int', 'The amount of love to propose with.'),
            ):
    """Propose marriage to a user."""
    source_user_id = event.user.id
    target_user_id = user.id
    
    if source_user_id == target_user_id:
        abort('You cannot propose to yourself.')
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.user_id,
                    user_common_model.waifu_slots,
                    user_common_model.total_love,
                    user_common_model.total_allocated,
                    user_common_model.waifu_cost,
                    user_common_model.waifu_owner_id,
                ]
            ).where(
                user_common_model.user_id.in_(
                    [
                        source_user_id,
                        target_user_id,
                    ]
                )
            )
        )
        
        results = await response.fetchall()
        
        result_count = len(results)
        if result_count == 0:
            source_entry = None
            target_entry = None
        else:
            source_entry = results[0]
            
            if result_count == 2:
                target_entry = results[1]
            
            if (source_entry[1] != source_user_id):
                source_entry, target_entry = target_entry, source_entry
        
        if source_entry is None:
            source_entry_id = -1
            source_waifu_slots = 1
            source_total_love = 0
            source_total_allocated = 0
            
            source_waifu_count = 0
            proposed_user_ids = None
        else:
            source_entry_id = source_entry[0]
            source_waifu_slots = source_entry[2]
            source_total_love = source_entry[3]
            source_total_allocated = source_entry[4]
            
            response = await connector.execute(
                select(
                    [
                         alchemy_function.count(waifu_list_model.waifu_id),
                    ]
                ).where(
                    waifu_list_model.user_id == source_user_id,
                )
            )
            
            source_waifu_count = (await response.fetchone())[0]
            
            response = await connector.execute(
                select(
                    [
                        waifu_proposal_model.id,
                        waifu_proposal_model.target_id,
                        waifu_proposal_model.investment,
                    ]
                ).where(
                    waifu_proposal_model.source_id == source_user_id
                )
            )
            
            results = await response.fetchall()
            if results:
                proposed_user_ids = {result[1]:(result[0], result[2]) for result in results}
            else:
                proposed_user_ids = None
        
        
        if target_entry is None:
            target_entry_id = -1
            target_waifu_cost = WAIFU_COST_DEFAULT
            target_waifu_owner_id = 0
        else:
            target_entry_id = target_entry[0]
            target_waifu_owner_id = target_entry[6]
            
            target_waifu_cost = target_entry[5]
            if not target_waifu_cost:
                target_waifu_cost = WAIFU_COST_DEFAULT
        
        
        required_love = floor(target_waifu_cost*get_multiplier(source_user_id, target_user_id))
        
        # Case 1: the user has not enough money
        if amount < required_love:
            yield Embed(
                None,
                f'You need to propose with at least {required_love} {EMOJI__HEART_CURRENCY.as_emoji} to '
                f'{user.full_name}.'
            )
            return
        
        # Case 2-4: The user already proposing
        if (proposed_user_ids is not None):
            try:
                proposal_entry_id, investment = proposed_user_ids[target_user_id]
            except KeyError:
                pass
            else:
                # Case 2: Both amount and investment are the same. No change is needed.
                if amount == investment:
                    yield Embed(
                        None,
                        f'You are already proposing to {user.full_name} with {amount} '
                        f'{EMOJI__HEART_CURRENCY.as_emoji}.'
                    )
                    return
                
                available_love = source_total_love-source_total_allocated+investment
                
                # Case 3: The user has not enough love even with proposition
                if available_love < amount:
                    embed_description_parts = []
                    
                    embed_description_parts.append('You do not have ')
                    embed_description_parts.append(repr(amount))
                    embed_description_parts.append(' ')
                    embed_description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
                    embed_description_parts.append(' to propose to ')
                    embed_description_parts.append(user.full_name)
                    embed_description_parts.append(
                        '.\n'
                        '\n'
                        'You have '
                    )
                    embed_description_parts.append(repr(source_total_love))
                    embed_description_parts.append(' ')
                    embed_description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
                    embed_description_parts.append(' love')
                    
                    if source_total_allocated:
                        embed_description_parts.append('(')
                        embed_description_parts.append(repr(source_total_allocated))
                        embed_description_parts.append(' in use).')
                    
                    embed_description_parts.append(
                        '\n'
                        'And additional '
                    )
                    embed_description_parts.append(repr(investment))
                    embed_description_parts.append(' ')
                    embed_description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
                    embed_description_parts.append(' already proposed.')
                    
                    yield Embed(
                        None,
                        ''.join(embed_description_parts)
                    )
                    return
                
                # Case 4: The user can modify it's actual proposition
                await connector.execute(
                    WAIFU_PROPOSAL_TABLE.update(
                        waifu_proposal_model.id == proposal_entry_id
                    ).values(
                        investment = amount,
                    )
                )
                
                await connector.execute(
                    USER_COMMON_TABLE.update(
                        user_common_model.id == source_entry_id,
                    ).values(
                        total_love = user_common_model.total_love-(amount-investment),
                    )
                )
                
                yield Embed(
                    None,
                    f'You changed your proposition towards {user.full_name} from {investment} '
                    f'{EMOJI__HEART_CURRENCY.as_emoji} to {amount} {EMOJI__HEART_CURRENCY.as_emoji}.'
                )
                
                try:
                    target_user_channel = await client.channel_private_create(user)
                except ConnectionError:
                    return
                
                try:
                    await client.message_create(
                        target_user_channel,
                        embed = Embed(
                            None,
                            f'{event.user.full_name} changed their proposition towards you from {investment} '
                            f'{EMOJI__HEART_CURRENCY.as_emoji} to {amount} {EMOJI__HEART_CURRENCY.as_emoji}.'
                        )
                    )
                except ConnectionError:
                    return
                
                except DiscordException as err:
                    if err.code == ERROR_CODES.cannot_message_user:
                        return
                    
                    raise
                
                return
        
        # case 5: The user can not propose more.
        if proposed_user_ids is None:
            proposed_user_count = 0
        else:
            proposed_user_count = len(proposed_user_ids)
        
        if source_waifu_slots-source_waifu_count-proposed_user_count <= 0:
            yield Embed(
                None,
                f'You can not propose to more users.\n'
                f'Waifu slots: {source_waifu_slots}\n'
                f'Waifus: {source_waifu_count}\n'
                f'Propositions: {proposed_user_count}'
            )
            
            return
        
        # case 6: The proposition amount is under required amount
        available_love = source_total_love-source_total_allocated
        if amount > available_love:
            embed_description_parts = []
            
            embed_description_parts.append('You do not have ')
            embed_description_parts.append(repr(amount))
            embed_description_parts.append(' ')
            embed_description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
            embed_description_parts.append(' to propose to ')
            embed_description_parts.append(user.full_name)
            embed_description_parts.append(
                '.\n'
                '\n'
                'You have '
            )
            embed_description_parts.append(repr(source_total_love))
            embed_description_parts.append(' ')
            embed_description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
            embed_description_parts.append(' love')
            
            if source_total_allocated:
                embed_description_parts.append('(')
                embed_description_parts.append(repr(source_total_allocated))
                embed_description_parts.append(' in use).')
            
            yield Embed(
                None,
                ''.join(embed_description_parts)
            )
            return
        
        # case 7: Proposing to a bot
        if user.is_bot:
            love_increase = (amount>>1)
            if target_entry_id == -1:
                to_execute = get_create_common_user_expression(
                    target_user_id,
                    total_love = love_increase,
                    waifu_owner_id = source_user_id,
                )
            else:
                to_execute = USER_COMMON_TABLE.update(
                    user_common_model.id == target_entry_id,
                ).values(
                    total_love = user_common_model.total_love+love_increase,
                    waifu_owner_id = source_user_id,
                )
                
                if target_waifu_owner_id:
                    to_execute.values(
                        waifu_divorces = user_common_model.waifu_divorces + 1,
                    )
            
            await connector.execute(to_execute)
            
            if target_waifu_owner_id:
                to_execute = WAIFU_LIST_TABLE.update(
                    waifu_list_model.waifu_id == target_user_id,
                ).values(
                    user_id = source_user_id,
                )
            else:
                to_execute = WAIFU_LIST_TABLE.insert().values(
                    user_id = source_user_id,
                    waifu_id = target_user_id,
                )
            
            await connector.execute(to_execute)
            
            yield Embed(
                None,
                f'You married {user.full_name} with {amount} {EMOJI__HEART_CURRENCY.as_emoji}.'
            )
            return
        
        # Case 8: Proposing to a user account
        await connector.execute(
            WAIFU_PROPOSAL_TABLE.insert().values(
                source_id = source_user_id,
                target_id = target_user_id,
                investment = amount,
            )
        
        )
        
        await connector.execute(
            USER_COMMON_TABLE.update(
                user_common_model.id == source_entry_id,
            ).values(
                total_love = user_common_model.total_love-amount,
            )
        )
        
        yield Embed(
            None,
            f'You proposed towards {user.full_name} with {amount} {EMOJI__HEART_CURRENCY.as_emoji}.'
        )
        
        try:
            target_user_channel = await client.channel_private_create(user)
        except ConnectionError:
            return
        
        try:
            await client.message_create(
                target_user_channel,
                embed = Embed(
                    None,
                    f'{event.user.full_name} proposed to you with {amount} {EMOJI__HEART_CURRENCY.as_emoji}.'
                )
            )
        except ConnectionError:
            return
        
        except DiscordException as err:
            if err.code == ERROR_CODES.cannot_message_user:
                return
            
            raise
        
        return


PROPOSITIONS = SLASH_CLIENT.interactions(
    None,
    name = 'propositions',
    description = 'Lists propositions',
    guild = GUILD__NEKO_DUNGEON
)

@PROPOSITIONS.interactions
async def outgoing(event,
        user: ('user', 'The user to list propositions of.') = None,
            ):
    """Lists outgoing propositions."""
    return await list_propositions(event, user, True)

@PROPOSITIONS.interactions
async def incoming(event,
        user: ('user', 'The user to list proposals of.') = None,
            ):
    """Lists incoming propositions."""
    return await list_propositions(event, user, False)

async def list_propositions(event, user, outgoing):
    if user is None:
        user = event.user
    
    user_id = user.id
    
    async with DB_ENGINE.connect() as connector:
        if outgoing:
            to_execute = select(
                [
                    waifu_proposal_model.target_id,
                    waifu_proposal_model.investment,
                ]
            ).where(
                waifu_proposal_model.source_id == user_id
            )
        else:
            to_execute = select(
                [
                    waifu_proposal_model.source_id,
                    waifu_proposal_model.investment,
                ]
            ).where(
                waifu_proposal_model.target_id == user_id
            )
        
        response = await connector.execute(to_execute)
        
        results = await response.fetchall()
    
    embed_description_parts = []
    
    length = len(results)
    if length:
        index = 0
        while True:
            target_id, investment = results[index]
            index += 1
            embed_description_parts.append(mention_user_by_id(target_id))
            embed_description_parts.append(' ')
            embed_description_parts.append(repr(investment))
            embed_description_parts.append(' ')
            embed_description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
            
            if index == length:
                break
            
            embed_description_parts.append('\n')
    
    else:
        embed_description_parts.append('*no result*')
    
    description = ''.join(embed_description_parts)
    
    if outgoing:
        title = f'Outgoing propositions of {user.full_name}'
    else:
        title = f'Incoming propositions to {user.full_name}'
    
    embed = Embed(
        title,
        description,
    ).add_thumbnail(
        user.avatar_url,
    )
    
    return InteractionResponse(embed=embed, allowed_mentions=None)


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON)
async def accept_proposition(client, event,
        user: ('user', 'Who\'s proposition to accept?'),
            ):
    target_user_id = event.user.id
    source_user_id = user.id
    
    if target_user_id == source_user_id:
        abort('Select someone else.')
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            WAIFU_PROPOSAL_TABLE.delete().where(
                and_(
                    waifu_proposal_model.source_id == source_user_id,
                    waifu_proposal_model.target_id == target_user_id,
                )
            ).returning(
                waifu_proposal_model.investment,
            )
        )
        
        results = await response.fetchall()
        if not results:
            yield Embed(
                None,
                f'{user.full_name} is not proposing to you.'
            )
            return
        
        investment = results[0][0]
        
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.waifu_owner_id,
                ]
            ).where(
                user_common_model.user_id == target_user_id,
            )
        )
        
        results = await response.fetchall()
        if response:
            entry_id, waifu_owner_id = results[0]
        else:
            entry_id = -1
            waifu_owner_id = 0
        
        love_increase = (investment>>1)
        if entry_id == -1:
            to_execute = get_create_common_user_expression(
                target_user_id,
                total_love = love_increase,
                waifu_owner_id = source_user_id,
            )
        else:
            to_execute = USER_COMMON_TABLE.update(
                user_common_model.id == entry_id,
            ).values(
                total_love = user_common_model.total_love+love_increase,
                waifu_owner_id = source_user_id,
            )
            
            if waifu_owner_id:
                to_execute.values(
                    waifu_divorces = user_common_model.waifu_divorces + 1,
                )
        
        await connector.execute(to_execute)
        
        if waifu_owner_id:
            to_execute = WAIFU_LIST_TABLE.update(
                waifu_list_model.waifu_id == target_user_id,
            ).values(
                user_id = source_user_id,
            )
        else:
            to_execute = WAIFU_LIST_TABLE.insert().values(
                user_id = source_user_id,
                waifu_id = target_user_id,
            )
        
        await connector.execute(to_execute)
        
        
        yield Embed(
            None,
            f'You accepted the proposal from {user.full_name}.\n'
            f'\n'
            f'You received {love_increase} {EMOJI__HEART_CURRENCY.as_emoji}.'
        )
        
        try:
            target_user_channel = await client.channel_private_create(user)
        except ConnectionError:
            return
        
        try:
            await client.message_create(
                target_user_channel,
                embed = Embed(
                    None,
                    f'{event.user.full_name} accepted your proposal.'
                )
            )
        except ConnectionError:
            return
        
        except DiscordException as err:
            if err.code == ERROR_CODES.cannot_message_user:
                return
            
            raise
        
        return


