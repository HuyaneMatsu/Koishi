import vampytest

from ...image_handling_core import ImageDetailAction
from ...touhou_core import KAENBYOU_RIN, REIUJI_UTSUHO, TouhouCharacter

from ..action_filtering import (
    PARAMETER_NAME_ACTION_TAG, PARAMETER_NAME_NAME, PARAMETER_NAME_SOURCE, PARAMETER_NAME_TARGET, PARAMETER_WILD_CARD,
    get_image_details_from_parameters
)
from ..asset_listings import TOUHOU_ACTION_ALL
from ..asset_listings.constants import ACTION_TAG_HUG


def _iter_options():
    yield (
        {},
        (
            None,
            None,
            None,
        ),
    )
    yield (
        {
            PARAMETER_NAME_ACTION_TAG: PARAMETER_WILD_CARD,
            PARAMETER_NAME_SOURCE: PARAMETER_WILD_CARD,
            PARAMETER_NAME_TARGET: PARAMETER_WILD_CARD,
            PARAMETER_NAME_NAME: PARAMETER_WILD_CARD,
        },
        (
            None,
            None,
            None,
        ),
    )
    
    action = ImageDetailAction(ACTION_TAG_HUG, KAENBYOU_RIN, REIUJI_UTSUHO)
    
    yield (
        {
            PARAMETER_NAME_ACTION_TAG: 'hug',
            PARAMETER_NAME_SOURCE: KAENBYOU_RIN.name,
            PARAMETER_NAME_TARGET: REIUJI_UTSUHO.name,
            PARAMETER_NAME_NAME: 'ok',
        },
        (
            KAENBYOU_RIN,
            REIUJI_UTSUHO,
            [
                image_detail for image_detail in TOUHOU_ACTION_ALL.iter_character_filterable()
                if image_detail.name.startswith('okuu-orin-hug-') and (action in image_detail.iter_actions())
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_image_details_from_parameters(parameters):
    """
    Tests whether ``get_image_details_from_parameters`` works as intended.
    
    Parameters
    ----------
    parameters : `dict<str, object>`
        Parameters to filter for.
    
    Returns
    -------
    output : `(None | TouhouCharacter, None | TouhouCharacter, None | list<ImageDetailBase>)`
    """
    output = get_image_details_from_parameters(parameters)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 3)
    
    source, target, image_details = output
    vampytest.assert_instance(source, TouhouCharacter, nullable = True)
    vampytest.assert_instance(target, TouhouCharacter, nullable = True)
    vampytest.assert_instance(image_details, list)
    
    if image_details == TOUHOU_ACTION_ALL._images:
        image_details = None
    
    return source, target, image_details
