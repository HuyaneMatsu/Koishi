__all__ = ()

import re
from random import choice, randint, shuffle

from hata import BUILTIN_EMOJIS, Color, Embed, Emoji, InteractionType
from hata.ext.slash import Button, ButtonStyle, InteractionResponse, Row

from ...bots import FEATURE_CLIENTS

from .category import CATEGORIES
from .item import ITEMS
from .trivias import CATEGORY_KOISHI_ALL, CATEGORY_KOISHI_CANON


OPTION_PATTERN = re.compile('trivia\\.([0-9a-fA-F]+)\\.option\\.([0-9a-fA-F]+)\\.([0-9a-fA-F]+)\\.([0-9a-fA-F]+)')
NEW_PATTERN = re.compile('trivia\\.([0-9a-fA-F]+)\\.new\\.([0-9a-fA-F]+)\\.([0-9a-fA-F]+)')


EMOJI_NEW = Emoji.precreate(1079504073981693962)


CATEGORY_NAME_TO_ID = {
    CATEGORY_KOISHI_CANON.name: CATEGORY_KOISHI_CANON.id,
    CATEGORY_KOISHI_ALL.name: CATEGORY_KOISHI_ALL.id,
}


COLOR_DEFAULT = Color(0x2accde)
COLOR_CORRECT = Color(0x49a800)
COLOR_BAD = Color(0xd9273c)


OPTION_EMOJIS = (
    BUILTIN_EMOJIS['regional_indicator_a'],
    BUILTIN_EMOJIS['regional_indicator_b'],
    BUILTIN_EMOJIS['regional_indicator_c'],
    BUILTIN_EMOJIS['regional_indicator_d'],
)

OPTION_MAX = len(OPTION_EMOJIS)


GOOD_ANSWER_RESPONSES = (
    (lambda client, event: 'I raised that neko.'),
    (lambda client, event: 'Biiingo~'),
    (lambda client, event: f'{client.name_at(event.guild_id)} is proud of you.'),
    (lambda client, event: f'{event.user.name_at(event.guild_id)} is a bit of a genius, it turns out.'),
    (
        lambda client, event:
        f'Roses are red, {client.name_at(event.guild_id)} is shiny, '
        f'{event.user.name_at(event.guild_id)} is eating with us, the dinner is fried shrimp.'
    ),
    (lambda client, event: f'Heart throbbing correct answer.'),
    (
        lambda client, event:
        f'{client.name_at(event.guild_id)} never gonna give {event.user.name_at(event.guild_id)} up, '
        f'never gonna let them down.'
    ),
    (
        lambda client, event:
        f'{client.name_at(event.guild_id)} just arrived. {event.user.name_at(event.guild_id)} seems smart.'
    ),
    (lambda client, event: f'{event.user.name_at(event.guild_id)} is here with the correct answer.'),
    (lambda client, event: f'{event.user.name_at(event.guild_id)} just answered correctly. Mr. Hat helped them.'),
    (lambda client, event: f'{event.user.name_at(event.guild_id)} seems conscious - please nerf.'),
)

BAD_ANSWER_RESPONSES = (
    (lambda client, event: f'{event.user.name_at(event.guild_id)} wont fish with us.'),
    (lambda client, event: f'{event.user.name_at(event.guild_id)} answered incorrectly - *staaaare*.'),
    (lambda client, event: f'{event.user.name_at(event.guild_id)} already stopped thinking.'),
    (
        lambda client, event:
        f'It\'s a youkai! It\'s a fairy! Nevermind, it\'s just {event.user.name_at(event.guild_id)}.'
    ),
    (
        lambda client, event:
        f'{event.user.name_at(event.guild_id)} couldn\'t help {client.name_at(event.guild_id)} find a fishing rod.'
    ),
    (lambda client, event: f'Is {event.user.name_at(event.guild_id)} a genius? Nah, they are a fumo!.'),
    (lambda client, event: f'Moshi Moshi? Wrong call.'),
    (lambda client, event: f'{event.user.name_at(event.guild_id)} couldn\'t join the Extra stage.'),
    (lambda client, event: f'{event.user.name_at(event.guild_id)} must collect additional Power items.'),
    (lambda client, event: f'{event.user.name_at(event.guild_id)} left Mr Hat by the door.'),
    (lambda client, event: f'{event.user.name_at(event.guild_id)} failed to capture this spellcard.'),
    (lambda client, event: f'{event.user.name_at(event.guild_id)} just pichuuned.'),
    (lambda client, event: f'Baaaka~'),
    (lambda client, event: f'{event.user.name_at(event.guild_id)} just lost a life.'),
    (lambda client, event: f'{event.user.name_at(event.guild_id)} has to use a continue.'),
)


