__all__ = ('check_can_gift',)

from hata.ext.slash import abort

from .embed_builders import build_failure_embed_gift_requirements_unsatisfied
from .utils import can_gift


def check_can_gift(source_user, relationship):
    """
    Checks whether the targeted user can be gifted.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who is gifting.
    
    relationship : `None | Relationship`
        The relationship connecting the two users (can be extend).
    
    Raises
    ------
    InteractionAbortedError
    """
    if can_gift(source_user, relationship):
        return
    
    abort(
        embed = build_failure_embed_gift_requirements_unsatisfied(),
    )
