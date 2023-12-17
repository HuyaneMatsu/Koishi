__all__ = ()

from hata import Embed, INVITE_URL_RP
from hata.discord.utils import URL_RP
from hata.ext.slash import Form, TextInput, TextInputStyle

from ...bots import FEATURE_CLIENTS

from ..automation_core import get_welcome_style_name
from ..embed_image_refresh import schedule_image_refresh

from .constants import CUSTOM_ID_WELCOME_REPLY, CUSTOM_ID_WELCOME_REPLY_CUSTOM, REPLY_EXPIRES_AFTER
from .spam_protection import is_reply_in_cache, put_reply_in_cache
from .welcome_styles import get_welcome_style


def get_censor_reason_for_message_content(message_content):
    """
    Gets why a message's content should be censored and not forwarded.
    
    Parameters
    ----------
    message_content : `str`
        The message content to censor.
    
    Returns
    -------
    censor_reason : `None | str`
    """
    if INVITE_URL_RP.search(message_content) is not None:
        return 'Invites in the message content are forbidden.'
    
    if URL_RP.search(message_content) is not None:
        return 'Urls in the message content are forbidden.'


async def check_should_censor_and_notify(client, event, message_content):
    """
    Checks whether the given message should be censored and censors it if applicable.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    message_content : `str`
        The message content to censor.
    
    Returns
    -------
    passed : `bool`
    """
    censor_reason = get_censor_reason_for_message_content(message_content)
    if censor_reason is None:
        return False
    
    await client.interaction_component_acknowledge(event)
    await client.interaction_followup_message_create(
        event,
        content = censor_reason,
        show_for_invoking_user_only = True,
    )
    return True


def get_joined_user(event):
    """
    Gets the joined user.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    joined_user : `None | ClientUserBase`
    """
    message = event.message
    if message is None:
        return None
    
    mentioned_users = message.mentioned_users
    if mentioned_users is None:
        return None
    
    return mentioned_users[0]


async def check_joined_user_and_notify(client, event, joined_user):
    """
    Checks whether the joined user is the same as the invoking one. If yes notifies.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    joined_user : `None | ClientUserBase`
        The user who joined.
    
    Returns
    -------
    passed : `bool`
    """
    if joined_user is None:
        return True
    
    if joined_user is not event.user:
        return False
    
    await client.interaction_component_acknowledge(event)
    await client.interaction_followup_message_create(
        event,
        content = 'Sorry, but you shall not welcome yourself. Please wait for someone else to join to welcome them.',
        show_for_invoking_user_only = True,
    )
    return True
    

async def check_expired_and_notify(client, event):
    """
    Notifies the user whether they are late to welcome.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    passed : `bool`
    """
    if event.id - event.message.id <= REPLY_EXPIRES_AFTER:
        return False
    
    await client.interaction_component_acknowledge(event)
    await client.interaction_followup_message_create(
        event,
        content = 'You are late to the party! Be earlier next time :3',
        show_for_invoking_user_only = True,
    )
    
    await client.interaction_response_message_edit(
        event,
        components = None,
    )
    return True


async def check_cache_and_notify(client, event, actioning):
    """
    Checks whether the welcoming action is in the cache.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    actioning : `bool`
        Whether we are actioning now and should insert or nah.
    
    Returns
    -------
    passed : `bool`
    """
    if actioning:
        check = put_reply_in_cache
    else:
        check = is_reply_in_cache
    
    if not check(event.guild_id, event.message.id, event.user_id):
        return False
    
    await client.interaction_component_acknowledge(event)
    await client.interaction_followup_message_create(
        event,
        content = 'You shall not welcome twice :3',
        show_for_invoking_user_only = True,
    )
    return True


def process_custom_message(custom_message_content):
    """
    Processes the custom message defined by the user.
    
    Parameters
    ----------
    custom_message_content : `None | str`
        The custom message content to get its lines of.
    
    Returns
    -------
    lines : `None | list<str>`
    """
    if custom_message_content is None:
        return None
    
    lines = custom_message_content.splitlines()
    lines = [line for line in (line.rstrip() for line in lines) if line]
    if not lines:
        return None
    
    return '\n'.join(lines)


async def create_welcome_reply(client, event, joined_user, custom_message_content):
    """
    Creates the welcome message reply.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    joined_user : ``ClientUserBase``
        The user who joined.
    custom_message_content : `None | str`
        Custom message content to attach.
    """
    await client.interaction_component_acknowledge(event)
    
    welcome_style = get_welcome_style(get_welcome_style_name(event.guild_id), client.id)
    
    seed = event.guild_id ^ joined_user.id
    reply_styles = welcome_style.reply_styles
    reply_style = reply_styles[seed % len(reply_styles)]

    content = '> ' + reply_style.reply_content_builder(event.user.mention, joined_user.mention)
    
    seed = seed ^ event.user_id
    images = welcome_style.images

    embed = Embed(color = event.user.color_at(event.guild_id)).add_image(images[seed % len(images)])
    
    custom_message_content = process_custom_message(custom_message_content)
    if custom_message_content is not None:
        embed.add_author(custom_message_content, event.user.avatar_url_at(event.guild_id))
    
    message = await client.interaction_followup_message_create(
        event,
        allowed_mentions = [joined_user],
        content = content,
        embed = embed,
        silent = True,
    )
    schedule_image_refresh(client, message, event)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_WELCOME_REPLY)
async def welcome_reply(client, event):
    """
    Sends a welcome reply.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    joined_user = get_joined_user(event)
    if await check_joined_user_and_notify(client, event, joined_user):
        return
    
    if await check_expired_and_notify(client, event):
        return
    
    if await check_cache_and_notify(client, event, True):
        return
    
    await create_welcome_reply(client, event, joined_user, None)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_WELCOME_REPLY_CUSTOM)
async def welcome_reply_custom_form(client, event):
    """
    Shows a form to type in the custom message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    form : `None | InteractionForm`
    """
    joined_user = get_joined_user(event)
    if await check_joined_user_and_notify(client, event, joined_user):
        return
    
    if await check_expired_and_notify(client, event):
        return
    
    if await check_cache_and_notify(client, event, False):
        return
    
    
    return Form(
        'Custom welcome',
        [
            TextInput(
                'Message content',
                min_length = 2,
                max_length = 256,
                custom_id = 'message_content',
                style = TextInputStyle.paragraph,
            ),
        ],
        custom_id = CUSTOM_ID_WELCOME_REPLY_CUSTOM,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_WELCOME_REPLY_CUSTOM, target = 'form')
async def welcome_reply_custom_form(client, event, *, message_content):
    """
    Shows a form to type in the custom message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    message_content : `str` (Keyword only)
        Content to send.
    """
    joined_user = get_joined_user(event)
    if await check_joined_user_and_notify(client, event, joined_user):
        return
    
    if await check_expired_and_notify(client, event):
        return
    
    if await check_cache_and_notify(client, event, True):
        return
    
    if await check_should_censor_and_notify(client, event, message_content):
        return
    
    await create_welcome_reply(client, event, joined_user, message_content)
