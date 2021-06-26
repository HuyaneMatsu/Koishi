# -*- coding: utf-8 -*-

from datetime import datetime

from hata import Client, Embed, DATETIME_FORMAT_CODE, Status, elapsed_time, ACTIVITY_TYPES
from hata.discord.utils import DISCORD_EPOCH_START

from bot_utils.shared import CHANNEL__NEKO_DUNGEON_LOG, GUILD__NEKO_DUNGEON, CATEGORY__NEKO_DUNGEON__BIG_BRO

Koishi: Client
def setup(lib):
    Koishi.events.message_create.append(GUILD__NEKO_DUNGEON, logger)
    Koishi.events.channel_delete.append(GUILD__NEKO_DUNGEON, big_bro_channel_delete_waiter)
    Koishi.events.channel_create.append(GUILD__NEKO_DUNGEON, big_bro_channel_create_waiter)
    Koishi.events.channel_edit.append(GUILD__NEKO_DUNGEON, big_bro_channel_edit_waiter)
    checkout_category()

def teardown(lib):
    Koishi.events.message_create.remove(GUILD__NEKO_DUNGEON, logger)
    Koishi.events.channel_delete.remove(GUILD__NEKO_DUNGEON, big_bro_channel_delete_waiter)
    Koishi.events.channel_create.remove(GUILD__NEKO_DUNGEON, big_bro_channel_create_waiter)
    Koishi.events.channel_edit.remove(GUILD__NEKO_DUNGEON, big_bro_channel_edit_waiter)
    checkout_category()


CLEAN_CONTENT_MAX_LENGTH = 1000
USER_MENTION_MAX = 7
ROLE_MENTION_MAX = 5
SEPARATOR_LINE = '\\_'*30


async def logger(client, message):
    everyone_mention = message.everyone_mention
    user_mentions = message.user_mentions
    role_mentions = message.role_mentions
    if (not everyone_mention) and (user_mentions is None) and (role_mentions is None):
        return
    
    content_parts = []
    
    author = message.author
    
    guild = message.channel.guild
    if guild is None:
        nick = None
    else:
        try:
            guild_profile = author.guild_profiles[guild]
        except KeyError:
            nick = None
        else:
            nick = guild_profile.nick
    
    content_parts.append('**Author:** ')
    content_parts.append(author.full_name)
    content_parts.append(' ')
    if (nick is not None):
        content_parts.append('[')
        content_parts.append(nick)
        content_parts.append('] ')
    content_parts.append('(')
    content_parts.append(repr(author.id))
    content_parts.append(')\n')
    
    channel = message.channel
    content_parts.append('**Channel:** ')
    content_parts.append(channel.display_name)
    content_parts.append(' (')
    content_parts.append(repr(channel.id))
    content_parts.append(')\n')
    
    message_id = message.id
    content_parts.append('**Message id**: ')
    content_parts.append(repr(message_id))
    content_parts.append('\n')
    
    message_type = message.type
    content_parts.append('**Message type**: ')
    content_parts.append(message_type.name)
    content_parts.append(' (')
    content_parts.append(repr(message_type.value))
    content_parts.append(')\n')
    
    created_at = message.created_at
    content_parts.append('**Created at**: ')
    content_parts.append(created_at.__format__(DATETIME_FORMAT_CODE))
    content_parts.append('\n')
    
    content_length = len(message)
    content_parts.append('**Message Length:** ')
    content_parts.append(repr(content_length))
    content_parts.append('\n')
    
    content_parts.append('\n**Content**:\n')
    content_parts.append(SEPARATOR_LINE)
    content_parts.append('\n')
    
    clean_content = message.clean_content
    clean_content_length = len(clean_content)
    if clean_content_length > CLEAN_CONTENT_MAX_LENGTH:
        clean_content = clean_content[:CLEAN_CONTENT_MAX_LENGTH]
        truncated = clean_content_length - CLEAN_CONTENT_MAX_LENGTH
    else:
        truncated = 0
    
    content_parts.append(clean_content)
    if truncated:
        content_parts.append('\n*<Truncated )')
        content_parts.append(repr(truncated))
        content_parts.append('>*')
    
    description = ''.join(content_parts)
    embed = Embed('Ping Log!', description)
    
    if everyone_mention:
        embed.add_field('Everyone mention', 'Hecatia Yeah!')
    
    if (user_mentions is not None):
        content_parts = []
        
        mention_count = len(user_mentions)
        if mention_count > USER_MENTION_MAX:
            truncated = mention_count - USER_MENTION_MAX
        else:
            truncated = 0
        
        content_parts.append('**Total:** ')
        content_parts.append(repr(mention_count))
        if truncated:
            content_parts.append(' (')
            content_parts.append(repr(truncated))
            content_parts.append(' truncated)')
        content_parts.append('\n')
        content_parts.append(SEPARATOR_LINE)
        content_parts.append('\n')
        
        index = 0
        limit = mention_count-truncated
        
        while True:
            user = user_mentions[index]
            index += 1
            
            if guild is None:
                nick = None
            else:
                try:
                    guild_profile = user.guild_profiles[guild]
                except KeyError:
                    nick = None
                else:
                    nick = guild_profile.nick
            
            content_parts.append('**')
            content_parts.append(repr(index))
            content_parts.append('.:** ')
            content_parts.append(user.full_name)
            content_parts.append(' ')
            if (nick is not None):
                content_parts.append('[')
                content_parts.append(nick)
                content_parts.append('] ')
            content_parts.append('(')
            content_parts.append(repr(author.id))
            content_parts.append(')')
            
            if index == limit:
                break
            
            content_parts.append('\n')
            continue
        
        field_value = ''.join(content_parts)
        
        embed.add_field('User mentions', field_value)
    
    if (role_mentions is not None):
        content_parts = []
        
        mention_count = len(role_mentions)
        if mention_count > ROLE_MENTION_MAX:
            truncated = mention_count - ROLE_MENTION_MAX
        else:
            truncated = 0
        
        content_parts.append('**Total:** ')
        content_parts.append(repr(mention_count))
        if truncated:
            content_parts.append(' (')
            content_parts.append(repr(truncated))
            content_parts.append(' truncated)')
        content_parts.append('\n')
        content_parts.append(SEPARATOR_LINE)
        content_parts.append('\n')
        
        index = 0
        limit = mention_count-truncated
        
        while True:
            role = role_mentions[index]
            index += 1
            
            content_parts.append('**')
            content_parts.append(repr(index))
            content_parts.append('.:** ')
            content_parts.append(role.name)
            content_parts.append(' (')
            content_parts.append(repr(role.id))
            content_parts.append(')')
            
            if index == limit:
                break
            
            content_parts.append('\n')
            continue
        
        field_value = ''.join(content_parts)
        
        embed.add_field('Role mentions', field_value)
    
    await client.message_create(CHANNEL__NEKO_DUNGEON_LOG, embed=embed, allowed_mentions=None)

