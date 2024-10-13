import vampytest

from ....plugins.image_handling_core import ImageDetailStatic, ImageHandlerStatic
from ....plugins.touhou_core import KAENBYOU_RIN, KOMEIJI_KOISHI, KOMEIJI_SATORI
from ....plugins.user_settings import PREFERRED_IMAGE_SOURCE_TOUHOU

from ..building import _build_asset_information_for

def test__build_asset_information_for():
    """
    Tests whether ``_build_asset_information_for`` works as intended.
    """

    image_detail_0 = ImageDetailStatic(
        'https://orindance.party/koishi_satori_kiss_0000.png',
    ).with_action(
        'kiss', KOMEIJI_KOISHI, KOMEIJI_SATORI,
    )
    
    image_detail_1 = ImageDetailStatic(
        'https://orindance.party/koishi_satori_kiss_0001.png'
    ).with_action(
        'kiss', KOMEIJI_SATORI, KOMEIJI_KOISHI,
    )
    
    image_detail_2 = ImageDetailStatic(
        'https://orindance.party/koishi_orin_satori_kiss_0000.png'
    ).with_actions(
        ('kiss', KOMEIJI_KOISHI, KOMEIJI_SATORI),
        ('kiss', KAENBYOU_RIN, KOMEIJI_SATORI),
    )
    
    image_handler = ImageHandlerStatic(
        PREFERRED_IMAGE_SOURCE_TOUHOU,
    ).with_images(
        [
            image_detail_0,
            image_detail_1,
            image_detail_2,
        ],
    )
    
    output = _build_asset_information_for(image_handler)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        (
            '### Asset Information\n'
            '\n'
            'Some creators may be unknown. If you know them please create a PR with it.\n'
            '\n'
            '---\n'
            '\n'
            '### koishi_satori_kiss_0000\n'
            '\n'
            '- Creator: *unknown*\n'
            '- Editor: *none*\n'
            '- Characters: **Komeiji Koishi**, **Komeiji Satori**\n'
            '- Source: **Touhou**\n'
            '\n'
            '---\n'
            '\n'
            '### koishi_satori_kiss_0001\n'
            '\n'
            '- Creator: *unknown*\n'
            '- Editor: *none*\n'
            '- Characters: **Komeiji Koishi**, **Komeiji Satori**\n'
            '- Source: **Touhou**\n'
            '\n'
            '---\n'
            '\n'
            '### koishi_orin_satori_kiss_0000\n'
            '\n'
            '- Creator: *unknown*\n'
            '- Editor: *none*\n'
            '- Characters: **Kaenbyou Rin**, **Komeiji Koishi**, **Komeiji Satori**\n'
            '- Source: **Touhou**\n'
            '\n'
            '---\n'
            '\n'
            'I don\'t own the image files. The credits goes their respective owners.\n'
            'This feature is purely fan-made, and will not be used for profit or illegal sharing!\n'
            'Please contact me if you\'re the owner of an image and want to remove it from this repository!\n'
            'Contact me via opening a new issue.\n'
            '\n'
            'Thank you!\n'
        ),
    )
