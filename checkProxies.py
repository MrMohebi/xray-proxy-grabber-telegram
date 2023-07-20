import json
import sys
from gitRepo import commitPushRActiveProxiesFile, getLatestActiveConfigs

sys.path.append('./xray_url_decoder/')
sys.path.append('./xray_ping/')

from xray_url_decoder.XrayUrlDecoder import XrayUrlDecoder
from xray_ping.XrayPing import XrayPing

with open("./proxies_row_url.txt", 'r') as rowProxiesFile:
    configs = []
    for url in rowProxiesFile:
        if len(url) > 10:
            c = XrayUrlDecoder(url)
            configs.append(c.vless_json_str())

    delays = XrayPing(configs)
    getLatestActiveConfigs()
    with open("./proxies_active.txt", 'w') as activeProxiesFile:
        for active in delays.actives:
            activeProxiesFile.write(json.dumps(active['proxy']) + "\n")

commitPushRActiveProxiesFile()
