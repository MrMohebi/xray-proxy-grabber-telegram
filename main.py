from client import app, PROXY_CHANNELS
from pyrogram import filters
import re
import datetime

from gitRepo import commitPushRowProxiesFile, getLatestRowProxies


def extract_v2ray_links(text) -> list[str]:
    regex = r"(vless|vmess|trojan):\/\/[^\\\n]*"
    matches = re.finditer(regex, text, re.MULTILINE)
    return [i.group() for i in matches]


# commit after every 50 proxy founded
PROXY_COUNTER_DEFAULT = 50
proxy_counter = PROXY_COUNTER_DEFAULT
temp_proxy_holder = []


@app.on_message(filters.text & filters.channel & filters.chat(PROXY_CHANNELS))
async def from_proxy_channels(client, message):
    global proxy_counter, PROXY_COUNTER_DEFAULT, temp_proxy_holder
    messageText = message.text
    has_v2ray_proxy = "vless://" in messageText or "vmess://" in messageText or "trojan://" in messageText
    if has_v2ray_proxy:
        v2rayProxies = extract_v2ray_links(messageText)
        print(str(datetime.datetime.now()) + " ===> ", end=None)
        print(v2rayProxies)

        temp_proxy_holder = temp_proxy_holder + v2rayProxies

        if proxy_counter < 0:
            proxy_counter = PROXY_COUNTER_DEFAULT

            getLatestRowProxies()
            with open("collected-proxies/row-url/all.txt", 'a') as f:
                f.write("\n".join(v2rayProxies))
                f.write("\n")
            commitPushRowProxiesFile(message.sender_chat.username)

        else:
            proxy_counter = proxy_counter - 1


app.run()
