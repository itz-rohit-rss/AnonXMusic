# Copyright (C) 2024 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import asyncio
import logging
import os
import re
import yt_dlp
from youtubesearchpython.__future__ import VideosSearch

LOGGER = logging.getLogger("AnonXMusic.YouTube")


class DummyLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


RAW_COOKIE_DATA = """# Netscape HTTP Cookie File
# https://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file! Do not edit.

.youtube.com	TRUE	/	TRUE	1825831691	PREF	f6=40000000&tz=Asia.Calcutta&f7=100
.youtube.com	TRUE	/	TRUE	1806472315	__Secure-BUCKET	CL0B
.youtube.com	TRUE	/	FALSE	1825487459	HSID	AHQEqmXCEIoAR2t7L
.youtube.com	TRUE	/	TRUE	1825487459	SSID	AZRB5fTdj8f2HWa5L
.youtube.com	TRUE	/	FALSE	1825487459	APISID	HMlPumDK244VNrou/AkF_KqonqoIQgMJxv
.youtube.com	TRUE	/	TRUE	1825487459	SAPISID	zc_uOjZi2ZKQIIvZ/A6tgLiJ7bh9iHMtyM
.youtube.com	TRUE	/	TRUE	1825487459	__Secure-1PAPISID	zc_uOjZi2ZKQIIvZ/A6tgLiJ7bh9iHMtyM
.youtube.com	TRUE	/	TRUE	1825487459	__Secure-3PAPISID	zc_uOjZi2ZKQIIvZ/A6tgLiJ7bh9iHMtyM
.youtube.com	TRUE	/	FALSE	1825487459	SID	g.a000DQmKdevG1vo7AWStL5wnw-sY_J-B3i0iaTDvbBjGUNCFD8sWoMSVJv9Zic9ru_0kmFk2KAACgYKAa8SARASFQHGX2MiKyv21PtmFwzLijwnvrUxUhoVAUF8yKo1I9Ep5BzgfdqPCbeW03bP0076
.youtube.com	TRUE	/	TRUE	1825487459	__Secure-1PSID	g.a000DQmKdevG1vo7AWStL5wnw-sY_J-B3i0iaTDvbBjGUNCFD8sWb0U6UQhuBFzy_bgCHmRe0gACgYKAYwSARASFQHGX2MirhTcrpdgorMsQFH282QLhhoVAUF8yKpac1k6b6iZDfk4CZQM4-NM0076
.youtube.com	TRUE	/	TRUE	1825487459	__Secure-3PSID	g.a000DQmKdevG1vo7AWStL5wnw-sY_J-B3i0iaTDvbBjGUNCFD8sWGsb_oTt9W99lyUxGUE-iVAACgYKAdYSARASFQHGX2Mi-BmUBHF9Iq3mRF-1OqLuzBoVAUF8yKp7uH8_w4-LexXKMJK7v9c50076
.youtube.com	TRUE	/	TRUE	1825490005	LOGIN_INFO	AFmmF2swRAIgLwv5rV05LoMdNFfAkl27nt2pOXMX22klOLSGlhwXtnkCIAx2nJ_JGY9rYaS_c9XOM4EQXXFLua9NsO1HAuJ3D1_V:QUQ3MjNmeFNhT2loaDdBMUVPVmM5eU1LM2ZPR3NzcUtCcVhPVUs5Ynp1TGtvNjNBUEZ4VDhZOExJZDdsMkx6bEs3Qzh1ZFliQjd0djZqSEJwUnpwcE5JbDJTSHZka3lDYXpaSjh0TmdqVVlXRVA2UXlTY0U1WjVNajlPM2tiOEM1cDVieU5zZ2RMOW1rRU0tZ2pzX3d6UFhLUDNvRUV5enZn
.youtube.com	TRUE	/	TRUE	1822807695	__Secure-1PSIDTS	sidts-CjUBkldj_-YX6C0DKSSsghOQ06LlQ5jyrHTSg46un-bH7ijEh_dBXk4prpXwUDsBhXInrMLMOxAA
.youtube.com	TRUE	/	TRUE	1822807695	__Secure-3PSIDTS	sidts-CjUBkldj_-YX6C0DKSSsghOQ06LlQ5jyrHTSg46un-bH7ijEh_dBXk4prpXwUDsBhXInrMLMOxAA
.youtube.com	TRUE	/	FALSE	1822807697	SIDCC	AKEyXzUUtN9DRi3Ine7w37pez3mdoA99nH5Zm0opAq2Y0DvzTcQ0qMrhCkbFPFyUOoFPhpXi
.youtube.com	TRUE	/	TRUE	1822807697	__Secure-1PSIDCC	AKEyXzXxztPD0nteRIzwVtea_HU0qxgWXZ9WVg-WHDZCADwn5c_ZjLzJG18f4U_HjY9UHtNE
.youtube.com	TRUE	/	TRUE	1822807697	__Secure-3PSIDCC	AKEyXzV-f08ulVUcJeiRycX6BG09UUU4jxAsF6EGiMKYifANPhG0rlVsAP6jw19Rapq2E7UBDw
.youtube.com	TRUE	/	TRUE	1806823686	VISITOR_INFO1_LIVE	sLOnAaQZRI4
.youtube.com	TRUE	/	TRUE	1806823686	VISITOR_PRIVACY_METADATA	CgJJThIEGgAgNA%3D%3D
.youtube.com	TRUE	/	TRUE	1806823492	__Secure-YNID	22.YT=kE1oTbSjs-zliekuLnlwqo_9GJJpXIX3uNtUKP-JU3jJt13SkcKuTGME8sQKRVQraML6DcvauwiOVYzd1v5mdSn1zEIChk5AtJCZgHs3y6ZvXBRHSeeyiqS9wne78srXgZrMMlAa2WmSWS6rE-FzGBJcAnn_28pISm1TmXjBFdH0DLcW-fqEniIM2jtxbEdxI-ro2CxWWqr05qBYv074Ep3F6sx48DS3Io7mfsLW_GqWsXKQ9kg9IFFjGdnPr-zidPuRjEl8P90rJ56jbODFxyCZrCodhO8QOA6wC8TIQP-2T4NswVhstTlUfLmqLQXQZqtxX3cOij22uy5v_KoOwA
.youtube.com	TRUE	/	TRUE	0	YSC	hFR3A02Cr0g
.youtube.com	TRUE	/	TRUE	1806823492	__Secure-ROLLOUT_TOKEN	CKDpj6KO1qzlfBCdi9ny2KaUAxjat-6n7qSXAw%3D%3D"""


