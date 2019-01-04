# -*- coding: utf-8 -*-
from discord_uwu.parsers import eventlist

infos=eventlist()

@infos.add('roles')
async def list_roles(client,message,content):
    guild=message.guild
    if guild is None:
        return

    result=[]
    if message.mentions:
        user=message.mentions[0]
        user_mode=True
        try:
            roles=user.guild_profiles[guild].roles
        except KeyError:
            roles=[]
        result.append(f'{user.display_name(guild)}\'s roles:\n')
    else:
        user_mode=False
        roles=guild.roles
    if roles:
        ln=len(roles)
        for index in range(1,len(roles)+user_mode):
            role=roles[ln-index]
            result.append(f'Role {index} : `{role.name}`')
            if role.separated or role.mentionable:
                extra=[]
                if role.separated:
                    extra.append('separated')
                if role.mentionable:
                    extra.append('mentionable')
                result.append(f'({", ".join(extra)})\n')
            else:
                result.append('\n')
    else:
        result.append('*(none)*')
    await client.message_create(message.channel,''.join(result))

@infos.add('emojis')
async def list_emojis(client,message,content):
    guild=message.guild
    if guild is None:
        return
    result=[str(emoji) for emoji in guild.emojis.values()]
    await client.message_create(message.channel,' '.join(result))
    
    
