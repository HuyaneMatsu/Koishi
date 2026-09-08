import vampytest

from ..calculate_piety_bonuses import (
    CLASS_ID_NONE, CLASS_ID_PRIEST, RACE_ID_DEMIGOD, RACE_ID_NONE, STAT_ID_FEAT_DEMIGOD, STAT_ID_FEAT_DEVOUT,
    initial_stats_construct
)


def _iter_options():
    yield (
        RACE_ID_NONE,
        CLASS_ID_NONE,
        {},
    )
    
    yield (
        RACE_ID_DEMIGOD,
        CLASS_ID_PRIEST,
        {
            STAT_ID_FEAT_DEMIGOD : 1,
            STAT_ID_FEAT_DEVOUT : 1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__initial_stats_construct(race_id, class_id):
    """
    Tests whether ``initial_stats_construct`` works as intended.
    
    Parameters
    ----------
    race_id : `int`
        The selected race's identifier.
    
    class_id : `int`
        The selected class' identifier
    
    Returns
    -------
    stats : `dict<int, int>`
    """
    output = initial_stats_construct(race_id, class_id)
    vampytest.assert_instance(output, dict)
    return output
