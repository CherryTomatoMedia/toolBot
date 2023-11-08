import asyncio
import aiohttp
import urllib.parse
import re


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


async def main():
    resp = await httpGet("https://dlpanda.com/zh-CN")
    cookie = resp['cookie']

    raw = "1.74 复制打开抖音，看看【美食 可能有关】# 减脂餐 一口没吃 有点饿# 减脂餐  https://v.douyin.com/iR2euxso/ C@h.oD Uyt:/ 10/22 "
    encoded_string = urllib.parse.quote(raw)

    resp = await httpGet(f"https://dlpanda.com/zh-CN?url={encoded_string}&token=G7eRpMaa", {"Cookie": cookie, "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"})

    open("test.txt", "w").write(resp['data'])

    matchres = re.search(r"downVideo\('(.*?)',.*?\)", resp['data'])
    if matchres != None:
        downUri = matchres.group(1)
        if downUri[0:2] == "//":
            downUri = "https:"+downUri
        print(downUri)
        resp = await httpGetRaw(downUri)
        open("test.mp4", "wb").write(resp)

asyncio.run(main())
