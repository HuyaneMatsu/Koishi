__all__ = ()

from math import floor
from re import compile as re_compile

from hata import Embed
from hata.ext.slash import Button, InteractionResponse, Row, abort
from scarletio import copy_docs
from sqlalchemy import and_, func as alchemy_function, or_
from sqlalchemy.sql import select

from ..bot_utils.constants import EMOJI__HEART_CURRENCY, WAIFU_COST_DEFAULT
from ..bot_utils.models import (
    DB_ENGINE, WAIFU_LIST_TABLE, WAIFU_PROPOSAL_TABLE, waifu_list_model, waifu_proposal_model
)
from ..bot_utils.user_getter import get_user, get_users_unordered
from ..bot_utils.utils import send_embed_to
from ..bots import FEATURE_CLIENTS

from .marriage_slot import BUY_WAIFU_SLOT_INVOKE_COMPONENT, EMOJI_NO, EMOJI_YES
from .user_balance import get_user_balance, get_user_balances
from .user_settings import (
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_DISABLE, get_one_user_settings_with_connector,
    get_preferred_client_for_user
)


CUSTOM_ID_DIVORCE_CANCEL = 'marriage.divorce.cancel'

BUTTON_DIVORCE_CANCEL = Button(
    'No',
    EMOJI_NO,
    custom_id = CUSTOM_ID_DIVORCE_CANCEL,
)

def get_multiplier(user_id_1, user_id_2):
    return 2.1 - (((user_id_1 & 0x1111111111111111111111) + (user_id_2 & 0x1111111111111111111111)) % 101 * 0.01)


@FEATURE_CLIENTS.interactions(is_global = True)
async def waifu_info(event,
    user: ('user', 'The user to get') = None,
):
    if user is None:
        user = event.user
    
    yield
    
    user_id = user.id
    
    user_balance = await get_user_balance(user_id)
    waifu_owner_id = user_balance.waifu_owner_id
    
    waifu_ids = await get_related_ids(user_id)
    waifu_ids.discard(waifu_owner_id)
    
    embed = Embed(
        f'{user:f}\'s waifu info',
    ).add_thumbnail(
        user.avatar_url
    )
    
    if waifu_owner_id:
        waifu_owner = await get_user(waifu_owner_id)
    
        field_value = waifu_owner.full_name
    else:
        field_value = '*none*'
    
    embed.add_field(
        f'Claimed by:',
        field_value,
        inline = True,
    )
    
    waifu_cost = user_balance.waifu_cost or WAIFU_COST_DEFAULT
    
    embed.add_field(
        f'Minimal cost:',
        f'{floor(waifu_cost * 1.1)} - {floor(waifu_cost * 2.1)} {EMOJI__HEART_CURRENCY}',
        inline = True,
    )
    
    embed.add_field(
        'Divorces',
        str(user_balance.waifu_divorces),
        inline = True,
    )
    
    if not waifu_ids:
        field_value = '*none*'
        waifu_count_value = '0'
    else:
        waifu_names = []
        
        for waifu_id in sorted(waifu_ids):
            waifu = await get_user(waifu_id)
            waifu_names.append(waifu.full_name)
        
        field_value = '\n'.join(waifu_names)
        waifu_count_value = repr(len(waifu_ids))
    
    embed.add_field(
        f'Waifus ({waifu_count_value} / {user_balance.waifu_slots})',
        field_value,
        inline = True,
    )
    
    event_user = event.user
    event_user_id = event_user.id
    if (user_id != event_user_id) and (waifu_owner_id != event_user_id):
        embed.add_footer(
            f'To buy {user:f} you need at least {floor(get_multiplier(event_user_id, user_id) * waifu_cost)} love.',
            icon_url = event_user.avatar_url,
        )
    
    yield InteractionResponse(embed = embed, allowed_mentions = None)


