import vampytest

from ..quest_reward_serialisables import quest_reward_serialisable_create_balance
from ..serialisation import quest_serialisable_serialise


def _iter_options():
    yield (
        None,
        None,
    )
    
    serialisable_0 = quest_reward_serialisable_create_balance(
        566,
    )
    
    serialisable_1 = quest_reward_serialisable_create_balance(
        526,
    )
    
    yield (
        (
            serialisable_0,
            serialisable_1,
        ),
        b''.join([
            serialisable_0.behaviour.type.to_bytes(1, 'little'),
            *serialisable_0.behaviour.serialise(serialisable_0.configuration),
            serialisable_1.behaviour.type.to_bytes(1, 'little'),
            *serialisable_1.behaviour.serialise(serialisable_1.configuration),
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
