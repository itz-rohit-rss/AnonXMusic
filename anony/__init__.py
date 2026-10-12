import os
import sys
import logging

# Ensure root directory is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# --- Monkey-Patch for Pyrogram / Python 3.13 String Sessions ---
# Fixes: AttributeError: 'NoneType' object has no attribute 'write' during invoke
try:
    import pyrogram.session.internals.msg_id
except Exception:
    pass

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
# ----------------------------------------------------------------

# Import root config module and expose it inside anony
import config
from config import *

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
