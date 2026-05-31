import vampytest

from hata import Client, Component, Guild, create_button, create_row, create_separator, create_text_display

from ..component_building import build_linked_quest_abandon_success_components


def _iter_options():
    user_id = 202509190000
    
    yield (
        user_id,
        1,
        202605300000,
        0,
        202605300001,
        [
            create_text_display('You successfully abandoned the quest.'),
            create_separator(),
            create_row(
                create_button(
                    'View quest board',
                    custom_id = f'quest_board.page.{user_id:x}.{0:x}',
                    enabled = True,
                ),
                create_button(
                    'View my quests',
                    custom_id = f'linked_quest.page.{user_id:x}.{1:x}',
                ),
            ),
        ],
    )
    
    yield (
        user_id,
        1,
        0,
        20,
        0,
        [
            create_text_display('You successfully abandoned the quest, losing 20 credibility.'),
            create_separator(),
            create_row(
                create_button(
                    'View quest board',
                    custom_id = f'quest_board.page.{user_id:x}.{0:x}',
                    enabled = False,
                ),
                create_button(
                    'View my quests',
                    custom_id = f'linked_quest.page.{user_id:x}.{1:x}',
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_linked_quest_abandon_success_components(user_id, page_index, guild_id, credibility_penalty, client_id):
    """
    Tests whether ``build_linked_quest_abandon_success_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        The linked quests' current page's index.
    
    guild_id : `int`
        The local guild's identifier.
    
    credibility_penalty : `int`
        Abandon credibility penalty.
    
    client_id : `int`
        Client to insert into the guild.
    
    Returns
    -------
    output : ``list<Component>``
    """
    client = None
    guild = None
    
    try:
        if guild_id:
            guild = Guild.precreate(guild_id)
            if client_id:
                client = Client(
                    client_id = client_id,
                    token = 'token_' + str(client_id),
                )
                guild.clients.append(client)
        
        output = build_linked_quest_abandon_success_components(user_id, page_index, guild, credibility_penalty)
        
        vampytest.assert_instance(output, list)
        for element in output:
            vampytest.assert_instance(element, Component)
        
        return output
    
    finally:
        if (client is not None):
            client._delete()
            client = None
