import os
import logging
from typing import List, Union

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
                    data = yaml.safe_load(stream) or {}
                    languages[code] = data
                    languages_present[code] = data.get("name", code)
            except Exception as e:
                LOGGER.warning(
                    f"Language file '{file}' load karne me dikkat: {e}"
                )


load_languages()


class Language:
    def __init__(self):
        self.languages = languages
        self.languages_present = languages_present

    async def get_lang(self, chat_id: Union[int, str]) -> str:
        try:
            val = await db.get(f"lang_{chat_id}")
            if val and val in self.languages:
                return val
        except Exception:
            pass
        return "en"

    async def set_lang(self, chat_id: Union[int, str], lang: str):
        try:
            await db.set(f"lang_{chat_id}", lang)
        except Exception:
            pass

    @classmethod
    def language(cls, mystic):
        async def wrapper(client, message, *args, **kwargs):
            if isinstance(message, CallbackQuery):
                chat_id = message.message.chat.id
            elif isinstance(message, Message):
                chat_id = message.chat.id
            else:
                chat_id = None

            lang_code = "en"
            if chat_id:
                try:
                    stored = await db.get(f"lang_{chat_id}")
                    if stored and stored in languages:
                        lang_code = stored
                except Exception:
                    lang_code = "en"

            _lang = languages.get(lang_code) or languages.get("en", {})
            return await mystic(client, message, _lang, *args, **kwargs)

        return wrapper

    def __call__(self, mystic):
        return self.language(mystic)


lang = Language()
