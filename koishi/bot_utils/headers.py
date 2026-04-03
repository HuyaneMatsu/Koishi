__all__ = ('get_header_for',)

from random import random

import config

# Generate at:
# https://patorjk.com/software/taag/#p=display&h=2&f=Doom&t=
#
# You can check which black-slashes to escape with:
# [^\\]\\[^\\n']


HEADER_ALICE = (
    '```\n'
    '  ___  _ _          \n'
    ' / _ \\| (_)         \n'
    '/ /_\\ \\ |_  ___ ___ \n'
    '|  _  | | |/ __/ _ \\\n'
    '| | | | | | (_|  __/\n'
    '\\_| |_/_|_|\\___\\___|\n'
    '```'
)


HEADER_FLANDRE = (
    '```\n'
    '______ _                 _          \n'
    '|  ___| |               | |         \n'
    '| |_  | | __ _ _ __   __| |_ __ ___ \n'
    '|  _| | |/ _` | \'_ \\ / _` | \'__/ _ \\\n'
    '| |   | | (_| | | | | (_| | | |  __/\n'
    '\\_|   |_|\\__,_|_| |_|\\__,_|_|  \\___|\n'
    '```'
)

HEADER_KOISHI = (
    '```\n'
    ' _   __      _     _     _ \n'
    '| | / /     (_)   | |   (_)\n'
    '| |/ /  ___  _ ___| |__  _ \n'
    '|    \\ / _ \\| / __| \'_ \\| |\n'
    '| |\\  \\ (_) | \\__ \\ | | | |\n'
    '\\_| \\_/\\___/|_|___/_| |_|_|\n'
    '```'
)

HEADER_NUE = (
    '```\n'
    ' _   _            \n'
    '| \\ | |           \n'
    '|  \\| |_   _  ___ \n'
    '| . ` | | | |/ _ \\\n'
    '| |\\  | |_| |  __/\n'
    '\\_| \\_/\\__,_|\\___|\n'
    '```'
)

HEADER_ORIN = (
    '```\n'
    ' ___________ _____ _   _ \n'
    '|  _  | ___ \\_   _| \\ | |\n'
    '| | | | |_/ / | | |  \\| |\n'
    '| | | |    /  | | | . ` |\n'
    '\\ \\_/ / |\\ \\ _| |_| |\\  |\n'
    ' \\___/\\_| \\_|\\___/\\_| \\_/\n'
    '```'
)

HEADER_TOY_KOISHI = (
    '```\n'
    ' _____           _   __      _     _     _ \n'
    '|_   _|         | | / /     (_)   | |   (_)\n'
    '  | | ___  _   _| |/ /  ___  _ ___| |__  _ \n'
    '  | |/ _ \\| | | |    \\ / _ \\| / __| \'_ \\| |\n'
    '  | | (_) | |_| | |\\  \\ (_) | \\__ \\ | | | |\n'
    '  \\_/\\___/ \\__, \\_| \\_/\\___/|_|___/_| |_|_|\n'
    '            __/ |                          \n'
    '           |___/                           \n'
    '```'
)

HEADER_YOSHIKA = (
    '```\n'
    '__   __        _     _ _         \n'
    '\\ \\ / /       | |   (_) |        \n'
    ' \\ V /___  ___| |__  _| | ____ _ \n'
    '  \\ // _ \\/ __| \'_ \\| | |/ / _` |\n'
    '  | | (_) \\__ \\ | | | |   < (_| |\n'
    '  \\_/\\___/|___/_| |_|_|_|\\_\\__,_|\n'
    '```'
)




HEADER_ALICE_EASTER_EGG = (
    '```\n'
    '  ___       _           \n'
    ' / _ \\     (_)          \n'
    '/ /_\\ \\_ __ _ ___ _   _ \n'
    '|  _  | \'__| / __| | | |\n'
    '| | | | |  | \\__ \\ |_| |\n'
    '\\_| |_/_|  |_|___/\\__,_|\n'
    '```'
)

