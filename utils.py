import html
import math
import os
import re
import sys
from io import BytesIO

from loguru import logger
from PIL import Image


logger.remove()
logger.add(sys.stdout, backtrace=True, diagnose=True)
logger.add("bili_feed.log", backtrace=True, diagnose=True, rotation="1 MB")


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) bilibili_pc/1.12.1 Chrome/106.0.5249.199 Electron/21.3.3 Safari/537.36"
}

BILI_API = os.environ.get("BILI_API", "https://api.bilibili.com")

LOCAL_MODE = os.environ.get("LOCAL_MODE", False)


class ParserException(Exception):
    def __init__(self, msg, url, res=None):
        self.msg = msg
        self.url = url
        self.res = str(res) if res else None

    def __str__(self):
        return f"{self.msg}: {self.url} ->\n{self.res}"


def compress(inpil, size=1280, fix_ratio=False) -> BytesIO:
    pil = Image.open(inpil)
    if fix_ratio:
        w, h = pil.size
        if w / h > 20:
            logger.info(f"{w}, {h}")
            new_h = math.ceil(w / 20)
            padded = Image.new("RGBA", (w, new_h))
            padded.paste(pil, (0, int((new_h - h) / 2)))
            pil = padded
        elif h / w > 20:
            logger.info(f"{w}, {h}")
            new_w = math.ceil(h / 20)
            padded = Image.new("RGBA", (new_w, h))
            padded.paste(pil, (int((new_w - h) / 2), 0))
            pil = padded
    if size > 0:
        pil.thumbnail((size, size), Image.LANCZOS)
    outpil = BytesIO()
    pil.save(outpil, "PNG", optimize=True)
    return outpil


def escape_markdown(text):
    return (
        re.sub(r"([_*\[\]()~`>\#\+\-=|{}\.!\\])", r"\\\1", html.unescape(text))
        if text
        else str()
    )
