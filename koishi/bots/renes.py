__all__ = ('Renes',)

from hata import APPLICATIONS, ActivityType, Client, Embed, InviteTargetType, is_media_url
from scarletio import LOOP_TIME

import config

from ..bot_utils.constants import (
    CHANNEL__ESTS_HOME__STREAM_NOTIFICATION, GUILD__ESTS_HOME, ROLE__ESTS_HOME__STREAM_NOTIFICATION, USER__EST
)
from ..bot_utils.response_data_streaming import create_http_stream_resource


Renes = Client(
    config.RENES_TOKEN,
    client_id = config.RENES_ID,
    application_id = config.RENES_ID,
    extensions = 'slash',
)


STREAM_PING_DIFFERENCE = 10.0 * 60.0 # 10 min
EST_DEFAULT_IMAGE_URL = 'https://cdn.discordapp.com/attachments/568837922288173058/1043516469218119791/est-0001.png'
EST_STREAMING_SETUP_IMAGE_URL = (
    'https://cdn.discordapp.com/attachments/568837922288173058/984793641254015016/est-alice-streaming-0000-cut-0000.png'
)
INVITE_MAX_AGE = 24 * 60 * 60 # 1 day


@Renes.events
async def guild_user_add(client, guild, user):
    if guild is not GUILD__ESTS_HOME:
        return
    
    if user.bot:
        return
    
    system_channel = guild.system_channel
    if system_channel is None:
        return
    
    await client.message_create(
        system_channel,
        f'Thanks for coming {user:m}, enjoy your stay~\n'
        f'If you wish to get notifications every time {USER__EST.name_at(GUILD__ESTS_HOME)} goes live '
        f'or wants to share something with you, please use the {ping_me_alice:m} command.'
    )


@Renes.interactions(guild = GUILD__ESTS_HOME)
async def ping_me_alice(client, event):
    user = event.user
    if user.has_role(ROLE__ESTS_HOME__STREAM_NOTIFICATION):
        await client.user_role_delete(user, ROLE__ESTS_HOME__STREAM_NOTIFICATION)
        return 'You will **not** be pinged for stream notifications anymore.'
    
    
    await client.user_role_add(user, ROLE__ESTS_HOME__STREAM_NOTIFICATION)
    return f'You will be pinged when {USER__EST.name_at(GUILD__ESTS_HOME)} goes live.'


class STREAM_DETAILS:
    TWITCH_STREAM_ENDED = -STREAM_PING_DIFFERENCE
    DISCORD_STREAM_ENDED = -STREAM_PING_DIFFERENCE


async def send_stream_notification(title, description, join_url, image_url, source):
    """
    Sends stream notification.
    
    This function is a coroutine.
    
    Parameters
    ----------
    title : `None | str`
        Notification title.
    
    description : `None | str`
        Notification description.
    
    join_url : `str`
        Activity to join the activity.
    
    image_url : `None | str`
        Image url to stream as banner.
    
    source : `str`
        Where did est go live.
    """
    embed = Embed(
        title,
        description,
    ).add_author(
        f'{USER__EST.name_at(GUILD__ESTS_HOME)} went live on {source}!',
        USER__EST.avatar_url_as(size = 128),
        join_url,
    ).add_thumbnail(
        EST_STREAMING_SETUP_IMAGE_URL,
    )
    
    if (image_url is None):
        file = None
        image_url = EST_DEFAULT_IMAGE_URL
    elif is_media_url(image_url):
        file = None
    else:
        file = ('image.png', create_http_stream_resource(Renes.http, image_url))
        image_url = 'attachment://image.png'
    
    embed.add_image(image_url)
    
    message = await Renes.message_create(
        CHANNEL__ESTS_HOME__STREAM_NOTIFICATION,
        f'> {ROLE__ESTS_HOME__STREAM_NOTIFICATION:m}',
        embed = embed,
        file = file,
    )
    
    await Renes.message_crosspost(message)


