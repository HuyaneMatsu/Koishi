__all__ = ()

from ...bot_utils.constants import COLOR__GAMBLING, ROLE__SUPPORT__ELEVATED

from hata import Embed


def build_failure_embed_gift_requirements_unsatisfied():
    """
    Builds a failure embed for the case when gifting requirements are not satisfied.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Cannot gift to user',
        (
            f'You must be either related the targeted user, '
            f'or have {ROLE__SUPPORT__ELEVATED.name} role in my support guild to target anyone.'
        ),
        color = COLOR__GAMBLING,
    )