HEADER_FLANDRE_EASTER_EGG = (
    '```\n'
    '______          _     _ _             \n'
    '| ___ \\        | |   | (_)            \n'
    '| |_/ /   _  __| | __| |_ _ __   __ _ \n'
    '|  __/ | | |/ _` |/ _` | | \'_ \\ / _` |\n'
    '| |  | |_| | (_| | (_| | | | | | (_| |\n'
    '\\_|   \\__,_|\\__,_|\\__,_|_|_| |_|\\__, |\n'
    '                                 __/ |\n'
    '                                |___/ \n'
    '```'
)

HEADER_KOISHI_EASTER_EGG = (
    '```\n'
    ' _____ __    ___ \n'
    '|  ___/  |  /   |\n'
    '|___ \\`| | / /| |\n'
    '    \\ \\| |/ /_| |\n'
    '/\\__/ /| |\\___  |\n'
    '\\____/\\___/   |_/\n'
    '```'
)

HEADER_NUE_EASTER_EGG = (
    '```\n'
    ' _   _       _                              \n'
    '| | | |     | |                             \n'
    '| | | |_ __ | | ___ __   _____      ___ __  \n'
    '| | | | \'_ \\| |/ / \'_ \\ / _ \\ \\ /\\ / / \'_ \\ \n'
    '| |_| | | | |   <| | | | (_) \\ V  V /| | | |\n'
    ' \\___/|_| |_|_|\\_\\_| |_|\\___/ \\_/\\_/ |_| |_|\n'
    '```'
)

HEADER_ORIN_EASTER_EGG = (
    '```\n'
    ' ___________ _   _ \n'
    '|  _  | ___ \\ \\ | |\n'
    '| | | | |_/ /  \\| |\n'
    '| | | |    /| . ` |\n'
    '\\ \\_/ / |\\ \\| |\\  |\n'
    ' \\___/\\_| \\_\\_| \\_/\n'
    '```'
)

HEADER_TOY_KOISHI_EASTER_EGG = (
    '```\n'
    ' _____ _   __ ___                      _ _   \n'
    '|_   _| | / // _ \\                    | | |  \n'
    '  | | | |/ // /_\\ \\___ ___  __ _ _   _| | |_ \n'
    '  | | |    \\|  _  / __/ __|/ _` | | | | | __|\n'
    '  | | | |\\  \\ | | \\__ \\__ \\ (_| | |_| | | |_ \n'
    '  \\_/ \\_| \\_|_| |_/___/___/\\__,_|\\__,_|_|\\__|\n'
    '```'
)


HEADER_YOSHIKA_EASTER_EGG = HEADER_YOSHIKA


HEADERS = {
    config.ALICE_ID : (HEADER_ALICE, HEADER_ALICE_EASTER_EGG),
    config.FLANDRE_ID : (HEADER_FLANDRE, HEADER_FLANDRE_EASTER_EGG),
    config.KOISHI_ID : (HEADER_KOISHI, HEADER_KOISHI_EASTER_EGG),
    config.NUE_ID : (HEADER_NUE, HEADER_NUE_EASTER_EGG),
    config.ORIN_ID : (HEADER_ORIN, HEADER_ORIN_EASTER_EGG),
    config.TOY_KOISHI_ID : (HEADER_TOY_KOISHI, HEADER_TOY_KOISHI_EASTER_EGG),
    config.YOSHIKA_ID : (HEADER_YOSHIKA, HEADER_YOSHIKA_EASTER_EGG),
}

HEADER_DEFAULT = HEADER_KOISHI


def get_header_for(client):
    """
    Gets the header for the given client.
    
    Parameters
    ----------
    client : ``Client``
        Client to get the header for.
    
    Returns
    -------
    header : `str`
    """
    header_choices = HEADERS.get(client.id, None)
    if header_choices is None:
        header = HEADER_DEFAULT
    else:
        header = header_choices[random() <= 0.01]
    
    return header