def select_options(item):
    """
    Selects options for the given item.
    
    Parameters
    ----------
    item : ``TriviaItem``
        Item to select options from.
    
    Returns
    -------
    selected_options : `list` of `tuple` (`str`, `int`)
        Options with their identifier. Always the option with id of 0 is the correct.
    """
    selected_options = [(item.correct, 0)]
    selected_option_count = 1
    
    options = [*item.options]
    
    option_to_id = {option: index for index, option in enumerate(options, 1)}
    
    option_count = len(options)
    
    while (selected_option_count < OPTION_MAX) and (option_count > 0):
        option_count -= 1
        option = options.pop(randint(0, option_count))
        
        selected_option_count += 1
        selected_options.append((option, option_to_id[option]))
    
    shuffle(selected_options)
    return selected_options


def get_final_style(index, selected_option_id):
    """
    Helper function of ``build_final_components`` to get the button's style.
    
    Parameters
    ----------
    index : `int`
        the component's index.
    selected_option_id : `int`
        The selected option's identifier.
    
    Returns
    -------
    style : ``ButtonStyle``
    """
    if index == 0:
        if index == selected_option_id:
            return ButtonStyle.green
        
        return ButtonStyle.blue
    
    if index == selected_option_id:
        return ButtonStyle.red
    
    return ButtonStyle.gray


def build_components(selected_options, user_id, category_id, item_id):
    """
    Builds response components.
    
    Parameters
    ----------
    selected_options : `list` of `tuple` (`str`, `int`)
        The selected options to show.
    user_id : `int`
        The user's identifier who invoked the command.
    category_id : `int`
        The trivia category's identifier.
    item_id : `int`
        The trivia item's identifier.
    
    Returns
    -------
    components : `list` of ``Component``
    """
    return [
        Row(Button(
            option[:100],
            emoji,
            custom_id = f'trivia.{user_id:x}.option.{category_id:x}.{item_id:x}.{option_id:x}',
        ))
        for (option, option_id), emoji in zip(selected_options, OPTION_EMOJIS)
    ]


def build_final_components(selected_options, user_id, category_id, item_id, selected_option_id):
    """
    Builds response components for a final response.
    
    Parameters
    ----------
    selected_options : `list` of `tuple` (`str`, `int`)
        The selected options to show.
    user_id : `int`
        The invoker user's identifier.
    category_id : `int`
        The trivia category's identifier.
    item_id : `int`
        The trivia item's identifier.
    selected_option_id : `int`
        The selected option's identifier by the user.
    
    Returns
    -------
    components : `list` of ``Component``
    """
    return [
        *(
            Row(Button(
                option[:100],
                emoji,
                custom_id = f'trivia.{user_id:x}.option.{category_id:x}.{item_id:x}.{option_id:x}',
                enabled = False,
                style = get_final_style(option_id, selected_option_id),
            ))
            for (option, option_id), emoji in zip(selected_options, OPTION_EMOJIS)
        ),
        Row(Button(
            '!! Another one !!',
            EMOJI_NEW,
            custom_id = f'trivia.{user_id:x}.new.{category_id:x}.{item_id:x}',
            style = ButtonStyle.blue,
        )),
    ]


def reparse_selected_options(event, item):
    """
    Re-parses the already selected options.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    item : ``triviaItem``
        the item to pull the options from.
    
    Returns
    -------
    selected_options : `list` of `tuple` (`str`, `int`)
    """
    selected_options = []
    
    for row in  event.message.iter_components():
        match = OPTION_PATTERN.fullmatch(row.components[0].custom_id)
        if match is None:
            continue
        
        option_id = int(match.group(4), base = 16)
        if option_id == 0:
            value = item.correct
        else:
            try:
                value = item.options[option_id - 1]
            except IndexError:
                continue
        
        selected_options.append((value, option_id))
    
    return selected_options


