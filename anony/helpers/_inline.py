from pyrogram import types

from anony import app, config


class Inline:
    def __init__(self):
        self.ikb = types.InlineKeyboardButton
        self.ikm = types.InlineKeyboardMarkup

    def cancel(self, text: types.InlineKeyboardButton):
        return self.ikm([[self.ikb(text=text, callback_data="cancel_dl")]])

    def start_key(self, lang, private: bool = False):
        def _(key, default):
            if isinstance(lang, dict):
                return lang.get(key, default)
            return getattr(lang, key, default)

        add_text = _("add_bot", _("add_me", "➕ Add Me To Your Group"))
        help_text = _("help", _("help_button", "✨ Commands / Help"))
        support_text = _("support", _("support_button", "📢 Support"))
        channel_text = _("channel", _("channel_button", "📣 Channel"))
        lang_text = _("language", _("lang_button", "🌐 Language"))

        if private:
            keyboard = [
                [
                    self.ikb(
                        text=add_text,
                        url=f"https://t.me/{app.username}?startgroup=true",
                    )
                ],
                [
                    self.ikb(text=help_text, callback_data="help_menu"),
                    self.ikb(text=lang_text, callback_data="lang_menu"),
                ],
                [
                    self.ikb(text=support_text, url=config.SUPPORT_CHAT),
                    self.ikb(text=channel_text, url=config.SUPPORT_CHANNEL),
                ],
            ]
        else:
            keyboard = [
                [
                    self.ikb(
                        text=add_text,
                        url=f"https://t.me/{app.username}?startgroup=true",
                    )
                ],
                [
                    self.ikb(text=support_text, url=config.SUPPORT_CHAT),
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
        lang,
        back: bool = False,
    ) -> types.InlineKeyboardMarkup:
        def _(key, default):
            if isinstance(lang, dict):
                return lang.get(key, default)
            return getattr(lang, key, default)

        if back:
            rows = [
                [
                    self.ikb(text=_("back", "Back"), callback_data="help_back"),
                    self.ikb(text=_("close", "Close"), callback_data="help_close"),
                ]
            ]
        else:
            cbl = ["admin", "auth", "blist", "cplay", "play", "queue", "tools"]
            buttons = [
                self.ikb(
                    text=_(f"help_{item}", item.capitalize()),
                    callback_data=f"help_{item}",
                )
                for item in cbl
            ]
            rows = [buttons[i : i + 3] for i in range(0, len(buttons), 3)]
            rows.append(
                [self.ikb(text=_("close", "Close"), callback_data="help_close")]
            )

        return self.ikm(rows)

    def lang_markup(self, langs: dict, current_lang: str) -> types.InlineKeyboardMarkup:
        buttons = [
            self.ikb(
                text=(f"•{name}•" if code == current_lang else name),
                callback_data=f"lang_change {code}",
            )
            for code, name in langs.items()
        ]

        rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        return self.ikm(rows)
        
