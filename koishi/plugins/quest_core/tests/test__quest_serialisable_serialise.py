import vampytest

from ..quest_reward_serialisables import QuestRewardSerialisableBalance
from ..serialisation import quest_serialisable_serialise


def _iter_options():
    yield (
        None,
        None,
    )
    
    serialisable_0 = QuestRewardSerialisableBalance(
        566,
    )
    
    serialisable_1 = QuestRewardSerialisableBalance(
        526,
    )
    
    yield (
        (
            serialisable_0,
            serialisable_1,
        ),
        b''.join([
            serialisable_0.TYPE.to_bytes(1, 'little'),
            *serialisable_0.serialise(),
            serialisable_1.TYPE.to_bytes(1, 'little'),
            *serialisable_1.serialise(),
        ]),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__quest_serialisable_serialise(serialisable_listing):
    """
    Tests whether ``quest_serialisable_serialise`` works as intended.
    
    Parameters
    ----------
    serialisable_listing : ``None | tuple<QuestSubTypeSerialisable>``
        To serialise.
    
    Returns
    -------
    output : `None | bytes`
    """
    output = quest_serialisable_serialise(serialisable_listing)
    vampytest.assert_instance(output, bytes, nullable = True)
    return output
