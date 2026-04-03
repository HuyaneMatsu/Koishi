import vampytest

from ..automation_reaction_role_item import AutomationReactionRoleItem
from ..items import pack_items


def _iter_options():
    emoji_id_0 = 202509270010
    emoji_id_1 = 202509270011
    emoji_id_2 = 202509270012
    emoji_id_3 = 202509270013
    
    role_id_0 = 202509270014
    role_id_1 = 202509270015
    role_id_2 = 202509270016
    role_id_3 = 202509270017
    role_id_4 = 202509270018
    role_id_5 = 202509270019
    
    
    yield (
        None,
        1,
        None,
    )
    
    yield (
        [
            AutomationReactionRoleItem(
                emoji_id_0,
                (role_id_0, role_id_1),
                (role_id_2, role_id_3),
            ),
        ],
        1,
        b''.join([
            emoji_id_0.to_bytes(8, 'little'),
            (2).to_bytes(1, 'little'),
            (2).to_bytes(1, 'little'),
            role_id_0.to_bytes(8, 'little'),
            role_id_1.to_bytes(8, 'little'),
            role_id_2.to_bytes(8, 'little'),
            role_id_3.to_bytes(8, 'little'),
        ]),
    )
    
    yield (
        [
            AutomationReactionRoleItem(
                emoji_id_0,
                (role_id_0,),
                None,
            ),
            AutomationReactionRoleItem(
                emoji_id_1,
                (role_id_1,),
                None,
            ),
            AutomationReactionRoleItem(
                emoji_id_2,
                (role_id_2,),
                None,
            ),
            AutomationReactionRoleItem(
                emoji_id_3,
                (role_id_3,),
                None,
            ),
        ],
        1,
        b''.join([
            emoji_id_0.to_bytes(8, 'little'),
            (1).to_bytes(1, 'little'),
            (0).to_bytes(1, 'little'),
            role_id_0.to_bytes(8, 'little'),
            emoji_id_1.to_bytes(8, 'little'),
            (1).to_bytes(1, 'little'),
            (0).to_bytes(1, 'little'),
            role_id_1.to_bytes(8, 'little'),
            emoji_id_2.to_bytes(8, 'little'),
            (1).to_bytes(1, 'little'),
            (0).to_bytes(1, 'little'),
            role_id_2.to_bytes(8, 'little'),
            emoji_id_3.to_bytes(8, 'little'),
            (1).to_bytes(1, 'little'),
            (0).to_bytes(1, 'little'),
            role_id_3.to_bytes(8, 'little'),
        ]),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__pack_items(items, data_version):
    """
    Tests whether ``pack_items`` works as intended.
    
    Parameters
    ----------
    items : ``None | list<AutomationReactionRoleItem>``
        Items to pack.
    
    data_version : `int`
        Serialization version.
    
    Returns
    -------
    output : `None | bytes`
    """
    output = pack_items(items, data_version)
    vampytest.assert_instance(output, bytes, nullable = True)
    return output
