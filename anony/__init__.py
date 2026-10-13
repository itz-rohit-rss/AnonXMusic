import os
import sys
import logging

# Ensure root directory is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# --- Monkey-Patch for Pyrogram / Python 3.13 String Sessions ---
try:
    import pyrogram.session.session

    def _safe_session_write(self):
        if getattr(self, "file", None) is not None:
            try:
                return self.file.write()
            except Exception:
                pass
        return b""

    pyrogram.session.session.Session.write = _safe_session_write
except Exception:
    pass
# --------------------------------------------------------------

# Root config import & export
import config
from config import *

from .logging import LOGGER
logger = LOGGER

from anony.core.bot import Anon
from anony.core.dir import dirr
from anony.core.git import git
from anony.core.userbot import Userbot
from anony.misc import dbb, heroku

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
