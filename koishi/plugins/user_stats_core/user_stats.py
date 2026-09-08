__all__ = (
    'UserStats', 'user_stats_calculate', 'user_stats_create', 'user_stats_create_from_entry', 
    'user_stats_modify_credibility_by', 'user_stats_modify_stat_bedroom_by', 'user_stats_modify_stat_charm_by',
    'user_stats_modify_stat_cuteness_by', 'user_stats_modify_stat_housewife_by', 'user_stats_modify_stat_loyalty_by',
    'user_stats_set_item_id_costume', 'user_stats_set_item_id_head', 'user_stats_set_item_id_species',
    'user_stats_set_item_id_weapon', 'user_stats_set_recovering_until',
    'user_stats_set_recovering_until_notification_at'
)

from datetime import timezone as TimeZone

from scarletio import RichAttributeErrorBaseType

from .helpers import generate_user_stats_defaults
from .user_stats_calculated import user_stats_calculated_create


USER_STATS_MODIFICATION_FLAG_CREDIBILITY = 1 << 0
USER_STATS_MODIFICATION_FLAG_ITEM_ID_COSTUME = 1 << 1
USER_STATS_MODIFICATION_FLAG_ITEM_ID_HEAD = 1 << 2
USER_STATS_MODIFICATION_FLAG_ITEM_ID_SPECIES = 1 << 3
USER_STATS_MODIFICATION_FLAG_ITEM_ID_WEAPON = 1 << 4
USER_STATS_MODIFICATION_FLAG_RECOVERY_UNTIL = 1 << 5
USER_STATS_MODIFICATION_FLAG_RECOVERY_UNTIL_NOTIFICATION_AT = 1 << 6
USER_STATS_MODIFICATION_FLAG_STAT_BEDROOM = 1 << 7
USER_STATS_MODIFICATION_FLAG_STAT_CHARM = 1 << 8
USER_STATS_MODIFICATION_FLAG_STAT_CUTENESS = 1 << 9
USER_STATS_MODIFICATION_FLAG_STAT_HOUSEWIFE = 1 << 10
USER_STATS_MODIFICATION_FLAG_STAT_LOYALTY = 1 << 11


class UserStats(RichAttributeErrorBaseType):
    """
    A user's stats.
    
    Attributes
    ----------
    _cache_user_stats_calculated : ``None | UserStatsCalculated``
        Cache field for the calculated stats after applying the modifiers.
    
    entry_id : `int`
        The entry's identifier in the database.
    
    credibility : `int`
        The accumulated credibility of the user.
    
    item_id_costume : `int`
        The user's costume item's identifier.
    
    item_id_head : `int`
        The user's head item's identifier.
    
    item_id_species : `int`
        Target user's species' identifier.
    
    item_id_weapon : `int`
        The user's weapon item's identifier.
    
    modification_flags : `int`
        Bit flags describing which fields were modified.
    
    recovering_until : `None | DateTime`
        Until when the user is in recovery.
    
    recovering_until_notification_at : `None | DateTime`
        When the recovery notification should be delivered at. Set upon delivering the original notification fails.
    
    stat_bedroom : `int`
        The user's bedroom skills.
    
    stat_charm : `int`
        The user's charm.
    
    stat_cuteness : `int`
        The user's cuteness.
    
    stat_housewife : `int`
        The user's housewife skills.
    
    stat_loyalty : `int`
        The user's loyalty.
    
    user_id : `int`
        The represented user's identifier.
    """
    __slots__ = (
        '__weakref__', '_cache_user_stats_calculated', 'credibility', 'entry_id', 'item_id_costume', 'item_id_head',
        'item_id_species', 'item_id_weapon', 'modification_flags', 'recovering_until',
        'recovering_until_notification_at', 'stat_bedroom', 'stat_charm', 'stat_cuteness', 'stat_housewife',
        'stat_loyalty', 'user_id',
    )

    
    def __repr__(self):
        """Returns repr(self)."""
        repr_parts = ['<', type(self).__name__]
        
        # entry_id
        entry_id = self.entry_id
        if entry_id != 0:
            repr_parts.append(' entry_id = ')
            repr_parts.append(repr(entry_id))
            repr_parts.append(',')
        
        # user_id
        repr_parts.append(' user_id = ')
        repr_parts.append(repr(self.user_id))
        
        repr_parts.append('>')
        return ''.join(repr_parts)


def user_stats_create(user_id):
    """
    Creates new user stats.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    
    Returns
    -------
    user_stats : ``UserStats``
    """
    user_stats = object.__new__(UserStats)
    user_stats._cache_user_stats_calculated = None
    user_stats.modification_flags = 0
    
    user_stats.entry_id = 0
    user_stats.user_id = user_id
    
    user_stats.credibility = 0
    user_stats.recovering_until = None
    user_stats.recovering_until_notification_at = None
    
    user_stats.item_id_costume = 0
    user_stats.item_id_head = 0
    user_stats.item_id_species = 0
    user_stats.item_id_weapon = 0
    
    (
        user_stats.stat_housewife,
        user_stats.stat_cuteness,
        user_stats.stat_bedroom,
        user_stats.stat_charm,
        user_stats.stat_loyalty,
    ) = generate_user_stats_defaults(user_id)
    
    return user_stats


