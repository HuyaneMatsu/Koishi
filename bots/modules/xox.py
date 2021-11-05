from functools import partial as partial_func
from random import random, choice

from hata import Emoji, BUILTIN_EMOJIS, Client, Embed, DiscordException, ERROR_CODES, Task, KOKORO
from hata.ext.slash import iter_component_interactions, Button, ButtonStyle, wait_for_component_interaction

from bot_utils.constants import GUILD__SUPPORT

EMOJI_P2 = Emoji.precreate(704393708467912875)
EMOJI_P1 = Emoji.precreate(812069466069663765)
EMOJI_NOTHING = Emoji.precreate(568838460434284574)

ARRAY_IDENTIFIER_EMPTY = 0
ARRAY_IDENTIFIER_P1 = 1
ARRAY_IDENTIFIER_P2 = 2

GAME_STATE_NONE = 0
GAME_STATE_DRAW = 1
GAME_STATE_P1_WIN = 2
GAME_STATE_P2_WIN = 3

CUSTOM_ID_MAP = {str(index): index for index in range(9)}
CUSTOM_ID_CHALLENGE = 'xox.challenge'

BUTTON_CHALLENGE_ENABLED = Button(
    label = 'Challenge!',
    custom_id = CUSTOM_ID_CHALLENGE,
)

BUTTON_CHALLENGE_DISABLED = BUTTON_CHALLENGE_ENABLED.copy_with(enabled=False)

SLASH_CLIENT: Client

def check_event_user(user, event):
    return event.user is user

def check_event_other_user(user, event):
    return event.user is not user

def render_array(array, all_disabled):
    row_buttons = []
    buttons = [row_buttons]
    
    for index in range(len(array)):
        if len(row_buttons) == 3:
            row_buttons = []
            buttons.append(row_buttons)
        
        element = array[index]
        
        if element == ARRAY_IDENTIFIER_EMPTY:
            emoji = EMOJI_NOTHING
            style = ButtonStyle.violet
        elif element == ARRAY_IDENTIFIER_P1:
            emoji = EMOJI_P1
            style = ButtonStyle.red
        else:
            emoji = EMOJI_P2
            style = ButtonStyle.green
        
        if all_disabled:
            enabled = False
        else:
            enabled = True
        
        custom_id = str(index)
        
        button = Button(
            emoji = emoji,
            custom_id = custom_id,
            style = style,
            enabled = enabled,
        )
        
        row_buttons.append(button)
    
    return buttons


def click(array, custom_id, identifier):
    try:
        index = CUSTOM_ID_MAP[custom_id]
    except KeyError:
        return False
    
    element = array[index]
    if element == ARRAY_IDENTIFIER_EMPTY:
        array[index] = identifier
        return True
    
    return False

def get_game_state(array, identifier_p1):
    # Check same lines
    for index_1, index_2, index_3 in LINES:
        
        element = array[index_1]
        if element == ARRAY_IDENTIFIER_EMPTY:
            continue
        
        if element != array[index_2]:
            continue
        
        if element != array[index_3]:
            continue
        
        if element == identifier_p1:
            return GAME_STATE_P1_WIN
        else:
            return GAME_STATE_P2_WIN
    
    # Check 3/2 occupied places
    for element in array:
        if element == ARRAY_IDENTIFIER_EMPTY:
            return GAME_STATE_NONE
    
    return GAME_STATE_DRAW

LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)

def generate_crosses():
    edge_pairs = (
        (0, 8),
        (1, 7),
        (2, 6),
        (3, 5),
        (5, 3),
        (6, 2),
        (7, 1),
        (8, 0),
    )
    
    combinations = []
    for index_1, index_3 in edge_pairs:
        for index_2, index_4 in edge_pairs:
            if (index_1 == index_2) or (index_1 == index_4):
                continue
            
            combinations.append((index_1, index_2, index_3, index_4))
    
    return tuple(combinations)

CROSSES = generate_crosses()

Y_PATTERN = (
    (0, 8, (1, 2, 3, 5, 6, 7)),
    (2, 6, (0, 1, 3, 5, 7, 8)),
)

Y_PATTERN_CHOOSE_FROM = (1, 3, 5, 7)

MIDDLE = 4
CORNERS = (0, 2, 6, 8)
CORNERS_TO_EDGES = {
    0: (1, 3),
    2: (1, 5),
    6: (3, 7),
    8: (5, 7),
}

