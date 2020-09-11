# Koishi
The most awesome bot built with Hata no Kokoro's Discord API wrapper.

When setupping Koishi, create an importable file, called `config.py`, what's structure should be the following:
```python
KOISHI_TOKEN = ''    # bot token (str)
KOISHI_ID = 0     # bot id (int), can be 0
KOISHI_SECRET = None  # client_secret (str) for oauth2, can be None.
KOISHI_PREFIX = 'k!'  # default prefix (str)

SATORI_TOKEN = ''    # bot token (str) for second bot
SATORI_ID = 0     # bot id (int) for second bot, can be 0
SATORI_SECRET = None  # client_secret (str) for oauth2, can be None.
SATORI_PREFIX = '&'   # default prefix (str)

FLAN_TOKEN = ''    # bot token (str) for third bot
FLAN_ID = 0     # bot id (int) for third bot, can be 0
FLAN_PREFIX = '\\'  # default prefix (str)

MARISA_TOKEN = ''    # bot token (str) for third bot
MARISA_ID = 0     # bot id (int) for 4th bot, can be 0
MARISA_PREFIX  = '*'   # default prefix (str)

AUDIO_PLAY_POSSIBLE = False # Whether FFmpeg and other voice requirement as satisfied
AUDIO_PATH = None  # path for local audio files, can be None
HATA_PATH = None  # path to hata if Any (str or None)

DATABASE_NAME = None    # The database's name to connect to (str)

ALLOW_KOISHI_SNEKBOX = False # (bool) Whether Koishi can use snekbox module
ALLOW_MARISA_SNEKBOX = True # (bool) Whether Marisa can load the snekbox module
```

#### Hata requirements
- [chardet](https://pypi.python.org/pypi/chardet)
- [dateutil](https://pypi.org/project/python-dateutil/)

#### Koishi requirements
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
- [PIL](https://pypi.org/project/PIL/)

#### Voice requirements
- `ffmpeg.exe`
- [PyNaCl](https://pypi.org/project/PyNaCl/) (for voice support)
- `youtube_dl` (from youtube)

#### More requirements
 - [psutil](https://pypi.org/project/psutil/)
