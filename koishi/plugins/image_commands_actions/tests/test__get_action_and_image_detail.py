import vampytest

from ...touhou_core import KAENBYOU_RIN, REIUJI_UTSUHO

from ..action_filtering import get_action_and_image_detail
from ..actions import ACTIONS
from ..asset_listings import TOUHOU_ACTION_ALL


def _iter_options():
    yield (
        None,
        None,
        None,
        None,
        (
            next((action for action in ACTIONS if action.name == 'pocky-kiss'), None),
            next(
                (
                    image_detail for image_detail in TOUHOU_ACTION_ALL.iter_character_filterable()
                    if image_detail.url.endswith('akyuu-kosuzu-pocky-0000.png')
                ),
                None,
            ),
        ),
    )
    
    yield (
        None,
        KAENBYOU_RIN.name,
        REIUJI_UTSUHO.name,
        None,
        (
            next((action for action in ACTIONS if action.name == 'hug'), None),
            next(
                (
                    image_detail for image_detail in TOUHOU_ACTION_ALL.iter_character_filterable()
                    if image_detail.url.endswith('okuu-orin-hug-0002.png')
                ),
                None,
            ),
        ),
    )
    
    yield (
        'kiss',
        KAENBYOU_RIN.name,
        REIUJI_UTSUHO.name,
        None,
        (
            next((action for action in ACTIONS if action.name == 'kiss'), None),
            None,
        ),
    )
    
    yield (
        'umuscope',
        KAENBYOU_RIN.name,
        REIUJI_UTSUHO.name,
        'miau',
        (
            None,
            None,
        ),
    )
    
    yield (
        'hug',
        KAENBYOU_RIN.name,
        REIUJI_UTSUHO.name,
        'okuu-orin-hug-0002',
        (
            next((action for action in ACTIONS if action.name == 'hug'), None),
            next(
                (
                    image_detail for image_detail in TOUHOU_ACTION_ALL.iter_character_filterable()
                    if image_detail.url.endswith('okuu-orin-hug-0002.png')
                ),
                None,
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_action_and_image_detail(action_tag_name, source_character_name, target_character_name, image_name):
    """
    Tests whether ``get_action_and_image_detail`` works as intended.
    
    Parameters
    ----------
    action_tag_name : `None | str`
        Selected action tag name.
    source_character_name : `None | str`
        Name of the source character.
    target_character_name : `None | str`
        Name of the target character.
    image_name : `None | str`
        The name of the image.
    
    Returns
    -------
    output : `(None | Action, None | ImageDetailBase)`
    """
    output = get_action_and_image_detail(action_tag_name, source_character_name, target_character_name, image_name)
    vampytest.assert_instance(output, tuple)
    return output
    if output == TOUHOU_ACTION_ALL._images:
        output = None
    
    return output
