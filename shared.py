# -*- coding: utf-8 -*-
import pers_data

import models
from hata.ext.commands import prefix_by_guild

KOISHI_PREFIX=prefix_by_guild(pers_data.KOISHI_PREFIX,models.DB_ENGINE,models.PREFIX_TABLE,models.pefix_model)
SATORI_PREFIX = pers_data.SATORI_PREFIX
FLAN_PREFIX = pers_data.FLAN_PREFIX


async def permission_check_handler(client, message, command, check):
    permission_names = ' '.join(permission_name.repleace('_', ' ') for permission_name in check.permissions)
    await client.message_create(message.channel, f'You must have {permission_names} permission to invoke `{command.name}` command.')

async def not_guild_owner_handler(client, message, command, check):
    await client.message_create(message.channel, f'You must be the owner of the guild to invoke `{command.name}` command.')

async def not_bot_owner_handler(client, message, command, check):
    await client.message_create(message.channel, f'You must be the owner of the bot to invoke `{command.name}` command.')

