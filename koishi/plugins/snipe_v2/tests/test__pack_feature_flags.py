import vampytest
from hata import Channel, ChannelType, InteractionEvent, User

from ..constants import FEATURE_FLAG_DETAILED, FEATURE_FLAG_DM, FEATURE_FLAG_REVEALED

from ..responding_helpers import pack_feature_flags


def _iter_options():
    interaction_event_0 = InteractionEvent.precreate(
        202511010010,
    )
    
    interaction_event_1 = InteractionEvent.precreate(
        202511010011,
        channel = Channel.precreate(
            202511010012,
            channel_type = ChannelType.private,
            users = [
                User.precreate(
                    202511010013,
                ),
                User.precreate(
                    202511010014,
                ),
            ],
        )
    )
    
    yield (
        interaction_event_0,
        False,
        True,
        FEATURE_FLAG_REVEALED,
    )
    
    yield (
        interaction_event_0,
        True,
        False,
        FEATURE_FLAG_DETAILED,
    )
    
    yield (
        interaction_event_1,
        False,
        False,
        FEATURE_FLAG_DM,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__pack_feature_flags(interaction_event, detailed, reveal):
    """
    Tests whether ``pack_feature_flags`` works as intended.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    detailed : `bool`
        Whether a detailed view of the entity should be shown.
    
    reveal : `bool`
        Whether the response should be revealed.
    
    Returns
    -------
    output : `int`
    """
    output = pack_feature_flags(interaction_event, detailed, reveal)
    vampytest.assert_instance(output, int)
    return output
