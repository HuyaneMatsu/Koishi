import vampytest
from hata import (
    ButtonStyle, Component, InteractionEvent, Guild, Message, User, create_button, create_row, create_separator,
    create_text_display
)
from ...game_21 import Game21Session

from ..component_building_game_21 import build_game_21_detailed_components


def _iter_options():
    user_id_0 = 202511230004
    user_id_1 = 202511230009
    page_index = 1
    session_id = 5666
    amount = 200
    guild_id = 202511230005
    message_id = 202511230006
    interaction_event_id = 202511230007
    channel_id = 202511230008
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    latest_interaction_event = InteractionEvent.precreate(
        interaction_event_id,
    )
    
    guild = Guild.precreate(
        guild_id,
    )
    
    user_0 = User.precreate(
        user_id_0,
        name = 'Momiji',
    )
    
    user_1 = User.precreate(
        user_id_1,
        name = 'Aya',
    )
    
    session = Game21Session(session_id, guild, amount, latest_interaction_event)
    session.user_ids = (user_id_0, user_id_1)
    session.message = message
    
    yield (
        user_id_0,
        page_index,
        session_id,
        amount,
        session,
        guild_id,
        [
            user_0,
            user_1,
        ],
        [
            create_text_display(
                '# `/21` allocating 200'
            ),
            create_text_display(
                '**Participants:**\n'
                '- Momiji\n'
                '- Aya'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Back to allocations',
                    custom_id = f'allocations.view.{user_id_0:x}.{page_index:x}'
                ),
                create_button(
                    'Get me there',
                    url = message.url,
                ),
            ),
        ],
    )
    
    user_id_0 = 202511230010
    page_index = 1
    session_id = 5666
    amount = 200
    guild_id = 202511230012
    interaction_event_id = 202511230014
    
    latest_interaction_event = InteractionEvent.precreate(
        interaction_event_id,
    )
    
    guild = Guild.precreate(
        guild_id,
    )
    
    session = Game21Session(session_id, guild, amount, latest_interaction_event)
    
    yield (
        user_id_0,
        page_index,
        session_id,
        amount,
        session,
        guild_id,
        [],
        [
            create_text_display(
                '# `/21` allocating 200'
            ),
            create_text_display(
                '**Participants:** *none*'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Back to allocations',
                    custom_id = f'allocations.view.{user_id_0:x}.{page_index:x}'
                ),
                create_button(
                    'Get me there',
                    custom_id =  'allocations.link.disabled',
                    enabled = False,
                    style = ButtonStyle.gray,
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_game_21_detailed_components(user_id, page_index, session_id, amount, session, guild_id, entity_cache):
    """
    Tests whether ``build_game_21_detailed_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        Page index to redirect to.
    
    session_id : `int`
        The session's identifier.
    
    amount : `int`
        The allocated amount.
    
    session : ``NoneType | Game21Session``
        The session.
    
    guild_id : `int`
        The local guild's identifier.
    
    entity_cache : `int`
        Additional entities to keep cached.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_game_21_detailed_components(user_id, page_index, session_id, amount, session, guild_id)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
