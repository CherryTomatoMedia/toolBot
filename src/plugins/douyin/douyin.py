import aiohttp
import urllib.parse
import re
from nonebot import logger


async def httpGetRaw(url, head={}):
    async with aiohttp.ClientSession(headers=head) as session:
        async with session.get(url) as resp:
            if resp.status == 200:  # Check if the response status is OK
                data = await resp.read()
                return data

            else:
                return None


async def httpGet(url, head={}):
    async with aiohttp.ClientSession(headers=head) as session:
        async with session.get(url) as resp:
            if resp.status == 200:  # Check if the response status is OK
                data = await resp.text()  # Parse JSON from the response
                return {"data": data, "header": dict(resp.headers), "cookie": "; ".join(resp.headers.getall('Set-Cookie'))}
                return data
            else:
                return None


async def getData(raw: str):
    # 第一步：模拟浏览器操作，获取Cookies
    resp = await httpGet("https://dlpanda.com/zh-CN", {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"})
    cookie = resp['cookie']

    # 第二步：URL编码中文
    encoded_string = urllib.parse.quote(raw)

    # 第三步：
    # URL：https://dlpanda.com/zh-CN?url={encoded_string}&token=G7eRpMaa
    # header： cookie + user-agent
    resp = await httpGet(f"https://dlpanda.com/zh-CN?url={encoded_string}&token=G7eRpMaa", {"Cookie": cookie, "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"})

    # 第四步：使用正则获取视频链接
    matchres = re.search(r"downVideo\('(.*?)',.*?\)", resp['data'])
    if matchres != None:  # 如果不为None，代表着获取到了结果
        downUri = matchres.group(1)
        if downUri == "":
            return None
        if downUri[0:2] == "//":
            downUri = "https:"+downUri
        logger.debug(f"获取抖音链接：{downUri}")
        resp = await httpGetRaw(downUri)
        return resp
    return None  # 如果没有获取到链接则返回None
