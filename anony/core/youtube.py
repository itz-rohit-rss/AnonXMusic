# Copyright (C) 2024 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import asyncio
import glob
import logging
import os
import re
import urllib.request

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


def ensure_cookies():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cookies_dir = os.path.join(base_dir, "cookies")
    os.makedirs(cookies_dir, exist_ok=True)
    target_file = os.path.join(cookies_dir, "cookies.txt")

    cookie_url = os.environ.get("COOKIES_URL", "https://batbin.me/raw/warms")
    if cookie_url and (cookie_url.startswith("http://") or cookie_url.startswith("https://")):
        try:
            req = urllib.request.Request(cookie_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode("utf-8")
                if "Netscape" in content or "youtube.com" in content:
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(content)
                    return target_file
        except Exception as e:
            LOGGER.error(f"Failed to fetch cookies from URL: {e}")

    if os.path.exists(target_file) and os.path.getsize(target_file) > 100:
        return target_file

    return None


def get_cookie_file():
    cookie = ensure_cookies()
    if cookie:
        return cookie

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cookies_dir = os.path.join(base_dir, "cookies")

    cookie_files = glob.glob(os.path.join(cookies_dir, "*.txt"))
    if cookie_files:
        return cookie_files[0]

    root_cookie = os.path.join(os.path.dirname(base_dir), "cookies.txt")
    if os.path.exists(root_cookie):
        return root_cookie

    if os.path.exists("cookies.txt"):
        return "cookies.txt"

    return None


class TrackDetails:
    def __init__(self, data: dict = None, file_path: str = None, video: bool = False):
        self.data = data or {}
        self.title = self.data.get("title", "Unknown Track")
        self.duration_min = self.data.get("duration_string") or self.data.get("duration", "00:00")
        if isinstance(self.duration_min, (int, float)):
            mins, secs = divmod(int(self.duration_min), 60)
            self.duration_min = f"{mins:02d}:{secs:02d}"

        self.duration = self.duration_min
        self.duration_sec = (
            utils.time_to_seconds(self.duration_min)
            if hasattr(utils, "time_to_seconds")
            else 0
        )
        self.seconds = self.duration_sec

        thumbnails = self.data.get("thumbnails", [])
        self.thumbnail = (
            thumbnails[-1].get("url") if thumbnails else self.data.get("thumbnail")
        )
        self.thumb = self.thumbnail
        self.vidid = self.data.get("id")
        self.id = self.vidid
        self.link = (
            self.data.get("webpage_url")
            or self.data.get("url")
            or f"https://www.youtube.com/watch?v={self.vidid}"
        )
        self.file_path = file_path
        self.file_name = file_path
        self.url = file_path or self.link
        self.video = video
        self.stream_type = "video" if video else "audio"
        self.user_id = None
        self.user_name = None
        self.req_by = None
        self.channel = self.data.get("uploader") or self.data.get("channel")

    def __getattr__(self, name):
        return self.data.get(name, "")

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
        cookie = get_cookie_file()
        if cookie:
            self.cookies = [cookie]

    def get_cookies(self):
        return self.cookies

    async def save_cookies(self, cookies=None):
        if not cookies:
            return True

        if isinstance(cookies, list):
            cookies = "".join(cookies)
        elif not isinstance(cookies, str):
            cookies = str(cookies)

        cookies = cookies.strip()

        if cookies.startswith("http://") or cookies.startswith("https://"):
            try:
                req = urllib.request.Request(
                    cookies,
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    cookies = resp.read().decode("utf-8")
            except Exception as e:
                LOGGER.error(f"Failed to fetch cookies from URL: {e}")
                return False

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cookies_dir = os.path.join(base_dir, "cookies")
        os.makedirs(cookies_dir, exist_ok=True)
        with open(os.path.join(cookies_dir, "cookies.txt"), "w", encoding="utf-8") as f:
            f.write(cookies)

        self.check_cookies()
        return True

    async def valid(self, link: str):
        if re.search(self.regex, link):
            return True
        return False

    async def invalid(self, link: str):
        return not await self.valid(link)

    async def exists(self, link: str):
        return await self.valid(link)

    async def search(self, query: str, message_id: int = None, video: bool = False, *args, **kwargs):
        cookie_file = get_cookie_file()
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "geo_bypass": True,
            "logger": DummyLogger(),
        }
        if cookie_file:
            ydl_opts["cookiefile"] = cookie_file

        loop = asyncio.get_event_loop()
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if not await self.valid(query):
                    info = await loop.run_in_executor(
                        None, lambda: ydl.extract_info(f"ytsearch1:{query}", download=False)
                    )
                    if not info or not info.get("entries"):
                        return None
                    entry = info["entries"][0]
                else:
                    entry = await loop.run_in_executor(
                        None, lambda: ydl.extract_info(query, download=False)
                    )

                vidid = entry.get("id")
                file_path = await self.download(vidid, video=video)
                return TrackDetails(entry, file_path=file_path, video=video)
        except Exception as e:
            LOGGER.error(f"YouTube search error: {e}")
            return None

    async def track(self, query: str):
        return await self.search(query)

    async def playlist(self, link: str, limit: int = 50):
        cookie_file = get_cookie_file()
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "logger": DummyLogger(),
        }
        if cookie_file:
            ydl_opts["cookiefile"] = cookie_file

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

        cookie_file = get_cookie_file()
        ydl_opts = {
            "format": "bestaudio/best" if not video else "bestvideo+bestaudio/best",
            "outtmpl": f"downloads/{vidid}.%(ext)s",
            "geo_bypass": True,
            "nocheckcertificate": True,
            "quiet": True,
            "no_warnings": True,
            "logger": DummyLogger(),
        }

        if cookie_file:
            ydl_opts["cookiefile"] = cookie_file

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
        
