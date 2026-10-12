import os
import re
from pyrogram import filters

# Explicit Credentials & Defaults
API_ID = int(os.getenv("API_ID", "35744976"))
API_HASH = os.getenv("API_HASH", "459c0a59bdca46c1069916ef20ce70c9")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8633245391:AAGVjsbGqZdCt4i7oWvBeXye-QWermZAx2k")

MONGO_DB_URI = os.getenv(
    "MONGO_DB_URI",
    "mongodb://mongo:BcqbVegOGzBWzNLXfDWtvSsEiFIMRLNK@mongodb.railway.internal:27017"
)
MONGO_URL = MONGO_DB_URI

DURATION_LIMIT_MIN = int(os.getenv("DURATION_LIMIT", 60))
SONG_DOWNLOAD_DURATION = int(os.getenv("SONG_DOWNLOAD_DURATION_LIMIT", 180))
OWNER_ID = int(os.getenv("OWNER_ID", "7885190981"))
LOGGER_ID = int(os.getenv("LOGGER_ID", "-1002925549087"))

UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "https://github.com/AnonymousX1025/AnonXMusic")
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "master")
GIT_TOKEN = os.getenv("GIT_TOKEN", None)
SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL", "https://t.me/itz_rohit_rss")
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT", "https://t.me/THW_WORLD")

AUTO_LEAVING_ASSISTANT = bool(os.getenv("AUTO_LEAVING_ASSISTANT", False))
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", None)
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", None)
PLAYLIST_FETCH_LIMIT = int(os.getenv("PLAYLIST_FETCH_LIMIT", 25))

TG_AUDIO_FILESIZE_LIMIT = int(os.getenv("TG_AUDIO_FILESIZE_LIMIT", 104857600))
TG_VIDEO_FILESIZE_LIMIT = int(os.getenv("TG_VIDEO_FILESIZE_LIMIT", 1073741824))

RAW_SESSION = (
    "BTV0SXYAqoprWbOtA6IU2A_MgiUVGhB1axA3MYdnpRD1ZiTFuyKesUhif2LD8fpgqS4xLkv0"
    "lD81IhgiT9WTbbzU6-Klcp9KIUvToMrAiMxNBIsc4sdIbYFOYeUadtqRprxd5-qz0jvzN-L7"
    "GtrIa4CyAmnn3IpmbENsoAf9sgNl_jcOHDhrU6HiEqaysqnI4j6fE6O-RxMewDUqV9JzaM_6"
    "XJUN0X9Qg7dqpQn7bMt_336rU5eWybuwyP6IS_bbY7qhGSFh6m1uHOLIp2qYkPphA1hHhA7"
    "krhLGsqmDubkcVCnNL8RVe9KJju8rha1_EMC-HpA3Ur6ovZgT5mJcYcrvUfAspQAAAAHkw3WaAA"
)

ACTIVE_SESSION = (
    os.getenv("SESSION1")
    or os.getenv("STRING_SESSION")
    or os.getenv("STRING1")
    or RAW_SESSION
)
ACTIVE_SESSION = ACTIVE_SESSION.strip('"').strip("'")

os.environ["SESSION1"] = ACTIVE_SESSION
os.environ["STRING_SESSION"] = ACTIVE_SESSION
os.environ["STRING1"] = ACTIVE_SESSION

STRING1 = ACTIVE_SESSION
SESSION1 = ACTIVE_SESSION
STRING_SESSION = ACTIVE_SESSION

STRING2 = os.getenv("STRING_SESSION2", None) or os.getenv("STRING2", None)
STRING3 = os.getenv("STRING_SESSION3", None) or os.getenv("STRING3", None)
STRING4 = os.getenv("STRING_SESSION4", None) or os.getenv("STRING4", None)
STRING5 = os.getenv("STRING_SESSION5", None) or os.getenv("STRING5", None)

COOKIES_URL = os.getenv("COOKIES_URL", "https://batbin.me/raw/warms")

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

START_IMG_URL = os.getenv("START_IMG_URL", "https://te.legra.ph/file/20641be20772719a7e289.jpg")
PING_IMG_URL = os.getenv("PING_IMG_URL", "https://te.legra.ph/file/20641be20772719a7e289.jpg")
PLAYLIST_IMG_URL = "https://te.legra.ph/file/20641be20772719a7e289.jpg"
STATS_IMG_URL = "https://te.legra.ph/file/20641be20772719a7e289.jpg"
TELEGRAM_AUDIO_URL = "https://te.legra.ph/file/20641be20772719a7e289.jpg"
TELEGRAM_VIDEO_URL = "https://te.legra.ph/file/20641be20772719a7e289.jpg"
STREAM_IMG_URL = "https://te.legra.ph/file/20641be20772719a7e289.jpg"
SOUNCLOUD_IMG_URL = "https://te.legra.ph/file/20641be20772719a7e289.jpg"
YOUTUBE_IMG_URL = "https://te.legra.ph/file/20641be20772719a7e289.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://te.legra.ph/file/20641be20772719a7e289.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://te.legra.ph/file/20641be20772719a7e289.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://te.legra.ph/file/20641be20772719a7e289.jpg"


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))


class Config:
    API_ID = API_ID
    API_HASH = API_HASH
    BOT_TOKEN = BOT_TOKEN
    MONGO_DB_URI = MONGO_DB_URI
    MONGO_URL = MONGO_URL
    DURATION_LIMIT_MIN = DURATION_LIMIT_MIN
    SONG_DOWNLOAD_DURATION = SONG_DOWNLOAD_DURATION
    OWNER_ID = OWNER_ID
    LOGGER_ID = LOGGER_ID
    UPSTREAM_REPO = UPSTREAM_REPO
    UPSTREAM_BRANCH = UPSTREAM_BRANCH
    GIT_TOKEN = GIT_TOKEN
    SUPPORT_CHANNEL = SUPPORT_CHANNEL
    SUPPORT_CHAT = SUPPORT_CHAT
    AUTO_LEAVING_ASSISTANT = AUTO_LEAVING_ASSISTANT
    SPOTIFY_CLIENT_ID = SPOTIFY_CLIENT_ID
    SPOTIFY_CLIENT_SECRET = SPOTIFY_CLIENT_SECRET
    PLAYLIST_FETCH_LIMIT = PLAYLIST_FETCH_LIMIT
    TG_AUDIO_FILESIZE_LIMIT = TG_AUDIO_FILESIZE_LIMIT
    TG_VIDEO_FILESIZE_LIMIT = TG_VIDEO_FILESIZE_LIMIT
    STRING1 = STRING1
    STRING2 = STRING2
    STRING3 = STRING3
    STRING4 = STRING4
    STRING5 = STRING5
    SESSION1 = SESSION1
    STRING_SESSION = STRING_SESSION
    COOKIES_URL = COOKIES_URL
    START_IMG_URL = START_IMG_URL
    PING_IMG_URL = PING_IMG_URL
    DURATION_LIMIT = DURATION_LIMIT

    @staticmethod
    def check():
        return True


def check():
    return True
