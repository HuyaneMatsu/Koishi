import vampytest
from hata.ext.slash import InteractionAbortedError

from ....bot_utils.constants import MAX_WAIFU_SLOTS

from ..checks import check_max_relationship_slots_self


def _iter_options__passing():
    yield MAX_WAIFU_SLOTS - 1


def _iter_options__failing():
    yield MAX_WAIFU_SLOTS
    yield MAX_WAIFU_SLOTS + 1


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_max_relationship_slots_self(relationship_slots):
    """
    Tests whether ``check_max_relationship_slots_self`` works as intended.
    
    Parameters
    ----------
    relationship_slots : `int`
        The amount of relationship slots.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_max_relationship_slots_self(relationship_slots)
