__all__ = ()

from math import sqrt

from hata.ext.slash import P

from ...bots import MAIN_CLIENT
from ...bot_utils.constants import GUILD__SUPPORT


GOD_ID_NONE = 0
GOD_ID_VOID = 1
GOD_ID_HARVEST = 2
GOD_ID_EARTH = 3
GOD_ID_ELEMENT = 4
GOD_ID_MACHINE = 5
GOD_ID_LUCK = 6
GOD_ID_HEALING = 7
GOD_ID_WIND = 8
GOD_ID_TRICKERY = 9
GOD_ID_MOONSHADOW = 10
GOD_ID_STRIFE = 11
GOD_ID_OBLIVION = 12
GOD_ID_HARMONY = 13

RACE_ID_NONE = 0
RACE_ID_DEMIGOD = 1

CLASS_ID_NONE = 0
CLASS_ID_PRIEST = 1
CLASS_ID_INQUISITOR = 2
CLASS_ID_PALADIN = 3


STAT_KIND_SHIFT = 8
STAT_KIND_MASK = 0xff
STAT_KIND_ID_BASE = 0
STAT_KIND_ID_SKILL = 1
STAT_KIND_ID_RESISTANCE = 2
STAT_KIND_ID_SPELL = 3
STAT_KIND_ID_FEAT = 4

STAT_ID_BASE_STRENGTH = (STAT_KIND_ID_BASE << STAT_KIND_SHIFT) | 1
STAT_ID_BASE_ENDURANCE = (STAT_KIND_ID_BASE << STAT_KIND_SHIFT) | 2
STAT_ID_BASE_DEXTERITY = (STAT_KIND_ID_BASE << STAT_KIND_SHIFT) | 3
STAT_ID_BASE_PERCEPTION = (STAT_KIND_ID_BASE << STAT_KIND_SHIFT) | 4
STAT_ID_BASE_LEARNING = (STAT_KIND_ID_BASE << STAT_KIND_SHIFT) | 5
STAT_ID_BASE_WILL = (STAT_KIND_ID_BASE << STAT_KIND_SHIFT) | 6
STAT_ID_BASE_MAGIC = (STAT_KIND_ID_BASE << STAT_KIND_SHIFT) | 7
STAT_ID_BASE_CHARISMA = (STAT_KIND_ID_BASE << STAT_KIND_SHIFT) | 8
STAT_ID_BASE_LUCK = (STAT_KIND_ID_BASE << STAT_KIND_SHIFT) | 9
STAT_ID_BASE_SPEED = (STAT_KIND_ID_BASE << STAT_KIND_SHIFT) | 10

STAT_ID_SKILL_FARMING = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 1
STAT_ID_SKILL_ALCHEMY = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 2
STAT_ID_SKILL_WEAVING = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 3
STAT_ID_SKILL_LITERACY = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 4
STAT_ID_SKILL_SHIELD = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 5
STAT_ID_SKILL_WEIGHTLIFTING = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 6
STAT_ID_SKILL_MINING = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 7
STAT_ID_SKILL_BLACKSMITH = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 8
STAT_ID_SKILL_LONG_SWORD = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 9
STAT_ID_SKILL_CASTING = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 10
STAT_ID_SKILL_REGENERATION = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 11
STAT_ID_SKILL_MEDITATION = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 12
STAT_ID_SKILL_GUN = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 13
STAT_ID_SKILL_SPOT_HIDDEN = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 14
STAT_ID_SKILL_DISARM_TRAP = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 15
STAT_ID_SKILL_LOCKPICKING = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 16
STAT_ID_SKILL_APPRAISING = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 17
STAT_ID_SKILL_STRATEGY = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 18
STAT_ID_SKILL_BOW = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 19
STAT_ID_SKILL_CROSSBOW = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 20
STAT_ID_SKILL_EVASION = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 21
STAT_ID_SKILL_MAGIC_DEVICE = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 22
STAT_ID_SKILL_MAGIC_CAPACITY = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 23
STAT_ID_SKILL_FISHING = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 24
STAT_ID_SKILL_STEALTH = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 25
STAT_ID_SKILL_ANATOMY = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 26
STAT_ID_SKILL_COOKING = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 27
STAT_ID_SKILL_MEMORIZATION = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 28
STAT_ID_SKILL_CONTROL_MAGIC = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 29
STAT_ID_SKILL_TAMING = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 30
STAT_ID_SKILL_MUSIC = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 31
STAT_ID_SKILL_TACTICS = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 32
STAT_ID_SKILL_TWO_HANDED = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 33
STAT_ID_SKILL_DUAL_WIELD = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 34
STAT_ID_SKILL_RIDING = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 35
STAT_ID_SKILL_TRAVEL = (STAT_KIND_ID_SKILL << STAT_KIND_SHIFT) | 36