@FEATURE_CLIENTS.interactions(is_global = True)
async def propose(
    client,
    event,
    target_user: ('user', 'The user to propose to.', 'user'),
    amount: ('int', 'The amount of love to propose with.'),
):
    """Propose marriage to a user."""
    source_user_id = event.user.id
    target_user_id = target_user.id
    
    if source_user_id == target_user_id:
        abort('You cannot propose to yourself.')
    
    async with DB_ENGINE.connect() as connector:
        user_balances = await get_user_balances((source_user_id, target_user_id),)
        source_user_balance = user_balances[source_user_id]
        target_user_balance = user_balances[target_user_id]
        
        source_waifu_slots = source_user_balance.waifu_slots
        source_balance = source_user_balance.balance
        source_allocated = source_user_balance.allocated
        
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
            proposed_user_ids = {result[1] : (result[0], result[2]) for result in results}
        else:
            proposed_user_ids = None
        
        target_waifu_owner_id = target_user_balance.owner_id
        target_waifu_cost = target_user_balance.waifu_cost or WAIFU_COST_DEFAULT
        
        target_user_user_settings = await get_one_user_settings_with_connector(target_user_id, connector)
        
        required_love = floor(target_waifu_cost * get_multiplier(source_user_id, target_user_id))
        
        # Case 1: the user has not enough money
        if amount < required_love:
            yield Embed(
                None,
                f'You need to propose with at least {required_love} {EMOJI__HEART_CURRENCY} to '
                f'{target_user:f}.'
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
                        f'You are already proposing to {target_user:f} with {amount} '
                        f'{EMOJI__HEART_CURRENCY}.'
                    )
                    return
                
                available = source_balance - source_allocated + investment
                
                # Case 3: The user has not enough love even with proposal
                if available < amount:
                    embed_description_parts = []
                    
                    embed_description_parts.append('You do not have ')
                    embed_description_parts.append(repr(amount))
                    embed_description_parts.append(' ')
                    embed_description_parts.append(EMOJI__HEART_CURRENCY)
                    embed_description_parts.append(' to propose to ')
                    embed_description_parts.append(target_user.full_name)
                    embed_description_parts.append(
                        '.\n'
                        '\n'
                        'You have '
                    )
                    embed_description_parts.append(repr(available))
                    embed_description_parts.append(' ')
                    embed_description_parts.append(EMOJI__HEART_CURRENCY)
                    
                    if source_allocated:
                        embed_description_parts.append('(')
                        embed_description_parts.append(repr(source_allocated))
                        embed_description_parts.append(' in use).')
                    
                    embed_description_parts.append(
                        '\n'
                        'And additional '
                    )
                    embed_description_parts.append(repr(investment))
                    embed_description_parts.append(' ')
                    embed_description_parts.append(EMOJI__HEART_CURRENCY)
                    embed_description_parts.append(' already proposed.')
                    
                    yield Embed(
                        None,
                        ''.join(embed_description_parts)
                    )
                    return
                
                # Case 4: The user can modify it's actual proposal
                await connector.execute(
                    WAIFU_PROPOSAL_TABLE.update(
                        waifu_proposal_model.id == proposal_entry_id
                    ).values(
                        investment = amount,
                    )
                )
                
                source_user_balance.set('balance', source_user_balance.balance - (amount - investment))
                await source_user_balance.save()
                
                yield Embed(
                    None,
                    f'You changed your proposal towards {target_user:f} from {investment} '
                    f'{EMOJI__HEART_CURRENCY} to {amount} {EMOJI__HEART_CURRENCY}.'
                )
                
                if target_user_user_settings.notification_proposal:
                    await send_embed_to(
                        get_preferred_client_for_user(target_user, target_user_user_settings.preferred_client_id, client),
                        target_user_id,
                        Embed(
                            None,
                            f'{event.user:f} changed their proposal towards you from {investment} '
                            f'{EMOJI__HEART_CURRENCY} to {amount} {EMOJI__HEART_CURRENCY}.'
                        )
                    )
                
                return
        
        # case 5: The user can not propose more.
        if proposed_user_ids is None:
            proposed_user_count = 0
        else:
            proposed_user_count = len(proposed_user_ids)
        
        if source_waifu_slots - source_waifu_count - proposed_user_count <= 0:
            yield InteractionResponse(
                embed = Embed(
                    'You can not propose to more users.',
                    (
                        f'Waifu slots: {source_waifu_slots}\n'
                        f'Waifus: {source_waifu_count}\n'
                        f'Propositions: {proposed_user_count}'
                    ),
                ).add_footer(
                    'To buy more waifu slot, use: /shop waifu-slot'
                ),
                components = BUY_WAIFU_SLOT_INVOKE_COMPONENT,
            )
            return
        
        # case 6: The proposal amount is under required amount.
        available = source_balance - source_allocated
        if amount > available:
            embed_description_parts = []
            
            embed_description_parts.append('You do not have ')
            embed_description_parts.append(repr(amount))
            embed_description_parts.append(' ')
            embed_description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
            embed_description_parts.append(' to propose to ')
            embed_description_parts.append(target_user.full_name)
            embed_description_parts.append(
                '.\n'
                '\n'
                'You have '
            )
            embed_description_parts.append(repr(available))
            embed_description_parts.append(' ')
            embed_description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
            
            if source_allocated:
                embed_description_parts.append('(')
                embed_description_parts.append(repr(source_allocated))
                embed_description_parts.append(' in use).')
            
            yield Embed(
                None,
                ''.join(embed_description_parts)
            )
            return
        
        # case 7: Proposing to a bot
        if target_user.bot:
            love_increase = (amount >> 1)
            
            target_user_balance.set('balance', target_user_balance.balance + love_increase)
            target_user_balance.set('waifu_owner_id', source_user_id)
            target_user_balance.set('waifu_cost', amount)
            if target_waifu_owner_id:
                target_user_balance.set('waifu_divorces', target_user_balance.waifu_divorces + 1)
            await target_user_balance.save()
            
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
                f'You married {target_user:f} with {amount} {EMOJI__HEART_CURRENCY}.'
            )
            
            # Notify the divorced if not bot.
            if target_waifu_owner_id:
                owner = await client.user_get(target_waifu_owner_id)
                if not owner.bot:
                    owner_user_settings = await get_one_user_settings_with_connector(target_waifu_owner_id, connector)
                    await send_embed_to(
                        get_preferred_client_for_user(owner, owner_user_settings.preferred_client_id, client),
                        target_waifu_owner_id,
                        Embed(
                            None,
                            f'{event.user:f} divorced you in favor of marrying {target_user:f} instead.'
                        )
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
        
        source_user_balance.set('balance', source_user_balance.balance - amount)
        await source_user_balance.save()
        
        
        yield Embed(
            None,
            f'You proposed towards {target_user:f} with {amount} {EMOJI__HEART_CURRENCY}.'
        )
        
        
        if target_user_user_settings.notification_proposal:
            await send_embed_to(
                get_preferred_client_for_user(target_user, target_user_user_settings.preferred_client_id, client),
                target_user_id,
                Embed(
                    None,
                    f'{event.user:f} proposed to you with {amount} {EMOJI__HEART_CURRENCY}.'
                ),
                Button(
                    'I don\'t want notifs, nya!!',
                    custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_PROPOSAL_DISABLE,
                )
            )


PROPOSAL = FEATURE_CLIENTS.interactions(
    None,
    name = 'proposal',
    description = 'Commands to handle proposals.',
    is_global = True,
)

@PROPOSAL.interactions
async def list_outgoing(
    event,
    user: ('user', 'The user to list proposals of.') = None,
):
    """Lists outgoing proposals."""
    yield
    yield await list_proposals(event, user, True)


@PROPOSAL.interactions
async def list_incoming(
    event,
    user: ('user', 'The user to list proposals of.') = None,
):
    """Lists incoming proposals."""
    yield
    yield await list_proposals(event, user, False)


async def list_proposals(event, user, outgoing):
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
                waifu_proposal_model.source_id == user_id,
            )
        else:
            to_execute = select(
                [
                    waifu_proposal_model.source_id,
                    waifu_proposal_model.investment,
                ]
            ).where(
                waifu_proposal_model.target_id == user_id,
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
            requested_user = await get_user(target_id)
            embed_description_parts.append(requested_user.full_name)
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
        title = f'Proposals from {user:f}'
    else:
        title = f'Proposals to {user:f}'
    
    embed = Embed(
        title,
        description,
    ).add_thumbnail(
        user.avatar_url,
    )
    
    return InteractionResponse(embed = embed, allowed_mentions = None)


async def get_proposing_ids(user_id, outgoing):
    async with DB_ENGINE.connect() as connector:
        if outgoing:
            to_execute = select(
                [
                    waifu_proposal_model.target_id,
                ]
            ).where(
                waifu_proposal_model.source_id == user_id,
            )
        else:
            to_execute = select(
                [
                    waifu_proposal_model.source_id,
                ]
            ).where(
                waifu_proposal_model.target_id == user_id,
            )
        
        response = await connector.execute(to_execute)
        
        results = await response.fetchall()
        
        return [waifu_id for (waifu_id,) in results]


async def get_one_proposing_with_name(event, name, outgoing):
    user_id = event.user.id
    waifu_ids = await get_proposing_ids(user_id, outgoing)
    waifus = await get_users_unordered(waifu_ids)
    
    for waifu in waifus:
        if waifu.has_name_like_at(name, event.guild_id):
            return waifu


async def get_all_proposing_with_name(event, value, outgoing):
    user_id = event.user.id
    waifu_ids = await get_proposing_ids(user_id, outgoing)
    waifus = await get_users_unordered(waifu_ids)
    
    if value is not None:
        waifus = [waifu for waifu in waifus if waifu.has_name_like_at(value, event.guild_id)]
    
    return waifus


@PROPOSAL.interactions
async def accept(
    client,
    event,
    target_user_name: (str, 'Who\'s proposal to accept?', 'user'),
):
    target_user = await get_one_proposing_with_name(event, target_user_name, False)
    if (target_user is None):
        if len(target_user_name) > 100:
            target_user_name = target_user_name[:100] + '...'
        
        abort(f'User not found: `{target_user_name}`')
        return
    
    source_user_id = event.user.id
    target_user_id = target_user.id
    
    if source_user_id == target_user_id:
        abort('Select someone else.')
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            WAIFU_PROPOSAL_TABLE.delete().where(
                and_(
                    waifu_proposal_model.source_id == target_user_id,
                    waifu_proposal_model.target_id == source_user_id,
                )
            ).returning(
                waifu_proposal_model.investment,
            )
        )
        
        result = await response.fetchone()
        if (result is None):
            yield Embed(
                None,
                f'{target_user:f} is not proposing to you.'
            )
            return
        
        investment = result[0]
        
        user_balance = await get_user_balance(source_user_id)
        waifu_owner_id = user_balance.waifu_owner_id
        love_increase = (investment >> 1)
        user_balance.set('balance', user_balance.balance + love_increase)
        user_balance.set('waifu_cost', investment)
        user_balance.set('waifu_owner_id', waifu_owner_id)
        if waifu_owner_id:
            user_balance.set('waifu_divorces', user_balance.waifu_divorces + 1)
        await user_balance.save()
        
        if waifu_owner_id:
            to_execute = WAIFU_LIST_TABLE.update(
                waifu_list_model.waifu_id == source_user_id,
            ).values(
                user_id = target_user_id,
            )
        else:
            to_execute = WAIFU_LIST_TABLE.insert().values(
                user_id = target_user_id,
                waifu_id = source_user_id,
            )
        
        await connector.execute(to_execute)
    
    
    yield Embed(
        None,
        f'You accepted the proposal from {target_user:f}.\n'
        f'\n'
        f'You received {love_increase} {EMOJI__HEART_CURRENCY}.'
    )
    
    await send_embed_to(
        client,
        target_user_id,
        Embed(
            None,
            f'{event.user:f} accepted your proposal.',
        )
    )
    
    # Notify the divorced if not bot.
    if waifu_owner_id:
        owner = await client.user_get(waifu_owner_id)
        if not owner.bot:
            await send_embed_to(
                client,
                waifu_owner_id,
                Embed(
                    None,
                    f'{event.user:f} divorced you in favor of marrying {target_user:f} instead.',
                )
            )