def click_p2(array, identifier_p1, identifier_p2):
    should_click_at = -1
    
    while True:
        # Check whether we or the enemy can do 3 next to each other
        # ? ? ?
        # ? ? ?
        # X X _
        
        for indexes in LINES:
            
            count_enemy = 0
            count_own = 0
            free_index = -1
            for index in indexes:
                element = array[index]
                if element == ARRAY_IDENTIFIER_EMPTY:
                    free_index = index
                    continue
                
                if element == identifier_p1:
                    count_enemy += 1
                    continue
                
                count_own += 1
                continue
            
            if free_index == -1:
                continue
            
            if count_own == 2:
                should_click_at = free_index
                break
            
            if count_enemy == 2:
                should_click_at = free_index
                continue
        
        if should_click_at != -1:
            break
        
        # Check whether it is the first move for us after the enemy's
        #
        # There are 3 cases.
        #
        # 1.:
        # If the enemy selected middle
        # _ _ _
        # _ O _
        # _ _ _
        #
        # We select a corner one.
        # X _ X
        # _ O _
        # X _ X
        #
        # 2.:
        # If the enemy selected a corner
        # O _ O
        # _ _ _
        # O _ O
        #
        # We select an adjacent edge to it
        # O X _
        # X _ _
        # _ _ _
        #
        # 3.:
        # If the enemy selected and edge.
        # _ O _
        # O _ O
        # _ O _
        #
        # We select the middle
        #
        # _ O _
        # O X O
        # _ O _
        
        count_enemy = 0
        count_own = 0
        enemy_index = -1
        
        for index in range(9):
            element = array[index]
            
            if element == ARRAY_IDENTIFIER_EMPTY:
                continue
            
            if element == identifier_p1:
                count_enemy += 1
                enemy_index = index
                continue
            
            count_own += 1
            continue
        
        if (count_enemy == 1) and (count_own == 0):
            if enemy_index == MIDDLE:
                should_click_at = choice(CORNERS)
                break
            
            try:
                edges = CORNERS_TO_EDGES[enemy_index]
            except KeyError:
                pass
            else:
                should_click_at = choice(edges)
                break
            
            should_click_at = MIDDLE
            break
        
        # Check whether the enemy or we are trying to setup a trap
        if array[4] == ARRAY_IDENTIFIER_EMPTY:
            # _ _ _
            # _ _ _
            # O X O
            #
            # If the middle is empty and the sides look like that, it is possible.
            #
            # _ ? _
            # ? O ?
            # O X O
            for index_1, index_2, index_empty_1, index_empty_2 in CROSSES:
                
                if array[index_empty_1] != ARRAY_IDENTIFIER_EMPTY:
                    continue
                
                if array[index_empty_2] != ARRAY_IDENTIFIER_EMPTY:
                    continue
                
                element = array[index_1]
                if element == ARRAY_IDENTIFIER_EMPTY:
                    continue
                
                if element != array[index_2]:
                    continue
                
                should_click_at = 4
                break
                
            if should_click_at != -1:
                break
            
            # _ _ O
            # _ X ?
            # O ? _
            #
            # Y pattern matching
            # O _ O
            # _ X ?
            # O ? _
            for index_1, index_2, empty_indexes in Y_PATTERN:
                element = array[index_1]
                if element == ARRAY_IDENTIFIER_EMPTY:
                    continue
                
                if element != array[index_2]:
                    continue
                
                for index in empty_indexes:
                    if array[index] != ARRAY_IDENTIFIER_EMPTY:
                        all_empty = False
                        break
                else:
                    all_empty = True
                
                if not all_empty:
                    break
                
                should_click_at = choice(Y_PATTERN_CHOOSE_FROM)
                break
            
            if should_click_at != -1:
                break
        
        free_indexes = []
        for index in range(len(array)):
            if array[index] == ARRAY_IDENTIFIER_EMPTY:
                free_indexes.append(index)
        
        should_click_at = choice(free_indexes)
        break
    
    array[should_click_at] = identifier_p2


@SLASH_CLIENT.interactions(is_global=True)
async def xox(client, event,
    mode : ([('single-player', 'sg'), ('multi-player', 'mp')], 'Game mode') = 'sg',
):
    """The X-O-X game with buttons."""
    if mode == 'sg':
        coroutine_function = xox_single_player
    else:
        coroutine_function = xox_multi_player
    
    await coroutine_function(client, event)


async def xox_single_player(client, event):
    array = [0 for _ in range(9)]
    
    if random() < 0.5:
        identifier_user = ARRAY_IDENTIFIER_P1
        identifier_ai = ARRAY_IDENTIFIER_P2
        emoji = EMOJI_P1
    else:
        identifier_user = ARRAY_IDENTIFIER_P2
        identifier_ai = ARRAY_IDENTIFIER_P1
        emoji = EMOJI_P2
    
    if random() < 0.5:
        click_p2(array, identifier_user, identifier_ai)
    
    title = f'It is your turn {event.user.full_name} | {emoji.as_emoji}'
    
    buttons = render_array(array, False)
    
    await client.interaction_response_message_create(event, title, components=buttons)
    
    component_interaction_event = None
    
    try:
        async for component_interaction_event in iter_component_interactions(event, timeout=300.0,
                check=partial_func(check_event_user, event.user)):
            
            if not click(array, component_interaction_event.interaction.custom_id, identifier_user):
                await client.interaction_component_acknowledge(component_interaction_event)
                continue
            
            game_state = get_game_state(array, identifier_user)
            if game_state == GAME_STATE_NONE:
                click_p2(array, identifier_user, identifier_ai)
                game_state = get_game_state(array, identifier_user)
                if game_state == GAME_STATE_NONE:
                    buttons = render_array(array, False)
                    await client.interaction_component_message_edit(component_interaction_event, components=buttons)
                    continue
            
            if game_state == GAME_STATE_DRAW:
                title = 'Draw'
            elif game_state == GAME_STATE_P1_WIN:
                title = 'You won'
            else:
                title = f'{client.full_name} won'
            
            buttons = render_array(array, True)
            await client.interaction_component_message_edit(component_interaction_event, title, components=buttons)
            break
    
    except TimeoutError:
        title = 'Timeout occurred.'
        buttons = render_array(array, True)
        
        if (component_interaction_event is not None):
            event = component_interaction_event
        
        await client.interaction_response_message_edit(event, title, components=buttons)


