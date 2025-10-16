import vampytest
from hata import InteractionForm, Message, create_text_display

from ..automation_reaction_role_entry import AutomationReactionRoleEntry
from ..component_builders import build_automation_reaction_role_entry_delete_form


def _iter_options():
    guild_id = 202510040050
    channel_id = 202510040051
    message_id = 202510040052
    entry_id = 6
    
    message = Message.precreate(
        message_id,
        channel_id = channel_id,
        guild_id = guild_id,
    )
    
    automation_reaction_role_entry = AutomationReactionRoleEntry(
        message,
    )
    automation_reaction_role_entry.entry_id = entry_id
    
    yield (
        1,
        automation_reaction_role_entry,
        InteractionForm(
            'Please confirm your deletion',
            [
                create_text_display('-# _ _')
            ],
            custom_id = f'automation_reaction_role.delete.{1:x}.{message_id:x}',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_automation_reaction_role_entry_delete_form(listing_page_index, automation_reaction_role_entry):
    """
    Tests whether ``build_automation_reaction_role_entry_delete_form`` works as intended.
    
    Parameters
    ----------
    listing_page_index : `int`
        The current listing page index.
    
    overview_page_index : `int`
        The overview's page index to redirect back to.
    
    Returns
    -------
    output : ``InteractionForm``
    """
    output = build_automation_reaction_role_entry_delete_form(listing_page_index, automation_reaction_role_entry)
    vampytest.assert_instance(output, InteractionForm)
    return output
