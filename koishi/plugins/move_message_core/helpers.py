__all__ = ()

from hata import DATETIME_FORMAT_CODE, WebhookBase

from .constants import DATE_CONNECTOR, NAME_LENGTH_MAX, NAME_WITH_DATE_RP


def _get_user_name(message):
    """
    Gets the message's author's name.
    
    Parameters
    ----------
    message : ``Message``
        The respective message.
    
    Returns
    -------
    name : `str`
    """
    user = message.author
    name = user.name_at(message.guild_id)
    
    if isinstance(user, WebhookBase) and (NAME_WITH_DATE_RP.fullmatch(name) is not None):
        return name
    
    if len(name) > NAME_LENGTH_MAX:
        name = name[: NAME_LENGTH_MAX - len(' ...')] + ' ...'
    
    return f'{name}{DATE_CONNECTOR}{message.created_at:{DATETIME_FORMAT_CODE}}'