@accept.autocomplete('target_user_name')
async def autocomplete_accept_user_name(event, value):
    waifus = await get_all_proposing_with_name(event, value, False)
    return sorted(waifu.full_name for waifu in waifus)


@PROPOSAL.interactions
async def reject(
    client,
    event,
    target_user_name: (str, 'The user, who\'s proposal you want to reject.', 'user'),
):
    target_user = await get_one_proposing_with_name(event, target_user_name, False)
    if (target_user is None):
        if len(target_user_name) > 100:
            target_user_name = target_user_name[:100] + '...'
        
        abort(f'User not found: `{target_user_name}`')
        return
    
    target_user_id = target_user.id
    source_user_id = event.user.id
    
    if source_user_id == target_user_id:
        abort('Select someone else.')
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            WAIFU_PROPOSAL_TABLE.delete().where(
                and_(
                    waifu_proposal_model.source_id == target_user_id,
                    waifu_proposal_model.target_id == source_user_id,
                )
            ).returning(
                waifu_proposal_model.investment,
            )
        )
        
        result = await response.fetchone()
        
        if (result is None):
            yield Embed(
                None,
                f'{target_user:f} is not proposing to you.'
            )
            return
        
        investment = result[0]
        
        user_balance = await get_user_balance(target_user_id)
        user_balance.set('balance', user_balance.balance + investment)
        await user_balance.save()
        
        target_user_user_settings = await get_one_user_settings_with_connector(
            target_user_id, connector
        )
    
    
    yield Embed(
        None,
        f'You rejected the proposal from {target_user:f}.'
    )
    
    await send_embed_to(
        get_preferred_client_for_user(target_user, target_user_user_settings.preferred_client_id, client),
        target_user_id,
        Embed(
            None,
            (
                f'{event.user:f} rejected your proposal.\n'
                f'\n'
                f'You got your {investment} {EMOJI__HEART_CURRENCY} back.'
            ),
        )
    )