def is_interaction_chained(interaction_event):
    """
    Returns whether the interaction is chained.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    chained : `bool`
    """
    message = interaction_event.message
    if message is None:
        return False
    
    interaction = message.interaction
    
    # Old style -> chained through `.referenced_message`
    if interaction is None:
        return True
    
    # New style -> chained through `.interaction.type == InteractionType.message_component`
    if interaction.type is InteractionType.message_component:
        return True
    
    return False


async def send_user_mismatch_notification(client, event):
    """
    Sends user mismatch notification.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_acknowledge(event)
    await client.interaction_followup_message_create(
        event,
        content = 'You must be the same user who invoked the command.',
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def trivia(
    event,
    category_id: (CATEGORY_NAME_TO_ID, 'Choose a category.', 'category') = CATEGORY_KOISHI_ALL.id,
):
    """
    Koishi trivia for everyone!
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        the received interaction event.
    category_id : `int`
        The category's identifier.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    category = CATEGORIES[category_id]
    item = choice(category.items)
    
    return InteractionResponse(
        embed = Embed(item.question, color = COLOR_DEFAULT),
        components = build_components(select_options(item), event.user.id, category.id, item.id),
        allowed_mentions = None,
    )



@FEATURE_CLIENTS.interactions(custom_id = OPTION_PATTERN)
async def trivia_select(client, event, user_id_string, category_id_string, item_id_string, selected_option_id_string):
    """
    Handles when an option is selected.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    user_id_string : `str`
        The original invoker user's identifier as string (hexadecimal).
    category_id_string : `str`
        The category's id as string (hexadecimal).
    item_id_string : `str`
        The item's id as string (hexadecimal).
    selected_option_id_string : `str`
        The option's identifier (hexadecimal).
    
    Returns
    -------
    response : `None`, ``InteractionResponse``
    """
    user_id = int(user_id_string, base = 16)
    if event.user.id != user_id:
        return await send_user_mismatch_notification(client, event)
    
    category_id = int(category_id_string, base = 16)
    item_id = int(item_id_string, base = 16)
    selected_option_id = int(selected_option_id_string, base = 16)
    
    try:
        item = ITEMS[item_id]
    except KeyError:
        return
    
    if selected_option_id:
        description_generators = BAD_ANSWER_RESPONSES
        color = COLOR_BAD
    else:
        description_generators = GOOD_ANSWER_RESPONSES
        color = COLOR_CORRECT
    
    embed = Embed(item.question, f'**{choice(description_generators)(client, event)}**', color = color)
    if is_interaction_chained(event):
        user = event.user
        guild_id = event.guild_id
        
        embed.add_author(
            user.name_at(guild_id),
            user.avatar_url_at(guild_id),
        )
    
    return InteractionResponse(
        embed = embed,
        components = build_final_components(
            reparse_selected_options(event, item), user_id, category_id, item_id, selected_option_id,
        ),
        allowed_mentions = None,
    )


@FEATURE_CLIENTS.interactions(custom_id = NEW_PATTERN)
async def trivia_new(client, event, user_id_string, category_id_string, item_id_string):
    """
    Shows a new trivia.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    user_id_string : `str`
        The original invoker user's identifier as string (hexadecimal).
    category_id_string : `str`
        The category's id as string (hexadecimal).
    item_id_string : `str`
        The previous item's id as string (hexadecimal).
    
    Returns
    -------
    response : `None`, ``InteractionResponse``
    """
    user_id = int(user_id_string, base = 16)
    if event.user.id != user_id:
        return await send_user_mismatch_notification(client, event)
    
    category_id = int(category_id_string, base = 16)
    item_id = int(item_id_string, base = 16)
    
    await client.interaction_component_message_edit(
        event,
        components = event.message.components[:-1],
    )
    
    try:
        category = CATEGORIES[category_id]
    except KeyError:
        return
    
    items = category.items
    # select random except last
    item = items[randint(0, len(items) - 2)]
    if item.id == item_id:
        # if we hit same select last
        item = items[-1]
    
    user = event.user
    guild_id = event.guild_id
    
    return InteractionResponse(
        embed = Embed(
            item.question,
            color = COLOR_DEFAULT
        ).add_author(
            user.name_at(guild_id),
            user.avatar_url_at(guild_id),
        ),
        components = build_components(select_options(item), user.id, category.id, item.id),
        allowed_mentions = None,
    )
