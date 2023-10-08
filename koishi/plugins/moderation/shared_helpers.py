__all__ = ()

from hata.ext.slash import abort


def process_reason(reason):
    """
    Validates the raw reason given.
    
    Parameters
    ----------
    reason : `None`, `str`
        The reason to validate.
    
    Returns
    -------
    reason : `None`, `str`
    """
    if (reason is None):
        pass
    
    elif (not reason):
        reason = None
    
    elif len(reason) > 400:
        reason = reason[:400] + ' ...'
    
    return reason


def create_auto_reason(event, reason):
    """
    Auto creates action reason if not given.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interactions event.
    reason : `None`, `str`
        Reason given.
    
    Returns
    -------
    reason : `str`
    """
    reason_parts = []
    if (reason is not None):
        reason_parts.append(reason)
        reason_parts.append('\n')
    
    caller = event.user
    reason_parts.append('Requested by: ')
    reason_parts.append(caller.full_name)
    reason_parts.append(' [')
    reason_parts.append(str(caller.id))
    reason_parts.append(']')
    
    return ''.join(reason_parts)


def add_reason_field(embed, reason):
    """
    Adds the reason field to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to add the field to.
    
    reason : `None`, `str`
        Action reason.
    """
    if reason is None:
        reason = ' '
    
    return add_standalone_field(embed, 'Reason', reason)


def add_standalone_field(embed, name, value):
    """
    Adds a standalone field to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to add the field to.
    name : `str`
        The field's name.
    value : `str`
        The field's value.
    """
    embed.add_field(
        name,
        (
            f'```\n'
            f'{value}\n'
            f'```'
        ),
        inline = True
    )


def check_user_cannot_be_admin(guild, user, word_config):
    """
    Checks whether the target user is not administrator.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild where the action would be executed.
    user : ``ClientUserBase``
        The user in context.
    word_config : ``WordConfig``
        Words to use for filling up the error messages about the action to be executed.
    """
    if guild.permissions_for(user).can_administrator:
        abort(f'Cannot {word_config.name} admins.')
