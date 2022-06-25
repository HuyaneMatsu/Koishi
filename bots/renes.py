from scarletio import LOOP_TIME
from hata import Client, ACTIVITY_TYPES, Embed
from bot_utils.constants import GUILD__ESTS_HOME, ROLE__ESTS_HOME__STREAM_NOTIFICATION, USER__EST, \
    CHANNEL__ESTS_HOME__STREAM_NOTIFICATION

Renes: Client
Koishi: Client
Satori: Client

@Renes.events
async def guild_user_add(client, guild, user):
    if guild is not GUILD__ESTS_HOME:
        return
    
    if user.is_bot:
        return
    
    system_channel = guild.system_channel
    if system_channel is None:
        return
    
    await client.message_create(system_channel, f'Thanks for coming {user:m}, enjoy your stay~')


@Renes.interactions(guild=GUILD__ESTS_HOME)
async def ping_me_hime(client, event):
    user = event.user
    if user.has_role(ROLE__ESTS_HOME__STREAM_NOTIFICATION):
        await client.user_role_delete(user, ROLE__ESTS_HOME__STREAM_NOTIFICATION)
        return 'You will **not** be pinged for stream notifications anymore.'
    
    
    await client.user_role_add(user, ROLE__ESTS_HOME__STREAM_NOTIFICATION)
    return 'You will be pinged when Est goes live.'


ALICE_STREAMING_SETUP_IMAGE_URL = 'https://cdn.discordapp.com/attachments/568837922288173058/984793641254015016/est-alice-streaming-0000-cut-0000.png'

@Satori.events
class user_presence_update:
    LAST_STREAM_OVER = 0.0
    STREAM_PING_DIFFERENCE = 10.0 * 60.0 # 10 min
    
    async def __new__(cls, client, user, activity_change):
        if user is not USER__EST:
            return
        
        await Koishi.message_create(557187647831932938, f'Debug: {activity_change!r}', allowed_mentions=None)
        
        for activity in activity_change.iter_removed():
            if activity.type == ACTIVITY_TYPES.stream:
                removed_streaming_activity = activity
                break
        else:
            removed_streaming_activity = None
        
        if (removed_streaming_activity is not None):
            cls.LAST_STREAM_OVER = LOOP_TIME()
        
        
        for activity in activity_change.iter_added():
            if activity.type == ACTIVITY_TYPES.stream:
                added_streaming_activity = activity
                break
        else:
            added_streaming_activity = None
        
        if (added_streaming_activity is not None):
            if LOOP_TIME() > cls.LAST_STREAM_OVER - cls.STREAM_PING_DIFFERENCE:
                message = await client.message_create(
                    CHANNEL__ESTS_HOME__STREAM_NOTIFICATION,
                    f'> {ROLE__ESTS_HOME__STREAM_NOTIFICATION:m}',
                    embed = Embed(
                        added_streaming_activity.state,
                        added_streaming_activity.details,
                    ).add_author(
                        f'{USER__EST.name_at(GUILD__ESTS_HOME)} went live!',
                        USER__EST.avatar_url_as(size=128),
                        added_streaming_activity.url,
                    ).add_image(
                        added_streaming_activity.twitch_preview_image_url,
                    ).add_thumbnail(
                        ALICE_STREAMING_SETUP_IMAGE_URL,
                    )
                )
                
                await client.message_crosspost(message)
