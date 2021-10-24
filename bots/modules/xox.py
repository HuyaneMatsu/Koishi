from functools import partial as partial_func
from random import random, choice

from hata import Emoji, BUILTIN_EMOJIS, Client

from hata.ext.slash import iter_component_interactions, Button, ButtonStyle
from bot_utils.constants import GUILD__NEKO_DUNGEON

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

SLASH_CLIENT: Client

def check_event_user(user, event):
    return event.user is user

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

def click_p2(array, identifier_p1, identifier_p2):
    should_click_at = -1
    
    while True:
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
        
        # Check whether the enemy or we are trying to setup a trap
        # _ _ _
        # _ _ _
        # O X O
        # If the middle is empty and the sides look like that, it is possible.
        if array[4] == ARRAY_IDENTIFIER_EMPTY:
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
async def xox(client, event):
    """The X-O-X game with buttons."""
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
    
    title = f'It is your turn {event.user.full_name}\nYou are {emoji.as_emoji}'
    
    buttons = render_array(array, False)
    
    await client.interaction_response_message_create(event, title, components=buttons)
    
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
        message = event.message
        if (message is not None) and event.channel.cached_permissions_for(client).can_view_channel:
            title = 'Timeout occurred.'
            buttons = render_array(array, True)
            
            await client.message_edit(message, title, components=buttons)
