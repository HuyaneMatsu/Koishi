__all__ = ()

import re
from math import floor

from hata import Client, Embed
from hata.ext.slash import InteractionResponse, abort, Button, Row
from hata.ext.extension_loader import import_extension

from bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE, get_create_common_user_expression, \
    waifu_list_model, WAIFU_LIST_TABLE, waifu_proposal_model, WAIFU_PROPOSAL_TABLE
from bot_utils.constants import EMOJI__HEART_CURRENCY, WAIFU_COST_DEFAULT
from bot_utils.utils import send_embed_to
from bot_utils.user_getter import get_user

from sqlalchemy import func as alchemy_function, and_, or_
from sqlalchemy.sql import select


class RequestDetail:
    __slots__ = ('name',)
    
    def __new__(cls, name):
        
        self = object.__new__(cls)
        self.name = name
        return self


async def request(client, event, target_user, request_detail):
    source_user = event.user
    
    source_user_id = source_user.id
    target_user_id = target_user.id
    
    if source_user_id == target_user_id:
        return abort(f'You cannot {request_detail.name} to yourself.')
    
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.user_id,
                    user_common_model.id,
                    user_common_model.waifu_slots,
                    user_common_model.total_love,
                    user_common_model.total_allocated,
                    user_common_model.waifu_cost,
                    user_common_model.notify_proposal,
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
            else:
                target_entry = None
            
            if (source_entry[0] != source_user_id):
                source_entry, target_entry = target_entry, source_entry
        
        
        if source_entry is None:
            source_entry_id = -1
            source_waifu_slots = 1
            source_total_love = 0
            source_total_allocated = 0
            source_