@reject.autocomplete('target_user_name')
async def autocomplete_reject_user_name(event, value):
    waifus = await get_all_proposing_with_name(event, value, False)
    return sorted(waifu.full_name for waifu in waifus)


@PROPOSAL.interactions
async def cancel(
    client,
    event,
    target_user_name: (str, 'The user, who\'s proposal you want to cancel.', 'user'),
):
    target_user = await get_one_proposing_with_name(event, target_user_name, True)
    if (target_user is None):
        if len(target_user_name) > 100:
            target_user_name = target_user_name[:100] + '...'
        
        abort(f'User not found: `{target_user_name}`')
        return
    
    source_user_id = event.user.id
    target_user_id = target_user.id
    
    if source_user_id == target_user_id:
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
                f'You are not proposing towards {target_user:f}.',
            )
            return
        
        investment = results[0][0]
        
        user_balance = await get_user_balance(source_user_id)
        user_balance.set('balance', user_balance.balance + investment)
        await user_balance.save()
        
        target_user_user_settings = await get_one_user_settings_with_connector(
            target_user_id, connector
        )
    
    yield Embed(
        None,
        f'You canceled the proposal towards {target_user:f}.'
        f'\n'
        f'You got your {investment} {EMOJI__HEART_CURRENCY} back.'
    )
    
    
    if (not target_user.bot) and target_user_user_settings.notification_proposal:
        await send_embed_to(
            get_preferred_client_for_user(target_user, target_user_user_settings.preferred_client_id, client),
            target_user_id,
            Embed(
                None,
                f'{event.user:f} cancelled the proposal towards you.'
            )
        )


