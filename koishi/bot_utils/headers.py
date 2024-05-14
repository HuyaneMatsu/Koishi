__all__ = ('get_header_for',)

from random import random

import config

# https://patorjk.com/software/taag/#p=display&h=2&f=Doom&t=


HEADER_KOISHI = (
    '```\n'
    ' _   __      _     _     _ \n'
    '| | / /     (_)   | |   (_)\n'
    '| |/ /  ___  _ ___| |__  _ \n'
    '|    \ / _ \| / __| \'_ \| |\n'
    '| |\  \ (_) | \__ \ | | | |\n'
    '\_| \_/\___/|_|___/_| |_|_|\n'
    '```'
)


HEADER_FLANDRE = (
    '```\n'
    '______ _                 _          \n'
    '|  ___| |               | |         \n'
    '| |_  | | __ _ _ __   __| |_ __ ___ \n'
    '|  _| | |/ _` | \'_ \ / _` | \'__/ _ \\\n'
    '| |   | | (_| | | | | (_| | | |  __/\n'
    '\_|   |_|\__,_|_| |_|\__,_|_|  \___|\n'
    '```'
)

HEADER_YOSHIKA = (
    '```\n'
    '__   __        _     _ _         \n'
    '\ \ / /       | |   (_) |        \n'
    ' \ V /___  ___| |__  _| | ____ _ \n'
    '  \ // _ \/ __| \'_ \| | |/ / _` |\n'
    '  | | (_) \__ \ | | | |   < (_| |\n'
    '  \_/\___/|___/_| |_|_|_|\_\__,_|\n'
    '```'
)

HEADER_CURSED_SAKUYA = (
    '```\n'
    ' _____ _____       _                      \n'
    '/  __ /  ___|     | |                     \n'
    '| /  \\\\ `--.  __ _| | ___   _ _   _  __ _ \n'
    '| |    `--. \\/ _` | |/ | | | | | | |/ _` |\n'
    '| \\__//\\__/ | (_| |   <| |_| | |_| | (_| |\n'
    ' \\____\\____/ \\__,_|_|\\_\\\\__,_|\\__, |\\__,_|\n'
    '                               __/ |      \n'
    '                              |___/       \n'
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

HEADER_KOISHI_EASTER_EGG = (
    '```\n'
    ' _____ __    ___ \n'
    '|  ___/  |  /   |\n'
    '|___ \`| | / /| |\n'
    '    \ \| |/ /_| |\n'
    '/\__/ /| |\___  |\n'
    '\____/\___/   |_/\n'
    '```'
)

HEADER_FLANDRE_EASTER_EGG = (
    '```\n'
    '______          _     _ _             \n'
    '| ___ \        | |   | (_)            \n'
    '| |_/ /   _  __| | __| |_ _ __   __ _ \n'
    '|  __/ | | |/ _` |/ _` | | \'_ \ / _` |\n'
    '| |  | |_| | (_| | (_| | | | | | (_| |\n'
    '\_|   \__,_|\__,_|\__,_|_|_| |_|\__, |\n'
    '                                 __/ |\n'
    '                                |___/ \n'
    '```'
)

HEADER_CURSED_SAKUYA_EASTER_EGG = (
    '```\n'
    ' _____ _____                   \n'
    '/  __ /  ___|                  \n'
    '| /  \\\\ `--. _   _ _   _ _   _ \n'
    '| |    `--. | | | | | | | | | |\n'
    '| \\__//\\__/ | |_| | |_| | |_| |\n'
    ' \\____\\____/ \\__,_|\\__, |\\__,_|\n'
    '                    __/ |      \n'
    '                   |___/\n'
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

HEADERS = {
    config.KOISHI_ID: (HEADER_KOISHI, HEADER_KOISHI_EASTER_EGG),
    config.FLANDRE_ID: (HEADER_FLANDRE, HEADER_FLANDRE_EASTER_EGG),
    config.YOSHIKA_ID: (HEADER_YOSHIKA, HEADER_YOSHIKA),
    config.CURSED_SAKUYA_ID: (HEADER_CURSED_SAKUYA, HEADER_CURSED_SAKUYA_EASTER_EGG),
    config.ORIN_ID: (HEADER_ORIN, HEADER_ORIN_EASTER_EGG),
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
