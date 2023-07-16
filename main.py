from client import app
from pyrogram import filters
import re

PROXY_CHANNELS = ["test_telegram_bot_mrm"]


def extract_v2ray_links(text):
    regex = r"(vless|vmess|trojan):\/\/[^\\\n]*"
    matches = re.finditer(regex, text, re.MULTILINE)
    return [i.group() for i in matches]


@app.on_message(filters.text & filters.channel & filters.chat(PROXY_CHANNELS))
async def from_proxy_channels(client, message):
    messageText = message.text.lower()
    has_v2ray_proxy = "vless://" in messageText or "vmess://" in messageText or "trojan://" in messageText
    if has_v2ray_proxy:
        v2rayProxies = extract_v2ray_links(messageText)
        print(v2rayProxies)
        await message.reply(v2rayProxies)


app.run()
