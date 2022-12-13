__all__ = ()

from hata import DiscordException, ERROR_CODES, Embed, GuildFeature, ICON_TYPE_NONE
from hata.ext.slash import abort


async def get_guild_welcome_screen(client, event, guild):
    """
    Gets the guild's welcome screen. Only applicable if the guild has welcome screen also enabled.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    guild : ``Guild``
        The event's guild.
    
    Returns
    -------
    welcome_screen : `None`, ``WelcomeScreen``
    """
    if GuildFeature.welcome_screen_enabled not in guild.features:
        welcome_screen = None
    else:
        await client.interaction_application_command_acknowledge(event)
        
        try:
            welcome_screen = await client.welcome_screen_get(guild)
        except ConnectionError:
            return
        except DiscordException as err:
            # If the guild's settings were changed meanwhile, this can drop up.
            if err.code == ERROR_CODES.unknown_guild_welcome_screen:
                welcome_screen = None
            
            else:
                raise
    
    return welcome_screen


def build_welcome_screen_embed(guild, welcome_screen):
    """
    Converts the given welcome screen into it's embed representation.
    
    Parameters
    ----------
    guild : ``Guild``
        Respective guild.
    welcome_screen : ``WelcomeScreen``
        The welcome screen of the guild.
    
    Returns
    -------
    embed : ``Embed``
    """
    description = welcome_screen.description
    if (description is None):
        description = '*TOP THINGS TO DO HERE*'
    else:
        description = f'{description}\n\n*TOP THINGS TO DO HERE*'
    
    embed = Embed(
        f'Welcome to **{guild.name}**',
        description,
        color = (guild.icon_hash & 0xffffff if (guild.icon_type is ICON_TYPE_NONE) else (guild.id >> 22) & 0xffffff),
    )
    
    icon_url = guild.icon_url
    if (icon_url is not None):
        embed.add_thumbnail(icon_url)
    
    welcome_channels = welcome_screen.welcome_channels
    if (welcome_channels is not None):
        for welcome_channel in welcome_channels:
            embed.add_field(
                f'{welcome_channel.emoji} {welcome_channel.description}',
                f'{welcome_channel.channel.mention}',
            )
    
    return embed


async def welcome_screen_command(client, event):
    """Shows the guild's welcome screen."""
    guild = event.guild
    if (guild is None) or guild.partial:
        abort('The command unavailable in guilds, where the application\'s bot is not in.')
    
    welcome_screen = await get_guild_welcome_screen(client, event, guild)
    if welcome_screen is None:
        return Embed(None, f'**{guild.name}** has no welcome screen enabled.')
    
    return build_welcome_screen_embed(guild, welcome_screen)
