from hata import ActivityType, Client, Embed
from scarletio import LOOP_TIME

from bot_utils.constants import (
    CHANNEL__ESTS_HOME__STREAM_NOTIFICATION, GUILD__ESTS_HOME, ROLE__ESTS_HOME__STREAM_NOTIFICATION, USER__EST
)

Renes: Client

STREAM_PING_DIFFERENCE = 10.0 * 60.0 # 10 min
EST_DEFAULT_IMAGE_URL = 'https://cdn.discordapp.com/attachments/568837922288173058/1043516469218119791/est-0001.png'
EST_STREAMING_SETUP_IMAGE_URL = 'https://cdn.discordapp.com/attachments/568837922288173058/984793641254015016/est-alice-streaming-0000-cut-0000.png'
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
        f'If you wish to get notification every time Est goes live please use the {ping_me_hime:m} command.'
    )


@Renes.interactions(guild = GUILD__ESTS_HOME)
async def ping_me_hime(client, event):
    user = event.user
    if user.has_role(ROLE__ESTS_HOME__STREAM_NOTIFICATION):
        await client.user_role_delete(user, ROLE__ESTS_HOME__STREAM_NOTIFICATION)
        return 'You will **not** be pinged for stream notifications anymore.'
    
    
    await client.user_role_add(user, ROLE__ESTS_HOME__STREAM_NOTIFICATION)
    return 'You will be pinged when Est goes live.'


class STREAM_DETAILS:
    TWITCH_STREAM_ENDED = -STREAM_PING_DIFFERENCE
    DISCORD_STREAM_ENDED = -STREAM_PING_DIFFERENCE


async def send_stream_notification(activity, join_url, image):
    """
    Sends stream notification.
    
    This function is a coroutine.
    
    Parameters
    ----------
    activity : `None`, ``Activity``
        Est's activity.
    
    join_url : `str`
        Activity to join the activity.
    
    image : `None`, `bytes`
        Image url for banner.
    """
    if activity is None:
        title = None
        description = None
    else:
        title = activity.state
        description = activity.details
    
    embed = Embed(
        title,
        description,
    ).add_author(
        f'{USER__EST.name_at(GUILD__ESTS_HOME)} went live!',
        USER__EST.avatar_url_as(size = 128),
        join_url,
    ).add_thumbnail(
        EST_STREAMING_SETUP_IMAGE_URL,
    )
    
    if (image is None):
        image_url = EST_DEFAULT_IMAGE_URL
    else:
        image_url = 'attachment://image.png'
        
    embed.add_image(image_url)
    
    if image is None:
        file = None
    else:
        file = ('image.png', image)
    
    message = await Renes.message_create(
        CHANNEL__ESTS_HOME__STREAM_NOTIFICATION,
        f'> {ROLE__ESTS_HOME__STREAM_NOTIFICATION:m}',
        embed = embed,
        file = file,
    )
    
    await Renes.message_crosspost(message)


async def discord_stream_started():
    """
    Called when a Discord stream started by Est.
    
    This function is a coroutine.
    """
    if LOOP_TIME() > STREAM_DETAILS.DISCORD_STREAM_ENDED + STREAM_PING_DIFFERENCE:
        return
    
    invite = await Renes.stream_invite_create(GUILD__ESTS_HOME, USER__EST, max_age = INVITE_MAX_AGE)
    
    await send_stream_notification(USER__EST.activity, invite.url, None)


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
    if LOOP_TIME() > STREAM_DETAILS.TWITCH_STREAM_ENDED + STREAM_PING_DIFFERENCE:
        return
    
    image_url = activity.twitch_preview_image_url
    if (image_url is None):
        image = None
    else:
        async with Renes.http.get(image_url) as response:
            if response.status == 200:
                image = await response.read()
            else:
                image = None
    
    await send_stream_notification(activity, activity.url, image)


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
        await discord_stream_started()


@Renes.events
async def user_voice_update(client, voice_state, old_attributes):
    if voice_state.user is not USER__EST:
        return
    
    if 'self_stream' not in old_attributes:
        return
    
    if voice_state.self_stream:
        await discord_stream_started()
    else:
        await discord_stream_ended()


@Renes.events
async def user_voice_leave(client, voice_state, channel_id):
    if voice_state.user is not USER__EST:
        return
    
    await discord_stream_ended()
