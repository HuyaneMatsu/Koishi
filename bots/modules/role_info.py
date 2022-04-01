import re

from hata import ROLES, Embed, Client, elapsed_time, BUILTIN_EMOJIS, RoleManagerType, DATETIME_FORMAT_CODE
from hata.ext.slash import abort, InteractionResponse, Button, Row


SLASH_CLIENT: Client

CLOSE_EMOJI = BUILTIN_EMOJIS['x']
LIST_EMOJI = BUILTIN_EMOJIS['clipboard']


CUSTOM_ID_ROLE_INFO_CLOSE = 'role_info.close'
CUSTOM_ID_ROLE_INFO_SHOW_PERMISSIONS = 'role_info.show_permissions'


ROLE_ID_RP = re.compile('```\n(\d+)\n```', re.M)


COMPONENTS_ROLE_INFO = Row(
    Button(
        emoji = CLOSE_EMOJI,
        custom_id = CUSTOM_ID_ROLE_INFO_CLOSE,
    ),
    Button(
        'Show permissions',
        LIST_EMOJI,
        custom_id = CUSTOM_ID_ROLE_INFO_SHOW_PERMISSIONS,
    ),
)


@SLASH_CLIENT.interactions(is_global=True)
async def role_info(
    client,
    event,
    role: ('role', 'Select the role to show information of.'),
):
    """Shows the information about a role."""
    if role.partial:
        abort('I must be in the guild, where the role is.')
    
    color = role.color
    
    embed = Embed(
        f'Role info: {role.name}',
    )
    
    if color:
        embed.color = color
    
    embed.add_field(
        'Identifier',
        (
            f'```\n'
            f'{role.id}\n'
            f'```'
        ),
        inline = True,
    )
    
    embed.add_field(
        'Permissions',
        (
            f'```\n'
            f'{role.permissions:d}\n'
            f'```'
        ),
        inline = True
    )
    
    created_at = role.created_at
    
    embed.add_field(
        'Created at',
        (
            f'```\n'
            f'{created_at:{DATETIME_FORMAT_CODE}} | {elapsed_time(created_at)} ago\n'
            f'```'
        ),
    )
    
    embed.add_field(
        'Position',
        (
            f'```\n'
            f'{role.position}\n'
            f'```'
        ),
        inline = True,
    )
    
    embed.add_field(
        'Mentionable',
        (
            f'```\n'
            f'{"true" if role.mentionable else "false"}'
            f'```'
        ),
        inline = True,
    )
    
    embed.add_field(
        'Separated',
        (
            f'```\n'
            f'{"true" if role.separated else "false"}'
            f'```'
        ),
        inline = True,
    )
    
    color = role.color
    if color:
        embed.add_field(
            'color',
            (
                f'```\n'
                f'html: {color.as_html} | rgb: {color.red}, {color.green}, {color.blue} | int: {color:d}\n'
                f'```'
            ),
        )
    
    manager_type = role.manager_type
    if manager_type is not RoleManagerType.none:
        if manager_type is RoleManagerType.unset:
            await client.sync_roles(role.guild)
            manager_type = role.manager_type
        
        if manager_type is RoleManagerType.bot:
            managed_description = f'Special role for bot: {role.manager:f}'
        elif manager_type is RoleManagerType.booster:
            managed_description = 'Role for the boosters of the guild.'
        elif manager_type is RoleManagerType.integration:
            managed_description = f'Special role for integration: {role.manager.name}'
        elif manager_type is RoleManagerType.unknown:
            managed_description = 'Some new things.. Never heard of them.'
        else:
            managed_description = 'I have no clue.'
        
        embed.add_field(
            'Managed',
            (
                f'```\n'
                f'{managed_description}\n'
                f'```'
            )
        )
    
    unicode_emoji = role.unicode_emoji
    if (unicode_emoji is not None):
        embed.add_field(
            'Icon (unicode emoji)',
            f'{unicode_emoji} | {unicode_emoji.name}'
        )
        
    else:
        icon_url = role.icon_url
        if (icon_url is not None):
            embed.add_image(icon_url)
    
    
    return InteractionResponse(embed=embed, components=COMPONENTS_ROLE_INFO)


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_ROLE_INFO_CLOSE)
async def close_role_info(client, event):
    if (event.user is event.message.interaction.user):
        await client.interaction_component_acknowledge(event)
        await client.interaction_response_message_delete(event)


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_ROLE_INFO_SHOW_PERMISSIONS)
async def close_role_info(client, event):
    embed = event.message.embed
    if embed is None:
        return
    
    fields = embed.fields
    if fields is None or not fields:
        return
    
    parsed = ROLE_ID_RP.fullmatch(fields[0].value)
    if parsed is None:
        return
    
    role_id = int(parsed.group(1))
    
    try:
        role = ROLES[role_id]
    except KeyError:
        title = f'Unknown role: {role_id}'
        description = None
        color = None
    
    else:
        title = f'Permissions of {role.name}'
        
        description_parts = ['```diff\n']
        
        for permission_name, has_permission in role.permissions.items():
            description_parts.append('+' if has_permission else '-')
            description_parts.append(permission_name.replace("_", "-"))
            description_parts.append('\n')
        
        description_parts.append('```')
        
        description = ''.join(description_parts)
        description_parts = None
        
        color = role.color
    
    
    await client.interaction_response_message_create(
        event,
        embed = Embed(title, description, color=color),
        show_for_invoking_user_only = True,
    )
