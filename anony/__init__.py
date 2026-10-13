import os
import sys
from pyrogram import Client
from pytgcalls import PyTgCalls

import config

# Logging setup
import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
LOGGER = logging.getLogger("AnonX")

class Anon(Client):
    def __init__(self):
        super().__init__(
            name="AnonX",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        LOGGER.info("Bot Started Successfully")

    async def stop(self):
        await super().stop()
        LOGGER.info("Bot Stopped")

app = Anon()

userbot = Client(
    name="AnonUserbot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    session_string=config.STRING_SESSION,
)

pytgcalls = PyTgCalls(userbot)
