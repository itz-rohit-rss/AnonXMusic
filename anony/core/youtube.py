# Copyright (C) 2024 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import asyncio
import os
import random
import re
from pathlib import Path

import aiohttp
import yt_dlp
from py_compile import compile
from youtubesearchpython.__future__ import Playlist, VideosSearch

from anony import LOGGER
from anony.helpers import utils


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
        self.link = self.data.get("link")
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
        if await self.valid(query):
            link = query
        else:
            search = VideosSearch(query, limit=1)
            results = await search.next()
            if not results["result"]:
                return None
            link = results["result"][0]["link"]

        details = VideosSearch(link, limit=1)
        res = await details.next()
        if not res["result"]:
            return None
        return TrackDetails(res["result"][0])

    async def playlist(self, link: str, limit: int = 50):
        try:
            plist = await Playlist.create(link)
            tracks = []
            for video in plist.videos[:limit]:
                tracks.append(TrackDetails(video))
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
        
