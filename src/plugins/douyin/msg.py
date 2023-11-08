from anyio import open_file
from nonebot import on_command
from nonebot.adapters.telegram import Bot
from nonebot.adapters.telegram.message import File
from nonebot.adapters.telegram.event import MessageEvent
from nonebot.adapters.telegram.model import InputMediaPhoto


@on_command("douyin").handle()
async def douyin():
    pass