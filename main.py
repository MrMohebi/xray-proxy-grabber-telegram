from client import app, PROXY_CHANNELS, IS_DEBUG
from pyrogram import filters
import re
from git import Repo

repo = Repo("./")


def commitPushRowProxiesFile(chanelUsername):
    if not IS_DEBUG:
        with repo.config_reader() as git_config:
            email = git_config.get_value('user', 'email')
            user = git_config.get_value('user', 'name')
        with repo.config_writer() as git_config:
            git_config.set_value('user', 'email', 'bot@auto.com')
            git_config.set_value('user', 'name', 'Bot-auto')
        repo.remotes.origin.pull()
        repo.index.add(["proxies_row_url.txt"])
        repo.index.commit('update proxies from {}'.format(chanelUsername))
        repo.remotes.origin.push()
        with repo.config_writer() as git_config:
            git_config.set_value('user', 'email', email)
            git_config.set_value('user', 'name', user)


def extract_v2ray_links(text) -> list[str]:
    regex = r"(vless|vmess|trojan):\/\/[^\\\n]*"
    matches = re.finditer(regex, text, re.MULTILINE)
    return [i.group() for i in matches]


@app.on_message(filters.text & filters.channel & filters.chat(PROXY_CHANNELS))
async def from_proxy_channels(client, message):
    global repo
    messageText = message.text
    has_v2ray_proxy = "vless://" in messageText or "vmess://" in messageText or "trojan://" in messageText
    if has_v2ray_proxy:
        v2rayProxies = extract_v2ray_links(messageText)
        print(v2rayProxies)
        with open("./proxies_row_url.txt", 'a') as f:
            f.write("\n".join(v2rayProxies))
            f.write("\n")

        commitPushRowProxiesFile(message.sender_chat.username)


app.run()

# b = XrayUrlDecoder(
#     "vless://86dee03e-8119-4215-e719-279602c5a366@cljoon.wtf-broo.ir:2087?encryption=none&security=tls&sni=cljoon.wtf-broo.ir&alpn=h2%2Chttp%2F1.1&fp=chrome&type=ws&path=%2F#JoonWS-MrAR")
#
# c = XrayUrlDecoder(
#     "vless://1fbe1e72-1a3b-4b75-dce5-5598631f7efc@levi.wtf-broo.ir:57356?encryption=none&security=reality&sni=telewebion.com&fp=chrome&pbk=sq7N8HmEL1cPskTNP4h5M31BqAoeIQ76bBcCDh9fKQc&spx=%2F&type=grpc#Heaven%2B2-qngk0z2yv")
#
# proxyPings = XrayPing(
#     [b.vless_json_str(), c.vless_json_str()])
#
# print(json.dumps(proxyPings.result))

