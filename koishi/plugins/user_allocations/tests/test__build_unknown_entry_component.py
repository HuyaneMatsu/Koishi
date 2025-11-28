import vampytest
from hata import Component, create_button, create_section, create_text_display

from ...user_balance import ALLOCATION_FEATURE_ID_NONE

from ..component_building_unknown import build_unknown_entry_component


def _iter_options():
    user_id = 202511230000
    page_index = 1
    session_id = 5666
    amount = 200
    
    yield (
        user_id,
        page_index,
        session_id,
        amount,
        create_section(
            create_text_display(
                '`unknown` allocating 200'
            ),
            thumbnail = create_button(
                'Details',
                custom_id = (
                    f'allocations.details.{user_id:x}.{page_index:x}.{ALLOCATION_FEATURE_ID_NONE:x}.{session_id:x}'
                ),
                enabled = False,
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_unknown_entry_component(user_id, page_index, session_id, amount):
    """
    Tests whether ``build_unknown_entry_component`` works as intended.
    
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
    
    Returns
    -------
    output : ``Component``
    """
    output = build_unknown_entry_component(user_id, page_index, session_id, amount)
    vampytest.assert_instance(output, Component)
    return output