# Hata best wrapper

OFFLINE = Status.offline.name

BIG_BROS = {}

@Koishi.events
async def ready(client):
    checkout_category()

def checkout_category():
    BIG_BROS.clear()
    for channel in CATEGORY__NEKO_DUNGEON__BIG_BRO.channel_list:
        try:
            user_id = int(channel.name)
        except ValueError:
            continue
        
        BIG_BROS[user_id] = channel


async def big_bro_channel_delete_waiter(client, channel, guild):
    try:
        user_id = int(channel.name)
    except ValueError:
        return
    
    try:
        del BIG_BROS[user_id]
    except KeyError:
        pass


async def big_bro_channel_create_waiter(client, channel):
    if channel.parent is not CATEGORY__NEKO_DUNGEON__BIG_BRO:
        return
    
    try:
        user_id = int(channel.name)
    except KeyError:
        return
    
    BIG_BROS[user_id] = channel


async def big_bro_channel_edit_waiter(client, channel, old_attributes):
    try:
        old_category = old_attributes['category']
    except KeyError:
        pass
    else:
        # Moved out
        if old_category is CATEGORY__NEKO_DUNGEON__BIG_BRO:
            try:
                name = old_attributes['name']
            except ValueError:
                name = channel.name
            
            try:
                user_id = int(name)
            except KeyError:
                pass
            else:
                try:
                    del BIG_BROS[user_id]
                except KeyError:
                    pass
            
            return
        
        # Moved in
        if channel.parent is CATEGORY__NEKO_DUNGEON__BIG_BRO:
            try:
                user_id = int(channel.name)
            except ValueError:
                pass
            else:
                BIG_BROS[user_id] = channel
            
            return
    
    if channel.parent is not CATEGORY__NEKO_DUNGEON__BIG_BRO:
        return
    
    try:
        name = old_attributes['name']
    except KeyError:
        pass
    else:
        try:
            user_id = int(name)
        except KeyError:
            pass
        else:
            try:
                del BIG_BROS[user_id]
            except KeyError:
                pass
    
    try:
        user_id = int(channel.name)
    except KeyError:
        pass
    else:
        BIG_BROS[user_id] = channel


