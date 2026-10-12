import os
import logging
from typing import List, Union

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from anony import db

LOGGER = logging.getLogger(__name__)

languages = {}
languages_present = {}


def get_command(command: str) -> List[str]:
    try:
        from anony import COMMANDS
        return COMMANDS[command]
    except Exception:
        return [command]


def load_languages():
    global languages, languages_present
    languages_dir = "./anony/strings/langs"
    if not os.path.exists(languages_dir):
        return

    for file in os.listdir(languages_dir):
        if file.endswith(".yml"):
            code = file[:-4]
            try:
                import yaml

                with open(
                    os.path.join(languages_dir, file),
                    "r",
                    encoding="utf-8",
                ) as stream:
                    languages[code] = yaml.safe_load(stream) or {}
                languages_present[code] = languages[code].get("name", code)
            except Exception as e:
                LOGGER.warning(
                    f"Language file '{file}' ko load karne mein error: {e}"
                )


load_languages()


class Language:
    def __init__(self):
        self.languages = languages
        self.languages_present = languages_present

    async def get_lang(self, chat_id: Union[int, str]) -> str:
        try:
            lang = await db.get(f"lang_{chat_id}")
            return lang or "en"
        except Exception:
            return "en"

    async def set_lang(self, chat_id: Union[int, str], lang: str):
        try:
            await db.set(f"lang_{chat_id}", lang)
        except Exception:
            pass

    def __call__(self, mystic):
        async def wrapper(client, message, *args, **kwargs):
            if isinstance(message, CallbackQuery):
                chat_id = message.message.chat.id
            elif isinstance(message, Message):
                chat_id = message.chat.id
            else:
                chat_id = None

            lang_code = None
            if chat_id:
                try:
                    lang_code = await self.get_lang(chat_id)
                except Exception:
                    lang_code = "en"

            # Safe Language Fallback (KeyError: None Prevention)
            if not lang_code or lang_code not in self.languages:
                lang_code = "en"

            lang_dict = self.languages.get(lang_code) or self.languages.get("en", {})

            return await mystic(client, message, lang_dict, *args, **kwargs)

        return wrapper


lang = Language()