async def discord_stream_started(channel):
    """
    Called when a Discord stream started by Est.
    
    This function is a coroutine.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel where Est went live.
    """
    if LOOP_TIME() < STREAM_DETAILS.DISCORD_STREAM_ENDED + STREAM_PING_DIFFERENCE:
        return
    
    invite = await Renes.invite_create(
        channel, max_age = INVITE_MAX_AGE, target_type = InviteTargetType.stream, target_user = USER__EST
    )
    
    for activity in USER__EST.iter_activities():
        if activity.type is ActivityType.playing or activity.type is ActivityType.competing:
            break
    else:
        activity = None
    
    # Title & Image
    while True:
        if activity is None:
            title = None
            image_url = None
            break
        
        while True:
            application_id = activity.application_id
            if not application_id:
                title = activity.name
                image_url = None
                break
            
            applications = await Renes.application_get_all_detectable()
            try:
                application = APPLICATIONS[application_id]
            except KeyError:
                title = activity.name
                image_url = None
                break
            
            title = application.name
            image_url = application.icon_url_as(size = 1024)
            break
        
        if (image_url is None):
            image_url = activity.image_large_url_as(size = 1024)
        break
    
    # Description
    state = activity.state
    details = activity.details
    if state is None:
        if details is None:
            description = None
        else:
            description = details
    else:
        if details is None:
            description = state
        else:
            description = f'{state} | {details}'
    
    await send_stream_notification(
        title,
        description,
        invite.url,
        image_url,
        'discord',
    )


async def discord_stream_ended():
    """
    Called when Est stopped streaming on Discord.
    
    This function is a coroutine.
    """
    STREAM_DETAILS.DISCORD_STREAM_ENDED = LOOP_TIME()


async def twitch_stream_started(activity):
    """
    Called when a Twitch stream started by Est.
    
    This function is a coroutine.
    
    Parameters
    ----------
    activity : ``Activity``
        The started activity.
    """
    if LOOP_TIME() < STREAM_DETAILS.TWITCH_STREAM_ENDED + STREAM_PING_DIFFERENCE:
        return
    
    await send_stream_notification(
        activity.state,
        activity.details,
        activity.url,
        activity.twitch_preview_image_url,
        'twitch',
    )


async def twitch_stream_ended():
    """
    Called when Est stopped streaming on Discord.
    
    This function is a coroutine.
    """
    STREAM_DETAILS.TWITCH_STREAM_ENDED = LOOP_TIME()


@Renes.events
async def user_presence_update(client, user, presence_update):
    if user is not USER__EST:
        return
    
    try:
        activity_change = presence_update['activities']
    except KeyError:
        return
    
    for activity in activity_change.iter_removed():
        if activity.type == ActivityType.stream:
            removed_streaming_activity = activity
            break
    else:
        removed_streaming_activity = None
    
    if (removed_streaming_activity is not None):
        await twitch_stream_ended()
    
    
    for activity in activity_change.iter_added():
        if activity.type == ActivityType.stream:
            added_streaming_activity = activity
            break
    else:
        added_streaming_activity = None
    
    if (added_streaming_activity is None):
        return
    
    await twitch_stream_started(added_streaming_activity)


@Renes.events
async def user_voice_join(client, voice_state):
    if voice_state.user is not USER__EST:
        return
    
    if voice_state.self_stream:
        await discord_stream_started(voice_state.channel)


@Renes.events
async def user_voice_update(client, voice_state, old_attributes):
    if voice_state.user is not USER__EST:
        return
    
    if 'self_stream' not in old_attributes:
        return
    
    if voice_state.self_stream:
        await discord_stream_started(voice_state.channel)
    else:
        await discord_stream_ended()


@Renes.events
async def user_voice_leave(client, voice_state, channel_id):
    if voice_state.user is not USER__EST:
        return
    
    await discord_stream_ended()