@cancel.autocomplete('target_user_name')
async def autocomplete_reject_user_name(event, value):
    waifus = await get_all_proposing_with_name(event, value, True)
    return sorted(waifu.full_name for waifu in waifus)


async def are_related(source_user_id, target_user_id):
    """
    Returns whether the two users are related.
    
    This function is a coroutine.
    
    Parameters
    ----------
    source_user_id : `int`
        Source user's identifier.
    
    target_user : `int`
        Target user's identifier.
    
    Returns
    -------
    related : `bool`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    waifu_list_model.id,
                ]
            ).where(
                or_(
                    and_(
                        waifu_list_model.user_id == source_user_id,
                        waifu_list_model.waifu_id == target_user_id,
                    ),
                    and_(
                        waifu_list_model.user_id == target_user_id,
                        waifu_list_model.waifu_id == source_user_id,
                    ),
                )
            )
        )
        
        return response.rowcount > 0


if (DB_ENGINE is None):
    @copy_docs(are_related)
    async def are_related(user_id):
        return False


async def get_related_ids(user_id):
    """
    Gets the users identifiers who are related to the given user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to request their relateds of.
    
    Returns
    -------
    related_ids : `set<int>`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    waifu_list_model.user_id,
                ]
            ).where(
                waifu_list_model.waifu_id == user_id,
            ).union(
                select(
                    [
                        waifu_list_model.waifu_id,
                    ]
                ).where(
                    waifu_list_model.user_id == user_id,
                )
            )
        )

        entries = await response.fetchall()
        return {entry[0] for entry in entries}


