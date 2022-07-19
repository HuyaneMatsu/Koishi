__all__ = ()

from hata import Client, DiscordException, ERROR_CODES, Sticker, Emoji

Koishi: Client

STICKER_KOISHI_KNIFE = Sticker.precreate(990556966298464297)
STICKER_KOISHI_HONK = Sticker.precreate(990556669161406504)
EMOJI_KOISHI_DEAL = Emoji.precreate(990558169963049041)

LEFT_GUILD_IDS = set()
LEFT_GUILD_OWNER_IDS = set()


@Koishi.events
async def guild_create(client, guild):
    if guild.id in LEFT_GUILD_IDS:
        should_leave = True
        repeated_leave = True
    
    else:
        await client.request_all_members_of(guild)
        
        bot_count = sum(user.is_bot for user in guild.users.values())
        if (bot_count >= 50) or (bot_count >= len(guild.users) >> 1):
            
            should_leave = True
            repeated_leave = guild.owner_id in LEFT_GUILD_OWNER_IDS
            
            LEFT_GUILD_IDS.add(guild.id)
            LEFT_GUILD_OWNER_IDS.add(guild.owner_id)
        
        else:
            should_leave = False
            repeated_leave = False
    
    
    if not should_leave:
        return
    
    
    if repeated_leave:
        contents = [STICKER_KOISHI_KNIFE.url]
    
    else:
        contents = [
            (
                f'{client.name} just flew into the {guild.name} server.\n'
                f'Mr. Hat foretold this server lacks subconscious beings and I would not enjoy the parties there!\n'
                f'\n'
                f'So I am off {EMOJI_KOISHI_DEAL} Bye, have a great time with your bot friends!'
            ),
            STICKER_KOISHI_HONK.url,
        ]
    
    try:
        channel = await client.channel_private_create(guild.owner_id)
        
        try:
            for content in contents:
                await client.message_create(channel, content)
        
        except DiscordException as err:
            if err.code != ERROR_CODES.cannot_message_user:
                raise
    
    finally:
        await client.guild_leave(guild)