STAT_ID_RESISTANCE_FIRE = (STAT_KIND_ID_RESISTANCE << STAT_KIND_SHIFT) | 1
STAT_ID_RESISTANCE_COLD = (STAT_KIND_ID_RESISTANCE << STAT_KIND_SHIFT) | 2
STAT_ID_RESISTANCE_LIGHTING = (STAT_KIND_ID_RESISTANCE << STAT_KIND_SHIFT) | 3
STAT_ID_RESISTANCE_NETHER = (STAT_KIND_ID_RESISTANCE << STAT_KIND_SHIFT) | 4
STAT_ID_RESISTANCE_HOLY = (STAT_KIND_ID_RESISTANCE << STAT_KIND_SHIFT) | 5
STAT_ID_RESISTANCE_DARKNESS = (STAT_KIND_ID_RESISTANCE << STAT_KIND_SHIFT) | 6
STAT_ID_RESISTANCE_CHAOS = (STAT_KIND_ID_RESISTANCE << STAT_KIND_SHIFT) | 7

STAT_ID_FEAT_DEMIGOD = (STAT_KIND_ID_FEAT << STAT_KIND_SHIFT) | 1
STAT_ID_FEAT_DEVOUT = (STAT_KIND_ID_FEAT << STAT_KIND_SHIFT) | 2


STAT_NAME_DEFAULT = 'Unknown'

STAT_ID_TO_NAME = {
    STAT_ID_BASE_STRENGTH : 'Strength',
    STAT_ID_BASE_ENDURANCE : 'Endurance',
    STAT_ID_BASE_DEXTERITY : 'Dexterity',
    STAT_ID_BASE_PERCEPTION : 'Perception',
    STAT_ID_BASE_LEARNING : 'Learning',
    STAT_ID_BASE_WILL : 'Will',
    STAT_ID_BASE_MAGIC : 'Magic',
    STAT_ID_BASE_CHARISMA : 'Charisma',
    STAT_ID_BASE_LUCK : 'Luck',
    STAT_ID_BASE_SPEED : 'Speed',
    
    STAT_ID_SKILL_FARMING : 'Farming',
    STAT_ID_SKILL_ALCHEMY : 'Alchemy',
    STAT_ID_SKILL_WEAVING : 'Weaving',
    STAT_ID_SKILL_LITERACY : 'Literacy',
    STAT_ID_SKILL_SHIELD : 'Shield',
    STAT_ID_SKILL_WEIGHTLIFTING : 'Weightlifting',
    STAT_ID_SKILL_MINING : 'Mining',
    STAT_ID_SKILL_BLACKSMITH : 'Blacksmith',
    STAT_ID_SKILL_LONG_SWORD : 'Long Sword',
    STAT_ID_SKILL_CASTING : 'Casting',
    STAT_ID_SKILL_REGENERATION : 'Regeneration',
    STAT_ID_SKILL_MEDITATION : 'Meditation',
    STAT_ID_SKILL_GUN : 'Gun',
    STAT_ID_SKILL_SPOT_HIDDEN : 'Spot Hidden',
    STAT_ID_SKILL_DISARM_TRAP : 'Disarm trap',
    STAT_ID_SKILL_LOCKPICKING : 'Lockpicking',
    STAT_ID_SKILL_APPRAISING : 'Appraising',
    STAT_ID_SKILL_STRATEGY : 'Strategy',
    STAT_ID_SKILL_BOW : 'Bow',
    STAT_ID_SKILL_CROSSBOW : 'Crossbow',
    STAT_ID_SKILL_EVASION : 'Evasion',
    STAT_ID_SKILL_MAGIC_DEVICE : 'Magic Device',
    STAT_ID_SKILL_MAGIC_CAPACITY : 'Magic Capacity',
    STAT_ID_SKILL_FISHING : 'Fishing',
    STAT_ID_SKILL_STEALTH : 'Stealth',
    STAT_ID_SKILL_ANATOMY : 'Anatomy',
    STAT_ID_SKILL_COOKING : 'Cooking',
    STAT_ID_SKILL_MEMORIZATION : 'Memorization',
    STAT_ID_SKILL_CONTROL_MAGIC : 'Control Magic',
    STAT_ID_SKILL_TAMING : 'Taming',
    STAT_ID_SKILL_MUSIC : 'Music',
    STAT_ID_SKILL_TACTICS : 'Tactics',
    STAT_ID_SKILL_TWO_HANDED : 'Two hHanded',
    STAT_ID_SKILL_DUAL_WIELD : 'Dual Wield',
    STAT_ID_SKILL_RIDING : 'Riding',
    STAT_ID_SKILL_TRAVEL : 'Travel',
    
    
    STAT_ID_RESISTANCE_FIRE : 'Fire Resistance',
    STAT_ID_RESISTANCE_COLD : 'Cold Resistance',
    STAT_ID_RESISTANCE_LIGHTING : 'Lighting Resistance',
    STAT_ID_RESISTANCE_NETHER : 'Nether Resistance',
    STAT_ID_RESISTANCE_HOLY : 'Holy Resistance',
    STAT_ID_RESISTANCE_DARKNESS : 'Darkness Resistance',
    STAT_ID_RESISTANCE_CHAOS : 'Chaos Resistance',
    
    STAT_ID_FEAT_DEMIGOD : 'Demigod',
    STAT_ID_FEAT_DEVOUT : 'Piety',
}


