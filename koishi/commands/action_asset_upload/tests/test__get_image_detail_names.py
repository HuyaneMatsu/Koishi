import vampytest

from ....plugins.image_commands_actions.asset_listings.constants import ACTION_TAG_FEED, ACTION_TAG_KISS
from ....plugins.image_handling_core import ImageHandlerStatic
from ....plugins.touhou_core import CHIRUNO, SCARLET_FLANDRE, SCARLET_REMILIA
from ....plugins.user_settings import PREFERRED_IMAGE_SOURCE_TOUHOU

from ..filtering import get_image_detail_names


def test__get_image_detail_names():
    """
    Tests whether ``get_image_detail_names`` works as intended.
    """
    ACTIONS = ImageHandlerStatic(PREFERRED_IMAGE_SOURCE_TOUHOU)
    
    ACTIONS.add(
        'https://orindance.party/miaus/chiruno-feed-0000.png',
    ).with_action(
        ACTION_TAG_FEED, CHIRUNO, CHIRUNO,
    )
    
    ACTIONS.add(
        'https://orindance.party/miaus/flandre-remilia-kiss-0000.png',
    ).with_action(
        ACTION_TAG_KISS, SCARLET_FLANDRE, SCARLET_REMILIA,
    )
    
    output = get_image_detail_names(ACTIONS)
    vampytest.assert_instance(output, set)
    vampytest.assert_eq(output, {'chiruno-feed-0000', 'flandre-remilia-kiss-0000'})