def get_cookie_file():
    target = os.path.join(os.getcwd(), "cookies.txt")
    if not os.path.exists(target) or os.path.getsize(target) < 100:
        with open(target, "w", encoding="utf-8") as f:
            f.write(RAW_COOKIE_DATA.strip())
    return target


class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?([a-zA-Z0-9_-]{11})"
        self.status = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v="
        self.cookie_file = get_cookie_file()

    async def exists(self, link: str, videoid: bool = False):
        if videoid:
            link = self.base + link
        if re.search(self.regex, link):
            return True
        return False

    async def url(self, message_1):
        messages = [message_1]
        offset = None
        length = None
        for message in messages:
            if message.entities:
                for entity in message.entities:
                    if entity.type.name == "URL":
                        offset = entity.offset
                        length = entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type.name == "URL":
                        offset = entity.offset
                        length = entity.length
                        break
        if offset is not None:
            text = message_1.text or message_1.caption
            return text[offset : offset + length]
        return None

    async def details(self, link: str, videoid: bool = False):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        opts = {
            "quiet": True,
            "no_warnings": True,
            "logger": DummyLogger(),
            "cookiefile": self.cookie_file,
        }

        loop = asyncio.get_running_loop()

        def _get_info():
            with yt_dlp.YoutubeDL(opts) as ydl:
                return ydl.extract_info(link, download=False)

        info = await loop.run_in_executor(None, _get_info)
        title = info.get("title")
        duration_min = info.get("duration")
        thumbnail = info.get("thumbnail")
        vidid = info.get("id")
        duration_sec = int(duration_min) if duration_min else 0
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: bool = False):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        opts = {
            "quiet": True,
            "no_warnings": True,
            "logger": DummyLogger(),
            "cookiefile": self.cookie_file,
        }

        loop = asyncio.get_running_loop()

        def _get_title():
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(link, download=False)
                return info.get("title")

        return await loop.run_in_executor(None, _get_title)

    async def duration(self, link: str, videoid: bool = False):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        opts = {
            "quiet": True,
            "no_warnings": True,
            "logger": DummyLogger(),
            "cookiefile": self.cookie_file,
        }

        loop = asyncio.get_running_loop()

        def _get_dur():
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(link, download=False)
                return info.get("duration")

        dur = await loop.run_in_executor(None, _get_dur)
        return int(dur) if dur else 0

    async def thumbnail(self, link: str, videoid: bool = False):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        opts = {
            "quiet": True,
            "no_warnings": True,
            "logger": DummyLogger(),
            "cookiefile": self.cookie_file,
        }

        loop = asyncio.get_running_loop()

        def _get_thumb():
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(link, download=False)
                return info.get("thumbnail")

        return await loop.run_in_executor(None, _get_thumb)

    async def track(self, link: str, videoid: bool = False):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        opts = {
            "quiet": True,
            "no_warnings": True,
            "logger": DummyLogger(),
            "cookiefile": self.cookie_file,
        }

        loop = asyncio.get_running_loop()

        def _get_track():
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(link, download=False)
                title = info.get("title")
                dur = info.get("duration")
                vidid = info.get("id")
                yturl = info.get("webpage_url")
                return {
                    "title": title,
                    "link": yturl,
                    "vidid": vidid,
                    "duration_min": dur,
                }, vidid

        return await loop.run_in_executor(None, _get_track)

    async def formats(self, link: str, videoid: bool = False):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        opts = {
            "quiet": True,
            "no_warnings": True,
            "logger": DummyLogger(),
            "cookiefile": self.cookie_file,
        }

        loop = asyncio.get_running_loop()

        def _get_formats():
            formats_available = []
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(link, download=False)
                for f in info.get("formats", []):
                    try:
                        format_id = f.get("format_id")
                        format_note = f.get("format_note")
                        ext = f.get("ext")
                        formats_available.append(
                            {
                                "format": f"{format_id} - {format_note} ({ext})",
                                "id": format_id,
                            }
                        )
                    except Exception:
                        continue
            return formats_available, link

        return await loop.run_in_executor(None, _get_formats)

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: bool = False,
    ):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]

        opts = {
            "quiet": True,
            "no_warnings": True,
            "logger": DummyLogger(),
            "cookiefile": self.cookie_file,
        }

        loop = asyncio.get_running_loop()

        def _get_slider():
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(link, download=False)
                title = info.get("title")
                duration_min = info.get("duration")
                thumbnail = info.get("thumbnail")
                vidid = info.get("id")
                return title, duration_min, thumbnail, vidid

        return await loop.run_in_executor(None, _get_slider)

    async def download(
        self,
        link: str,
        mystic,
        video: bool = False,
        videoid: bool = False,
        songaudio: bool = False,
        songvideo: bool = False,
        format_id: str = None,
        title: str = None,
    ) -> str:
        if videoid:
            link = self.base + link

        loop = asyncio.get_running_loop()

        def _download():
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "logger": DummyLogger(),
                "cookiefile": self.cookie_file,
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
            }

            if songvideo:
                ydl_opts["format"] = (
                    f"{format_id}+bestaudio/best" if format_id else "bestvideo+bestaudio/best"
                )
            elif songaudio:
                ydl_opts["format"] = "bestaudio/best"
                ydl_opts["postprocessors"] = [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",
                    }
                ]
            elif video:
                ydl_opts["format"] = "bestvideo[height<=?720][width<=?1280]+bestaudio/best"
            else:
                ydl_opts["format"] = "bestaudio/best"
                ydl_opts["postprocessors"] = [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                downloaded_file = ydl.prepare_filename(info)
                if not songvideo and (not video or songaudio):
                    downloaded_file = os.path.splitext(downloaded_file)[0] + ".mp3"
                return downloaded_file

        return await loop.run_in_executor(None, _download)

    async def search(self, query: str):
        try:
            search = VideosSearch(query, limit=1)
            results = (await search.next())["result"]
            if results:
                title = results[0]["title"]
                duration_min = results[0]["duration"]
                thumbnail = results[0]["thumbnails"][0]["url"].split("?")[0]
                vidid = results[0]["id"]
                return title, duration_min, thumbnail, vidid
        except Exception as e:
            LOGGER.warning(f"VideosSearch failed: {e}. Trying fallback...")

        opts = {
            "quiet": True,
            "no_warnings": True,
            "logger": DummyLogger(),
            "cookiefile": self.cookie_file,
            "extract_flat": True,
        }
        loop = asyncio.get_running_loop()

        def _fallback():
            with yt_dlp.YoutubeDL(opts) as ydl:
                res = ydl.extract_info(f"ytsearch1:{query}", download=False)
                if "entries" in res and res["entries"]:
                    entry = res["entries"][0]
                    t = entry.get("title")
                    d = entry.get("duration")
                    thumb = entry.get("thumbnail") or ""
                    v = entry.get("id")
                    return t, d, thumb, v
            return None, None, None, None

        return await loop.run_in_executor(None, _fallback)


# Instance jo init.py expect kar raha hai
YouTube = YouTubeAPI()
