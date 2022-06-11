from hata import Client, Embed, parse_custom_emojis_ordered, parse_emoji
from hata.ext.slash import abort, Select, Option, InteractionResponse

SLASH_CLIENT: Client


CUSTOM_ID_ENLARGE_EMOJIS = 'enlarge_emojis.emoji'
CUSTOM_ID_ENLARGE_REACTIONS = 'enlarge_emojis.reaction'


def build_embed(event, emoji, message_url, say_emojis):
    user = event.user
    
    emoji_url = emoji.url
    
    guild = emoji.guild
    if (guild is None):
        footer_text = 'Unknown guild'
        footer_icon_url = None
    else:
        footer_text = f'from {guild.name}'
        footer_icon_url = guild.icon_url
    
    return Embed(
        'Click to open',
        color = (emoji.id >> 22) & 0xffffff,
        url = emoji_url,
    ).add_author(
        f'{user.name_at(event.guild_id)}\'s enlarged {"reaction" if say_emojis else "reaction"}s!',
        user.avatar_url,
        message_url,
    ).add_image(
        emoji_url,
    ).add_field(
        'Name',
        f'```\n{emoji.name}\n```',
        inline = True,
    ).add_field(
        'ID',
        f'```\n{emoji.id}\n```',
        inline = True,
    ).add_footer(
        footer_text,
        footer_icon_url,
    )


def create_initial_response(event, target, emojis, say_emojis):
    embed = build_embed(event, emojis[0], target.url, say_emojis)
    
    if len(emojis) == 1:
        components = None
    
    else:
        del emojis[25:]
        
        components = Select(
            [Option(emoji.as_emoji, emoji.name, emoji) for emoji in emojis],
            custom_id = CUSTOM_ID_ENLARGE_EMOJIS,
            placeholder = 'Select an emoji!',
        )
    
    return InteractionResponse(embed=embed, components=components)


@SLASH_CLIENT.interactions(is_global=True, target='message')
async def enlarge_emojis(event, target):
    emojis = parse_custom_emojis_ordered(target.content)
    if not emojis:
        abort('The message has no emojis.')
    
    
    return create_initial_response(event, target, emojis, True)
    


@SLASH_CLIENT.interactions(is_global=True, target='message')
async def enlarge_reactions(event, target):
    reactions = target.reactions
    if (reactions is None) or (not reactions):
        abort('The message has no reactions.')
    
    emojis = [*reactions.keys()]
    
    return create_initial_response(event, target, emojis, False)


def create_select_response(event, say_emojis):
    # Check permission
    if event.user is not event.message.interaction.user:
        return
    
    # Get emoji
    selected_emojis = event.interaction.options
    if (selected_emojis is None):
        return
    
    selected_emoji = selected_emojis[0]
    emoji = parse_emoji(selected_emoji)
    if emoji is None:
        return
    
    # get message.url
    embed = event.message.embed
    if embed is None:
        message_url = None
    else:
        embed_author = embed.author
        if embed_author is None:
            message_url = None
        else:
            message_url = embed_author.url
    
    return build_embed(event, emoji, message_url, say_emojis)


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_ENLARGE_EMOJIS)
async def select_emoji(event):
    return create_select_response(event, True)


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_ENLARGE_REACTIONS)
async def select_emoji(event):
    return create_select_response(event, False)
