import vampytest

from hata import InteractionForm, create_text_display

from ...adventure_core import (
    Adventure, LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATIONS,
    TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, TARGETS
)

from ..component_builders import build_adventure_cancellation_confirmation_form


def _iter_options():
    user_id = 202510250000
    entry_id = 56
    
    adventure = Adventure(
        user_id,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.entry_id = entry_id
    
    yield (
        adventure,
        InteractionForm(
            'Confirm adventure cancellation',
            [
                create_text_display(
                    f'Are you sure to cancel your adventure towards {LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name} for '
                    f'{TARGETS[TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION].name}?'
                ),
            ],
            f'adventure.cancel.{user_id:x}.{entry_id:x}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_adventure_cancellation_confirmation_form(adventure):
    """
    Tests whether ``build_adventure_cancellation_confirmation_form`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to build for.
    
    Returns
    -------
    output : ``InteractionForm``
    """
    output = build_adventure_cancellation_confirmation_form(adventure)
    
    vampytest.assert_instance(output, InteractionForm)
    
    return output
