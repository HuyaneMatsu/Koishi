__all__ = ()

from collections import namedtuple as NamedTuple

from hata import ButtonStyle, Emoji, create_button


EMOJI_KOISHI = Emoji.precreate(704393708467912875)
EMOJI_SATORI = Emoji.precreate(812069466069663765)

EMOJI_NOTHING = Emoji.precreate(568838460434284574)

ARRAY_IDENTIFIER_EMPTY = 0
ARRAY_IDENTIFIER_P1 = 1
ARRAY_IDENTIFIER_P2 = 2

GAME_STATE_NONE = 0
GAME_STATE_DRAW = 1
GAME_STATE_P1_WIN = 2
GAME_STATE_P2_WIN = 3

CUSTOM_ID_MAP = {str(index): index for index in range(9)}
CUSTOM_ID_CHALLENGE = 'xox.challenge'

BUTTON_CHALLENGE_ENABLED = create_button(
    label = 'Challenge!',
    custom_id = CUSTOM_ID_CHALLENGE,
)

BUTTON_CHALLENGE_DISABLED = BUTTON_CHALLENGE_ENABLED.copy_with(enabled = False)


LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


def generate_crosses():
    """
    Generates cross indexes, like:
    
    O O -
    - - -
    - O O
    
    Used to setup traps.
    
    Returns
    -------
    crosses : `tuple` of `tuple` (`int`, `int`, `int`, `int`)
    """
    edge_pairs = (
        (0, 8),
        (1, 7),
        (2, 6),
        (3, 5),
        (5, 3),
        (6, 2),
        (7, 1),
        (8, 0),
    )
    combinations = []
    for index_1, index_3 in edge_pairs:
        for index_2, index_4 in edge_pairs:
            if (index_1 == index_2) or (index_1 == index_4):
                continue
            
            combinations.append((index_1, index_2, index_3, index_4))
    
    return tuple(combinations)

CROSSES = generate_crosses()

Y_PATTERN = (
    (0, 8, (1, 2, 3, 5, 6, 7)),
    (2, 6, (0, 1, 3, 5, 7, 8)),
)

Y_PATTERN_CHOOSE_FROM = (1, 3, 5, 7)

MIDDLE = 4
CORNERS = (0, 2, 6, 8)
CORNERS_TO_EDGES = {
    0: (1, 3),
    2: (1, 5),
    6: (3, 7),
    8: (5, 7),
}


PlayerSettings = NamedTuple('PlayerSettings', ('emoji', 'style', 'identifier'))

PLAYER_SETTINGS_KOISHI = PlayerSettings(
    EMOJI_KOISHI,
    ButtonStyle.green,
    ARRAY_IDENTIFIER_P1,
)

PLAYER_SETTINGS_SATORI = PlayerSettings(
    EMOJI_SATORI,
    ButtonStyle.red,
    ARRAY_IDENTIFIER_P2,
)