def user_stats_create_from_entry(entry):
    """
    Creates an new user stats from the given entry.
    
    Parameters
    ----------
    entry : `sqlalchemy.engine.result.RowProxy`
        The entry to create the instance based on.
    
    Returns
    -------
    user_stats : ``UserStats``
    """
    user_stats = object.__new__(UserStats)
    user_stats.entry_id = entry['id']
    user_stats.user_id = entry['user_id']
    user_stats._cache_user_stats_calculated = None
    user_stats.modification_flags = 0
    
    user_stats.stat_housewife = entry['stat_housewife']
    user_stats.stat_cuteness = entry['stat_cuteness']
    user_stats.stat_bedroom = entry['stat_bedroom']
    user_stats.stat_charm = entry['stat_charm']
    user_stats.stat_loyalty = entry['stat_loyalty']
    
    user_stats.credibility = entry['credibility']
    
    recovering_until = entry['recovering_until']
    if (recovering_until is not None):
        recovering_until = recovering_until.replace(tzinfo = TimeZone.utc)
    user_stats.recovering_until = recovering_until
    
    recovering_until_notification_at = entry['recovering_until_notification_at']
    if (recovering_until_notification_at is not None):
        recovering_until_notification_at = recovering_until_notification_at.replace(
            tzinfo = TimeZone.utc
        )
    user_stats.recovering_until_notification_at = recovering_until_notification_at
    
    user_stats.item_id_costume = entry['item_id_costume']
    user_stats.item_id_head = entry['item_id_head']
    user_stats.item_id_species = entry['item_id_species']
    user_stats.item_id_weapon = entry['item_id_weapon']
    
    return user_stats


def user_stats_calculate(user_stats):
    """
    Returns the calculated stats.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        User stats to get calculated stats of.
    
    Returns
    -------
    stats_calculated : ``UserStatsCalculated``
    """
    stats_calculated = user_stats._cache_user_stats_calculated
    if stats_calculated is None:
        stats_calculated = user_stats_calculated_create(user_stats)
        user_stats._cache_user_stats_calculated = stats_calculated
    
    return stats_calculated


def user_stats_modify_stat_housewife_by(user_stats, value):
    """
    Modifies the housewife of the user stats.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        User stats to modify.
    
    value : `int`
        value to modify by.
    """
    user_stats.stat_housewife = max(user_stats.stat_housewife + value, 0)
    user_stats.modification_flags |= USER_STATS_MODIFICATION_FLAG_STAT_HOUSEWIFE
    user_stats._cache_user_stats_calculated = None


def user_stats_modify_stat_cuteness_by(user_stats, value):
    """
    Modifies the cuteness of the user stats.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        User stats to modify.
    
    value : `int`
        value to modify by.
    """
    user_stats.stat_cuteness = max(user_stats.stat_cuteness + value, 0)
    user_stats.modification_flags |= USER_STATS_MODIFICATION_FLAG_STAT_CUTENESS
    user_stats._cache_user_stats_calculated = None


def user_stats_modify_stat_bedroom_by(user_stats, value):
    """
    Modifies the bedroom of the user stats.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        User stats to modify.
    
    value : `int`
        value to modify by.
    """
    user_stats.stat_bedroom = max(user_stats.stat_bedroom + value, 0)
    user_stats.modification_flags |= USER_STATS_MODIFICATION_FLAG_STAT_BEDROOM
    user_stats._cache_user_stats_calculated = None


def user_stats_modify_stat_charm_by(user_stats, value):
    """
    Modifies the charm of the user stats.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        User stats to modify.
    
    value : `int`
        value to modify by.
    """
    user_stats.stat_charm = max(user_stats.stat_charm + value, 0)
    user_stats.modification_flags |= USER_STATS_MODIFICATION_FLAG_STAT_CHARM
    user_stats._cache_user_stats_calculated = None


def user_stats_modify_stat_loyalty_by(user_stats, value):
    """
    Modifies the loyalty of the user stats.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        User stats to modify.
    
    value : `int`
        value to modify by.
    """
    user_stats.stat_loyalty = max(user_stats.stat_loyalty + value, 0)
    user_stats.modification_flags |= USER_STATS_MODIFICATION_FLAG_STAT_LOYALTY
    user_stats._cache_user_stats_calculated = None


def user_stats_set_recovering_until(user_stats, date_time):
    """
    Sets till when the user is recovering.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        User stats to modify.
    
    date_time : `DateTime`
        Amount to set to.
    """
    user_stats.recovering_until = date_time
    user_stats.modification_flags |= USER_STATS_MODIFICATION_FLAG_RECOVERY_UNTIL
    user_stats._cache_user_stats_calculated = None