@Koishi.events
async def user_presence_update(client, user, old_attributes):
    try:
        channel = BIG_BROS[user.id]
    except KeyError:
        return
    
    try:
        content_parts = render_contents(user, old_attributes)
        chunks = make_chunks(content_parts)
        
        for chunk in chunks:
            await client.message_create(channel, embed=Embed(description=chunk))
    except BaseException as err:
        await client.events.error(client, 'log.user_presence_update', err)


MAX_CHUNK_SIZE = 2000
BREAK_AFTER_LINE_COUNT = 1500


def render_contents(user, old_attributes):
    content_parts = []
    
    content_parts.append('User: ')
    content_parts.append(user.full_name)
    
    try:
        guild_profile = user.guild_profiles[CATEGORY__NEKO_DUNGEON__BIG_BRO]
    except KeyError:
        nick = None
    else:
        nick = guild_profile.nick
    
    if (nick is not None):
        content_parts.append(' [')
        content_parts.append(nick)
        content_parts.append(']')
    
    content_parts.append(' (')
    content_parts.append(repr(user.id))
    content_parts.append(')\n')
    
    content_parts.append('At: ')
    content_parts.append(datetime.now().__format__(DATETIME_FORMAT_CODE))
    content_parts.append('\n')
    content_parts.append('\n')
    
    try:
        statuses = old_attributes['statuses']
    except KeyError:
        pass
    else:
        try:
            status = old_attributes['status']
        except KeyError:
            pass
        else:
            content_parts.append('**Display status**')
            content_parts.append('\n')
            content_parts.append(status.name)
            content_parts.append(' -> ')
            content_parts.append(user.status.name)
            content_parts.append('\n')
            content_parts.append('\n')
        
        content_parts.append('**Statuses by device**')
        content_parts.append('\n')
        
        for key in ('desktop', 'mobile', 'web'):
            content_parts.append(key)
            content_parts.append(': ')
            content_parts.append(statuses.get(key, OFFLINE))
            content_parts.append(' -> ')
            content_parts.append(user.statuses.get(key, OFFLINE))
            content_parts.append('\n')
        
        content_parts.append('\n')
    
    try:
        activities = old_attributes['activities']
    except KeyError:
        pass
    else:
        added, updated, removed = activities
        if (added is not None):
            for activity in added:
                content_parts.append('**Added activity**:')
                content_parts.append('\n')
                render_activity(content_parts, activity)
                content_parts.append('\n')
        
        if (updated is not None):
            for activity_change in updated:
                content_parts.append('**Updated activity**:')
                content_parts.append('\n')
                activity = activity_change.activity
                for key, value in activity_change.old_attributes.items():
                    ACTIVITY_DIFFERENCE_RENDERERS[key](content_parts, value, activity)
                content_parts.append('\n')
        
        if (removed is not None):
            for activity in removed:
                content_parts.append('**Removed activity**:')
                content_parts.append('\n')
                render_activity(content_parts, activity)
                content_parts.append('\n')
    
    return content_parts


ACTIVITY_TYPE_NAMES = {
    0: 'game',
    1: 'stream',
    2: 'spotify',
    3: 'watching',
    4: 'custom',
    5: 'competing',
        }

def render_datetime_to(render_to, datetime_value):
    render_to.append(datetime_value.__format__(DATETIME_FORMAT_CODE))
    render_to.append(' [')
    render_to.append(elapsed_time(datetime_value))
    render_to.append(' ago]')


