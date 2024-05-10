import vampytest

from ...image_handling_core import (
    WEIGHT_DIRECT_MATCH, ImageDetailMatcherContextSensitive, ImageDetailStatic, ImageHandlerStatic
)
from ...touhou_core import IZAYOI_SAKUYA, KAENBYOU_RIN, KOMEIJI_KOISHI, KOMEIJI_SATORI
from ...user_settings import PREFERRED_IMAGE_SOURCE_TOUHOU

from ..character_preference import get_match_groups


def _iter_options():
    
    
    image_detail_0 = ImageDetailStatic(
        'https://orindance.party/',
    ).with_action(
        'kiss', KOMEIJI_KOISHI, KOMEIJI_SATORI,
    )
    
    image_detail_1 = ImageDetailStatic(
        'https://orindance.party/'
    ).with_action(
        'kiss', KOMEIJI_SATORI, KOMEIJI_KOISHI,
    )
    
    image_detail_2 = ImageDetailStatic(
        'https://orindance.party/'
    ).with_actions(
        ('kiss', KOMEIJI_KOISHI, KOMEIJI_SATORI),
        ('kiss', KOMEIJI_SATORI, KOMEIJI_KOISHI),
    )
    
    image_detail_3 = ImageDetailStatic(
        'https://orindance.party/'
    ).with_action(
        'kiss', KOMEIJI_KOISHI, KAENBYOU_RIN
    )
    
    image_detail_4 = ImageDetailStatic(
        'https://orindance.party/'
    ).with_action(
        'kiss', KOMEIJI_SATORI, KAENBYOU_RIN
    )
    
    image_detail_5 = ImageDetailStatic(
        'https://orindance.party/'
    ).with_action(
        'kiss', KAENBYOU_RIN, KOMEIJI_SATORI,
    )
    
    image_detail_6 = ImageDetailStatic(
        'https://orindance.party/'
    ).with_action(
        'kiss', KAENBYOU_RIN, KOMEIJI_KOISHI,
    )
    
    image_handler = ImageHandlerStatic(
        PREFERRED_IMAGE_SOURCE_TOUHOU,
    ).with_images(
        [
            image_detail_0,
            image_detail_1,
            image_detail_2,
            image_detail_3,
            image_detail_4,
            image_detail_5,
            image_detail_6,
        ],
    )
    
    yield (
        image_handler,
        {KOMEIJI_KOISHI.system_name},
        None,
        {
            WEIGHT_DIRECT_MATCH + 0: [image_detail_0, image_detail_2, image_detail_3],
        },
    )

    yield (
        image_handler,
        {KOMEIJI_KOISHI.system_name},
        {KOMEIJI_SATORI.system_name},
        {
            WEIGHT_DIRECT_MATCH + WEIGHT_DIRECT_MATCH : [image_detail_3, image_detail_5],
            WEIGHT_DIRECT_MATCH + 0 : [image_detail_0, image_detail_2],
        },
    )
    
    yield (
        image_handler,
        {IZAYOI_SAKUYA.system_name},
        None,
        {},
    )
    
    # Not optimal
    yield (
        image_handler,
        {KOMEIJI_KOISHI.system_name},
        {KOMEIJI_KOISHI.system_name},
        {
            WEIGHT_DIRECT_MATCH + 0: [image_detail_0, image_detail_1, image_detail_2, image_detail_3, image_detail_6],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_match_groups(image_handler, source_character_system_names, target_character_system_names):
    """
    Tests whether ``get_match_groups`` works as intended.
    
    Parameters
    ----------
    image_handler : `ImageHandlerBase`
        Image handler.
    source_character_system_names : `None | set<str>`
        Character system names to match the source user.
    target_character_system_names : `None | set<str>`
        Character system names to match the target user.
    
    Returns
    -------
    match_groups_by_weight : `dict<int, list<ImageDetailBase>>`
    """
    matcher = ImageDetailMatcherContextSensitive(source_character_system_names, target_character_system_names)
    return get_match_groups(image_handler, matcher)
