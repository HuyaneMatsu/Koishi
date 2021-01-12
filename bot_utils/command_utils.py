# -*- coding: utf-8 -*-
import re
from hata import Permission, ChannelText
from hata.ext.commands import checks, Converter, ConverterFlag

# CHECK_HANDLERS

async def PERMISSION_CHECK_HANDLER(client, message, command, check):
    permission_names = ' '.join(permission_name.replace('_', ' ') for permission_name in check.permissions)
    text = f'You must have {permission_names} permission to invoke `{command.display_name}` command.'
    await client.message_create(message, text, allowed_mentions='!replied_user')

async def SELF_PERMISSION_CHECK_HANDLER(client, message, command, check):
    permission_names = ' '.join(permission_name.replace('_', ' ') for permission_name in check.permissions)
    text = f'I need to have {permission_names} permission to invoke `{command.display_name}` command, what I lack.'
    await client.message_create(message, text, allowed_mentions='!replied_user')

async def GUILD_OWNER_CHECK_HANDLER(client, message, command, check):
    text = f'You must be the owner of the guild to invoke `{command.display_name}` command.'
    await client.message_create(message, text, allowed_mentions='!replied_user')

async def BOT_OWNER_CHECK_HANDLER(client, message, command, check):
    text = f'You must be the owner of the bot to invoke `{command.display_name}` command.'
    await client.message_create(message, text, allowed_mentions='!replied_user')

async def NSFW_HANDLER(client, message, command, check):
    if re.search(client.name, message.content, re.I) is None:
        text = 'Onii chaan\~,\nthis is not the right place to lewd.'
    else:
        text = 'I love you too\~,\nbut this is not the right place to lewd.'
    await client.message_create(message, text, allowed_mentions='!replied_user')

async def YEET_CHECK_HANDLER(client, message, command, check):
    text = f'You must have yeet permission to invoke `{command.display_name}` command.'
    await client.message_create(message, text, allowed_mentions='!replied_user')

# CHECKS

CHECK_MANAGE_MESSAGES = checks.has_permissions(
    Permission().update_by_keys(manage_messages=True),
    handler=PERMISSION_CHECK_HANDLER,
        )

CHECK_OWNER_OR_CAN_INVITE = checks.owner_or_has_guild_permissions(
    Permission().update_by_keys(create_instant_invite=True),
    handler=PERMISSION_CHECK_HANDLER,
        )


CHECK_BAN_USERS = checks.has_guild_permissions(
    Permission().update_by_keys(ban_users=True),
    handler=PERMISSION_CHECK_HANDLER,
        )

CHECK_OWNER_OR_GUILD_OWNER = checks.owner_or_guild_owner(
    handler=GUILD_OWNER_CHECK_HANDLER,
        )

CHECK_MANAGE_CHANNEL_AND_INVITES = checks.has_guild_permissions(
    Permission().update_by_keys(manage_channel=True, create_instant_invite=True),
    handler=PERMISSION_CHECK_HANDLER,
        )

CHECK_OWNER_ONLY = checks.owner_only(
    handler=BOT_OWNER_CHECK_HANDLER
        )

CHECK_VIEW_LOGS = checks.owner_or_has_guild_permissions(
    Permission().update_by_keys(view_audit_logs=True),
    handler=PERMISSION_CHECK_HANDLER,
        )

CHECK_ADMINISTRATION = checks.owner_or_has_guild_permissions(
    Permission().update_by_keys(administrator=True),
    handler=PERMISSION_CHECK_HANDLER,
        )

CHECK_NSFW_CHANNEL = checks.nsfw_channel_only(
    handler=NSFW_HANDLER,
        )

SELF_CHECK_MOVE_USERS = checks.client_has_guild_permissions(
    Permission().update_by_keys(move_users=True),
    handler=SELF_PERMISSION_CHECK_HANDLER,
        )

CHECK_YEET_USERS = checks.has_guild_permissions(
    Permission().update_by_keys(ban_users=True),
    handler=YEET_CHECK_HANDLER,
        )

# CONVERTERS

USER_CONVERTER_EVERYWHERE = Converter('user',
    ConverterFlag.user_default.update_by_keys(everywhere=True),
        )

USER_CONVERTER_EVERYWHERE_NONE_DEFAULT = Converter('user',
    ConverterFlag.user_default.update_by_keys(everywhere=True),
    default=None,
        )

USER_CONVERTER_EVERYWHERE_AUTHOR_DEFAULT = Converter('user',
    ConverterFlag.user_default.update_by_keys(everywhere=True),
    default_code='message.author',
        )

USER_CONVERTER_ALL_NONE_DEFAULT = Converter('user',
    ConverterFlag.user_all,
    default=None,
        )

USER_CONVERTER_ALL_CLIENT_DEFAULT = Converter('user',
    ConverterFlag.user_all,
    default_code='client',
        )

USER_CONVERTER_ALL_AUTHOR_DEFAULT = Converter('user',
    ConverterFlag.user_all,
    default_code='message.author',
        )

CLIENT_CONVERTER_ALL_CLIENT_DEFAULT = Converter('client',
    flags=ConverterFlag.client_all,
    default_code='client',
        )

MESSAGE_CONVERTER_ALL = Converter('message',
    ConverterFlag.message_all,
        )

CHANNEL_TEXT_CONVERTER_MESSAGE_CHANNEL_DEFAULT = Converter(ChannelText,
    default_code='message.channel',
        )