def render_activity(render_to, activity):
    render_to.append('**name:** ')
    render_to.append(repr(activity.name))
    render_to.append('\n')
    
    activity_type = activity.type
    activity_type_name = ACTIVITY_TYPE_NAMES.get(activity_type, 'unknown')
    render_to.append('**type:** ')
    render_to.append(activity_type_name)
    render_to.append(' (')
    render_to.append(repr(activity_type))
    render_to.append(')')
    render_to.append('\n')
    
    if activity_type != ACTIVITY_TYPES.custom:
        timestamps = activity.timestamps
        if (timestamps is not None):
            timestamp_start = activity.start
            if (timestamp_start is not None):
                render_to.append('**timestamp start:** ')
                render_datetime_to(render_to, timestamp_start)
                render_to.append('\n')
            
            timestamp_end = activity.end
            if (timestamp_end is not None):
                render_to.append('**timestamp end:** ')
                render_datetime_to(render_to, timestamp_end)
                render_to.append('\n')
        
        details = activity.details
        if (details is not None):
            render_to.append('**details:** ')
            render_to.append(repr(details))
            render_to.append('\n')
        
        state = activity.state
        if (state is not None):
            render_to.append('**state:** :')
            render_to.append(repr(state))
            render_to.append('\n')
        
        party = activity.party
        if (party is not None):
            party_id = party.id
            if (party_id is not None):
                render_to.append('**party id:** ')
                render_to.append(repr(party_id))
                render_to.append('\n')
            
            party_size = party.size
            party_max = party.max
            if party_size or party_max:
                if party_size:
                    render_to.append('**party size:** ')
                    render_to.append(repr(party_size))
                    render_to.append('\n')
                
                if party_max:
                    render_to.append('**party max:** ')
                    render_to.append(repr(party_max))
                    render_to.append('\n')
        
        assets = activity.assets
        if (assets is not None):
            asset_image_large = assets.image_large
            if (asset_image_large is not None):
                render_to.append('**asset image large:** ')
                render_to.append(repr(asset_image_large))
                render_to.append('\n')
            
            asset_text_large = assets.text_large
            if (asset_text_large is not None):
                render_to.append('**asset text large:** ')
                render_to.append(repr(asset_text_large))
                render_to.append('\n')
            
            asset_image_small = assets.image_small
            if (asset_image_small is not None):
                render_to.append('**asset image small:** ')
                render_to.append(repr(asset_image_small))
                render_to.append('\n')
            
            asset_text_small = assets.text_small
            if asset_text_small:
                render_to.append('**asset text small:** ')
                render_to.append(repr(asset_text_small))
                render_to.append('\n')
        
        album_cover_url = activity.album_cover_url
        if (album_cover_url is not None):
            render_to.append('**album cover url:** ')
            render_to.append(repr(album_cover_url))
            render_to.append('\n')
        
        secrets = activity.secrets
        if (secrets is not None):
            secret_join = secrets.join
            if (secret_join is not None):
                render_to.append('**secrets join:** ')
                render_to.append(repr(secret_join))
                render_to.append('\n')
            
            secret_spectate = secrets.spectate
            if (secret_spectate is not None):
                render_to.append('**secrets spectate:** ')
                render_to.append(repr(secret_spectate))
                render_to.append('\n')
            
            secret_match = secrets.match
            if (secret_match is not None):
                render_to.append('**secrets match:** ')
                render_to.append(repr(secret_match))
                render_to.append('\n')
        
        url = activity.url
        if (url is not None):
            render_to.append('**url:** ')
            render_to.append(repr(url))
            render_to.append('\n')
        
        sync_id = activity.sync_id
        if (sync_id is not None):
            render_to.append('**sync id:** ')
            render_to.append(repr(sync_id))
            render_to.append('\n')
        
        session_id = activity.session_id
        if (session_id is not None):
            render_to.append('**session id:** ')
            render_to.append(repr(session_id))
            render_to.append('\n')
        
        flags = activity.flags
        if flags:
            render_to.append('**flags:** ')
            render_to.append(', '.join(flags))
            render_to.append('\n')
        
        application_id = activity.application_id
        if activity.application_id:
            render_to.append('**application id:** ')
            render_to.append(repr(application_id))
            render_to.append('\n')
        
        created_at = activity.created_at
        if created_at > DISCORD_EPOCH_START:
            render_to.append('**created at:** ')
            render_datetime_to(render_to, created_at)
            render_to.append('\n')
        
        activity_id = activity.id
        if activity_id:
            render_to.append('**id:** ')
            render_to.append(repr(activity_id))
            render_to.append('\n')


def render_simple_difference(render_to, old_value, new_value):
    render_to.append(repr(old_value))
    render_to.append(' -> ')
    render_to.append(repr(new_value))
    render_to.append('\n')


def render_datetime_or_none_to(render_to, datetime_value):
    if datetime_value is None:
        render_to.append('None')
    else:
        render_datetime_to(render_to, datetime_value)


def render_simple_datetime_difference(render_to, old_value, new_value):
    render_datetime_or_none_to(render_to, old_value)
    render_to.append(' -> ')
    render_datetime_or_none_to(render_to, new_value)
    render_to.append('\n')


def render_name_difference(render_to, old_value, activity):
    render_to.append('**name:** ')
    render_simple_difference(render_to, old_value, activity.name)


