__all__ = (
    'iter_build_attachment_message_content', 'iter_build_attachment_message_mentions', 'iter_build_attachment_voters',
)

from .constants import MENTIONED_ROLES_MAX, MENTIONED_USERS_MAX
from .value_renderers import iter_render_listing_into, render_role_into, render_user_into, render_voters_into


def iter_build_attachment_message_content(message):
    """
    Iterates over building content attachment.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    message : ``Message``
        Message to build content attachment for.
    
    yields
    ------
    attachment : `(str, str)`
    """
    content = message.content
    if content is None:
        return
    
    yield (
        'content.txt',
        f'### Content\n\n{content!s}\n',
    )


def iter_build_attachment_message_mentions(message):
    """
    Iterates over building mentions attachment.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    message : ``Message``
        Message to build mentions attachment for.
    
    yields
    ------
    attachment : `(str, str)`
    """
    mentioned_everyone = message.mentioned_everyone
    mentioned_users = message.mentioned_users
    mentioned_roles = message.mentioned_roles
    if (not mentioned_everyone) and (mentioned_users is None) and (mentioned_roles is None):
        return
    
    into = []
    field_added = False
    
    if mentioned_everyone:
        into.append('### Mentioned everyone\n\ntrue\n')
        field_added = True
    
    if (mentioned_roles is not None):
        if field_added:
            into.append('\n')
        else:
            field_added = True
        
        into.append('### Mentioned roles\n\n')
        for role in iter_render_listing_into(into, mentioned_roles, MENTIONED_ROLES_MAX):
            into = render_role_into(into, role)
        
        into.append('\n')
    
    if (mentioned_users is not None):
        if field_added:
            into.append('\n')
        else:
            field_added = True
        
        into.append('### Mentioned users\n\n')
        guild = message.guild
        for user in iter_render_listing_into(into, mentioned_users, MENTIONED_USERS_MAX):
            into = render_user_into(into, user, guild)
        
        into.append('\n')
    
    
    yield ('mentions.txt', ''.join(into))


def iter_build_attachment_voters(down_voters, up_voters, guild):
    """
    Iterates over building voter attachments.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    down_voters : `set<ClientUserBase>`
        Down voters to create attachment for.
    up_voters : `set<ClientUserBase>`
        Up voters to create attachment for.
    guild : `None | Guild`
        The respective guild where the votes were counted at.
    
    Yields
    -------
    attachment : `(str, str)`
    """
    if (not down_voters) and (not up_voters):
        return
    
    into = []
    field_added = False
    
    for title, voters in zip(('Down voters', 'Up voters'), (down_voters, up_voters)):
        if not voters:
            continue
        
        if field_added:
            into.append('\n')
        else:
            field_added = True
        
        into.append('### ')
        into.append(title)
        into.append('\n\n')
        into = render_voters_into(into, voters, guild)
        into.append('\n') # always end files with line break
    
    yield ('voters.txt', ''.join(into))
