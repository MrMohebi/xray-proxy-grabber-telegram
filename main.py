from client import app, PROXY_CHANNELS
from pyrogram import filters
import re

from gitRepo import commitPushRowProxiesFile, getLatestRowProxies


def extract_v2ray_links(text) -> list[str]:
    regex = r"(vless|vmess|trojan):\/\/[^\\\n]*"
    matches = re.finditer(regex, text, re.MULTILINE)
    return [i.group() for i in matches]


@app.on_message(filters.text & filters.channel & filters.chat(PROXY_CHANNELS))
async def from_proxy_channels(client, message):
    messageText = message.text
    has_v2ray_proxy = "vless://" in messageText or "vmess://" in messageText or "trojan://" in messageText
    if has_v2ray_proxy:
        v2rayProxies = extract_v2ray_links(messageText)
        print(v2rayProxies)
        getLatestRowProxies()
        with open("./proxies_row_url.txt", 'a') as f:
            f.write("\n".join(v2rayProxies))
            f.write("\n")

        commitPushRowProxiesFile(message.sender_chat.username)


app.run()
