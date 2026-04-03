__all__ = ()

from random import choice

from hata.ext.slash import InteractionResponse, P

from ..bots import FEATURE_CLIENTS


CHOICE_PARAMETER = P(str, 'choice', min_length = 1, max_length = 2000)


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def choose(
    choice_1: CHOICE_PARAMETER,
    choice_2: CHOICE_PARAMETER = None,
    choice_3: CHOICE_PARAMETER = None,
    choice_4: CHOICE_PARAMETER = None,
    choice_5: CHOICE_PARAMETER = None,
    choice_6: CHOICE_PARAMETER = None,
    choice_7: CHOICE_PARAMETER = None,
    choice_8: CHOICE_PARAMETER = None,
    choice_9: CHOICE_PARAMETER = None,
    choice_10: CHOICE_PARAMETER = None,
    choice_11: CHOICE_PARAMETER = None,
    choice_12: CHOICE_PARAMETER = None,
    choice_13: CHOICE_PARAMETER = None,
    choice_14: CHOICE_PARAMETER = None,
    choice_15: CHOICE_PARAMETER = None,
    choice_16: CHOICE_PARAMETER = None,
    choice_17: CHOICE_PARAMETER = None,
    choice_18: CHOICE_PARAMETER = None,
    choice_19: CHOICE_PARAMETER = None,
    choice_20: CHOICE_PARAMETER = None,
    choice_21: CHOICE_PARAMETER = None,
    choice_22: CHOICE_PARAMETER = None,
    choice_23: CHOICE_PARAMETER = None,
    choice_24: CHOICE_PARAMETER = None,
    choice_25: CHOICE_PARAMETER = None,
):
    """
    Choices one off the given options.
    
    This function is a coroutine.
    
    Parameters
    ----------
    choice_{\\d+} : `None | str` = `None`, Optional
        Choice(s) to choose from.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    return InteractionResponse(
        choice([
            choice_ for choice_ in (
                choice_1, choice_2, choice_3, choice_4, choice_5,
                choice_6, choice_7, choice_8, choice_9, choice_10,
                choice_11, choice_12, choice_13, choice_14, choice_15,
                choice_16, choice_17, choice_18, choice_19, choice_20,
                choice_21, choice_22, choice_23, choice_24, choice_25,
            ) if choice_ is not None
        ]),
        allowed_mentions = None,
    )
