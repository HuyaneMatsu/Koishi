import vampytest
from hata import InteractionEvent, InteractionType, Message, Embed

from ..helpers import get_name_and_page


def _iter_options():
    yield (
        InteractionEvent(
            interaction_type = InteractionType.message_component,
            message = Message()
        ),
        None,
    )
    yield (
        InteractionEvent(
            interaction_type = InteractionType.message_component,
            message = Message(),
        ),
        None,
    )
    yield (
        InteractionEvent(
            interaction_type = InteractionType.message_component,
            message = Message(
                embeds = [
                    Embed(),
                ],
            ),
        ),
        None,
    )
    yield (
        InteractionEvent(
            interaction_type = InteractionType.message_component,
            message = Message(
                embeds = [
                    Embed('Search result for: koishi'),
                ],
            ),
        ),
        None,
    )
    yield (
        InteractionEvent(
            interaction_type = InteractionType.message_component,
            message = Message(
                embeds = [
                    Embed('Search result for: koishi').add_footer('Page: 12'),
                ],
            ),
        ),
        ('koishi', 12),
    )
    yield (
        InteractionEvent(
            interaction_type = InteractionType.message_component,
            message = Message(
                embeds = [
                    Embed('Search result for:').add_footer('Page: 12'),
                ],
            ),
        ),
        ('', 12),
    )
    yield (
        InteractionEvent(
            interaction_type = InteractionType.message_component,
            message = Message(
                embeds = [
                    Embed('Search result for: koishi').add_footer('Page: fifty'),
                ],
            ),
        ),
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_name_and_page(event):
    """
    Asserts whether ``get_name_and_page`` works as intended.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        Interaction event to get name and page from.
    
    Returns
    -------
    name_and_page : `None | (str, int)`
    """
    return get_name_and_page(event)
