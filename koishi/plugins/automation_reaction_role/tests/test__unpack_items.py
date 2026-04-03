import vampytest

from ..automation_reaction_role_item import AutomationReactionRoleItem
from ..items import unpack_items


def _iter_options():
    emoji_id_0 = 202509270040
    emoji_id_1 = 202509270041
    emoji_id_2 = 202509270042
    emoji_id_3 = 202509270043
    
    role_id_0 = 202509270044
    role_id_1 = 202509270045
    role_id_2 = 202509270046
    role_id_3 = 202509270047
    role_id_4 = 202509270048
    role_id_5 = 202509270049
    
    
    yield (
        None,
        1,
        None,
    )
    
    yield (
        b''.join([
            emoji_id_0.to_bytes(8, 'little'),
            (2).to_bytes(1, 'little'),
            (2).to_bytes(1, 'little'),
            role_id_0.to_bytes(8, 'little'),
            role_id_1.to_bytes(8, 'little'),
            role_id_2.to_bytes(8, 'little'),
            role_id_3.to_bytes(8, 'little'),
        ]),
        1,
        [
            AutomationReactionRoleItem(
                emoji_id_0,
                (role_id_0, role_id_1),
                (role_id_2, role_id_3),
            ),
        ],
    )
    
    yield (
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
        1,
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
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__unpack_items(data, data_version):
    """
    Tests whether ``unpack_items`` works as intended.
    
    Parameters
    ----------
    data : `None | bytes`
        Data to unpack from.
    
    data_version : `int`
        Serialization version.
    
    Returns
    -------
    items : ``None | list<AutomationReactionRoleItem>``
    """
    output = unpack_items(data, data_version)
    vampytest.assert_instance(output, list, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, AutomationReactionRoleItem)
    
    return output