GOD_ID_TO_PIETY_BONUSES = {
    GOD_ID_VOID : (
        (STAT_ID_BASE_STRENGTH, 8),
        (STAT_ID_BASE_ENDURANCE, 8),
        (STAT_ID_BASE_DEXTERITY, 8),
        (STAT_ID_BASE_PERCEPTION, 8),
        (STAT_ID_BASE_LEARNING, 8),
        (STAT_ID_BASE_WILL, 8),
        (STAT_ID_BASE_MAGIC, 8),
        (STAT_ID_BASE_CHARISMA, 8),
        (STAT_ID_BASE_LUCK, 20),
        (STAT_ID_BASE_SPEED, 20),
    ),
    GOD_ID_HARVEST : (
        (STAT_ID_BASE_PERCEPTION, 8),
        (STAT_ID_BASE_DEXTERITY, 12),
        (STAT_ID_BASE_LEARNING, 16),
        (STAT_ID_SKILL_FARMING, 12),
        (STAT_ID_SKILL_ALCHEMY, 10),
        (STAT_ID_SKILL_WEAVING, 10),
        (STAT_ID_SKILL_LITERACY, 8),
    ),
    GOD_ID_EARTH : (
        (STAT_ID_BASE_STRENGTH, 11),
        (STAT_ID_BASE_ENDURANCE, 16),
        (STAT_ID_SKILL_SHIELD, 15),
        (STAT_ID_SKILL_WEIGHTLIFTING, 16),
        (STAT_ID_SKILL_MINING, 12),
        (STAT_ID_SKILL_BLACKSMITH, 12),
        
    ),
    GOD_ID_ELEMENT : (
        (STAT_ID_BASE_MAGIC, 18),
        (STAT_ID_SKILL_CASTING, 8),
        (STAT_ID_RESISTANCE_FIRE, 15),
        (STAT_ID_RESISTANCE_COLD, 15),
        (STAT_ID_RESISTANCE_LIGHTING, 15),
        (STAT_ID_RESISTANCE_LIGHTING, 15),
    ),
    GOD_ID_MACHINE : (
        (STAT_ID_BASE_DEXTERITY, 14),
        (STAT_ID_BASE_PERCEPTION, 14),
        (STAT_ID_SKILL_GUN, 18),
        (STAT_ID_SKILL_SPOT_HIDDEN, 8),
        (STAT_ID_SKILL_DISARM_TRAP, 5),
        (STAT_ID_SKILL_LOCKPICKING, 16),
        (STAT_ID_SKILL_APPRAISING, 12),
        (STAT_ID_SKILL_STRATEGY, 10),
    ),
    GOD_ID_LUCK : (
        (STAT_ID_BASE_CHARISMA, 20),
        (STAT_ID_BASE_LUCK, 25),
        (STAT_ID_SKILL_EVASION, 15),
        (STAT_ID_SKILL_MAGIC_CAPACITY, 17),
        (STAT_ID_SKILL_FISHING, 12),
        (STAT_ID_SKILL_STEALTH, 12),
        
    ),
    GOD_ID_HEALING : (
        (STAT_ID_BASE_WILL, 16),
        (STAT_ID_BASE_ENDURANCE, 10),
        (STAT_ID_SKILL_REGENERATION, 18),
        (STAT_ID_SKILL_MEDITATION, 10),
        (STAT_ID_SKILL_ANATOMY, 9),
        (STAT_ID_SKILL_COOKING, 8),
        (STAT_ID_SKILL_MAGIC_DEVICE, 10),
        (STAT_ID_SKILL_MAGIC_CAPACITY, 12),
    ),
    GOD_ID_WIND : (
        (STAT_ID_BASE_PERCEPTION, 10),
        (STAT_ID_BASE_SPEED, 30),
        (STAT_ID_SKILL_BOW, 16),
        (STAT_ID_SKILL_CROSSBOW, 12),
        (STAT_ID_SKILL_EVASION, 14),
        (STAT_ID_SKILL_TAMING, 8),
    ),
    GOD_ID_TRICKERY : (
        (STAT_ID_BASE_CHARISMA, 12),
        (STAT_ID_BASE_LUCK, 15),
        (STAT_ID_BASE_SPEED, 10),
        (STAT_ID_SKILL_MEMORIZATION, 10),
        (STAT_ID_SKILL_CONTROL_MAGIC, 12),
        (STAT_ID_RESISTANCE_NETHER, 10),
        (STAT_ID_RESISTANCE_HOLY, 5),
    ),
    GOD_ID_MOONSHADOW : (
        (STAT_ID_BASE_MAGIC, 16),
        (STAT_ID_BASE_CHARISMA, 12),
        (STAT_ID_SKILL_LONG_SWORD, 14),
        (STAT_ID_SKILL_CASTING, 12),
        (STAT_ID_SKILL_MUSIC, 8),
        (STAT_ID_RESISTANCE_DARKNESS, 15),
        
    ),
    GOD_ID_STRIFE : (
        (STAT_ID_BASE_STRENGTH, 10),
        (STAT_ID_BASE_DEXTERITY, 9),
        (STAT_ID_BASE_PERCEPTION, 8),
        (STAT_ID_SKILL_TACTICS, 12),
        (STAT_ID_SKILL_TWO_HANDED, 12),
        (STAT_ID_SKILL_DUAL_WIELD, 12),
        (STAT_ID_SKILL_RIDING, 8),
        (STAT_ID_SKILL_TRAVEL, 10),
        
    ),
    GOD_ID_OBLIVION : (
        (STAT_ID_BASE_PERCEPTION, 0),
        (STAT_ID_BASE_MAGIC, 0),
        (STAT_ID_SKILL_MEDITATION, 0),
        (STAT_ID_RESISTANCE_NETHER, 0),
        (STAT_ID_RESISTANCE_CHAOS, 0),
        
    ),
    GOD_ID_HARMONY : (
        (STAT_ID_BASE_CHARISMA, 8),
        (STAT_ID_SKILL_COOKING, 0),
    ),
}


