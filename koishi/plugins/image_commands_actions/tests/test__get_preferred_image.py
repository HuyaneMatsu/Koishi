import vampytest
from hata import User

from ...image_handling_core import ImageDetail, ImageHandlerStatic
from ...touhou_character_preference import CharacterPreference
from ...touhou_core import KAENBYOU_RIN, KOMEIJI_KOISHI, KOMEIJI_SATORI
from ...user_settings import PREFERRED_IMAGE_SOURCE_TOUHOU

from ..character_preference import get_preferred_image


def _iter_options():
    user_id_0 = 202309170073
    user_id_1 = 202309170074
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)

    image_detail_0 = ImageDetail('https://orindance.party/').with_source(KOMEIJI_KOISHI).with_target(KOMEIJI_SATORI)
    image_detail_1 = ImageDetail('https://orindance.party/').with_any(KOMEIJI_SATORI).with_any(KAENBYOU_RIN)
    image_detail_2 = ImageDetail('https://orindance.party/').with_source(KOMEIJI_KOISHI).with_target(KAENBYOU_RIN)
    image_detail_3 = ImageDetail('https://orindance.party/').with_source(KAENBYOU_RIN).with_target(KOMEIJI_KOISHI)
    
    image_handler = ImageHandlerStatic(
        [
            image_detail_0,
            image_detail_1,
            image_detail_2,
            image_detail_3,
        ],
        PREFERRED_IMAGE_SOURCE_TOUHOU,
    )
    
    yield (
        image_handler,
        user_0,
        [user_1],
        None,
        None,
    )

    yield (
        image_handler,
        user_0,
        [],
        [
            CharacterPreference(user_id_0, KOMEIJI_SATORI.system_name),
        ],
        image_detail_1,
    )

    yield (
        image_handler,
        user_0,
        [user_1],
        [
            CharacterPreference(user_id_0, KOMEIJI_SATORI.system_name),
        ],
        image_detail_1,
    )

    yield (
        image_handler,
        user_0,
        [user_1],
        [
            CharacterPreference(user_id_0, KOMEIJI_KOISHI.system_name),
            CharacterPreference(user_id_1, KAENBYOU_RIN.system_name),
        ],
        image_detail_2,
    )

    yield (
        image_handler,
        user_0,
        [user_1],
        [
            CharacterPreference(user_id_0, KAENBYOU_RIN.system_name),
            CharacterPreference(user_id_1, KOMEIJI_SATORI.system_name),
        ],
        image_detail_1,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_preferred_image(image_handler, source_user, target_users, character_preferences):
    """
    Tests whether ``get_preferred_image`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    image_handler : `ImageHandlerBase`
        Image handler.
    source_user : ``ClientUserBase``
        Source user.
    target_users : `set<ClientUserBase>`
        Target users(s).
    character_preferences : `None | list<CharacterPreference>`
        Character preferences to return by the query.
    
    Returns
    -------
    selected : `None | ImageDetail`
        The selected image detail.
    """
    query_called = False
    called_with_user_ids = False
    
    async def query(user_ids):
        nonlocal query_called
        nonlocal called_with_user_ids
        nonlocal character_preferences
        
        query_called = True
        called_with_user_ids = user_ids
        return character_preferences
    
    
    mocked = vampytest.mock_globals(
        get_preferred_image,
        2,
        OPTIMAL_GROUP_LENGTH = 1,
        get_more_touhou_character_preference = query,
    )
    
    output = await mocked(image_handler, source_user, target_users)
    
    vampytest.assert_true(query_called)
    vampytest.assert_instance(called_with_user_ids, list)
    vampytest.assert_eq({*called_with_user_ids}, {source_user.id, *(user.id for user in target_users)})
    
    return output
