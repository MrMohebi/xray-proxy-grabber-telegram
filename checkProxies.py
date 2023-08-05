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
            c_json = c.generate_json_str()
            if c.isSupported and c.isValid:
                configs.append(c_json)

    delays = XrayPing(configs)
    getLatestActiveConfigs()
    with open("./proxies_active.txt", 'w') as activeProxiesFile:
        for active in delays.actives:
            activeProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open("./proxies_active_under_1000ms.txt", 'w') as active1000ProxiesFile:
        for active in delays.realDelay_under_1000:
            active1000ProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open("./proxies_active_under_1500ms.txt", 'w') as active1500ProxiesFile:
        for active in delays.realDelay_under_1500:
            active1500ProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open("./proxies_active_no_403_under_1000ms.txt", 'w') as active1000no403ProxiesFile:
        for active in delays.no403_realDelay_under_1000:
            active1000no403ProxiesFile.write(json.dumps(active['proxy']) + "\n")


commitPushRActiveProxiesFile()
