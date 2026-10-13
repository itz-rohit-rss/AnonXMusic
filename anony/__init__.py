import os
import sys
import logging
from pyrogram import Client

# Ensure root directory is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Standard logging setup
logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[logging.StreamHandler()],
    level=logging.INFO,
)
LOGGER = logging.getLogger("AnonXMusic")
logger = LOGGER

# --- Monkey-Patch for Pyrogram String Sessions on Python 3.13 ---
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

# Import root config
import config
from config import *

# Safe dynamic import for Core Bot class
try:
    import anony.core.bot as core_bot
    Anon = getattr(
        core_bot,
        "Anon",
        getattr(
            core_bot,
            "AnonX",
            getattr(
                core_bot,
                "AnonMusic",
                getattr(core_bot, "Anony", Client),
            ),
        ),
    )
except Exception:
    Anon = Client

# Safe dynamic import for Userbot
try:
    from anony.core.userbot import Userbot
except Exception:
    Userbot = Client

# Core startup steps
try:
    from anony.core.dir import dirr
    dirr()
except Exception:
    pass

try:
    from anony.core.git import git
    git()
except Exception:
    pass

try:
    from anony.misc import dbb, heroku
    dbb()
    heroku()
except Exception:
    pass

app = Anon()
userbot = Userbot()

# Load platforms safely
try:
    from .platforms import *
    YouTube = YouTube()
    Carbon = Carbon()
    Spotify = Spotify()
    Apple = Apple()
    Resso = Resso()
    SoundCloud = SoundAPI()
    Telegram = TeleAPI()
except Exception:
    pass

COMMANDS = {}
