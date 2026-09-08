import vampytest

from ..calculate_piety_bonuses import (
    GOD_ID_TRICKERY, GOD_ID_VOID, STAT_ID_BASE_CHARISMA, STAT_ID_BASE_LUCK, STAT_ID_BASE_SPEED, STAT_ID_FEAT_DEMIGOD,
    STAT_ID_FEAT_DEVOUT, STAT_ID_RESISTANCE_HOLY, STAT_ID_RESISTANCE_NETHER, STAT_ID_SKILL_CONTROL_MAGIC,
    STAT_ID_SKILL_MEMORIZATION, calculate_piety_bonuses
)


def _iter_options():
    yield (
        0,
        0,
        GOD_ID_VOID,
        {},
        None,
    )
    
    yield (
        10,
        10,
        GOD_ID_VOID,
        {},
        None,
    )
    
    yield (
        0,
        0,
        GOD_ID_TRICKERY,
        {},
        [
            (STAT_ID_BASE_CHARISMA, 2),
            (STAT_ID_BASE_LUCK, 3),
            (STAT_ID_BASE_SPEED, 2),
            (STAT_ID_SKILL_MEMORIZATION, 2),
            (STAT_ID_SKILL_CONTROL_MAGIC, 2),
            (STAT_ID_RESISTANCE_NETHER, 2),
            (STAT_ID_RESISTANCE_HOLY, 1),
        ],
    )
    
    yield (
        30,
        1000,
        GOD_ID_TRICKERY,
        {},
        [
            (STAT_ID_BASE_CHARISMA, 16),
            (STAT_ID_BASE_LUCK, 20),
            (STAT_ID_BASE_SPEED, 13),
            (STAT_ID_SKILL_MEMORIZATION, 13),
            (STAT_ID_SKILL_CONTROL_MAGIC, 16),
            (STAT_ID_RESISTANCE_NETHER, 13),
            (STAT_ID_RESISTANCE_HOLY, 6),
        ],
    )
    
    yield (
        60,
        10000,
        GOD_ID_TRICKERY,
        {},
        [
            (STAT_ID_BASE_CHARISMA, 40),
            (STAT_ID_BASE_LUCK, 50),
            (STAT_ID_BASE_SPEED, 26),
            (STAT_ID_SKILL_MEMORIZATION, 33),
            (STAT_ID_SKILL_CONTROL_MAGIC, 40),
            (STAT_ID_RESISTANCE_NETHER, 20),
            (STAT_ID_RESISTANCE_HOLY, 16),
        ],
    )
    
    yield (
        60,
        10000,
        GOD_ID_TRICKERY,
        {
            STAT_ID_FEAT_DEMIGOD : 1,
            STAT_ID_FEAT_DEVOUT : 2,
        },
        [
            (STAT_ID_BASE_CHARISMA, 57),
            (STAT_ID_BASE_LUCK, 71),
            (STAT_ID_BASE_SPEED, 31),
            (STAT_ID_SKILL_MEMORIZATION, 47),
            (STAT_ID_SKILL_CONTROL_MAGIC, 57),
            (STAT_ID_RESISTANCE_NETHER, 20),
            (STAT_ID_RESISTANCE_HOLY, 20),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__calculate_piety_bonuses(piety_level, days_with_god, god_id, stats):
    """
    Tests whether ``calculate_piety_bonuses`` works as intended.
    
    Parameters
    -----------
    piety_level : `int`
        The user's piety level.
    
    days_with_god : `int`
        The user's days with its god.
    
    god_id : `int`
        The god's identifier.
    
    stats : `dict<int, int>`
        The user's already constructed stats.
    
    Parameters
    ----------
    output : `None | list<(int, int)>`
    """
    output = calculate_piety_bonuses(piety_level, days_with_god, god_id, stats)
    vampytest.assert_instance(output, list, nullable = True)
    return output
