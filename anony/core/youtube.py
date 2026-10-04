# Copyright (C) 2024 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import asyncio
import logging
import os
import re

import yt_dlp

from anony.helpers import utils

LOGGER = logging.getLogger("AnonXMusic.YouTube")


class DummyLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


class TrackDetails:
    def __init__(self, data: dict = None, file_path: str = None, video: bool = False):
        self.data = data or {}
        self.title = self.data.get("title", "Unknown Track")
        self.duration_min = self.data.get("duration", "00:00")
        self.duration_sec = (
            utils.time_to_seconds(self.duration_min)
            if hasattr(utils, "time_to_seconds")
            else 0
        )
        self.thumbnail = (
            self.data.get("thumbnails", [{}])[0].get("url")
            if self.data.get("thumbnails")
            else None
        )
        self.vidid = self.data.get("id")
        self.id = self.vidid
        self.link = self.data.get("webpage_url") or self.data.get("url")
        self.file_path = file_path
        self.file_name = file_path
        self.url = file_path or self.link
        self.video = video
        self.stream_type = "video" if video else "audio"
        self.user_id = None
        self.user_name = None
        self.req_by = None
        self.channel = None

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        return self.data.get(item, None)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def get(self, key, default=None):
        return self.__dict__.get(key, self.data.get(key, default))

    def set(self, key, value):
        self.__dict__[key] = value


class YouTube:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?([a-zA-Z0-9_-]{11})"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.cookies = []
        self.check_cookies()

    def check_cookies(self):
        if os.path.exists("cookies.txt"):
            self.cookies = ["cookies.txt"]

    async def valid(self, link: str):
        if re.search(self.regex, link):
            return True
        return False

    async def exists(self, link: str):
        return await self.valid(link)

    async def track(self, query: str):
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "geo_bypass": True,
            "logger": DummyLogger(),
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "ios"]
                }
            },
        }
        if os.path.exists("cookies.txt"):
            ydl_opts["cookiefile"] = "cookies.txt"

        loop = asyncio.get_event_loop()
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if not await self.valid(query):
                    info = await loop.run_in_executor(
                        None, lambda: ydl.extract_info(f"ytsearch1:{query}", download=False)
                    )
                    if not info or not info.get("entries"):
                        return None
                    data = info["entries"][0]
                else:
                    data = await loop.run_in_executor(
                        None, lambda: ydl.extract_info(query, download=False)
                    )
                return TrackDetails(data)
        except Exception as e:
            LOGGER.error(f"YouTube search error: {e}")
            return None

    async def playlist(self, link: str, limit: int = 50):
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "logger": DummyLogger(),
        }
        if os.path.exists("cookies.txt"):
            ydl_opts["cookiefile"] = "cookies.txt"

        loop = asyncio.get_event_loop()
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = await loop.run_in_executor(
                    None, lambda: ydl.extract_info(link, download=False)
                )
                tracks = []
                for entry in info.get("entries", [])[:limit]:
                    tracks.append(TrackDetails(entry))
                return tracks
        except Exception:
            return []

    async def download(self, vidid: str, video: bool = False):
        link = self.base + vidid if not vidid.startswith("http") else vidid
        os.makedirs("downloads", exist_ok=True)
        out = f"downloads/{vidid}.{'mp4' if video else 'mp3'}"

        if os.path.exists(out):
            return out

        ydl_opts = {
            "format": "bestvideo+bestaudio/best" if video else "bestaudio/best",
            "outtmpl": f"downloads/{vidid}.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "no_warnings": True,
            "logger": DummyLogger(),
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "ios"]
                }
            },
        }

        if os.path.exists("cookies.txt"):
            ydl_opts["cookiefile"] = "cookies.txt"

        if not video:
            ydl_opts["postprocessors"] = [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ]

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([link])
        )

        if os.path.exists(out):
            return out

        for f in os.listdir("downloads"):
            if f.startswith(vidid):
                return os.path.join("downloads", f)
        return None
            
