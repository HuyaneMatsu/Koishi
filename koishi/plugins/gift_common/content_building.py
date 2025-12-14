__all__ = ('produce_gift_requirements_unsatisfied_error_message',)

from ...bot_utils.constants import ROLE__SUPPORT__ELEVATED


def produce_gift_requirements_unsatisfied_error_message():
    """
    produces gift requirements unsatisfied error message.
    
    This function is an iterable generator.
    
    Yields
    ------
    part : `str`
    """
    yield 'You must be either related the targeted user, or have '
    yield ROLE__SUPPORT__ELEVATED.name
    yield ' role in my support guild to target anyone.'
    
