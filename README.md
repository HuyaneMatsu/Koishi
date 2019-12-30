# Koishi
Test client for hata


#### `pers_data.py`
```python
KOISHI_TOKEN    = #bot token (str)
KOISHI_ID       = #bot id (int), can be 0
KOISHI_SECRET   = #client_secret (str) for oauth2, can be None.
KOISHI_PREFIX   = 'k!' #default prefix (str)

SATORI_TOKEN    = #bot token (str) for second bot
SATORI_ID       = #bot id (int) for second bot, can be 0
SATORI_PREFIX   = '&' #default prefix (str)

FLAN_TOKEN      = #bot token (str) for third bot
FLAN_ID         = #bot id (int) for third bot, can be 0
FLAN_PREFIX     = '\\' #default prefix (str)

AUDIO_PATH      = #path for local audio files
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

