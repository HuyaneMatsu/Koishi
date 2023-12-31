import vampytest

from ...image_handling_core import ImageDetail, ImageHandlerStatic
from ...touhou_core.characters import IZAYOI_SAKUYA, KAENBYOU_RIN, KOMEIJI_KOISHI, KOMEIJI_SATORI

from ..character_preference import get_match_groups


def _iter_options():
    image_detail_0 = ImageDetail('https://orindance.party/').with_source(KOMEIJI_KOISHI).with_target(KOMEIJI_SATORI)
    image_detail_1 = ImageDetail('https://orindance.party/').with_source(KOMEIJI_SATORI).with_target(KOMEIJI_KOISHI)
    image_detail_2 = ImageDetail('https://orindance.party/').with_any(KOMEIJI_SATORI).with_any(KOMEIJI_KOISHI)
    image_detail_3 = ImageDetail('https://orindance.party/').with_source(KOMEIJI_KOISHI).with_target(KAENBYOU_RIN)
    image_detail_4 = ImageDetail('https://orindance.party/').with_source(KOMEIJI_SATORI).with_target(KAENBYOU_RIN)
    image_detail_5 = ImageDetail('https://orindance.party/').with_source(KAENBYOU_RIN).with_target(KOMEIJI_SATORI)
    image_detail_6 = ImageDetail('https://orindance.party/').with_source(KAENBYOU_RIN).with_target(KOMEIJI_KOISHI)
    
    image_handler = ImageHandlerStatic([
        image_detail_0,
        image_detail_1,
        image_detail_2,
        image_detail_3,
        image_detail_4,
        image_detail_5,
        image_detail_6,
    ])
    
    yield (
        image_handler,
        {KOMEIJI_KOISHI.system_name},
        None,
        (
            [image_detail_0, image_detail_2, image_detail_3],
            [],
        ),
    )

    yield (
        image_handler,
        {KOMEIJI_KOISHI.system_name},
        {KOMEIJI_SATORI.system_name},
        (
            [image_detail_3, image_detail_5],
            [image_detail_0, image_detail_2],
        ),
    )
    
    yield (
        image_handler,
        {IZAYOI_SAKUYA.system_name},
        None,
        (
            [],
            [],
        ),
    )
    
    # Not optimal
    yield (
        image_handler,
        {KOMEIJI_KOISHI.system_name},
        {KOMEIJI_KOISHI.system_name},
        (
            [image_detail_0, image_detail_1, image_detail_3, image_detail_6],
            [image_detail_2],
        ),
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
    match_groups : `tuple<list<ImageDetail>>`
    """
    return get_match_groups(image_handler, source_character_system_names, target_character_system_names)
