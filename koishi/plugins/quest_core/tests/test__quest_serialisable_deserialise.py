import vampytest

from ..quest_reward_types import QUEST_REWARD_TYPE_BALANCE
from ..quest_reward_serialisables import quest_reward_serialisable_create_balance
from ..serialisation import QUEST_REWARD_SERIALISATION_RESOLUTION, quest_serialisable_deserialise


def _iter_options():
    yield (
        QUEST_REWARD_SERIALISATION_RESOLUTION,
        None,
        (
            True,
            None,
        ),
    )
    
    serialisable_0 = quest_reward_serialisable_create_balance(
        566,
    )
    
    serialisable_1 = quest_reward_serialisable_create_balance(
        526,
    )
    
    yield (
        QUEST_REWARD_SERIALISATION_RESOLUTION,
        b''.join([
            serialisable_0.behaviour.type.to_bytes(1, 'little'),
            *serialisable_0.behaviour.serialise(serialisable_0.configuration),
            serialisable_1.behaviour.type.to_bytes(1, 'little'),
            *serialisable_1.behaviour.serialise(serialisable_1.configuration),
        ]),
        (
            True,
            [
                (
                    serialisable_0.behaviour.type,
                    serialisable_0.configuration.balance,
                ),
                (
                    serialisable_1.behaviour.type,
                    serialisable_1.configuration.balance,
                ),
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__quest_serialisable_deserialise(resolution, data):
    """
    Tests whether ``quest_serialisable_deserialise`` works as intended.
    
    Parameters
    ----------
    resolution : ``dict<int, type<QuestSubTypeSerialisable>>``
        Type identifier to type mapping.
    
    data : `None | bytes`
        Data to deserialise.
    
    Returns
    -------
    output : ``(bool, None | tuple<(int, int)>)``
    """
    success, serialisable_listing = quest_serialisable_deserialise(resolution, data)
    vampytest.assert_instance(success, bool)
    vampytest.assert_instance(serialisable_listing, tuple, nullable = True)
    
    if serialisable_listing is None:
        serialisable_listing_output = None
    else:
        serialisable_listing_output = []
        
        for element in serialisable_listing:
            sub_type_type = element.behaviour.type
            if sub_type_type == QUEST_REWARD_TYPE_BALANCE:
                value = element.configuration.balance
            else:
                value = 0
            
            serialisable_listing_output.append((sub_type_type, value))
    
    return (success, serialisable_listing_output)
