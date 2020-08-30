# -*- coding: utf-8 -*-
from hata import KOKORO, Task

import pers_data

import models


class prefix_by_guild(dict):
    __slots__=('default', 'orm',)
    
    def __init__(self,default,*orm):
        if type(default) is not str:
            raise TypeError (f'Default expected type str, got type {default.__class__.__name__}')
        self.default=default
        if orm:
            if len(orm)!=3:
                raise TypeError(f'Expected \'engine\', \'table\', \'model\' for orm, but got {len(orm)} elements')
            self.orm=orm
            Task(self._load_orm(),KOKORO)
            KOKORO.wakeup()
            
    def __call__(self,message):
        guild=message.guild
        if guild is not None:
            return self.get(guild.id,self.default)
        return self.default
    
    def __getstate__(self):
        return self.default
    def __setstate__(self,state):
        self.default=state
        self.orm=None
    
    def add(self,guild,prefix):
        guild_id=guild.id
        if guild_id in self:
            if prefix==self.default:
                del self[guild_id]
                if self.orm is not None:
                    Task(self._remove_prefix(guild_id),KOKORO)
                    KOKORO.wakeup()
                return True
            self[guild_id]=prefix
            if self.orm is not None:
                Task(self._modify_prefix(guild_id,prefix),KOKORO)
                KOKORO.wakeup()
            return True
        else:
            if prefix==self.default:
                return False
            self[guild_id]=prefix
            if self.orm is not None:
                Task(self._add_prefix(guild_id,prefix),KOKORO)
                KOKORO.wakeup()
            return True
    
    def to_json_serializable(self):
        result=dict(self)
        result['default']=self.default
        return result
    
    @classmethod
    def from_json_serialization(cls,data):
        self=dict.__new__(cls)
        self.default=data.pop('default')
        for id_,prefix in data.items():
            self[int(id_)]=prefix
        self.orm=None
        return self
    
    async def _load_orm(self,):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            result = await connector.execute(table.select())
            prefixes = await result.fetchall()
            for item in prefixes:
                self[item.guild_id]=item.prefix
    
    async def _add_prefix(self,guild_id,prefix):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            await connector.execute(table.insert(). \
                values(guild_id=guild_id,prefix=prefix))
    
    async def _modify_prefix(self,guild_id,prefix):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            await connector.execute(table.update(). \
                values(prefix=prefix). \
                where(model.guild_id==guild_id))
    
    async def _remove_prefix(self,guild_id):
        engine,table,model=self.orm
        async with engine.connect() as connector:
            await connector.execute(table.delete(). \
                where(model.guild_id==guild_id))
    
    def __repr__(self):
        return f'<{self.__class__.__name__} default={self.default!r} len={len(self)}>'
    
    # because it is a builtin subclass, it will have __str__, so we overwrite that as well
    __str__=__repr__

KOISHI_PREFIX = prefix_by_guild(pers_data.KOISHI_PREFIX, models.DB_ENGINE, models.PREFIX_TABLE, models.pefix_model)
SATORI_PREFIX = pers_data.SATORI_PREFIX
FLAN_PREFIX = pers_data.FLAN_PREFIX


async def permission_check_handler(client, message, command, check):
    permission_names = ' '.join(permission_name.repleace('_', ' ') for permission_name in check.permissions)
    await client.message_create(message.channel,
        f'You must have {permission_names} permission to invoke `{command.display_name}` command.')

async def not_guild_owner_handler(client, message, command, check):
    await client.message_create(message.channel,
        f'You must be the owner of the guild to invoke `{command.display_name}` command.')

async def not_bot_owner_handler(client, message, command, check):
    await client.message_create(message.channel,
        f'You must be the owner of the bot to invoke `{command.display_name}` command.')