def user_stats_set_recovering_until_notification_at(user_stats, date_time):
    """
    Sets when the recovery notification should be delivered at.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        User stats to modify.
    
    date_time : `DateTime`
        Amount to set to.
    """
    user_stats.recovering_until_notification_at = date_time
    user_stats.modification_flags |= USER_STATS_MODIFICATION_FLAG_RECOVERY_UNTIL_NOTIFICATION_AT
    user_stats._cache_user_stats_calculated = None


def user_stats_modify_credibility_by(user_stats, value):
    """
    Modifies the credibility of the user stats.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        User stats to modify.
    
    value : `int`
        value to modify by.
    """
    user_stats.credibility = max(user_stats.credibility + value, 0)
    user_stats.modification_flags |= USER_STATS_MODIFICATION_FLAG_CREDIBILITY
    user_stats._cache_user_stats_calculated = None


def user_stats_set_item_id_costume(user_stats, item_id):
    """
    Sets the costume item.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        User stats to modify.
    
    item_id : `int`
        Item identifier to set to.
    """
    user_stats.item_id_costume = item_id
    user_stats.modification_flags |= USER_STATS_MODIFICATION_FLAG_ITEM_ID_COSTUME
    user_stats._cache_user_stats_calculated = None


def user_stats_set_item_id_head(user_stats, item_id):
    """
    Sets the head item.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        User stats to modify.
    
    item_id : `int`
        Item identifier to set to.
    """
    user_stats.item_id_head = item_id
    user_stats.modification_flags |= USER_STATS_MODIFICATION_FLAG_ITEM_ID_HEAD
    user_stats._cache_user_stats_calculated = None


def user_stats_set_item_id_species(user_stats, item_id):
    """
    Sets the species item.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        User stats to modify.
    
    item_id : `int`
        Item identifier to set to.
    """
    user_stats.item_id_species = item_id
    user_stats.modification_flags |= USER_STATS_MODIFICATION_FLAG_ITEM_ID_SPECIES
    user_stats._cache_user_stats_calculated = None


def user_stats_set_item_id_weapon(user_stats, item_id):
    """
    Sets the weapon item.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        User stats to modify.
    
    item_id : `int`
        Item identifier to set to.
    """
    user_stats.item_id_weapon = item_id
    user_stats.modification_flags |= USER_STATS_MODIFICATION_FLAG_ITEM_ID_WEAPON
    user_stats._cache_user_stats_calculated = None


def user_stats_collect_modifications(user_stats):
    """
    Collects the modifications done to the user stats.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        The user stats to collect of.
    
    Returns
    -------
    modifications : `None | dict<str, object>`
    """
    modification_flags = user_stats.modification_flags
    if not modification_flags:
        return None
    
    user_stats.modification_flags = 0
    
    modifications = {}
    
    if modification_flags & USER_STATS_MODIFICATION_FLAG_CREDIBILITY:
        modifications['credibility'] = user_stats.credibility
    
    if modification_flags & USER_STATS_MODIFICATION_FLAG_ITEM_ID_COSTUME:
        modifications['item_id_costume'] = user_stats.item_id_costume
    
    if modification_flags & USER_STATS_MODIFICATION_FLAG_ITEM_ID_HEAD:
        modifications['item_id_head'] = user_stats.item_id_head
    
    if modification_flags & USER_STATS_MODIFICATION_FLAG_ITEM_ID_SPECIES:
        modifications['item_id_species'] = user_stats.item_id_species
    
    if modification_flags & USER_STATS_MODIFICATION_FLAG_ITEM_ID_WEAPON:
        modifications['item_id_weapon'] = user_stats.item_id_weapon
    
    if modification_flags & USER_STATS_MODIFICATION_FLAG_RECOVERY_UNTIL:
        modifications['recovering_until'] = user_stats.recovering_until
    
    if modification_flags & USER_STATS_MODIFICATION_FLAG_RECOVERY_UNTIL_NOTIFICATION_AT:
        modifications['recovering_until_notification_at'] = user_stats.recovering_until_notification_at
    
    if modification_flags & USER_STATS_MODIFICATION_FLAG_STAT_BEDROOM:
        modifications['stat_bedroom'] = user_stats.stat_bedroom
    
    if modification_flags & USER_STATS_MODIFICATION_FLAG_STAT_CHARM:
        modifications['stat_charm'] = user_stats.stat_charm
    
    if modification_flags & USER_STATS_MODIFICATION_FLAG_STAT_CUTENESS:
        modifications['stat_cuteness'] = user_stats.stat_cuteness
    
    if modification_flags & USER_STATS_MODIFICATION_FLAG_STAT_HOUSEWIFE:
        modifications['stat_housewife'] = user_stats.stat_housewife
    
    if modification_flags & USER_STATS_MODIFICATION_FLAG_STAT_LOYALTY:
        modifications['stat_loyalty'] = user_stats.stat_loyalty
    
    return modifications