def render_type_difference(render_to, old_value, activity):
    activity_type = activity.type
    activity_type_name = ACTIVITY_TYPE_NAMES.get(activity_type, 'unknown')
    old_value_name = ACTIVITY_TYPE_NAMES.get(activity_type, 'unknown')
    render_to.append('**type:** ')
    render_to.append(activity_type_name)
    render_to.append(' (')
    render_to.append(repr(activity_type))
    render_to.append(')')
    render_to.append(' -> ')
    render_to.append(old_value_name)
    render_to.append(' (')
    render_to.append(repr(old_value))
    render_to.append(')')
    render_to.append('\n')


def render_timestamps_difference(render_to, old_value, activity):
    new_value = activity.timestamps
    if old_value is None:
        old_timestamp_start = None
    else:
        old_timestamp_start = old_value.start
    if new_value is None:
        new_timestamp_start = None
    else:
        new_timestamp_start = new_value.start
    
    if old_timestamp_start != new_timestamp_start:
        render_to.append('**timestamp start:** ')
        render_simple_datetime_difference(render_to, old_timestamp_start, new_timestamp_start)
    
    if old_value is None:
        old_timestamp_end = None
    else:
        old_timestamp_end = old_value.end
    if new_value is None:
        new_timestamp_end = None
    else:
        new_timestamp_end = new_value.end
    
    if old_timestamp_end != new_timestamp_end:
        render_to.append('**timestamp end:** ')
        render_simple_datetime_difference(render_to, old_timestamp_end, new_timestamp_end)


def render_details_difference(render_to, old_value, activity):
    render_to.append('**details:** ')
    render_simple_difference(render_to, old_value, activity.details)


def render_state_difference(render_to, old_value, activity):
    render_to.append('**state:** ')
    render_simple_difference(render_to, old_value, activity.state)


def render_party_difference(render_to, old_value, activity):
    new_value = activity.party
    
    if old_value is None:
        old_party_id = None
    else:
        old_party_id = old_value.id
    if new_value is None:
        new_party_id = None
    else:
        new_party_id = new_value.id
    
    if old_party_id != new_party_id:
        render_to.append('**party id:** ')
        render_simple_difference(render_to, old_party_id, new_party_id)
    
    if old_value is None:
        old_party_size = 0
        old_party_max = 0
    else:
        old_party_size = old_value.size
        old_party_max = old_value.max
    if new_value is None:
        new_party_size = 0
        new_party_max = 0
    else:
        new_party_size = new_value.size
        new_party_max = new_value.max
    
    if old_party_size or old_party_max or new_party_size or new_party_max:
        if (old_party_size or new_party_size) and (old_party_size != new_party_size):
            render_to.append('**party size:** ')
            render_simple_difference(render_to, old_party_size, new_party_size)
        
        if (old_party_max or new_party_max) and (old_party_max != new_party_max):
            render_to.append('**party max:** ')
            render_simple_difference(render_to, old_party_max, new_party_max)


def render_assets_difference(render_to, old_value, activity):
    new_value = activity.assets
    
    if old_value is None:
        old_asset_image_large = None
    else:
        old_asset_image_large = old_value.image_large
    if new_value is None:
        mew_asset_image_large = None
    else:
        mew_asset_image_large = new_value.image_large
    if old_asset_image_large != mew_asset_image_large:
        render_to.append('**asset image large:** ')
        render_simple_difference(render_to, old_asset_image_large, mew_asset_image_large)
    
    if old_value is None:
        old_asset_text_large = None
    else:
        old_asset_text_large = old_value.text_large
    if new_value is None:
        new_asset_text_large = None
    else:
        new_asset_text_large = new_value.text_large
    if old_asset_text_large != new_asset_text_large:
        render_to.append('**asset text large:** ')
        render_simple_difference(render_to, old_asset_text_large, new_asset_text_large)
    
    if old_value is None:
        old_asset_image_small = None
    else:
        old_asset_image_small = old_value.image_small
    if new_value is None:
        mew_asset_image_small = None
    else:
        mew_asset_image_small = new_value.image_small
    if old_asset_image_small != mew_asset_image_small:
        render_to.append('**asset image small:** ')
        render_simple_difference(render_to, old_asset_image_small, mew_asset_image_small)
    
    if old_value is None:
        old_asset_text_small = None
    else:
        old_asset_text_small = old_value.text_small
    if new_value is None:
        new_asset_text_small = None
    else:
        new_asset_text_small = new_value.text_small
    if old_asset_text_small != new_asset_text_small:
        render_to.append('**asset text small:** ')
        render_simple_difference(render_to, old_asset_text_small, new_asset_text_small)


