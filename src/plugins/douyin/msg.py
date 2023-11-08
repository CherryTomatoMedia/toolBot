from anyio import open_file
from nonebot import on_command, logger
from nonebot.matcher import Matcher
from nonebot.params import CommandArg,  ArgStr
from nonebot.adapters.telegram import Bot, Message
from nonebot.adapters.telegram.message import File
from nonebot.adapters.telegram.event import MessageEvent
from . import douyin


duoyin_matcher = on_command("douyin", aliases={"dy"})
@duoyin_matcher.handle()
async def cookieUploadPre(bot: Bot, event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    raw = args.extract_plain_text().strip()
    raw = raw.replace("@cherryTomatoTool_bot", "")
    if raw != '':
        matcher.set_arg("arg", raw)


@duoyin_matcher.got("arg", prompt="请输入抖音分享链接")
async def cookieUpload(bot: Bot,  event: MessageEvent, arg: str = ArgStr('arg')):
    await bot.send(event, "💦正在解析", reply_to_message_id=event.message_id)
    data = await douyin.getData(arg)
    if data == None:
        await bot.send(event, "🧎未解析到视频", reply_to_message_id=event.message_id)
    else:
        await bot.send(event, File.video(data), reply_to_message_id=event.message_id)
