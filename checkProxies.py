import json
import sys
from gitRepo import commitPushRActiveProxiesFile, getLatestActiveConfigs

sys.path.append('./xray_url_decoder/')
sys.path.append('./xray_ping/')

from xray_url_decoder.XrayUrlDecoder import XrayUrlDecoder
from xray_ping.XrayPing import XrayPing


def is_good_for_game(config: XrayUrlDecoder):
    return (config.type in ['tcp', 'grpc']) and (config.security in [None, "tls"])


with open("collected-proxies/row-url/all.txt", 'r') as rowProxiesFile:
    configs = []
    for_game_proxies = []
    for url in rowProxiesFile:
        if len(url) > 10:
            try:
                c = XrayUrlDecoder(url)
                c_json = c.generate_json_str()
                if c.isSupported and c.isValid:
                    configs.append(c_json)

                if is_good_for_game(c):
                    for_game_proxies.append(url)
            except:
                print("There is error with this proxy => " + url)

    # getLatestGoodForGame()
    # with open("collected-proxies/row-url/for_game.txt", 'w') as forGameProxiesFile:
    #     for forGame in for_game_proxies:
    #         forGameProxiesFile.write(forGame)
    # commitPushForGameProxiesFile()

    delays = XrayPing(configs)
    getLatestActiveConfigs()
    with open("collected-proxies/xray-json/actives_all.txt", 'w') as activeProxiesFile:
        for active in delays.actives:
            activeProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open("collected-proxies/xray-json/actives_under_1000ms.txt", 'w') as active1000ProxiesFile:
        for active in delays.realDelay_under_1000:
            active1000ProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open("collected-proxies/xray-json/actives_under_1500ms.txt", 'w') as active1500ProxiesFile:
        for active in delays.realDelay_under_1500:
            active1500ProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open("collected-proxies/xray-json/actives_no_403_under_1000ms.txt", 'w') as active1000no403ProxiesFile:
        for active in delays.no403_realDelay_under_1000:
            active1000no403ProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open("collected-proxies/xray-json/actives_for_ir_server_no403_u1s.txt", 'w') as active1000no403ForServerProxiesFile:
        for active in delays.no403_realDelay_under_1000:
            if active['proxy']["streamSettings"]["network"] not in ["ws", "grpc"]:
                active1000no403ForServerProxiesFile.write(json.dumps(active['proxy']) + "\n")

commitPushRActiveProxiesFile()
