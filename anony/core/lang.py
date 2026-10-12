import os
import inspect
import logging
from typing import List, Union
from functools import wraps

from pyrogram.types import CallbackQuery, Message
from anony import db

LOGGER = logging.getLogger("AnonXMusic")

# Load native string mappings safely
languages = {}
languages_present = {}

try:
    from strings import languages as _langs, languages_present as _lp
    languages = _langs
    languages_present = _lp
except Exception:
    try:
        from anony.strings import languages as _langs, languages_present as _lp
        languages = _langs
        languages_present = _lp
    except Exception:
        pass

# Fallback: Agar upar se import na ho sake toh filesystem scan
if not languages:
    paths = ["./strings/langs", "./anony/strings/langs", "strings/langs"]
    langs_dir = None
    for p in paths:
        if os.path.exists(p):
            langs_dir = p
            break
    if langs_dir:
        for file in os.listdir(langs_dir):
            if file.endswith(".yml"):
                code = file[:-4]
                try:
                    import yaml
                    with open(os.path.join(langs_dir, file), "r", encoding="utf-8") as s:
                        data = yaml.safe_load(s) or {}
                        languages[code] = data
                        languages_present[code] = data.get("name", code)
                except Exception:
                    pass

# Fail-safe dict jo missing keys par kabhi KeyError na feke
class SafeLangDict(dict):
    def __missing__(self, key):
        en_dict = languages.get("en", {})
        if isinstance(en_dict, dict) and key in en_dict:
            return en_dict[key]
        return "{0}"

def get_safe_lang(chat_lang_code):
    raw = languages.get(chat_lang_code) or languages.get("en") or {}
    safe = SafeLangDict()
    if isinstance(raw, dict):
        safe.update(raw)
    return safe

def get_string(lang_code: str):
    return get_safe_lang(lang_code)

def get_command(command: str) -> List[str]:
    try:
        from anony import COMMANDS
        return COMMANDS[command]
    except Exception:
        return [command]

def language_universal(*args, **kwargs):
    def decorator(mystic):
        @wraps(mystic)
        async def wrapper(client, message, *w_args, **w_kwargs):
            chat_id = None
            if isinstance(message, CallbackQuery):
                chat_id = message.message.chat.id if getattr(message, "message", None) else None
            elif isinstance(message, Message):
                chat_id = message.chat.id
            elif hasattr(message, "chat"):
                chat_id = getattr(message.chat, "id", None)

            lang_code = "en"
            if chat_id:
                try:
                    stored = await db.get(f"lang_{chat_id}")
                    if stored:
                        lang_code = stored
                except Exception:
                    lang_code = "en"

            _lang = get_safe_lang(lang_code)

            try:
                setattr(message, "lang", _lang)
            except Exception:
                pass

            try:
                sig = inspect.signature(mystic)
                num_params = len(sig.parameters)
            except Exception:
                num_params = 2

            if num_params == 2:
                return await mystic(client, message, *w_args, **w_kwargs)
            else:
                return await mystic(client, message, _lang, *w_args, **w_kwargs)

        return wrapper

    if args and callable(args[0]):
        return decorator(args[0])
    return decorator

def language_cb_universal(*args, **kwargs):
    def decorator(mystic):
        @wraps(mystic)
        async def wrapper(client, CallbackQuery, *w_args, **w_kwargs):
            chat_id = CallbackQuery.message.chat.id if getattr(CallbackQuery, "message", None) else None

            lang_code = "en"
            if chat_id:
                try:
                    stored = await db.get(f"lang_{chat_id}")
                    if stored:
                        lang_code = stored
                except Exception:
                    lang_code = "en"

            _lang = get_safe_lang(lang_code)

            try:
                setattr(CallbackQuery, "lang", _lang)
                if hasattr(CallbackQuery, "message") and CallbackQuery.message:
                    setattr(CallbackQuery.message, "lang", _lang)
            except Exception:
                pass

            try:
                sig = inspect.signature(mystic)
                num_params = len(sig.parameters)
            except Exception:
                num_params = 2

            if num_params == 2:
                return await mystic(client, CallbackQuery, *w_args, **w_kwargs)
            else:
                return await mystic(client, CallbackQuery, _lang, *w_args, **w_kwargs)

        return wrapper

    if args and callable(args[0]):
        return decorator(args[0])
    return decorator

class Language:
    def __init__(self):
        self.languages = languages
        self.languages_present = languages_present

    async def get_lang(self, chat_id: Union[int, str]) -> str:
        try:
            val = await db.get(f"lang_{chat_id}")
            if val:
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
    def language(*args, **kwargs):
        return language_universal(*args, **kwargs)

    @staticmethod
    def languageCB(*args, **kwargs):
        return language_cb_universal(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return language_universal(*args, **kwargs)

lang = Language()
language = language_universal
languageCB = language_cb_universal
        
