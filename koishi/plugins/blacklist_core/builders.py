__all__ = ('build_blacklist_user_add_embed', 'build_blacklist_user_entry_embed', 'build_blacklist_user_remove_embed')

from hata import Embed


def build_blacklist_user_add_embed(user, success):
    """
    Builds blacklist user add embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who was just blacklisted.
    success : `bool`
        Whether they were added.
    
    Returns
    -------
    embed : ``Embed``
    """
    user_name = user.full_name
    
    if success:
        description = f'{user_name} has been blacklisted.'
    else:
        description = f'{user_name} is already blacklisted.'
    
    return Embed(
        ('Great success!' if success else 'Nice'),
        description,
    ).add_thumbnail(
        user.avatar_url,
    )


def build_blacklist_user_entry_embed(user, blacklisted):
    """
    Builds blacklist user entry embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who was just blacklisted.
    blacklisted : `bool`
        Whether the user is blacklisted. This is the whole entry.
    
    Returns
    -------
    embed : ``Embed``
    """
    user_name = user.full_name
    
    if blacklisted:
        description = f'{user_name} is blacklisted.'
    else:
        description = f'{user_name} is **NOT YET** blacklisted.'
    
    return Embed(
        ('Nice!' if blacklisted else 'Uoh'),
        description,
    ).add_thumbnail(
        user.avatar_url,
    )


def build_blacklist_user_remove_embed(user, success):
    """
    Builds blacklist user remove embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who was just blacklisted.
    success : `bool`
        Whether they were removed.
    
    Returns
    -------
    embed : ``Embed``
    """
    user_name = user.full_name
    
    if success:
        # This will make me smile one day
        description = f'Why was {user_name} removed from blacklist??'
    else:
        description = f'{user_name} was not blacklisted.'
   
    return Embed(
        ('WHAT!!!??' if success else 'Okay'),
        description,
    ).add_thumbnail(
        user.avatar_url,
    )
