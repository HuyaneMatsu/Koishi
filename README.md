# Koishi
The most awesome bot built with Hata no Kokoro's Discord API wrapper.

When setupping Koishi, create an importable file, called `config.py`, what's structure should be the following:
```python
MARISA_MODE = True              # (bool) Whether Marisa or the other clients should run up.

KOISHI_TOKEN = ''               # bot token. (str)
KOISHI_ID = 0                   # bot id (int), can be 0.
KOISHI_SECRET = None            # client_secret (str) for oauth2, can be None.
KOISHI_PREFIX = 'k!'            # default prefix. (str)

SATORI_TOKEN = ''               # bot token (str) for second bot.
SATORI_ID = 0                   # bot id (int) for second bot, can be 0.
SATORI_SECRET = None            # client_secret (str) for oauth2, can be None.
SATORI_PREFIX = '&'             # default prefix (str)

FLAN_TOKEN = ''                 # bot token (str) for third bot.
FLAN_ID = 0                     # bot id (int) for third bot, can be 0.
FLAN_PREFIX = '/'               # default prefix. (str)

MARISA_TOKEN = ''               # bot token (str) for third bot.
MARISA_ID = 0                   # bot id (int) for 4th bot, can be 0.
MARISA_PREFIX  = '$'            # default prefix (str)

AUDIO_PLAY_POSSIBLE = False     # Whether FFmpeg and other voice requirement as satisfied
AUDIO_PATH = None               # path for local audio files, can be None
HATA_PATH = None                # path to Hata if Any (str or None)
KOISHI_PATH = None              # path to Koishi if specific. (str or None)

DATABASE_NAME = None            # The database's name to connect to. (str)

ALLOW_KOISHI_SNEKBOX = False    # (bool) Whether Koishi can use snekbox module.
ALLOW_MARISA_SNEKBOX = True     # (bool) Whether Marisa can load the snekbox module.

RUN_WEBAPP_AS_MAIN = True       # (bool) Whether web app should be started if manage.py is the local file.
                                # Have this as `False` if not self-hosting.
WEBAPP_SECRET_KEY = None        # (str) Secret key for webapp.
```

#### Koishi requirements
- [hata](https://pypi.org/project/hata/)
- [lxml](https://pypi.org/project/lxml/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
- [PIL](https://pypi.org/project/PIL/)

#### Hata requirements
- [chardet](https://pypi.python.org/pypi/chardet)
- [dateutil](https://pypi.org/project/python-dateutil/)

#### Voice requirements
- `ffmpeg.exe`
- [PyNaCl](https://pypi.org/project/PyNaCl/)
- [youtube_dl](https://pypi.org/project/youtube_dl/)

#### Web requirements
- [Flask](https://pypi.org/project/Flask/)

#### More requirements
- [psutil](https://pypi.org/project/psutil/)
- [nsjail](https://github.com/google/nsjail)

