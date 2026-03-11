import vampytest

from ..quest_reward_serialisables import QuestRewardSerialisableBalance
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
    
    serialisable_0 = QuestRewardSerialisableBalance(
        566,
    )
    
    serialisable_1 = QuestRewardSerialisableBalance(
        526,
    )
    
    yield (
        QUEST_REWARD_SERIALISATION_RESOLUTION,
        b''.join([
            serialisable_0.TYPE.to_bytes(1, 'little'),
            *serialisable_0.serialise(),
            serialisable_1.TYPE.to_bytes(1, 'little'),
            *serialisable_1.serialise(),
        ]),
        (
            True,
            (
                serialisable_0,
                serialisable_1,
            ),
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
    output : ``(bool, None | tuple<QuestSubTypeSerialisable>)``
    """
    success, serialisable_listing = quest_serialisable_deserialise(resolution, data)
    vampytest.assert_instance(success, bool)
    vampytest.assert_instance(serialisable_listing, tuple, nullable = True)
    return (success, serialisable_listing)
