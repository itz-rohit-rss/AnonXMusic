# Copyright (C) 2024 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import types

from anony import app, config, lang
from anony.core.lang import lang_codes


class Inline:
    def __File `anony/helpers/_inline.py` ke liye corrected code niche diya gaya hai, jisme `anony.core.lang` ka import aur `start_key` function dono include kiye gaye hain:

```python
from pyrogram import types

from anony import app, config, lang
from anony.core.lang import lang_codes


class Inline:
    def __init__(self):
        self.ikb = types.InlineKeyboardButton
        self.ikm = types.InlineKeyboardMarkup

    def cancel(self, text: types.InlineKeyboardButton):
        return self.ikm([[self.ikb(text=text, callback_data="cancel_dl")]])

    def start_key(self, lang_code: str, private: bool = False):
        if private:
            keyboard = [
                [
                    self.ikb(
                        text=lang["add_me"],
                        url=f"[https://t.me/](https://t.me/){app.username}?startgroup=true",
                    )
                ],
                [
                    self.ikb(text=lang["help_button"], callback_data="help_menu"),
                    self.ikb(text=lang["lang_button"], callback_data="lang_menu"),
                ],
                [
                    self.ikb(text=lang["support_button"], url=config.SUPPORT_CHAT),
                    self.ikb(text=lang["channel_button"], url=config.SUPPORT_CHANNEL),
                ],
            ]
        else:
            keyboard = [
                [
                    self.ikb(
                        text=lang["add_me"],
                        url=f"[https://t.me/](https://t.me/){app.username}?startgroup=true",
                    )
                ],
                [
                    self.ikb(text=lang["support_button"], url=config.SUPPORT_CHAT),
                ],
            ]
        return self.ikm(keyboard)

    def controls(
        self,
        chat_id: int,
        status: str = None,
        timer: str = None,
        remove: bool = False,
    ) -> types.InlineKeyboardMarkup:
        keyboard = []
        if status:
            keyboard.append(
                [
                    self.ikb(text=status, callback_data="controls_status"),
                ]
            )
        elif timer:
            keyboard.append(
                [
                    self.ikb(text=timer, callback_data="controls_status"),
                ]
            )

        if not remove:
            keyboard.append(
                [
                    self.ikb(text="▶️", callback_data=f"controls resume {chat_id}"),
                    self.ikb(text="⏸️️", callback_data=f"controls pause {chat_id}"),
                    self.ikb(text="🔄", callback_data=f"controls replay {chat_id}"),
                ]
            )
            keyboard.append(

        
