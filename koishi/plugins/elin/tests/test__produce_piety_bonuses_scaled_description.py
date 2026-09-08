import vampytest

from ..calculate_piety_bonuses import (
    STAT_ID_BASE_CHARISMA, STAT_ID_BASE_LUCK, STAT_ID_BASE_SPEED, STAT_ID_RESISTANCE_HOLY, STAT_ID_RESISTANCE_NETHER,
    STAT_ID_SKILL_CONTROL_MAGIC, STAT_ID_SKILL_MEMORIZATION, produce_piety_bonuses_scaled_description
)

def _iter_options():
   yield (
       None,
       '\\*none\\*'
   )
   
   yield (
        [
            (STAT_ID_BASE_CHARISMA, 40),
            (STAT_ID_BASE_LUCK, 50),
            (STAT_ID_BASE_SPEED, 26),
            (STAT_ID_SKILL_MEMORIZATION, 33),
            (STAT_ID_SKILL_CONTROL_MAGIC, 40),
            (STAT_ID_RESISTANCE_NETHER, 20),
            (STAT_ID_RESISTANCE_HOLY, 16),
        ],
        (
            '- Charisma +40\n'
            '- Luck +50\n'
            '- Speed +26\n'
            '- Memorization +33\n'
            '- Control Magic +40\n'
            '- Nether Resistance +20\n'
            '- Holy Resistance +16'
        ),
    )
   

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_piety_bonuses_scaled_description(piety_bonuses_scaled):
    """
    Tests whether ``produce_piety_bonuses_scaled_description`` works as intended.
    
    Parameters
    ----------
    piety_bonuses_scaled : `None | list<(int, int)>`
        Start identifier - value pairs.
    
    Yields
    ------
    part : `str`
    """
    parts = [*produce_piety_bonuses_scaled_description(piety_bonuses_scaled)]
    for part in parts:
        vampytest.assert_instance(part, str)
    
    return ''.join(parts)
