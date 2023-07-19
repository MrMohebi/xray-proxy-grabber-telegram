import json
import sys
import os
from dotenv import load_dotenv

from git import Repo

sys.path.append('./xray_url_decoder/')
sys.path.append('./xray_ping/')

from xray_url_decoder.XrayUrlDecoder import XrayUrlDecoder
from xray_ping.XrayPing import XrayPing

load_dotenv()
IS_DEBUG = bool(int(os.getenv('DEBUG_MODE')))

repo = Repo("./")
if not IS_DEBUG:
    with repo.config_writer() as git_config:
        git_config.set_value('user', 'email', 'bot@auto.com')
        git_config.set_value('user', 'name', 'Bot-auto')


def commitPushRActiveProxiesFile():
    if not IS_DEBUG:
        with repo.config_reader() as git_config:
            email = git_config.get_value('user', 'email')
            user = git_config.get_value('user', 'name')
        with repo.config_writer() as git_config:
            git_config.set_value('user', 'email', 'bot@auto.com')
            git_config.set_value('user', 'name', 'Bot-auto')
        repo.remotes.origin.pull()
        repo.index.add(["proxies_active.txt"])
        repo.index.commit('update active proxies')
        repo.remotes.origin.push()
        with repo.config_writer() as git_config:
            git_config.set_value('user', 'email', email)
            git_config.set_value('user', 'name', user)


with open("./proxies_row_url.txt", 'r') as rowProxiesFile:
    configs = []
    for url in rowProxiesFile:
        c = XrayUrlDecoder(url)
        configs.append(c.vless_json_str())

    delays = XrayPing(configs)
    with open("./proxies_active.txt", 'w') as activeProxiesFile:
        for active in delays.actives:
            activeProxiesFile.write(json.dumps(active['proxy']) + "\n")

commitPushRActiveProxiesFile()