async def try_send_notification(client, event, message, user_1, user_2, timestamp, emoji):
    channel = await client.channel_private_create(user_1)
    
    embed = Embed(
        None,
        f'You are {emoji}\n\n**Good luck!**',
        color = 0x8000AB,
        timestamp = timestamp,
    ).add_author(
        user_2.avatar_url_as(size=64),
        f'{user_2.full_name} accepted your X-O-X challenge',
        url = message.url,
    )
    
    guild = event.guild
    if (guild is not None):
        source_channel = event.channel
        if source_channel is None:
            channel_name = '???'
        else:
            channel_name = source_channel.name
        
        embed.add_footer(
            f'{guild.name} • {channel_name}',
            guild.icon_url_as(size=64)
        )
    
    try:
        await client.message_create(
            channel,
            embed = embed,
            components = Button(
                label = 'Go to message',
                url = message.url,
            )
        )
    except ConnectionError:
        # No Internet
        return
    
    except DiscordException as err:
        if err.code != ERROR_CODES.cannot_message_user:
            raise


async def xox_multi_player(client, event):
    """The X-O-X game against someone."""
    user_1 = event.user
    timestamp = event.created_at
    
    embed = Embed(
        timestamp = timestamp,
    ).add_author(
        user_1.avatar_url_as(size=64),
        f'Challenge {user_1.full_name} in X-O-X!'
    ).add_footer(
        'This message times out after 300 seconds.',
    )
    
    await client.interaction_application_command_acknowledge(event)
    message = await client.interaction_followup_message_create(event, embed=embed, components=BUTTON_CHALLENGE_ENABLED)
    
    try:
        event = await wait_for_component_interaction(
            message,
            timeout = 300.0,
            check = partial_func(check_event_other_user, user_1),
        )
    except TimeoutError:
        
        embed = Embed(
            timestamp = timestamp,
        ).add_author(
            user_1.avatar_url_as(size=64),
            f'Challenge {user_1.full_name} X-O-X!'
        ).add_footer(
            'This message timed out.',
        )
        
        await client.interaction_response_message_edit(event, embed=embed, components=BUTTON_CHALLENGE_DISABLED)
        
        return
    
    # acknowledge it for the cases of timeout. If Discord or teh user lags, this might happen.
    user_2 = event.user
    
    array = [0 for _ in range(9)]
    
    if random() < 0.5:
        emoji_user_1 = EMOJI_P1
        emoji_user_2 = EMOJI_P2
    else:
        emoji_user_1 = EMOJI_P2
        emoji_user_2 = EMOJI_P1
    
    if random() < 0.5:
        user = user_1
        identifier = ARRAY_IDENTIFIER_P1
        emoji = emoji_user_1
    else:
        user = user_2
        identifier = ARRAY_IDENTIFIER_P2
        emoji = emoji_user_2
    
    Task(try_send_notification(client, event, message, user_1, user_2, timestamp, emoji_user_1), KOKORO)
    
    title = f'It is your turn {user.mention} | {emoji}'
    
    buttons = render_array(array, False)
    
    await client.interaction_component_message_edit(event, title, embed=None, components=buttons)
    
    while True:
        try:
            event = await wait_for_component_interaction(
                event,
                timeout = 300.0,
                check = partial_func(check_event_user, user),
            )
        except TimeoutError:
            title = 'Timeout occurred.'
            buttons = render_array(array, True)
            
            await client.interaction_response_message_edit(event, title, components=buttons)
            break
        
        if not click(array, event.interaction.custom_id, identifier):
            await client.interaction_component_acknowledge(event)
            continue
        
        game_state = get_game_state(array, ARRAY_IDENTIFIER_P1)
        if game_state == GAME_STATE_NONE:
            
            if identifier == ARRAY_IDENTIFIER_P1:
                user = user_2
                identifier = ARRAY_IDENTIFIER_P2
                emoji = emoji_user_2
            else:
                user = user_1
                identifier = ARRAY_IDENTIFIER_P1
                emoji = emoji_user_1
            
            title = f'It is your turn {user.mention} | {emoji.as_emoji}'
            
            buttons = render_array(array, False)
            await client.interaction_component_message_edit(event, title, components=buttons)
            continue
        
        if game_state == GAME_STATE_DRAW:
            title = 'Draw'
        elif game_state == GAME_STATE_P1_WIN:
            title = f'{user_1.full_name} won against {user_2.full_name}'
        else:
            title = f'{user_2.full_name} won against {user_1.full_name}'
        
        buttons = render_array(array, True)
        await client.interaction_component_message_edit(event, title, components=buttons)
        break
