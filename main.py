from client import app, PROXY_CHANNELS
from telethon.sync import events
import re
import datetime

from gitRepo import commitPushRowProxiesFile, getLatestRowProxies


def extract_v2ray_links(text) -> list[str]:
    regex = r"(vless|vmess|trojan):\/\/[^\\\n]*"
    matches = re.finditer(regex, text, re.MULTILINE)
    return [i.group() for i in matches]


# commit after every 50 proxy founded
PROXY_COUNTER_DEFAULT = 100
temp_proxy_holder = []


@app.on(events.NewMessage())
async def handler(event):
    usernameMatched = (event.sender.username is not None) and (event.sender.username != "") and event.sender.username.lower() in PROXY_CHANNELS
    idMatched =  event.sender.id in PROXY_CHANNELS
    if usernameMatched or idMatched:
        global PROXY_COUNTER_DEFAULT, temp_proxy_holder
        messageText = event.text
        has_v2ray_proxy = "vless://" in messageText or "vmess://" in messageText or "trojan://" in messageText
        if has_v2ray_proxy:
            v2rayProxies = extract_v2ray_links(messageText)
            print(str(datetime.datetime.now()) + " ===> ", end=None)
            print(v2rayProxies)

            temp_proxy_holder = temp_proxy_holder + v2rayProxies

            if len(temp_proxy_holder) > PROXY_COUNTER_DEFAULT:
                getLatestRowProxies()
                with open("collected-proxies/row-url/all.txt", 'a') as f:
                    f.write("\n".join(temp_proxy_holder))
                    f.write("\n")
                commitPushRowProxiesFile(event.sender.username)
                temp_proxy_holder = []

app.start()
app.run_until_disconnected()