def render_album_cover_url_difference(render_to, old_value, activity):
    render_to.append('**album cover url:** ')
    render_simple_difference(render_to, old_value, activity.album_cover_url)


def render_secret_difference(render_to, old_value, activity):
    new_value = activity.secrets
    
    if old_value is None:
        old_secret_join = None
    else:
        old_secret_join = old_value.join
    if new_value is None:
        new_secret_join = None
    else:
        new_secret_join = new_value.join
    if old_secret_join != new_secret_join:
        render_to.append('**secrets join:** ')
        render_simple_difference(render_to, old_secret_join, new_secret_join)
    
    if old_value is None:
        old_secret_spectate = None
    else:
        old_secret_spectate = old_value.spectate
    if new_value is None:
        new_secret_spectate = None
    else:
        new_secret_spectate = new_value.spectate
    if old_secret_spectate != new_secret_spectate:
        render_to.append('**secrets spectate:** ')
        render_simple_difference(render_to, old_secret_spectate, new_secret_spectate)
    
    if old_value is None:
        old_secret_match = None
    else:
        old_secret_match = old_value.match
    if new_value is None:
        new_secret_match = None
    else:
        new_secret_match = new_value.match
    if old_secret_match != new_secret_match:
        render_to.append('**secrets spectate:** ')
        render_simple_difference(render_to, old_secret_match, new_secret_match)


def render_url_difference(render_to, old_value, activity):
    render_to.append('**url:** ')
    render_simple_difference(render_to, old_value, activity.url)


def render_sync_id_difference(render_to, old_value, activity):
    render_to.append('**sync id:** ')
    render_simple_difference(render_to, old_value, activity.sync_id)


def render_session_id_difference(render_to, old_value, activity):
    render_to.append('**session id:** ')
    render_simple_difference(render_to, old_value, activity.session_id)


def render_flags_difference(render_to, old_value, activity):
    render_to.append('**flags:** ')
    render_to.append(', '.join(old_value))
    render_to.append(' -> ')
    render_to.append(', '.join(activity.flags))
    render_to.append('\n')


def render_application_id_difference(render_to, old_value, activity):
    render_to.append('**application id:** ')
    render_simple_difference(render_to, old_value, activity.application_id)


def render_created_at_difference(render_to, old_value, activity):
    if old_value == 0:
        old_value = DISCORD_EPOCH_START
    else:
        old_value = datetime.utcfromtimestamp(old_value/1000.)

    render_to.append('**created at:** ')
    render_simple_datetime_difference(render_to, old_value, activity.created_at)


def render_id_difference(render_to, old_value, activity):
    render_to.append('**id:** ')
    render_simple_difference(render_to, old_value, activity.id)


ACTIVITY_DIFFERENCE_RENDERERS = {
    'name' : render_name_difference,
    'type' : render_type_difference,
    'timestamps' : render_timestamps_difference,
    'details' : render_details_difference,
    'state' : render_state_difference,
    'party' : render_party_difference,
    'assets' : render_assets_difference,
    'album_cover_url' : render_album_cover_url_difference,
    'secrets' : render_secret_difference,
    'url'  : render_url_difference,
    'sync_id' : render_sync_id_difference,
    'session_id' : render_session_id_difference,
    'flags' : render_flags_difference,
    'application_id' : render_application_id_difference,
    'created' : render_created_at_difference,
    'id' : render_id_difference,
        }


def add_chunk(chunks, chunk):
    while chunk:
        if chunk[-1] == '\n':
            del chunk[-1]
            continue
        
        break
    else:
        return
    
    chunks.append(''.join(chunk))
    chunk.clear()

def make_chunks(parts):
    chunks = []
    chunk = []
    chunk_length = 0
    for part in parts:
        if part == '\n':
            if chunk:
                if chunk_length > BREAK_AFTER_LINE_COUNT:
                    add_chunk(chunks, chunk)
                    chunk_length = 0
                else:
                    chunk.append('\n')
                    chunk_length += 1
            else:
                # Do not add linebreak at the start
                continue
        else:
            chunk_length += len(part)
            if chunk_length > MAX_CHUNK_SIZE:
                chunk_length = MAX_CHUNK_SIZE-chunk_length
                chunk.append(part[:chunk_length])
                add_chunk(chunks, chunk)
                chunk.append(part[chunk_length:])
                chunk_length = -chunk_length
            else:
                chunk.append(part)
    
    add_chunk(chunks, chunk)
    return chunks