RACE_ID_TO_BONUSES = {
    RACE_ID_DEMIGOD : (
        (STAT_ID_FEAT_DEMIGOD, 1),
    ),
}


CLASS_ID_TO_BONUSES = {
    CLASS_ID_PRIEST : (
        (STAT_ID_FEAT_DEVOUT, 1),
    ),
    CLASS_ID_INQUISITOR : (
        (STAT_ID_FEAT_DEVOUT, 1),
    ),
    CLASS_ID_PALADIN : (
        (STAT_ID_FEAT_DEVOUT, 2),
    ),
}


def clamp(value, threshold_lower, threshold_upper):
    """
    Clamps the value within the lower and upper threshold.
    
    Parameters
    ----------
    value : `int`
        Value to clamp.
    
    threshold_lower : `int`
        The lower threshold to clamp to.
    
    threshold_upper : `int`
        The upper threshold to clamp to.
    
    Returns
    -------
    value : `int`
    """
    if value < threshold_lower:
        value = threshold_lower
    elif value > threshold_upper:
        value = threshold_upper
    return value


def curve(value, start, step, rate):
    """
    Curves the given value.
    
    Parameters
    ----------
    value : `int`
        The value to curve.
    
    start : `int`
        Where curving starts.
    
    step : `int`
        Step between each curving level.
    
    rate : `int`
        Rate of curving.
    
    Returns
    -------
    value : `int`
    """
    threshold = start
    for index in range(10):
        if value <= threshold:
            break
        
        value = threshold + (value - threshold) * rate // 100
        threshold += step
        continue
    
    return clamp(value, -2147483600, 2147483600)