if (DB_ENGINE is None):
    @copy_docs(get_related_ids)
    async def get_related_ids(user_id):
        return [859886212251779083]


async def get_one_divorce_with_name(event, name):
    user_id = event.user.id
    waifu_ids = await get_related_ids(user_id)
    waifus = await get_users_unordered(waifu_ids)
    
    for waifu in waifus:
        if waifu.has_name_like_at(name, event.guild_id):
            return waifu


async def get_all_divorce_with_name(event, value):
    user_id = event.user.id
    waifu_ids = await get_related_ids(user_id)
    waifus = await get_users_unordered(waifu_ids)
    
    if value is not None:
        waifus = [waifu for waifu in waifus if waifu.has_name_like_at(value, event.guild_id)]
    
    return waifus


@FEATURE_CLIENTS.interactions(is_global = True)
async def divorce(
    client,
    event,
    target_user_name: (str, 'Who do you want to divorce?', 'user'),
):
    target_user = await get_one_divorce_with_name(event, target_user_name)
    if (target_user is None):
        if len(target_user_name) > 100:
            target_user_name = target_user_name[:100] + '...'
        
        abort(f'Waifu not found: `{target_user_name}`')
        return
    
    source_user_id = event.user.id
    target_user_id = target_user.id
    
    if source_user_id == target_user_id:
        abort('Cannot divorce yourself, but nice try.')
    
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    waifu_list_model.id,
                ]
            ).where(
                and_(
                    waifu_list_model.user_id == source_user_id,
                    waifu_list_model.waifu_id == target_user_id,
                )
            )
        )
        
        is_outgoing = True if response.rowcount else False
    
    
    user_balance = await get_user_balance(source_user_id)
    is_incoming = user_balance.waifu_owner_id == target_user_id
    
    
    if is_incoming:
        allocated = user_balance.allocated
        waifu_cost = user_balance.waifu_cost or WAIFU_COST_DEFAULT
        available = user_balance.balance - allocated
        
        if available < waifu_cost:
            embed_description_parts = []
            embed_description_parts.append('You don\'t have enough ')
            embed_description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
            embed_description_parts.append(f' to divorce ')
            embed_description_parts.append(target_user.full_name)
            embed_description_parts.append(
                '.\n'
                '\n'
                'You need '
            )
            embed_description_parts.append(repr(waifu_cost))
            embed_description_parts.append(' ')
            embed_description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
            embed_description_parts.append(', but you only have ')
            embed_description_parts.append(repr(available))
            embed_description_parts.append(' ')
            embed_description_parts.append(EMOJI__HEART_CURRENCY.as_emoji)
            
            if allocated:
                embed_description_parts.append('(')
                embed_description_parts.append(repr(allocated))
                embed_description_parts.append(' in use).')
            
            return Embed(
                None,
                ''.join(embed_description_parts)
            )
        
        if is_outgoing:
            mode = 'c'
        else:
            mode = 'i'
        
        return InteractionResponse(
            embed = Embed(
                None,
                f'Are you sure you want to divorce {target_user:f}?\n'
                f'\n'
                f'This action requires {waifu_cost} {EMOJI__HEART_CURRENCY}'
            ),
            components = Row(
                Button(
                    'Yes',
                    EMOJI_YES,
                    custom_id = (
                        f'marriage.divorce.{mode}-{source_user_id:x}-{target_user_id:x}'
                    ),
                ),
                BUTTON_DIVORCE_CANCEL,
            ),
        )
    
    
    if is_outgoing:
        return InteractionResponse(
            embed = Embed(
                None,
                f'Are you sure to divorce {target_user:f}?'
            ),
            components = Row(
                Button(
                    'Yes',
                    EMOJI_YES,
                    custom_id = (
                        f'marriage.divorce.o-{source_user_id:x}-{target_user_id:x}'
                    ),
                ),
                Button(
                    'No',
                    EMOJI_NO,
                    custom_id = CUSTOM_ID_DIVORCE_CANCEL,
                ),
            ),
        )
    
    return Embed(
        None,
        f'You are not married to {target_user:f}.'
    )


