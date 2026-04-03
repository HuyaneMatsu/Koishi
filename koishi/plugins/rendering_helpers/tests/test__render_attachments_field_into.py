import vampytest
from hata import Attachment

from ..field_renderers import render_attachments_field_into


def _iter_options():
    attachment_id_0 = 202401310010
    url_0 = 'https://orindance.party/'
    name_0 = 'hey.png'
    
    attachment_id_1 = 202401310011
    url_1 = url_0 + '?kek'
    name_1 = 'mister.png'
    
    attachment_0 = Attachment.precreate(
        attachment_id_0,
        url = url_0,
        name = name_0,
    )
    attachment_1 = Attachment.precreate(
        attachment_id_1,
        url = url_1,
        name = name_1,
    )
    
    yield (
        False, None, False, 'Attachments',
        ('Attachments: *none*', True),
    )
    
    yield (
        True, None, False, 'Attachments',
        ('\nAttachments: *none*', True),
    )
    
    yield (
        False, (attachment_0,), False, 'Attachments',
        (f'Attachments:\n- [{name_0!s}]({url_0!s})', True),
    )
    
    yield (
        True, (attachment_0,), False, 'Attachments',
        (f'\nAttachments:\n- [{name_0!s}]({url_0!s})', True),
    )

    yield (
        False, None, True, 'Attachments',
        ('', False),
    )
    
    yield (
        True, None, True, 'Attachments',
        ('', True),
    )
    
    yield (
        False, (attachment_0,), True, 'Attachments',
        (f'Attachments:\n- [{name_0!s}]({url_0!s})', True),
    )
    
    yield (
        True, (attachment_0,), True, 'Attachments',
        (f'\nAttachments:\n- [{name_0!s}]({url_0!s})', True),
    )
    
    # Multiple attachments
    yield (
        False, (attachment_0, attachment_1), True, 'Attachments',
        (f'Attachments:\n- [{name_0!s}]({url_0!s})\n- [{name_1!s}]({url_0!s})', True),
    )
    
    # Different name.
    yield (
        False, None, False, 'Koishis',
        ('Koishis: *none*', True),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_attachments_field_into(field_added, attachments, optional, title):
    """
    Tests whether ``render_attachments_field_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether any fields were added already.
    attachments : ``None | tuple<Attachment>``
        The attachments to render.
    optional : `bool` = `True`
        Whether should not render if `attachments` is `None`.
    title : `str`
        The title of the line.
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    into, field_added = render_attachments_field_into([], field_added, attachments, optional = optional, title = title)
    
    vampytest.assert_instance(into, list)
    
    for element in into:
        vampytest.assert_instance(element, str)
    
    vampytest.assert_instance(field_added, bool)
    
    output = ''.join(into)
    return output, field_added
