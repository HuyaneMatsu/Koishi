__all__ = ()

from random import choice, shuffle
from html import unescape as html_unescape
from functools import partial as partial_func

from scarletio import Lock
from hata import Client, Embed, BUILTIN_EMOJIS, KOKORO, Color
from hata.ext.slash import InteractionResponse, abort, Button, Row, wait_for_component_interaction, ButtonStyle

from bot_utils.constants import GUILD__SUPPORT

SLASH_CLIENT : Client

TRIVIA_QUEUE = []
TRIVIA_URL = 'https://opentdb.com/api.php'
TRIVIA_REQUEST_LOCK = Lock(KOKORO)
TRIVIA_USER_LOCK = set()


COLOR_DEFAULT = Color(0x2accde)
COLOR_CORRECT = Color(0x49a800)
COLOR_BAD = Color(0xd9273c)

COUNTER = range(5)


TRIVIA_EMOJIS = (
    BUILTIN_EMOJIS['regional_indicator_a'],
    BUILTIN_EMOJIS['regional_indicator_b'],
    BUILTIN_EMOJIS['regional_indicator_c'],
    BUILTIN_EMOJIS['regional_indicator_d'],
    BUILTIN_EMOJIS['regional_indicator_e'],
)


CUSTOM_IDS = (
    'trivia.answer.0',
    'trivia.answer.1',
    'trivia.answer.2',
    'trivia.answer.3',
    'trivia.answer.4',
)

CUSTOM_ID_TO_INDEX = {custom_id: index for index, custom_id in enumerate(CUSTOM_IDS)}


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

async def get_trivias():
    """
    Gets a chunk of trivias and extends `TRIVIA_QUEUE` with them.
    
    This function is a coroutine.
    """
    if TRIVIA_REQUEST_LOCK.is_locked():
        await TRIVIA_REQUEST_LOCK
        return
    
    async with TRIVIA_REQUEST_LOCK:
        async with SLASH_CLIENT.http.get(TRIVIA_URL, params = {'amount': 100, 'category': 31}) as response:
            if response.status != 200:
                return
            
            json = await response.json()
        
        for trivia_data in json['results']:
            trivia = (
                html_unescape(trivia_data['question']),
                html_unescape(trivia_data['correct_answer']),
                [html_unescape(element) for element in trivia_data['incorrect_answers']],
            )
            
            TRIVIA_QUEUE.append(trivia)
            shuffle(TRIVIA_QUEUE)


async def get_trivia():
    """
    Gets a trivia. If there is none, tries to request them. If non is received returns `None`.
    
    This function is a coroutine.
    
    Returns
    -------
    trivia : `None`, `list` (`str`, `str`, `list` of `str`)
    """
    if TRIVIA_QUEUE:
        return TRIVIA_QUEUE.pop()
    
    await get_trivias()
    
    if TRIVIA_QUEUE:
        return TRIVIA_QUEUE.pop()
    
    return None


def check_is_user_same(user, event):
    """
    Checks whether the two users match.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        Event received from the original event.
    event : ``InteractionEvent``
        The received event.
    
    Returns
    -------
    is_user_same : `bool`
    """
    return user is event.user


def build_initial_components(possibilities, enabled):
    """
    Builds components for initial response of ``trivia_``.
    
    Parameters
    ----------
    possibilities : `list` of `str`
        Possible answers.
    enabled : `bool`
        Whether the components should be enabled.
    
    Returns
    -------
    components : `list` of ``Component``
    """
    return [
        Row(Button(possibility[:100], emoji, custom_id = custom_id, enabled = enabled))
        for possibility, emoji, custom_id in zip(possibilities, TRIVIA_EMOJIS, CUSTOM_IDS)
    ]


def get_final_style(index, correct_index, selected_index):
    """
    Helper function of ``build_final_components`` to get the button's style.
    
    Parameters
    ----------
    index : `int`
        the component's index.
    correct_index : `int`
        The correct answer's index.
    selected_index : `int`
        The selected answer's index.
    
    Returns
    -------
    style : ``ButtonStyle``
    """
    if index == correct_index:
        if index == selected_index:
            return ButtonStyle.green
        
        return ButtonStyle.blue
    
    if index == selected_index:
        return ButtonStyle.red
    
    return ButtonStyle.gray


def build_final_components(possibilities, correct_index, selected_index):
    """
    Builds the final response components.
    
    Parameters
    ----------
    possibilities : `list` of `str`
        Possible answers.
    correct_index : `int`
        The correct answer's index.
    selected_index : `int`
        The selected answer's index.
    
    Returns
    -------
    components : `list` of ``Component``
    """
    return [
        Row(Button(
            possibility[:100],
            emoji,
            custom_id = custom_id,
            enabled = False,
            style = get_final_style(index, correct_index, selected_index),
        ))
        for possibility, emoji, custom_id, index in zip(possibilities, TRIVIA_EMOJIS, CUSTOM_IDS, COUNTER)
    ]


@SLASH_CLIENT.interactions(guild = GUILD__SUPPORT, name = 'trivia')
async def trivia_(client, event):
    """Asks a trivia."""
    user = event.user
    if user.id in TRIVIA_USER_LOCK:
        abort('You are already in a trivia game.')
    
    TRIVIA_USER_LOCK.add(user.id)
    try:
        yield
        
        trivia = await get_trivia()
        if trivia is None:
            abort('No trivias for now.')
            return
        
        question, correct, wrong = trivia
        del wrong[4:]
        possibilities = [correct, *wrong]
        shuffle(possibilities)
        correct_index = possibilities.index(correct)
        
        message = yield InteractionResponse(
            embed = Embed(question, color = COLOR_DEFAULT,).add_author(user.full_name, user.avatar_url),
            components = build_initial_components(possibilities, True),
            allowed_mentions = None,
        )
        
        try:
            component_interaction = await wait_for_component_interaction(
                message,
                timeout = 300.0,
                check = partial_func(check_is_user_same, event.user)
            )
        except TimeoutError:
            title = question
            description = '*Timeout occurred.*'
            component_interaction = None
            components = build_initial_components(possibilities, False)
            color = COLOR_DEFAULT
        
        else:
            selected_index = CUSTOM_ID_TO_INDEX.get(component_interaction.custom_id, -1)
            components = build_final_components(possibilities, correct_index, selected_index)
            
            if selected_index == correct_index:
                title = question
                description_generators = GOOD_ANSWER_RESPONSES
                color = COLOR_CORRECT
            
            else:
                title = question
                description_generators = BAD_ANSWER_RESPONSES
                color = COLOR_BAD
            
            description = f'**{choice(description_generators)(client, event)}**'
        
        yield InteractionResponse(
            embed = Embed(title, description, color = color).add_author(user.full_name, user.avatar_url),
            components = components,
            event = component_interaction,
            message = message,
            allowed_mentions = None,
        )
    
    finally:
        TRIVIA_USER_LOCK.discard(user.id)
