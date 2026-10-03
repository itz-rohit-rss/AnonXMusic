# Copyright (C) 2024 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import asyncio
import os
import time

from pyrogram import types

from anony import config
from anony.helpers import buttons, media, utils


class Telegram:
    def __init__(self):
        self.active = []
        self.events = {}
        self.last_edit = {}
        self.active_tasks = {}
        self.sleep = 7

    def get_media(self, msg: types.Message) -> bool:
        return bool(any([msg.audio, msg.voice, msg.video, msg.document]))

    async def cancel(self, query: types.CallbackQuery):
        event = self.events.get(query.message.id)
        task = self.active_tasks.pop(query.message.id, None)
        if event:
            event.set()

        if task and not task.done():
            task.cancel()

        if event or task:
            await query.edit_message_text(
                query.lang["dl_cancel"].format(query.from_user.mention)
            )
        else:
            await query.answer(query.lang["dl_not_found"], show_alert=True)

    async def download(self, msg: types.Message, sent: types.Message):
        msg_id = sent.id
        event = asyncio.Event()
        self.events[msg_id] = event
        self.last_edit[msg_id] = 0
        start_time = time.time()

        media_obj = msg.audio or msg.voice or msg.video or msg.document
        file_id = getattr(media_obj, "file_unique_id", None)
        file_ext = getattr(media_obj, "file_name", "").split(".")[-1]
        file_size = getattr(media_obj, "file_size", 0)
        file_title = getattr(media_obj, "title", "Telegram File") or "Telegram File"
        duration = getattr(media_obj, "duration", 0)
        video = bool(getattr(media_obj, "mime_type", "").startswith("video"))

        if duration > config.DURATION_LIMIT:
            await sent.edit_text(sent.lang["play_duration_limit"].format(config.DURATION_LIMIT))
            return await sent.stop_propagation()

        if file_size > 200 * 1024 * 1024:
            await sent.edit_text(sent.lang["dl_limit"])
            return await sent.stop_propagation()

        async def progress(current, total):
            if event.is_set():
                return

            now = time.time()
            if now - self.last_edit[msg_id] < self.sleep:
                return

            self.last_edit[msg_id] = now
            percent = current * 100 / total
            speed = current / (now - start_time)
            eta = utils.format_duration((total - current) / speed)
            bar = utils.get_progress_bar(percent)

            cancel_btn = None
            try:
                if hasattr(buttons, "cancel"):
                    cancel_btn = buttons.cancel(sent.lang["cancel"])
                elif hasattr(buttons, "cancel_dl"):
                    cancel_btn = buttons.cancel_dl(sent.lang["cancel"])
            except Exception:
                cancel_btn = None

            try:
                await sent.edit_text(
                    sent.lang["download_progress"].format(
                        file_title,
                        bar,
                        round(percent, 2),
                        utils.format_size(current),
                        utils.format_size(total),
                        utils.format_size(speed),
                        eta,
                    ),
                    reply_markup=cancel_btn,
                )
            except Exception:
                pass

        task = asyncio.create_task(
            msg.download(
                file_name=f"downloads/{file_id}.{file_ext}",
                progress=progress,
            )
        )
        self.active_tasks[msg_id] = task

        try:
            file_path = await task
        except asyncio.CancelledError:
            file_path = None
        finally:
            self.events.pop(msg_id, None)
            self.last_edit.pop(msg_id, None)
            self.active_tasks.pop(msg_id, None)

        return file_path
        
