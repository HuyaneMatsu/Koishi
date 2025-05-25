__all__ = ()

from hata import create_button, create_row, ButtonStyle

from .constants import ARRAY_IDENTIFIER_EMPTY, EMOJI_NOTHING


def create_component(array, disabled, player_settings_1, player_settings_2, index):
    """
    Creates a X-O-X component.
    
    Parameters
    ----------
    array : `list<int>`
        The array to render.
    disabled : `bool`
        Whether the component should be rendered as disabled.
    player_settings_1 : ``PlayerSettings``
        Settings of player one.
    player_settings_2 : ``PlayerSettings``
        Settings of player two.
    index : `int`
        The element's index.
    
    Returns
    -------
    component : ``Component``
    """
    element = array[index]
    
    if element == ARRAY_IDENTIFIER_EMPTY:
        emoji = EMOJI_NOTHING
        style = ButtonStyle.blue
    elif element == player_settings_1.identifier:
        emoji = player_settings_1.emoji
        style = player_settings_1.style
    else:
        emoji = player_settings_2.emoji
        style = player_settings_2.style
    
    return create_button(
        emoji = emoji,
        custom_id = str(index),
        style = style,
        enabled = not disabled,
    )


def render_components(array, all_disabled, player_settings_1, player_settings_2):
    """
    Renders the X-O-X component array.
    
    Parameters
    ----------
    array : `list<int>`
        The array to render.
    disabled : `bool`
        Whether all components should be rendered as disabled.
    player_settings_1 : ``PlayerSettings``
        Settings of player one.
    player_settings_2 : ``PlayerSettings``
        Settings of player two.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_row(*(
            create_component(array, all_disabled, player_settings_1, player_settings_2, index)
            for index in range(row_start, row_start + 3)
        ))
        for row_start in range(0, 9, 3)
    ]
