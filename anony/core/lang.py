import os
import logging
from typing import List, Union
from functools import wraps
from pyrogram.types import CallbackQuery, Message
from anony import db

LOGGER = logging.getLogger("AnonXMusic")

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
    paths = ["./anony/strings/langs", "./strings/langs", "strings/langs"]
    langs_dir = None
    for p in paths:
        if os.path.exists(p):
            langs_dir = p
            break

    if not langs_dir:
        return

    for file in os.listdir(langs_dir):
        if file.endswith(".yml"):
            code = file[:-4]
            try:
                import yaml
                with open(os.path.join(langs_dir, file), "r", encoding="utf-8") as stream:
                    data = yaml.safe_load(stream) or {}
                    languages[code] = data
                    languages_present[code] = data.get("name", code)
            except Exception as e:
                LOGGER.warning(f"Failed to load lang file {file}: {e}")


load_languages()


def get_string(lang_code: str):
    return languages.get(lang_code) or languages.get("en", {})


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

    @staticmethod
    def language(mystic):
        @wraps(mystic)
        async def wrapper(client, message, *args, **kwargs):
            chat_id = message.chat.id if isinstance(message, Message) else getattr(getattr(message, "message", None), "chat", None)
            chat_id = chat_id.id if hasattr(chat_id, "id") else chat_id

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

    @staticmethod
    def languageCB(mystic):
        @wraps(mystic)
        async def wrapper(client, CallbackQuery, *args, **kwargs):
            chat_id = CallbackQuery.message.chat.id if CallbackQuery.message else None

            lang_code = "en"
            if chat_id:
                try:
                    stored = await db.get(f"lang_{chat_id}")
                    if stored and stored in languages:
                        lang_code = stored
                except Exception:
                    lang_code = "en"

            _lang = languages.get(lang_code) or languages.get("en", {})
            return await mystic(client, CallbackQuery, _lang, *args, **kwargs)

        return wrapper


lang = Language()

# Top-level exports required by AnonXMusic plugins
language = Language.language
languageCB = Language.languageCB