@divorce.autocomplete('target_user_name')
async def autocomplete_divorce_name(event, value):
    divorces = await get_all_divorce_with_name(event, value)
    return sorted(divorce.full_name for divorce in divorces)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_DIVORCE_CANCEL)
async def divorce_cancelled(event):
    if event.user is not event.message.interaction.user:
        return
    
    return InteractionResponse(
        embed = Embed(
            None,
            'Divorce cancelled.',
        ),
        components = None,
    )


@FEATURE_CLIENTS.interactions(
    custom_id = re_compile('marriage\\.divorce\\.([cio])\\-([0-9a-f]{6,16})\\-([0-9a-f]{6,16})')
)
async def divorce_execute(client, event, mode, source_user_id, target_user_id):
    if event.user is not event.message.interaction.user:
        return
    
    source_user_id = int(source_user_id, 16)
    target_user_id = int(target_user_id, 16)
    
    yield
    
    target_user = await get_user(target_user_id)
    
    if mode == 'i':
        yield divorce_incoming(client, event, source_user_id, target_user)
    elif mode == 'o':
        yield divorce_outgoing(client, event, source_user_id, target_user)
    elif mode == 'c':
        yield divorce_circular(client, event, source_user_id, target_user)


async def divorce_incoming(client, event, source_user_id, target_user):
    async with DB_ENGINE.connect() as connector:
        user_balance = await get_user_balance(source_user_id)
        
        waifu_owner_id = user_balance.waifu_owner_id
        if waifu_owner_id != target_user.id:
            yield InteractionResponse(
                embed = Embed(
                    None,
                    (
                        f'You are not claimed by {target_user:f} anymore.'
                    ),
                ),
                allowed_mentions = None,
                components = None,
            )
            return
         
        waifu_cost = user_balance.waifu_cost or WAIFU_COST_DEFAULT
        
        if (user_balance.balance - user_balance.allocated) < waifu_cost:
            yield InteractionResponse(
                embed = Embed(
                    None,
                    (
                        f'Heart amounts changed meanwhile. You have sufficient amount of '
                        f'{EMOJI__HEART_CURRENCY} to divorce {target_user:f}'
                    ),
                ),
                allowed_mentions = None,
                components = None,
            )
            return
        
        refund = (waifu_cost >> 1)
        
        user_balance.set('balance', user_balance.balance - waifu_cost)
        user_balance.set('waifu_cost', (user_balance.waifu_cost or WAIFU_COST_DEFAULT) - refund)
        user_balance.set('waifu_divorces', user_balance.waifu_divorces + 1)
        user_balance.set('waifu_owner_id', 0)
        await user_balance.save()
        
        user_balance = await get_user_balance(target_user.id)
        user_balance.set('balance', user_balance.balance + waifu_cost)
        await user_balance.save()
        
        await connector.execute(
            WAIFU_LIST_TABLE.delete().where(
                waifu_list_model.waifu_id == source_user_id,
            )
        )
        
        target_user_user_settings = await get_one_user_settings_with_connector(
            target_user.id, connector
        )
    
    
    yield InteractionResponse(
        embed = Embed(
            None,
            (
                f'You divorced {target_user:f} successfully.\n'
                f'\n'
                f'You paid {refund} {EMOJI__HEART_CURRENCY} as refund.'
            ),
        ),
        allowed_mentions = None,
        components = None,
    )
    
    if not target_user.bot:
        await send_embed_to(
            get_preferred_client_for_user(target_user, target_user_user_settings.preferred_client_id, client),
            target_user.id,
            Embed(
                None,
                f'{event.user:f} divorced you.\n'
                f'\n'
                f'You received back {refund} {EMOJI__HEART_CURRENCY}.'
            )
        )


