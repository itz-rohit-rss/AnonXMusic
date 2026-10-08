

def save_cookies(self, *args, **kwargs):
        self.cookie_file = get_cookie_file()
        return self.cookie_file
        # Copyright (C) 2024 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import asyncio
import logging
import os
import re
import yt_dlp

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

.youtube.com	TRUE	/	TRUE	1826036239	PREF	f6=40000000&tz=Asia.Calcutta&f7=100
.youtube.com	TRUE	/	TRUE	1806472315	__Secure-BUCKET	CL0B
.youtube.com	TRUE	/	FALSE	1825851113	SID	g.a000DQmKdbVAf9BBAwdSV4LlXjtlM10nAtxnfwFbL4oT0NT48Jom5rZBpJBkUqx988zFNLvwaAACgYKAeQSARASFQHGX2Mi_eHriWI7EY_sADHPxrGVehoVAUF8yKqOmzeKj8Sdkm0qKP2w6grQ0076
.youtube.com	TRUE	/	TRUE	1825851113	__Secure-1PSID	g.a000DQmKdbVAf9BBAwdSV4LlXjtlM10nAtxnfwFbL4oT0NT48JomBnr11T258EyuF0p0iPNg3AACgYKAR0SARASFQHGX2MizKniWSARnIAWE9CCa7ZihRoVAUF8yKpxaGRnGhGzcWVUDgmU8F6l0076
.youtube.com	TRUE	/	TRUE	1825851113	__Secure-3PSID	g.a000DQmKdbVAf9BBAwdSV4LlXjtlM10nAtxnfwFbL4oT0NT48JomEf-Y1Z2THf_5nTGDVVb2vAACgYKAZcSARASFQHGX2Mi_JngN2c9phl_KxRXFXsfsRoVAUF8yKr2z8SFvjk9lTQMOZjeQzGT0076
.youtube.com	TRUE	/	FALSE	1825851113	HSID	APvq3RZYh3b4-u173
.youtube.com	TRUE	/	TRUE	1825851113	SSID	AIFeYsDBfen9JQvD6
.youtube.com	TRUE	/	FALSE	1825851113	APISID	ol37OUVa8kFaa1cl/AcbkC5IJsPi_i9Rkn
.youtube.com	TRUE	/	TRUE	1825851113	SAPISID	7wdiHMbUjiWESERo/AXoolGBlkWsS7QAPj
.youtube.com	TRUE	/	TRUE	1825851113	__Secure-1PAPISID	7wdiHMbUjiWESERo/AXoolGBlkWsS7QAPj
.youtube.com	TRUE	/	TRUE	1825851113	__Secure-3PAPISID	7wdiHMbUjiWESERo/AXoolGBlkWsS7QAPj
.youtube.com	TRUE	/	TRUE	1825853378	LOGIN_INFO	AFmmF2swRAIgZf-GJ0KTvslyx4vuPZ3VlE0EFi2pWJ1ZXDAAzkWq9PYCIHv3DjX5GfF66sWPaNTE_3aDjL47RaBHHPZvPKElXOm0:QUQ3MjNmelgxdGdEYmdpdTBPWUF0dk9TVVJQZnVCbG95dnkyai1qY0xkQ0xGTVBSaTJQd3VCM3JiX0tUQVhqMTU5RExGVGdJYlo3SE5lWHVOM04xMHlVTnlIZGxUMm5uT3lJcE5CMDRlaXNyc2hVaHRkVmc4Y1ZsZ3ZoS3dFSFdJcVhrOFpiOUVwRmU4LVFqZkUwSHEzS2c0ajhVczl1bUVn
.youtube.com	TRUE	/	TRUE	1823012248	__Secure-1PSIDTS	sidts-CjIBkldj_yIptJd-pRv2MKi7twb4x7c9ejIGotZRHDf1QCf6IJvWUkYVsh511FgS87dOvRAA
.youtube.com	TRUE	/	TRUE	1823012248	__Secure-3PSIDTS	sidts-CjIBkldj_yIptJd-pRv2MKi7twb4x7c9ejIGotZRHDf1QCf6IJvWUkYVsh511FgS87dOvRAA
.youtube.com	TRUE	/	FALSE	1823012252	SIDCC	AKEyXzUc-RmFB7gnrbq7vdVLB-LvWKMgY3oc3zoXpFVTxWz_-SVa3fYXP5erYSYp7YT2ncEx
.youtube.com	TRUE	/	TRUE	1823012252	__Secure-1PSIDCC	AKEyXzWs1y85Y-LhqzI0WlARC2EI0lt8yW1DJzOlxmsYu4Z5TErrIwCZOAHH1QljX1oaUuzf
.youtube.com	TRUE	/	TRUE	1823012252	__Secure-3PSIDCC	AKEyXzXnlYCuboVLKWBtkkH6VNNDtZ0VdY7EvBHCBf_-fM2qe0V1mu78AfPDn1U4rIri41m8DA
.youtube.com	TRUE	/	TRUE	1807028233	VISITOR_INFO1_LIVE	sLOnAaQZRI4
.youtube.com	TRUE	/	TRUE	1807028233	VISITOR_PRIVACY_METADATA	CgJJThIEGgAgNA%3D%3D
.youtube.com	TRUE	/	TRUE	1807025766	__Secure-YNID	22.YT=Ak5E31hC2DYQOPVGjgjgZGd5ys_ko4Ha-g8QpGtNDuNnE3gIpKY1-OgKh7J0RPh9NqeytiCbOeRl9Sec_vw4zEZ1mPHiqbEpD0XgZh7lJFaXYV7yWTpLl9xPts0x8BGQsiTnT04nE9saKk-amJHRJp6qmPRBdw4GUe2yOtHEqbbgVkXpYCUAQXlPkQ3kFnM_eY1mxOt0wg5FBw06r7ASiBIYOJDQw_Eb9d_m5Y2pOPPKm4JZS99opqsr-7T4zByods-pXQF6ywlGb5ScxeY7-izu5lZe3CbH9-sCKSB4l6ZtBVI6Wj59UPsefo1kvK1ViysZvyIaEDMRrEBgN_EPpA
.youtube.com	TRUE	/	TRUE	0	YSC	_sqN7P2FXxg
.youtube.com	TRUE	/	TRUE	1807025767	__Secure-ROLLOUT_TOKEN	CKDpj6KO1qzlfBCdi9ny2KaUAxieo4Ts36qXAw%3D%3D"""


def get_cookie_file():
    target = os.path.join(os.getcwd(), "cookies.txt")
    if not os.path.exists(target) or os.path.getsize(target) < 100:
        with open(target, "w", encoding="utf-8") as f:
            f.write(RAW_COOKIE_DATA.strip())
    return target


class YouTube:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?([a-zA-Z0-9_-]{11})"
        self.status = "https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v="
        self.cookie_file = get_cookie_file()

    def save_cookies(self, *args, **kwargs):
        self.cookie_file = get_cookie_file()
        return self.cookie_file

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
        opts = {
            "quiet": True,
            "no_warnings": True,
            "logger": DummyLogger(),
            "cookiefile": self.cookie_file,
            "extract_flat": True,
        }
        loop = asyncio.get_running_loop()

        def _search():
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

        return await loop.run_in_executor(None, _search)
        
