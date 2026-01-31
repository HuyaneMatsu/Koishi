import vampytest
from hata import ButtonStyle, User, Component, create_button, create_row, create_separator, create_text_display

from ...relationships_core import RELATIONSHIP_TYPE_MAMA, RelationshipRequest

from ..component_building_relationship_request import build_relationship_request_detailed_components


def _iter_options():
    user_id_0 = 202601200000
    user_id_1 = 202601200001
    
    page_index = 1
    
    session_id = 123
    amount = 1000
    session = RelationshipRequest(
        user_id_0,
        user_id_1,
        RELATIONSHIP_TYPE_MAMA,
        1000,
    )
    session.entry_id = session_id
    
    user_1 = User.precreate(
        user_id_0,
        name = 'Satori',
    )
    
    yield (
        user_id_0,
        page_index,
        session_id,
        amount,
        session,
        (user_1, ),
        0,
        [
            create_text_display(
                '# `/relationships propose` allocating 1000'
            ),
            create_text_display(
                f'Adoption agreement towards Satori.'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Back to allocations',
                    custom_id = f'allocations.view.{user_id_0:x}.{page_index:x}'
                ),
                create_button(
                    'Get me there',
                    custom_id = f'relationships_request.details.{user_id_0:x}.{True:x}.{0:x}.{session_id:x}',
                ),
            ),
        ],
    )
    
    yield (
        user_id_0,
        page_index,
        session_id,
        amount,
        None,
        None,
        0,
        [
            create_text_display(
                '# `/relationships propose` allocating 1000'
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
def test__build_relationship_request_detailed_components(
    user_id, page_index, session_id, amount, session, extra, guild_id
):
    """
    Tests whether ``build_relationship_request_detailed_components`` works as intended.
    
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
    
    session : ``NoneType | RelationshipRequest``
        The session.
    
    extra : ``None | (ClientUserBase, )``
        Additionally requested fields.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_relationship_request_detailed_components(user_id, page_index, session_id, amount, session, extra, guild_id)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
