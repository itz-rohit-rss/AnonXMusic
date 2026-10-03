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
from py_yt import Playlist, VideosSearch

from anony import logger
from anony.helpers import utils


class DummyLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


class TrackDetails:
    def __init__(self, data: dict, file_path: str = None, video: bool = False):
        self.title = data.get("title", "Unknown Title")
        self.duration_min = data.get("duration", "00:00")
        self.duration_sec = (
            utils.time_to_seconds(self.duration_min)
            if hasattr(utils, "time_to_seconds")
            else 0
        )
        self.thumbnail = (
            data.get("thumbnails", [{}])[0].get("url")
            if data.get("thumbnails")
            else None
        )
        self.vidid = data.get("id")
        self.link = data.get("link")
        self.file_path = file_path
        self.file = file_path
        self.file_name = file_path
        self.url = file_path or self.link
        self.video = video
        self.stream_type = "video" if video else "audio"

    def __getitem__(self, key):
        return getattr(self, key, None)


class YouTube:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.cookies = []
        self.checked = False
        self.cookie_dir = "anony/cookies"
        self.warned = False
        self.regex = re.compile(
            r"(https?://)?(www\.|m\.)?(youtube\.com/(watch\?v=|shorts/|playlist\?list=)|youtu\.be/)([a-zA-Z0-9_-]{11}|[a-zA-Z0-9_-]+)"
        )
        self.regex_ = re.compile(
            r"(https?://)?(www\.|m\.)?(youtube\.com/(watch\?v=|shorts/|playlist\?list=)|youtu\.be/)([a-zA-Z0-9_-]{11})"
        )

    def get_cookies(self):
        if not self.checked:
            if os.path.exists(self.cookie_dir):
                for file in os.listdir(self.cookie_dir):
                    if file.endswith(".txt"):
                        self.cookies.append(f"{self.cookie_dir}/{file}")
            if os.path.exists("cookies.txt"):
                self.cookies.append("cookies.txt")
            self.checked = True
        if not self.cookies:
            if not self.warned:
                self.warned = True
                logger.warning("Cookies are missing; downloads might fail.")
            return None
        return random.choice(self.cookies)

    async def save_cookies(self, urls: list[str] = None):
        logger.info("Saving cookies from urls...")
        async with aiohttp.ClientSession() as session:
            for url in urls:
                name = url.split("/")[-1]
                link = f"https://batbin.me/raw/{name}"
                async with session.get(link) as resp:
                    resp_raw = await resp.text()
                    os.makedirs(self.cookie_dir, exist_ok=True)
                    with open(f"{self.cookie_dir}/{name}.txt", "w") as f:
                        f.write(resp_raw)
        logger.info(f"Cookies saved in {self.cookie_dir}")

    def valid(self, url: str) -> bool:
        return bool(re.match(self.regex, url))

    def invalid(self, url: str) -> bool:
        return not bool(re.match(self.regex_, url))

    async def playlist(self, url: str, limit: int = 50) -> list[dict]:
        playlist = Playlist(url)
        while playlist.hasMoreVideos and len(playlist.videos) < limit:
            await playlist.getNextVideos()
        return playlist.videos

    async def download(self, link: str, video: bool = False) -> str:
        loop = asyncio.get_running_loop()

        def _download():
            cookie = self.get_cookies()
            ydl_opts = {
                "format": "bestaudio/best" if not video else "bestvideo+bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "logger": DummyLogger(),
                "extractor_args": {
                    "youtube": {
                        "player_client": ["android", "ios", "web_creator"]
                    }
                },
            }
            if cookie and os.path.exists(cookie):
                ydl_opts["cookiefile"] = cookie

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                filename = ydl.prepare_filename(info)
                if not video:
                    base, _ = os.path.splitext(filename)
                    for ext in [".mp3", ".m4a", ".webm", ".opus"]:
                        if os.path.exists(base + ext):
                            return base + ext
                return filename

        return await loop.run_in_executor(None, _download)

    async def search(self, query: str, sent_id: int = None, video: bool = False):
        if self.valid(query):
            link = query
            vid_id = (
                query.split("v=")[-1].split("&")[0]
                if "v=" in query
                else query.split("/")[-1]
            )
            data = {
                "title": "YouTube Audio",
                "duration": "04:00",
                "id": vid_id,
                "link": link,
            }
        else:
            search = VideosSearch(query, limit=1)
            results = await search.next()
            res = results.get("result", [])
            if not res:
                return None
            data = res[0]
            link = data.get("link")

        file_path = await self.download(link, video=video)
        return TrackDetails(data, file_path=file_path, video=video)
                        
