__all__ = ('info',)

from math import floor

from hata import Client, Embed
from hata.ext.slash import InteractionResponse

from bot_utils.models import DB_ENGINE, user_common_model, waifu_list_model
from bot_utils.constants import EMOJI__HEART_CURRENCY, WAIFU_COST_DEFAULT
from bot_utils.user_getter import get_user

from sqlalchemy import or_
from sqlalchemy.sql import select


from ..constants.waifu_type import get_relation_name
from ..helpers import get_multiplier


def relationship_members_by_category_sort_key(item):
    return item[0]


SLASH_CLIENT: Client

async def info(event,
    user: ('user', 'The user to get') = None,
):
    """Relationship info."""
    if user is None:
        user = event.user
    
    yield
    
    user_id = user.id
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
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
            waifu_cost, waifu_divorces, waifu_slots = results[0]
            
            entry_found = True
        else:
            waifu_cost = WAIFU_COST_DEFAULT
            waifu_divorces = 0
            waifu_slots = 1
            
            entry_found = False
        
        
        relationship_members_by_category = None
        
        if entry_found:
            response = await connector.execute(
                select(
                    [
                        waifu_list_model.user_id,
                        waifu_list_model.waifu_id,
                        waifu_list_model.waifu_type,
                    ]
                ).where(
                    or_(
                        waifu_list_model.user_id == user_id,
                        waifu_list_model.waifu_id == user_id,
                    )
                )
            )
            
            results = await response.fetchall()
            for relation_source_user_id, relation_target_user_id, relation_type in results:
                
                if relation_source_user_id == user_id:
                    reverted = False
                else:
                    reverted = True
                
                relation_name = get_relation_name(relation_type, reverted, True)
                if relationship_members_by_category is None:
                    relationship_members_by_category = {}
                
                try:
                    relation_member_ids = relationship_members_by_category[relation_name]
                except KeyError:
                    relation_member_ids = set()
                    relationship_members_by_category[relation_name] = relation_member_ids
                
                if relation_source_user_id == user_id:
                    relation_member_ids.add(relation_target_user_id)
                else:
                    relation_member_ids.add(relation_source_user_id)
    
    
    embed = Embed(
        f'{user:f}\'s relationship info',
        timestamp = event.created_at,
    ).add_thumbnail(
        user.avatar_url
    )
    
    if not waifu_cost:
        waifu_cost = WAIFU_COST_DEFAULT
    
    embed.add_field(
        f'Minimal cost:',
        f'{floor(waifu_cost * 1.1)} - {floor(waifu_cost * 2.1)} {EMOJI__HEART_CURRENCY}',
        inline = True,
    )
    
    embed.add_field(
        'Divorces',
        str(waifu_divorces),
        inline = True,
    )
    
    embed.add_field(
        'Relationship slots',
        str(waifu_slots),
        inline = True,
    )
    
    if (relationship_members_by_category is not None):
        for field_name, relation_member_ids in sorted(
            relationship_members_by_category.items(), key=relationship_members_by_category_sort_key,
        ):
            field_name = field_name.title()
            
            user_names = []
            for relation_member_id in sorted(relation_member_ids):
                waifu = await get_user(relation_member_id)
                user_names.append(waifu.full_name)
                
            field_value = '\n'.join(user_names)
            user_names = None
            
            embed.add_field(
                field_name,
                field_value,
                inline = True,
            )
    
    event_user = event.user
    event_user_id = event_user.id
    
    if user_id == event_user_id:
        should_show_add_to_relationship_notification = False
    elif relationship_members_by_category_sort_key is None:
        should_show_add_to_relationship_notification = True
    else:
        for relation_member_ids in relationship_members_by_category.values():
            if event_user_id in relation_member_ids:
                should_show_add_to_relationship_notification = False
                break
        else:
            should_show_add_to_relationship_notification = True
    
    if should_show_add_to_relationship_notification:
        footer_text = (
            f'To add {user:f} to your relationship, you need at least '
            f'{floor(get_multiplier(event_user_id, user_id) * waifu_cost)} {EMOJI__HEART_CURRENCY}.\n'
            f'Requested by {event_user:f}'
        )
    else:
        footer_text = f'Requested by {event_user:f}'
    
    embed.add_footer(
        footer_text,
        icon_url = event_user.avatar_url,
    )
    
    yield InteractionResponse(embed=embed, allowed_mentions=None)
