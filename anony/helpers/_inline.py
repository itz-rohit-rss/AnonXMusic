# Copyright (C) 2024 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import types

from anony import app, config, lang
from anony.utils.lang import lang_codes


class Inline:
    def __init__(self):
        self.ikb = types.InlineKeyboardButton
        self.ikm = types.InlineKeyboardMarkup

    def cancel(self, text: types.InlineKeyboardButton):
        return self.ikm([[self.ikb(text=text, callback_data="cancel_dl")]])

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
                    self.ikb(text="⏸️", callback_data=f"controls pause {chat_id}"),
                    self.ikb(text="🔄", callback_data=f"controls replay {chat_id}"),
                ]
            )
            keyboard.append(
                [
                    self.ikb(text="⏭️ 𝐒𝐤𝐢𝐩", callback_data=f"controls skip {chat_id}"),
                    self.ikb(text="⏹️ 𝐄𝐧𝐝", callback_data=f"controls stop {chat_id}"),
                ]
            )

        return self.ikm(keyboard)

    def help_markup(
        self,
        lang_code: str,
        back: bool = False,
    ) -> types.InlineKeyboardMarkup:
        if back:
            rows = [
                [
                    self.ikb(text=lang["back"], callback_data="help_back"),
                    self.ikb(text=lang["close"], callback_data="help_close"),
                ]
            ]
        else:
            cbl = ["admin", "auth", "blist", "cplay", "play", "queue", "tools"]
            buttons = [
                self.ikb(text=lang[f"help_{cbl[i]}"], callback_data=f"help_{cbl[i]}")
                for i in range(len(cbl))
            ]
            rows = [buttons[i : i + 3] for i in range(0, len(buttons), 3)]
            rows.append([self.ikb(text=lang["close"], callback_data="help_close")])

        return self.ikm(rows)

    def lang_markup(self, _: types.User) -> types.InlineKeyboardMarkup:
        langs = lang.get_languages()

        buttons = [
            self.ikb(
                text=(f"•{name}•" if code == _["lang"] else name),
                callback_data=f"lang_change {code}",
            )
            for code, name in langs.items()
        ]

        rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        return self.ikm(rows)
        