def initial_stats_construct(race_id, class_id):
    """
    Constructs initial stats.
    
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
    stats = {}
    
    bonuses = RACE_ID_TO_BONUSES.get(race_id, None)
    if (bonuses is not None):
        for stat_id, value in bonuses:
            stats[stat_id] = stats.get(stat_id, 0) + value
    
    bonuses = CLASS_ID_TO_BONUSES.get(class_id, None)
    if (bonuses is not None):
        for class_id, value in bonuses:
            stats[class_id] = stats.get(class_id, 0) + value
    
    return stats


def calculate_piety_bonuses(piety_level, days_with_god, god_id, stats):
    """
    Calculates piety bonuses.
    
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
    
    Returns
    -------
    output : `None | list<(int, int)>`
    """
    feat_level_demigod = stats.get(STAT_ID_FEAT_DEMIGOD, 0)
    if (god_id == GOD_ID_VOID) and (not feat_level_demigod):
        piety_bonuses = None
    else:
        piety_bonuses = GOD_ID_TO_PIETY_BONUSES.get(god_id, None)
    
    if piety_bonuses is None:
        return None
    
    piety_value = 10 + int(sqrt(days_with_god) * 2.0 + float(piety_level)) // 2
    
    scaling_rate = piety_value * (
        120 +
        stats.get(STAT_ID_FEAT_DEVOUT, 0) * 15 +
        feat_level_demigod * 20
    ) // 100
    
    piety_bonuses_scaled = []
    for stat_id, stat_scaling in piety_bonuses:
        value = stat_scaling * scaling_rate // 50
        
        if stat_id == STAT_ID_BASE_SPEED:
            # Speed is curved
            value = curve(value, stat_scaling * 2, 10, 50)
        
        elif (stat_id >> STAT_KIND_SHIFT) & STAT_KIND_MASK == STAT_KIND_ID_RESISTANCE:
            # Resistances are capped at 20
            value = min(value, 20)
        
        piety_bonuses_scaled.append((stat_id, max(value, 1)))
    
    return piety_bonuses_scaled


def produce_piety_bonuses_scaled_description(piety_bonuses_scaled):
    """
    Produces piety scaled description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    piety_bonuses_scaled : `None | list<(int, int)>`
        Start identifier - value pairs.
    
    Yields
    ------
    part : `str`
    """
    if (piety_bonuses_scaled is None):
        yield '\\*none\\*'
        return
    
    for index in range(len(piety_bonuses_scaled)):
        stat_id, value = piety_bonuses_scaled[index]
        if index:
            yield '\n'
        
        yield '- '
        yield STAT_ID_TO_NAME.get(stat_id, STAT_NAME_DEFAULT)
        yield ' '
        yield ('+' if value >= 0 else '-')
        yield str(abs(value))



@MAIN_CLIENT.interactions(guild = GUILD__SUPPORT)
async def elin_calculate_piety_bonuses(
    client,
    interaction_event,
    piety_level : P(int, 'Piety level', min_value = 0, max_value = 10000),
    days_with_god : P(int, 'Days with god', min_value = 0, max_value = 10000000),
    god_id : P(
        [
            ('Eyth of Void', GOD_ID_VOID),
            ('Kumiromi of Harvest', GOD_ID_HARVEST),
            ('Opatos of Earth', GOD_ID_EARTH),
            ('Itzpalt of Element', GOD_ID_ELEMENT),
            ('Mani of Machine', GOD_ID_MACHINE),
            ('Ehekatl of Luck', GOD_ID_LUCK),
            ('Jure of Healing', GOD_ID_HEALING),
            ('Lulwy of Wind', GOD_ID_WIND),
            ('Kizuami of Trickery', GOD_ID_TRICKERY),
            ('Horome of Moonshadow', GOD_ID_MOONSHADOW),
            ('Yevan of Strife', GOD_ID_STRIFE),
            ('Yakasha of Oblivion', GOD_ID_OBLIVION),
        ],
        'The worshipped god',
        'god',
    ) = GOD_ID_NONE,
    race_id : P(
        [
            ('Other', RACE_ID_NONE),
            ('Demigod', RACE_ID_DEMIGOD),
        ],
        'Your race',
        'race',
    ) = RACE_ID_NONE,
    class_id : P(
        [
            ('Other', CLASS_ID_NONE),
            ('Priest', CLASS_ID_PRIEST),
            ('Inquisitor', CLASS_ID_INQUISITOR),
            ('Paladin', CLASS_ID_PALADIN),
        ],
        'Your class',
        'class',
    ) = CLASS_ID_NONE,
):
    stats = initial_stats_construct(race_id, class_id)
    piety_bonuses_scaled = calculate_piety_bonuses(piety_level, days_with_god, god_id, stats)
    
    await client.interaction_response_message_create(
        interaction_event,
        content = ''.join([*produce_piety_bonuses_scaled_description(piety_bonuses_scaled)]),
    )
