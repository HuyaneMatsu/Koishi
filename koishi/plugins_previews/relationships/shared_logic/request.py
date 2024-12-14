__all__ = ()

from hata.ext.slash import abort

from sqlalchemy.sql import select

from ....bot_utils.models import DB_ENGINE
from ....plugins.user_balance import get_user_balances


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
        user_balances = await get_user_balances((source_user_id, target_user_id),)
        source_user_balance = user_balances[source_user_id]
        target_user_balance = user_balances[target_user_id]