async def divorce_outgoing(client, event, source_user_id, target_user):

    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            WAIFU_LIST_TABLE.delete().where(
                and_(
                    waifu_list_model.user_id == source_user_id,
                    waifu_list_model.waifu_id == target_user.id,
                )
            )
        )
        
        if not response.rowcount:
            yield InteractionResponse(
                embed = Embed(
                    None,
                    (
                        f'You are not claiming {target_user.id:f} anymore.'
                    ),
                ),
                allowed_mentions = None,
                components = None,
            )
            return
        
        user_balance = await get_user_balance(source_user_id.id)
        user_balance.set('waifu_divorces', user_balance.waifu_divorces + 1)
        await user_balance.save()
        
        
        user_balance = await get_user_balance(target_user.id)
        user_balance.set('waifu_owner_id', 0)
        await user_balance.save()
        
        target_user_user_settings = await get_one_user_settings_with_connector(
            target_user.id, connector
        )
    
    yield InteractionResponse(
        embed = Embed(
            None,
            (
                f'You divorced {target_user:f} successfully.'
            ),
        ),
        allowed_mentions = None,
        components = None,
    )
    
    if not target_user.bot:
        await send_embed_to(
            get_preferred_client_for_user(target_user, target_user_user_settings.preferred_client_id, client),
            target_user.id,
            Embed(
                None,
                f'You have been divorced by {event.user:f}.'
            )
        )


async def divorce_circular(client, event, source_user_id, target_user):

    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    waifu_list_model.id,
                ]
            ).where(
                or_(
                    and_(
                        waifu_list_model.user_id == source_user_id,
                        waifu_list_model.waifu_id == target_user.id,
                    ),
                    and_(
                        waifu_list_model.user_id == target_user.id,
                        waifu_list_model.waifu_id == source_user_id,
                    ),
                )
            )
        )
        
        results = await response.fetchall()
        if len(results) < 2:
            yield InteractionResponse(
                embed = Embed(
                    None,
                    (
                        f'You are not mutually married to {target_user:f} anymore.'
                    ),
                ),
                allowed_mentions = None,
                components = None,
            )
            return
        
        entry_ids = [result[0] for result in results]
        
        user_balance = await get_user_balance(source_user_id)
        balance = user_balance.balance
        allocated = user_balance.allocated
        waifu_cost = user_balance.waifu_cost or WAIFU_COST_DEFAULT
        
        available = balance - allocated
        
        if available < waifu_cost:
            yield InteractionResponse(
                embed = Embed(
                    None,
                    (
                        f'Heart amounts changed meanwhile. You have sufficient amount of '
                        f'{EMOJI__HEART_CURRENCY} to divorce {target_user:f}'
                    ),
                ),
                allowed_mentions = None,
                components = None,
            )
            return
        
        refund = (waifu_cost >> 1)
        
        user_balance.set('balance', balance - waifu_cost)
        user_balance.set('waifu_cost', waifu_cost - refund)
        user_balance.set('waifu_divorces', user_balance.waifu_divorces + 1)
        user_balance.set('waifu_owner_id', 0)
        await user_balance.save()
        
        
        user_balance = await get_user_balance(target_user.id)
        user_balance.set('balance', target_user.balance + waifu_cost)
        user_balance.set('waifu_owner_id', 0)
        await user_balance.save()
        
        
        await connector.execute(
            WAIFU_LIST_TABLE.delete().where(
                waifu_list_model.id.in_(entry_ids),
            )
        )
        
        target_user_user_settings = await get_one_user_settings_with_connector(
            target_user.id, connector
        )
    
    yield InteractionResponse(
        embed = Embed(
            None,
            (
                f'You divorced {target_user:f} successfully.\n'
                f'\n'
                f'You paid {refund} {EMOJI__HEART_CURRENCY} as refund.'
            ),
        ),
        allowed_mentions = None,
        components = None,
    )
    
    if not target_user.bot:
        await send_embed_to(
            get_preferred_client_for_user(target_user, target_user_user_settings.preferred_client_id, client),
            target_user.id,
            Embed(
                None,
                f'{event.user:f} divorced you.\n'
                f'\n'
                f'You received back {refund} {EMOJI__HEART_CURRENCY}.'
            )
        )
