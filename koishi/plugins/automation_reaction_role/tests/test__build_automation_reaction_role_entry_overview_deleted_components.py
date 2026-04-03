import vampytest
from hata import Component, create_button, create_row, create_separator, create_text_display

from ..component_builders import build_automation_reaction_role_entry_overview_deleted_components


def _iter_options():
    yield (
        1,
        [
            create_text_display('### Auto react role not found'),
            create_separator(),
            create_row(
                create_button(
                    'Back to listing',
                    custom_id =  f'automation_reaction_role.listing.{1:x}'
                ),
            )
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_automation_reaction_role_entry_overview_deleted_components(listing_page_index):
    """
    Tests whether ``build_automation_reaction_role_entry_overview_deleted_components`` works as intended.
    
    Parameters
    ----------
    listing_page_index : `int`
        The current listing page index.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_automation_reaction_role_entry_overview_deleted_components(listing_page_index)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
