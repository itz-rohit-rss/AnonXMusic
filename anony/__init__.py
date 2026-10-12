import os
import sys
import logging
from pyrogram import Client
import pyrogram.session.session

# --- Critical Monkey-Patch for Pyrogram / Python 3.13 String Sessions ---
# Pyrogram invokes Session.write() expecting self.file, which is None for in-memory string sessions.
def _safe_session_write(self):
    if getattr(self, "file", None) is not None:
        try:
            return self.file.write()
        except Exception:
            pass
    return b""

pyrogram.session.session.Session.write = _safe_session_write
# ------------------------------------------------------------------------

from config import (
    API_HASH,
    API_ID,
    BOT_TOKEN,
    LOGGER_ID,
    MONGO_DB_URI,
    OWNER_ID,
    STRING1,
    STRING2,
    STRING3,
    STRING4,
    STRING5,
)
from anony.core.bot import Anon
from anony.core.dir import dirr
from anony.core.git import git
from anony.core.userbot import Userbot
from anony.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Anon()
userbot = Userbot()

from .platforms import *

YouTube = YouTube()
Carbon = Carbon()
Spotify = Spotify()
Apple = Apple()
Resso = Resso()
SoundCloud = SoundAPI()
Telegram = TeleAPI()

COMMANDS = {}
