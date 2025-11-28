import vampytest
from hata import Component, create_button, create_row, create_separator, create_text_display

from ...user_balance import ALLOCATION_FEATURE_ID_NONE

from ..component_building import build_details_components


def _iter_options():
    user_id = 202511230040
    page_index = 1
    session_id = 5666
    amount = 200
    guild_id = 202511230041
    
    session = None
    
    yield (
        user_id,
        page_index,
        ALLOCATION_FEATURE_ID_NONE,
        session_id,
        amount,
        session,
        guild_id,
        [
            create_text_display(
                '# `unknown` allocating 200'
            ),
            create_separator(),
            create_row(
                create_button(
                    'Back to allocations',
                    custom_id = f'allocations.view.{user_id:x}.{page_index:x}'
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_details_components(user_id, page_index, allocation_feature_id, session_id, amount, session, guild_id):
    """
    Tests whether ``build_details_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        Page index to redirect to.
    
    allocation_feature_id : `int`
        The allocation feature's identifier.
    
    session_id : `int`
        The session's identifier.
    
    amount : `int`
        The allocated amount.
    
    session : `None | object`
        The game's session.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_details_components(user_id, page_index, allocation_feature_id, session_id, amount, session, guild_id)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
