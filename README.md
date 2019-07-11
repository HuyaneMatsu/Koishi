# Koishi
Test client for hata


#### `pers_data.py`
```python
KOISHI_TOKEN    = #bot token (str)
KOISHI_ID       = #bot id (int), can be 0
KOISHI_SECRET   = #client_secret (str) for oauth2, can be None.
PREFIX          = 'k!' #default prefix (str)

MOKOU_TOKEN     = #bot token (str) for second bot
MOKOU_ID        = #bot id (int) for second bot, can be 0

ELPHELT_TOKEN   = #bot token (str) for third bot
ELPHELT_ID      = #bot id (int) for third bot, can be 0
```

#### Voice requirements
- `ffmpeg.exe`
- `youtube_dl` (from youtube)

#### Koishi requirements
- BeautifulSoup
- sqlalchemy
- PIL

