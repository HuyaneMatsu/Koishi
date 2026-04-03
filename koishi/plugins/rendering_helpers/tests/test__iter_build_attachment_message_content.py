import vampytest
from hata import Message

from ..attachment_builders import iter_build_attachment_message_content


def test__iter_build_attachment_message_content__no_content():
    """
    tests whether ``iter_build_attachment_message_content`` works as intended.
    
    Case: No content.
    """
    content = None
    message_id = 202401310006
    
    message = Message.precreate(
        message_id,
        content = content,
    )
    
    output = [*iter_build_attachment_message_content(message)]
    vampytest.assert_eq(len(output), 0)


def test__iter_build_attachment_message_content__with_content():
    """
    tests whether ``iter_build_attachment_message_content`` works as intended.
    
    Case: With content.
    """
    content = 'hey mister'
    message_id = 202401310007
    
    message = Message.precreate(
        message_id,
        content = content,
    )
    
    output = [*iter_build_attachment_message_content(message)]
    vampytest.assert_eq(len(output), 1)
    
    vampytest.assert_eq(
        output[0],
        (
            'content.txt',
            f'### Content\n\n{content!s}\n',
        ),
    )
