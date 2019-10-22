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

#### Voice requirements
- `ffmpeg.exe`
- `youtube_dl` (from youtube)

#### Koishi requirements
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
- [PIL](https://pypi.org/project/PIL/)

