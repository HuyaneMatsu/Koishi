When setting up Koishi, create an importable `config.py` file, whose structure should be the following:

```python
MARISA_MODE = True               # (bool) Whether Marisa or the other clients should run up.


KOISHI_TOKEN = ''                # bot token (str) for the feature client.
KOISHI_ID = 0                    # bot id (int), can be 0.
KOISHI_SECRET = None             # client secret (str) for oauth2, can be None.
KOISHI_PREFIX = 'k!'             # default prefix. (str)
KOISHI_TOP_GG_TOKEN = ''         # top.gg token of the bot.
KOISHI_TOP_GG_AUTHORIZATION = '' # top.gg authorization used for received webhooks.

FLANDRE_TOKEN = ''               # bot token (str) for a secondary feature bot.
FLANDRE_ID = 0                   # bot id (int), can be 0.

YOSHIKA_TOKEN = ''               # bot token (str) for a secondary feature bot.
YOSHIKA_ID = 0                   # bot id (int), can be 0.

TOY_KOISHI_TOKEN = ''            # bot token (str) for a secondary feature bot.
TOY_KOISHI_ID = 0                # bot id (int), can be 0.

ORIN_TOKEN = ''                  # bot token (str) for a secondary feature bot.
ORIN_ID = 0                      # bot id (int), can be 0.


SATORI_TOKEN = ''                # bot token (str) for the system bot.
SATORI_ID = 0                    # bot id (int). can be 0.
SATORI_SECRET = None             # client secret (str) for oauth2, can be None.
SATORI_PREFIX = '&'              # default prefix (str)

MARISA_TOKEN = ''                # bot token (str) for the tetsing bot.
MARISA_ID = 0                    # bot id (int), can be 0.
MARISA_SECRET = None             # client secret (str) for oauth2, can be None.
MARISA_PREFIX  = '$'             # default prefix (str)

NITORI_TOKEN = ''                # bot token (str) for Nitori.
NITORI_ID = 0                    # bot id (int) for Nitori.

RENES_TOKEN = ''                 # bot token (str) for Renes.
RENES_ID = 0                     # bot id (int) for Renes.

SAKUYA_TOKEN = ''                # bot token (str) for Sakuya.
SAKUYA_ID = 0                    # bot id (int) for Sakuya.

ALICE_TOKEN = ''                # bot token (str) for Alice.
ALICE_ID = 0                    # bot id (int) for Alice.


AUDIO_PLAY_POSSIBLE = False      # Whether FFmpeg and other voice requirement as satisfied
AUDIO_PATH = None                # path for local audio files, can be None
HATA_PATH = None                 # path to Hata if Any (str or None)
KOISHI_PATH = None               # path to Koishi if specific. (str or None)
SCARLETIO_PATH = None            # path to Scarletio if Any (str or None)

DATABASE_NAME = None             # The database's name to connect to. (str)

ALLOW_KOISHI_SNEKBOX = False     # (bool) Whether Koishi can use snekbox module.
ALLOW_MARISA_SNEKBOX = True      # (bool) Whether Marisa can load the snekbox module.

RUN_WEBAPP_AS_MAIN = True        # (bool) Whether web app should be started if manage.py is the local file.
                                 # Have this as `False` if not self-hosting.
WEBAPP_SECRET_KEY = None         # (str) Secret key for webapp.

GOOGLE_API_KEYS = None           # (None or list of str) A list of google api keys.
```

#### Koishi requirements
- [hata](https://pypi.org/project/hata/)
- [lxml](https://pypi.org/project/lxml/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [sqlalchemy](https://pypi.org/project/SQLAlchemy/)
- [pillow](https://pypi.org/project/Pillow/)

#### Hata requirements
- [scarletio](https://pypi.org/project/scarletio/)
- [chardet](https://pypi.python.org/pypi/chardet)
- [dateutil](https://pypi.org/project/python-dateutil/)

#### Voice requirements
- `ffmpeg.exe`
- [PyNaCl](https://pypi.org/project/PyNaCl/)
- [youtube_dl](https://pypi.org/project/youtube_dl/)

#### Web requirements
- [Flask](https://pypi.org/project/Flask/)
- [Flask-WTF](https://pypi.org/project/Flask-WTF/)
- [WTForms](https://pypi.org/project/WTForms/)

#### More requirements
- [psutil](https://pypi.org/project/psutil/)
- [nsjail](https://github.com/google/nsjail)
- [gh-md-to-html](https://pypi.org/project/gh-md-to-html/)
- [gh-md-to-html](https://pypi.org/project/gh-md-to-html/)\[offline_conversion\]
