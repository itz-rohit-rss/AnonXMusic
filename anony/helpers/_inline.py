# Copyright (c) 2025 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

from pyrogram import types

from anony import app, config, lang
from anony.core.lang import lang_codes


class Inline:
    def __init__(self):
        self.ikb = types.InlineKeyboardButton
        self.ikm = types.InlineKeyboardMarkup

    def cancel_dl(self, text: types.InlineKeyboardButton):
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
                [self.ikb(text=status, callback_data="controls_status")]
            )

        elif timer:
            keyboard.append(
                [self.ikb(text=timer, callback_data="controls_status")]
            )

        if not remove:
            keyboard.append(
                [
                    self.ikb(text="▶️", callback_data=f"controls resume {chat_id}"),
                    self.ikb(text="⏸️", callback_data=f"controls pause {chat_id}"),
                    self.ikb(text="🔄", callback_data=f"controls replay {chat_id}"),
                    self.ikb(text="⏭️ 𝐒𝐤𝐢𝐩", callback_data=f"controls skip {chat_id}"),
                    self.ikb(text="⏹️ 𝐄𝐧𝐝", callback_data=f"controls stop {chat_id}"),
                ]
            )

        return self.ikm(keyboard)

    def help_markup(
        self, _lang: dict, back: bool = False
    ) -> types.InlineKeyboardMarkup:
        if back:
            rows = [
                [
                    self.ikb(text=_lang["back"], callback_data="help back"),
                    self.ikb(text=_lang["close"], callback_data="help close"),
                ]
            ]
        else:
            cbs = ["admin", "auth", "blist", "cplay", "play", "queue", "tools"]
            buttons = [
                self.ikb(text=_lang[f"help_{cb}"], callback_data=f"help {cb}")
                for cb in enumerate(cbs)
            ]
            rows = [buttons[i : i + 3] for i in range(0, len(buttons), 3)]
            rows.append([self.ikb(text=_lang["close"], callback_data="help close")])

        return self.ikm(rows)

    def lang_markup(self, _: types.User) -> types.InlineKeyboardMarkup:
        langs = lang.get_languages()

        buttons = [
            self.ikb(
                text=f"{name} ({code})" if code == _["lang"] else name,
                callback_data=f"lang change {code}",
            )
            for code, name in langs.items()
        ]
        rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        rows.append([self.ikb(text=_["back"], callback_data="settings back")])
        return self.ikm(rows)

    def ping_markup(self, _: dict) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text="➕ 𝐀𝐝𝐝 𝐌𝐞 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 ➕",
                        url=f"https://t.me/{app.username}?startgroup=true",
                    )
                ],
                [
                    self.ikb(
                        text="𝐉𝐨𝐢𝐧 𝐩𝐥𝐞𝐚𝐬𝐞 😻",
                        url=config.SUPPORT_CHAT,
                    ),
                    self.ikb(
                        text="🥀 𝐎𝐰𝐧𝐞𝐫 🥀",
                        url=config.SUPPORT_CHANNEL,
                    ),
                ],
            ]
        )

    def play_queued(
        self, _: dict, chat_id: int, item_id: str
    ) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text=_["queued_btn_1"],
                        callback_data=f"queue play {chat_id} {item_id}",
                    ),
                    self.ikb(
                        text=_["queued_btn_2"],
                        callback_data=f"queue cancel {chat_id} {item_id}",
                    ),
                ]
            ]
        )

    def queue_markup(
        self, _: dict, chat_id: int, current_page: int, total_pages: int
    ) -> types.InlineKeyboardMarkup:
        buttons = []
        if current_page > 1:
            buttons.append(
                self.ikb(
                    text="⬅️",
                    callback_data=f"queue page {chat_id} {current_page - 1}",
                )
            )
        buttons.append(
            self.ikb(text=f"{current_page}/{total_pages}", callback_data="noop")
        )
        if current_page < total_pages:
            buttons.append(
                self.ikb(
                    text="➡️",
                    callback_data=f"queue page {chat_id} {current_page + 1}",
                )
            )

        return self.ikm(
            [
                buttons,
                [self.ikb(text=_["close"], callback_data="help close")],
            ]
        )

    def settings_markup(self, _: dict) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(text=_["setting_btn_1"], callback_data="settings lang"),
                    self.ikb(text=_["setting_btn_2"], callback_data="settings mode"),
                ],
                [
                    self.ikb(text=_["setting_btn_3"], callback_data="settings auth"),
                    self.ikb(text=_["setting_btn_4"], callback_data="settings playmode"),
                ],
                [self.ikb(text=_["close"], callback_data="help close")],
            ]
        )

    def start_key(self, _: dict) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text="➕ 𝐀𝐝𝐝 𝐌𝐞 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 ➕",
                        url=f"https://t.me/{app.username}?startgroup=true",
                    )
                ],
                [
                    self.ikb(
                        text="𝐉𝐨𝐢𝐧 𝐩𝐥𝐞𝐚𝐬𝐞 😻",
                        url=config.SUPPORT_CHAT,
                    ),
                    self.ikb(
                        text="🥀 𝐎𝐰𝐧𝐞𝐫 🥀",
                        url=config.SUPPORT_CHANNEL,
                    ),
                ],
                [
                    self.ikb(
                        text="📖 𝐇𝐞𝐥𝐩 & 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬",
                        callback_data="help_markup",
                    )
                ],
            ]
        )

    def yt_key(self, link: str, _: dict) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text="𝐉𝐨𝐢𝐧 𝐩𝐥𝐞𝐚𝐬𝐞 😻",
                        url=config.SUPPORT_CHAT,
                    ),
                    self.ikb(
                        text="🥀 𝐎𝐰𝐧𝐞𝐫 🥀",
                        url=config.SUPPORT_CHANNEL,
                    ),
                ],
                [self.ikb(text=_["yt_btn"], url=link)],
            ]
            )
        
