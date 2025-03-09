__all__ = (
    'iter_build_attachment_message_attachments', 'iter_build_attachment_message_content',
    'iter_build_attachment_message_mentions', 'iter_build_attachment_voters',
)

from itertools import islice

from scarletio.streaming import ZipStreamFile, create_zip_stream_resource

from ...bot_utils.response_data_streaming import create_http_stream_resource

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


def _get_uploadable_attachment_count(guild, attachments):
    """
    Gets how much attachments are uploadable.
    
    Parameters
    ----------
    guild : `None | Guild`
        The respective guild where the message will be sent.
    
    attachments : `tuple<Attachment>`
        Attachments to determine count from.
    
    Returns
    -------
    uploadable_attachment_count : `int`
    """
    if guild is None:
        upload_limit = 8 * (1 << 20)
    else:
        upload_limit = guild.upload_limit
    
    # Reduce the allowed upload limit by 20 kb, so we do not hit the limit with all the attachments
    upload_limit -= 20 * (1 << 10)
    
    uploadable_attachment_count = 0
    
    for attachment in attachments:
        upload_limit -= attachment.size
        uploadable_attachment_count += (upload_limit >= 0)
    
    return uploadable_attachment_count


def _build_attachment_attachments(http, attachments, uploadable_attachment_count):
    """
    Builds an attachment that zips the attachments of the file.
    
    Parameters
    ----------
    http : ``HTTPClient``
        Http client to use.
    
    attachments : `tuple<Attachment>`
        Attachments to stream from.
    
    uploadable_attachment_count : `bool`
        The amount of attachments that can be uploaded.
    
    Returns
    -------
    attachment : `(str, ResourceStream)`
    """
    return (
        'attachments.zip',
        create_zip_stream_resource([
            ZipStreamFile(
                attachment.display_name,
                create_http_stream_resource(http, attachment.url),
                modified_at = attachment.content_created_at,
            )
            for attachment in islice(attachments, 0, uploadable_attachment_count)
        ]),
    )


def _build_attachment_truncated_attachments(attachments, uploadable_attachment_count):
    """
    Builds an attachments that lists the truncated attachments.
    
    Parameters
    ----------
    attachments : `tuple<Attachment>`
        Attachments to stream from.
    
    uploadable_attachment_count : `bool`
        The amount of attachments that can be uploaded.
    
    Returns
    -------
    attachment : `(str, str)`
    """
    into = ['Attachments truncated from zip due to lack of upload limit:']
    
    for attachment in islice(attachments, uploadable_attachment_count, len(attachments)):
        into.append('\n- ')
        into.append(attachment.display_name)
        into.append(' | size = ')
        into.append(repr(attachment.size))
        into.append(' bytes')
    
    return ('attachments_truncated.txt', ''.join(into))


def iter_build_attachment_message_attachments(http, message):
    """
    Parameters
    ----------
    http : ``HTTPClient``
        Http client to use.
    
    message : ``Message``
        Message to build mentions attachment attachments for.
    
    Returns
    -------
    attachment : `(str, ResourceStream | str)`
    """
    attachments = message.attachments
    if (attachments is None):
        return
    
    uploadable_attachment_count = _get_uploadable_attachment_count(message.guild, attachments)
    if uploadable_attachment_count:
        yield _build_attachment_attachments(http, attachments, uploadable_attachment_count)
    
    if (uploadable_attachment_count != len(attachments)):
        yield _build_attachment_truncated_attachments(attachments, uploadable_attachment_count)
